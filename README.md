# LLM Question-and-Answering System

A comprehensive Question-and-Answering system built with Python that connects to Large Language Model (LLM) APIs. This project includes both a powerful CLI application and a beautiful web-based GUI.

## 🌟 Features

### CLI Application (LLM_QA_CLI.py)
- ✅ Natural language question input
- ✅ Advanced NLP preprocessing:
  - Lowercasing
  - Tokenization
  - Punctuation removal
  - Extra whitespace handling
- ✅ Support for multiple LLM providers:
  - Groq (default, free and fast)
  - OpenAI
  - Cohere
  - Google Gemini
- ✅ Interactive command-line interface
- ✅ Display of processed questions and tokens

### Web GUI Application (Flask)
- ✅ Modern, responsive web interface
- ✅ Real-time question processing
- ✅ Beautiful result visualization
- ✅ Token display with animated badges
- ✅ Copy-to-clipboard functionality
- ✅ Error handling with user feedback
- ✅ Health check endpoint
- ✅ Mobile-responsive design

## 📋 Project Structure

```
LLM_QA_Project/
├── LLM_QA_CLI.py              # Command-line interface
├── app.py                      # Flask web application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── templates/
│   └── index.html            # Web GUI HTML template
├── static/
│   └── style.css             # Web GUI styling
└── LLM_QA_hosted_webGUI_link.txt  # Hosted URL (after deployment)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- An API key from one of the supported LLM providers

### Installation

1. **Clone the repository** (or download the project folder)
   ```bash
   cd LLM_QA_Project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your API key
   # For Groq: Get a free key from https://console.groq.com/keys
   ```

   Example `.env` file:
   ```
   GROQ_API_KEY=your_api_key_here
   LLM_PROVIDER=groq
   FLASK_DEBUG=True
   FLASK_PORT=5000
   ```

### Running the Application

#### Option 1: CLI Application
```bash
python LLM_QA_CLI.py
```

Interactive usage:
```
📝 Enter your question (or 'quit' to exit): What is machine learning?

⏳ Processing your question...

📌 ORIGINAL QUESTION:
   What is machine learning?

🔤 PROCESSED QUESTION:
   what is machine learning

🔤 TOKENIZED WORDS:
   what, is, machine, learning

💡 ANSWER:
   [LLM response here...]
```

#### Option 2: Web GUI (Flask)
```bash
python app.py
```

Then open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 🔧 Configuration

### Supported LLM Providers

#### Groq (Recommended - Free & Fast)
- **Website**: https://console.groq.com/
- **Model**: Mixtral 8x7B
- **Speed**: Very fast
- **Cost**: Free tier available
- **Setup**:
  ```
  LLM_PROVIDER=groq
  GROQ_API_KEY=your_key_here
  ```

#### OpenAI
- **Website**: https://platform.openai.com/
- **Model**: GPT-3.5 Turbo
- **Setup**:
  ```
  LLM_PROVIDER=openai
  OPENAI_API_KEY=your_key_here
  ```

#### Cohere
- **Website**: https://cohere.com/
- **Model**: Command R
- **Setup**:
  ```
  LLM_PROVIDER=cohere
  COHERE_API_KEY=your_key_here
  ```

#### Google Gemini
- **Website**: https://makersuite.google.com/
- **Model**: Gemini Pro
- **Setup**:
  ```
  LLM_PROVIDER=gemini
  GEMINI_API_KEY=your_key_here
  ```

## 📚 API Endpoints (Flask)

### POST /api/ask
Submit a question and get a response.

**Request:**
```json
{
  "question": "What is artificial intelligence?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "original_question": "What is artificial intelligence?",
    "processed_question": "what is artificial intelligence",
    "tokens": ["what", "is", "artificial", "intelligence"],
    "token_count": 4,
    "answer": "Artificial intelligence (AI) is..."
  }
}
```

### GET /api/health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "provider": "groq"
}
```

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**:
   - Create a GitHub repository
   - Push your project files

2. **Create Streamlit version** (Optional: For Streamlit Cloud compatibility):
   - Streamlit Cloud works best with `streamlit_app.py` or `app.py` using Streamlit

3. **Deploy on Streamlit Cloud**:
   - Go to https://streamlit.io/cloud
   - Connect your GitHub repository
   - Select the main file to run
   - Add secrets for API keys

### Deploy to Render.com

1. **Push to GitHub**
2. **Create Render account** at https://render.com
3. **Create New Web Service**:
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`
4. **Add environment variables** for API keys
5. **Deploy**

### Deploy to PythonAnywhere

1. **Upload project files**
2. **Set up virtual environment**
3. **Configure WSGI file**
4. **Add environment variables**
5. **Reload web app**

## 🧪 Testing

### Test CLI
```bash
python LLM_QA_CLI.py
# Type: "What is Python programming?"
# Press Ctrl+C to exit
```

### Test Web GUI
```bash
# Terminal 1: Start Flask app
python app.py

# Terminal 2: Test API endpoint
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello, how are you?"}'
```

## 🎯 NLP Preprocessing Details

The system applies the following preprocessing steps:

1. **Lowercasing**: Converts all text to lowercase for consistency
   - Input: "What IS Machine Learning?"
   - Output: "what is machine learning?"

2. **Tokenization**: Splits text into individual words/tokens
   - Input: "what is machine learning?"
   - Output: ["what", "is", "machine", "learning"]

3. **Punctuation Removal**: Removes special characters
   - Input: "What is AI?"
   - Output: "what is ai"

4. **Whitespace Normalization**: Removes extra spaces
   - Input: "what  is   ai"
   - Output: "what is ai"

## 📦 Dependencies

- **Flask 3.0.0**: Web framework
- **python-dotenv 1.0.0**: Environment variable management
- **groq 0.4.2**: Groq API client
- **openai 1.3.0**: OpenAI API client
- **cohere 4.47**: Cohere API client
- **google-generativeai 0.3.0**: Google Gemini client
- **nltk 3.8.1**: Natural Language Processing Toolkit
- **requests 2.31.0**: HTTP library
- **gunicorn 21.2.0**: WSGI HTTP Server

## ⚠️ Important Notes

1. **API Keys**: Keep your API keys secret. Never commit `.env` files to version control.
2. **Rate Limits**: Be aware of rate limits for your chosen API provider.
3. **Costs**: Some APIs may have usage costs. Check provider pricing.
4. **NLTK Data**: The system automatically downloads required NLTK data on first use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests

## 📄 License

This project is created for educational purposes.

## 🎓 Credits

Created for CSC 415 - Project 2 at Covenant University

**Student Information:**
- **Name**: [Your Name]
- **Matric Number**: [Your Matric Number]
- **Institution**: Covenant University
- **Department**: Computer Science
- **Level**: 400

## 📞 Support

For issues or questions:
1. Check the README thoroughly
2. Review error messages
3. Check API provider documentation
4. Test with different questions

## 🔗 Useful Links

- [Groq Console](https://console.groq.com/)
- [OpenAI API](https://platform.openai.com/)
- [Cohere Dashboard](https://cohere.com/)
- [Google Gemini](https://makersuite.google.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [NLTK Documentation](https://www.nltk.org/)

---

**Last Updated**: November 2025
