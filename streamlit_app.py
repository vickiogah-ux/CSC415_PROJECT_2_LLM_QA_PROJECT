"""
Streamlit version of the LLM Q&A System for easy cloud deployment
Run with: streamlit run streamlit_app.py
"""

import os
import string
import re
from typing import Tuple
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try importing NLTK for tokenization
try:
    import nltk
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
except ImportError:
    NLTK_AVAILABLE = False


class NLPPreprocessor:
    """Handles NLP preprocessing of user questions."""
    
    @staticmethod
    def lowercase(text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()
    
    @staticmethod
    def remove_punctuation(text: str) -> str:
        """Remove punctuation from text."""
        return text.translate(str.maketrans('', '', string.punctuation))
    
    @staticmethod
    def tokenize(text: str) -> list:
        """Tokenize text into words."""
        if NLTK_AVAILABLE:
            return word_tokenize(text)
        else:
            return re.findall(r'\b\w+\b', text.lower())
    
    @staticmethod
    def preprocess_question(question: str) -> dict:
        """
        Apply comprehensive preprocessing to a question.
        Returns: Dictionary with processed_question and tokens
        """
        processed = NLPPreprocessor.lowercase(question)
        tokens = NLPPreprocessor.tokenize(processed)
        processed = NLPPreprocessor.remove_punctuation(processed)
        processed = ' '.join(processed.split())
        
        return {
            "processed_question": processed,
            "tokens": tokens,
            "token_count": len(tokens)
        }


class LLMProvider:
    """Base class for LLM providers."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_response(self, question: str) -> str:
        raise NotImplementedError


class GroqProvider(LLMProvider):
    """Groq LLM Provider - Free and fast."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            from groq import Groq
            self.client = Groq(api_key=api_key)
        except ImportError:
            raise ImportError("groq package required")
    
    def get_response(self, question: str) -> str:
        """Get response from Groq API."""
        try:
            message = self.client.messages.create(
                messages=[{"role": "user", "content": question}],
                model="mixtral-8x7b-32768",
                max_tokens=1024,
            )
            return message.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"


class OpenAIProvider(LLMProvider):
    """OpenAI LLM Provider."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package required")
    
    def get_response(self, question: str) -> str:
        """Get response from OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}],
                max_tokens=1024,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


class CohereProvider(LLMProvider):
    """Cohere LLM Provider."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import cohere
            self.client = cohere.ClientV2(api_key=api_key)
        except ImportError:
            raise ImportError("cohere package required")
    
    def get_response(self, question: str) -> str:
        """Get response from Cohere API."""
        try:
            response = self.client.chat(
                model="command-r-v1:0",
                messages=[{"role": "user", "content": question}],
            )
            return response.message.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"


class GeminiProvider(LLMProvider):
    """Google Gemini LLM Provider."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except ImportError:
            raise ImportError("google-generativeai package required")
    
    def get_response(self, question: str) -> str:
        """Get response from Gemini API."""
        try:
            response = self.model.generate_content(question)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


class LLMQASystem:
    """Main Q&A system that coordinates preprocessing and API calls."""
    
    def __init__(self, provider: str = "groq"):
        """Initialize the Q&A system with the specified provider."""
        self.provider_name = provider.lower()
        self.provider = self._initialize_provider()
        self.preprocessor = NLPPreprocessor()
    
    def _initialize_provider(self) -> LLMProvider:
        """Initialize the appropriate LLM provider."""
        provider_map = {
            "groq": GroqProvider,
            "openai": OpenAIProvider,
            "cohere": CohereProvider,
            "gemini": GeminiProvider,
        }
        
        if self.provider_name not in provider_map:
            raise ValueError(f"Unsupported provider: {self.provider_name}")
        
        env_key_map = {
            "groq": "GROQ_API_KEY",
            "openai": "OPENAI_API_KEY",
            "cohere": "COHERE_API_KEY",
            "gemini": "GEMINI_API_KEY",
        }
        
        api_key = os.getenv(env_key_map[self.provider_name])
        if not api_key:
            raise ValueError(f"API key for {self.provider_name} not found")
        
        return provider_map[self.provider_name](api_key)
    
    def process_question(self, question: str) -> dict:
        """
        Process a question and get a response from the LLM.
        """
        preprocessing_result = self.preprocessor.preprocess_question(question)
        answer = self.provider.get_response(question)
        
        return {
            "original_question": question,
            "processed_question": preprocessing_result["processed_question"],
            "tokens": preprocessing_result["tokens"],
            "token_count": preprocessing_result["token_count"],
            "answer": answer
        }


