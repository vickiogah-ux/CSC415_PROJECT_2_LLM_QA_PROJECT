"""
Flask Web GUI for LLM Question-and-Answering System
A web interface for asking questions to an LLM API with NLP preprocessing.
"""

import os
import sys
import string
import re
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from threading import Lock

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
        # Step 1: Lowercase
        processed = NLPPreprocessor.lowercase(question)
        
        # Step 2: Tokenize
        tokens = NLPPreprocessor.tokenize(processed)
        
        # Step 3: Remove punctuation
        processed = NLPPreprocessor.remove_punctuation(processed)
        
        # Step 4: Remove extra whitespace
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
            return f"Error: {str(e)}"


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
        self.lock = Lock()
    
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
            raise ValueError(
                f"API key for {self.provider_name} not found in environment variables"
            )
        
        return provider_map[self.provider_name](api_key)
    
    def process_question(self, question: str) -> dict:
        """
        Process a question and get a response from the LLM.
        Uses thread lock to prevent concurrent API calls.
        """
        with self.lock:
            # Preprocess the question
            preprocessing_result = self.preprocessor.preprocess_question(question)
            
            # Get response from LLM
            answer = self.provider.get_response(question)
            
            return {
                "original_question": question,
                "processed_question": preprocessing_result["processed_question"],
                "tokens": preprocessing_result["tokens"],
                "token_count": preprocessing_result["token_count"],
                "answer": answer
            }


# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize LLM Q&A System
try:
    provider = os.getenv("LLM_PROVIDER", "groq")
    qa_system = LLMQASystem(provider=provider)
except (ValueError, ImportError) as e:
    print(f"Warning: Could not initialize Q&A system: {e}")
    qa_system = None


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Handle question submission and return answer."""
    try:
        # Validate request
        if not request.json or 'question' not in request.json:
            return jsonify({
                "success": False,
                "error": "No question provided"
            }), 400
        
        question = request.json['question'].strip()
        
        # Validate question
        if not question:
            return jsonify({
                "success": False,
                "error": "Question cannot be empty"
            }), 400
        
        if len(question) > 2000:
            return jsonify({
                "success": False,
                "error": "Question is too long (max 2000 characters)"
            }), 400
        
        # Check if Q&A system is initialized
        if qa_system is None:
            return jsonify({
                "success": False,
                "error": "Q&A system not initialized. Please check API configuration."
            }), 500
        
        # Process the question
        result = qa_system.process_question(question)
        
        return jsonify({
            "success": True,
            "data": {
                "original_question": result["original_question"],
                "processed_question": result["processed_question"],
                "tokens": result["tokens"],
                "token_count": result["token_count"],
                "answer": result["answer"]
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check API health and system status."""
    status = "healthy" if qa_system else "misconfigured"
    return jsonify({
        "status": status,
        "provider": os.getenv("LLM_PROVIDER", "groq") if qa_system else None
    }), 200 if qa_system else 503


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == '__main__':
    # Get configuration from environment
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    # For Render.com deployment: listen on 0.0.0.0 for all network interfaces
    # For local development: use 127.0.0.1
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    # For Render.com deployment: use PORT environment variable
    # For local development: default to 5000
    port = int(os.getenv('PORT', os.getenv('FLASK_PORT', 5000)))
    
    print(f"Starting Flask application on {host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"Q&A System Status: {'Initialized' if qa_system else 'Failed to initialize'}")
    
    if not qa_system:
        print("\n⚠️  WARNING: Q&A system failed to initialize!")
        print("Please check that the following environment variables are set:")
        print("- GROQ_API_KEY (or other LLM provider keys)")
        print("- LLM_PROVIDER (default: groq)")
    
    # Run the Flask app
    app.run(debug=debug, host=host, port=port)
