# ⚡ Quick Start Guide - LLM Q&A System

Get your project running in under **10 minutes**!

## 🚀 Ultra Quick Setup (Windows PowerShell)

```powershell
# 1. Navigate to project
cd "c:\Users\HP\OneDrive\Desktop\COVENANT UNIVERSITY\400 LEVEL\ALPHA SEMESTER\CSC 415\PROJECT 2\LLM_QA_Project"

# 2. Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Get API key from https://console.groq.com/keys
# (Copy your API key)

# 5. Create .env file
Copy-Item .env.example .env
# Edit .env: Open in Notepad and add your API key

# 6. Run CLI
python LLM_QA_CLI.py
# Try asking: "What is machine learning?"
# Type 'quit' to exit

# OR 7. Run Web GUI
python app.py
# Open browser: http://127.0.0.1:5000
```

---

## 📁 Project Files Overview

| File | Purpose |
|------|---------|
| **LLM_QA_CLI.py** | Command-line interface app |
| **app.py** | Flask web application |
| **streamlit_app.py** | Streamlit web version |
| **templates/index.html** | Web GUI interface |
| **static/style.css** | Web GUI styling |
| **requirements.txt** | Python dependencies |
| **.env.example** | API key template |
| **README.md** | Full documentation |
| **SETUP_AND_TESTING.md** | Detailed setup guide |
| **DEPLOYMENT.md** | Deployment instructions |
| **GITHUB_SETUP.md** | GitHub setup guide |

---

## 🎯 What Each Component Does

### LLM_QA_CLI.py
- **What**: Command-line question answering
- **Run**: `python LLM_QA_CLI.py`
- **Use**: Text questions → Get answers in terminal

### app.py (Flask Web GUI)
- **What**: Web interface with beautiful UI
- **Run**: `python app.py`
- **Use**: Open http://127.0.0.1:5000 in browser
- **Features**: Shows tokens, processes questions, styled results

### streamlit_app.py (Streamlit Alternative)
- **What**: Alternative web interface
- **Run**: `streamlit run streamlit_app.py`
- **Use**: Quick cloud deployment option

---

## 🔑 Getting an API Key (< 2 minutes)

### Option 1: Groq (Recommended - Free!)

1. Go to https://console.groq.com/keys
2. Click "Create API Key"
3. Copy the key (starts with `gsk_`)
4. Paste into `.env` file

### Option 2: OpenAI (Requires Card)

1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste into `.env`
4. Change `LLM_PROVIDER=openai` in `.env`

---

## 📝 Testing Checklist (5 min)

```
☐ Virtual environment activated (see (venv) in prompt)
☐ Dependencies installed (pip list shows Flask, groq, etc)
☐ .env file created with API key
☐ CLI runs: python LLM_QA_CLI.py
  - Ask: "Hello"
  - See answer? ✓
  - Type 'quit' to exit
☐ Web GUI runs: python app.py
  - Open http://127.0.0.1:5000
  - Type question
  - See answer? ✓
```

---

## 🐛 Quick Fixes

| Problem | Fix |
|---------|-----|
| "No module named 'flask'" | `.\venv\Scripts\activate` then `pip install -r requirements.txt` |
| "API key not found" | Check .env file exists with correct format |
| "Connection refused" | Make sure Flask app is running: `python app.py` |
| "Port 5000 in use" | Use different port: `FLASK_PORT=5001 python app.py` |

---

## 📊 Project Architecture

```
User Input
    ↓
[NLP Preprocessing] → Lowercase, Tokenize, Remove Punctuation
    ↓
[LLM API Call] → Groq/OpenAI/Cohere/Gemini
    ↓
[Display Results] → Original Q, Processed Q, Tokens, Answer
```

---

## 🌐 Deployment (After Local Testing)

```powershell
# 1. Push to GitHub
git init
git add .
git commit -m "LLM Q&A System"
git remote add origin https://github.com/YOU/LLM_QA_Project.git
git push -u origin main

# 2. Deploy to Streamlit Cloud (Easiest!)
# Go to https://streamlit.io/cloud
# Connect GitHub repo
# Select: streamlit_app.py
# Add secrets: GROQ_API_KEY=your_key
# Done! 🎉

# OR Deploy to Render
# Go to https://render.com
# Connect GitHub repo
# Build: pip install -r requirements.txt
# Start: gunicorn app:app
```

---

## 💡 Example Usage

### CLI
```
📝 Enter your question (or 'quit' to exit): What is Python?

⏳ Processing your question...

📌 ORIGINAL QUESTION:
   What is Python?

🔤 PROCESSED QUESTION:
   what is python

🔤 TOKENIZED WORDS:
   what, is, python

💡 ANSWER:
   Python is a high-level programming language...
```

### Web GUI
```
[Text input: "What is Python?"]
        ↓
    [Ask Button]
        ↓
[4 colored cards showing results with animations]
```

---

## 📚 Next Steps

1. ✅ **Setup complete?** → Run local tests
2. ✅ **Tests passing?** → Push to GitHub (see GITHUB_SETUP.md)
3. ✅ **GitHub ready?** → Deploy to cloud (see DEPLOYMENT.md)
4. ✅ **Deployed?** → Create submission file
5. ✅ **Done!** → Submit to instructor

---

## 🔗 Important Links

- **Groq API**: https://console.groq.com/keys
- **Streamlit Cloud**: https://streamlit.io/cloud
- **Render**: https://render.com
- **GitHub**: https://github.com
- **Full Docs**: See README.md

---

## ✨ Key Features

✅ **Multiple Interfaces**: CLI + Web GUI + Streamlit
✅ **NLP Processing**: Lowercase, Tokenize, Remove Punctuation
✅ **Multiple LLMs**: Groq, OpenAI, Cohere, Gemini
✅ **Beautiful UI**: Responsive, modern design
✅ **Production Ready**: Error handling, validation
✅ **Well Documented**: Guides for everything
✅ **Easy Deployment**: Streamlit Cloud (1 click!)

---

## 📞 Need Help?

| Issue | Where to Find Answer |
|-------|----------------------|
| Setup problems | SETUP_AND_TESTING.md |
| How to deploy | DEPLOYMENT.md |
| GitHub issues | GITHUB_SETUP.md |
| General docs | README.md |

---

## 🎓 About This Project

**Project**: CSC 415 - Project 2
**Topic**: NLP Question-and-Answering System
**Technologies**: Python, Flask, NLTK, LLM APIs
**Status**: ✅ Complete & Ready to Submit

---

**Good luck! 🚀 You've got this!**