# Streamlit Configuration
st.set_page_config(
    page_title="LLM Q&A System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .token-badge {
        display: inline-block;
        background-color: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        margin: 0.25rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .answer-box {
        background-color: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and Header
st.title("🧠 LLM Question-and-Answering System")
st.markdown("*Powered by Advanced Language Models with NLP Preprocessing*")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    provider = st.selectbox(
        "Select LLM Provider",
        ["groq", "openai", "cohere", "gemini"],
        help="Choose the LLM provider to use"
    )
    
    st.markdown("---")
    st.subheader("📚 About")
    st.info(
        """
        This application uses advanced NLP preprocessing on your questions:
        - **Lowercasing**: Normalize text case
        - **Tokenization**: Split into words
        - **Punctuation Removal**: Clean special characters
        
        Your questions are then sent to the selected LLM API for intelligent responses.
        """
    )

# Initialize session state
if 'qa_system' not in st.session_state:
    try:
        st.session_state.qa_system = LLMQASystem(provider=provider)
        st.session_state.provider = provider
    except (ValueError, ImportError) as e:
        st.error(f"❌ Error initializing Q&A system: {e}")
        st.stop()

# Check if provider changed
if st.session_state.provider != provider:
    try:
        st.session_state.qa_system = LLMQASystem(provider=provider)
        st.session_state.provider = provider
    except (ValueError, ImportError) as e:
        st.error(f"❌ Error changing provider: {e}")
        st.stop()

# Main Content
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📝 Ask Your Question")
    question = st.text_area(
        "Enter your question",
        placeholder="E.g., 'What is machine learning?' or 'Explain quantum computing.'",
        height=100,
        label_visibility="collapsed"
    )

with col2:
    st.subheader("Provider Status")
    st.success(f"✅ {provider.upper()}\nConnected")

# Submit button
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    submit_button = st.button("🚀 Ask Question", use_container_width=True)

with col2:
    clear_button = st.button("🔄 Clear", use_container_width=True)

if clear_button:
    st.session_state.question = ""
    st.rerun()

# Process question
if submit_button:
    if not question.strip():
        st.warning("⚠️ Please enter a question")
    else:
        with st.spinner("⏳ Processing your question..."):
            try:
                result = st.session_state.qa_system.process_question(question)
                
                # Display Results
                st.success("✅ Processing complete!")
                
                # Create tabs for results
                tab1, tab2, tab3, tab4 = st.tabs(
                    ["Original", "Processed", "Tokens", "Answer"]
                )
                
                with tab1:
                    st.markdown("### Original Question")
                    st.write(result["original_question"])
                
                with tab2:
                    st.markdown("### Processed Question")
                    st.code(result["processed_question"])
                    st.caption("After NLP preprocessing (lowercasing, tokenization, punctuation removal)")
                
                with tab3:
                    st.markdown("### Tokenized Words")
                    
                    # Display tokens in columns
                    cols = st.columns(4)
                    for idx, token in enumerate(result["tokens"]):
                        with cols[idx % 4]:
                            st.markdown(
                                f'<span class="token-badge">{token}</span>',
                                unsafe_allow_html=True
                            )
                    
                    st.metric("Total Tokens", result["token_count"])
                
                with tab4:
                    st.markdown("### Answer from LLM")
                    st.markdown(
                        f'<div class="answer-box">{result["answer"]}</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Copy button
                    if st.button("📋 Copy Answer"):
                        st.write(result["answer"])
                        st.success("Copied to clipboard!")
            
            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")

# Information Section
with st.expander("ℹ️ How It Works", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 1️⃣ Input")
        st.write("Enter any natural-language question")
    
    with col2:
        st.markdown("### 2️⃣ Processing")
        st.write("Apply NLP preprocessing steps")
    
    with col3:
        st.markdown("### 3️⃣ Query")
        st.write("Send to LLM API")
    
    with col4:
        st.markdown("### 4️⃣ Response")
        st.write("Receive comprehensive answer")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🎓 Created for CSC 415 - Project 2")

with col2:
    st.caption("🏫 Covenant University")

with col3:
    st.caption("📅 November 2025")
