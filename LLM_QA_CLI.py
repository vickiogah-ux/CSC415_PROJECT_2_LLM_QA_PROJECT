#!/usr/bin/env python3
"""
LLM Question-and-Answering CLI Application
A command-line interface for asking questions to an LLM API with NLP preprocessing.
Supports multiple LLM providers (Groq, OpenAI, Cohere, HuggingFace, Gemini)
"""

import os
import sys
import string
import re
from typing import Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try importing NLTK for tokenization (optional)
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
    print("Warning: NLTK not available. Using basic tokenization.")


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
            # Basic tokenization using regex
            return re.findall(r'\b\w+\b', text.lower())
    
    @staticmethod
    def preprocess_question(question: str) -> Tuple[str, list]:
        """
        Apply comprehensive preprocessing to a question.
        Returns: (processed_question, tokens)
        """
        # Step 1: Lowercase
        processed = NLPPreprocessor.lowercase(question)
        
        # Step 2: Tokenize (before removing punctuation for better tokenization)
        tokens = NLPPreprocessor.tokenize(processed)
        
        # Step 3: Remove punctuation
        processed = NLPPreprocessor.remove_punctuation(processed)
        
        # Step 4: Remove extra whitespace
        processed = ' '.join(processed.split())
        
        return processed, tokens


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
            raise ImportError("groq package required. Install with: pip install groq")
    
    def get_response(self, question: str) -> str:
        """Get response from Groq API."""
        try:
            message = self.client.messages.create(
                messages=[
                    {
                        "role": "user",
                        "content": question,
                    }
                ],
                model="mixtral-8x7b-32768",  # Fast and capable model
                max_tokens=1024,
            )
            return message.content[0].text
        except Exception as e:
            return f"Error communicating with Groq API: {str(e)}"


class OpenAIProvider(LLMProvider):
    """OpenAI LLM Provider."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")
    
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
            return f"Error communicating with OpenAI API: {str(e)}"


class CohereProvider(LLMProvider):
    """Cohere LLM Provider."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import cohere
            self.client = cohere.ClientV2(api_key=api_key)
        except ImportError:
            raise ImportError("cohere package required. Install with: pip install cohere")
    
    def get_response(self, question: str) -> str:
        """Get response from Cohere API."""
        try:
            response = self.client.chat(
                model="command-r-v1:0",
                messages=[{"role": "user", "content": question}],
            )
            return response.message.content[0].text
        except Exception as e:
            return f"Error communicating with Cohere API: {str(e)}"


class GeminiProvider(LLMProvider):
    """Google Gemini LLM Provider."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except ImportError:
            raise ImportError("google-generativeai package required. Install with: pip install google-generativeai")
    
    def get_response(self, question: str) -> str:
        """Get response from Gemini API."""
        try:
            response = self.model.generate_content(question)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"


class LLMQASystem:
    """Main Q&A system that coordinates preprocessing and API calls."""
    
    def __init__(self, provider: str = "groq"):
        """Initialize the Q&A system with the specified provider."""
        self.provider_name = provider.lower()
        self.provider = self._initialize_provider()
        self.preprocessor = NLPPreprocessor()
    
    def _initialize_provider(self) -> LLMProvider:
        """Initialize the appropriate LLM provider based on configuration."""
        provider_map = {
            "groq": GroqProvider,
            "openai": OpenAIProvider,
            "cohere": CohereProvider,
            "gemini": GeminiProvider,
        }
        
        if self.provider_name not in provider_map:
            raise ValueError(f"Unsupported provider: {self.provider_name}")
        
        # Map environment variable names
        env_key_map = {
            "groq": "GROQ_API_KEY",
            "openai": "OPENAI_API_KEY",
            "cohere": "COHERE_API_KEY",
            "gemini": "GEMINI_API_KEY",
        }
        
        api_key = os.getenv(env_key_map[self.provider_name])
        if not api_key:
            raise ValueError(
                f"API key for {self.provider_name} not found. "
                f"Set {env_key_map[self.provider_name]} environment variable."
            )
        
        return provider_map[self.provider_name](api_key)
    
    def process_question(self, question: str) -> dict:
        """
        Process a question and get a response from the LLM.
        
        Args:
            question: The user's question
        
        Returns:
            Dictionary containing:
            - original_question: The original input
            - processed_question: After preprocessing
            - tokens: Tokenized words
            - answer: The LLM response
        """
        # Preprocess the question
        processed_question, tokens = self.preprocessor.preprocess_question(question)
        
        # Get response from LLM
        answer = self.provider.get_response(question)
        
        return {
            "original_question": question,
            "processed_question": processed_question,
            "tokens": tokens,
            "answer": answer
        }


def main():
    """Main function for CLI interaction."""
    print("\n" + "="*70)
    print("LLM Question-and-Answering System (CLI)")
    print("="*70 + "\n")
    
    # Get provider preference
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    
    try:
        qa_system = LLMQASystem(provider=provider)
        print(f"✓ Connected to {provider.upper()} LLM API\n")
    except (ValueError, ImportError) as e:
        print(f"✗ Error: {e}\n")
        sys.exit(1)
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            question = input("\n📝 Enter your question (or 'quit' to exit): ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using the LLM Q&A System. Goodbye!\n")
                break
            
            if not question:
                print("⚠️  Please enter a valid question.")
                continue
            
            # Process the question
            print("\n⏳ Processing your question...")
            result = qa_system.process_question(question)
            
            # Display results
            print("\n" + "-"*70)
            print("📌 ORIGINAL QUESTION:")
            print(f"   {result['original_question']}")
            
            print("\n🔤 PROCESSED QUESTION:")
            print(f"   {result['processed_question']}")
            
            print("\n🔤 TOKENIZED WORDS:")
            print(f"   {', '.join(result['tokens'])}")
            
            print("\n💡 ANSWER:")
            print(f"   {result['answer']}")
            print("-"*70)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}\n")


if __name__ == "__main__":
    main()
