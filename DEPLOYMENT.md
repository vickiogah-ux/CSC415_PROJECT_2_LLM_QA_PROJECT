# Deployment Guide - LLM Q&A System

This guide covers deploying your LLM Q&A System to various cloud platforms.

## 🌐 Deployment Options

| Platform | Cost | Setup Time | Best For |
|----------|------|-----------|----------|
| **Streamlit Cloud** | Free | 5 min | Quick demos |
| **Render** | Free tier | 10 min | Production apps |
| **PythonAnywhere** | Free tier | 15 min | Python projects |
| **Vercel** | Free tier | 20 min | Edge functions |

---

## 🚀 Option 1: Deploy to Streamlit Cloud (EASIEST)

### Prerequisites
- GitHub account (https://github.com)
- Streamlit Cloud account (https://streamlit.io/cloud)

### Step 1: Push to GitHub

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: LLM Q&A System"

# Add remote repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/LLM_QA_Project.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Create Streamlit Cloud App

1. Go to https://streamlit.io/cloud
2. Sign up with GitHub
3. Click "New app"
4. Select your repository
5. Select branch: `main`
6. Select file path: `streamlit_app.py`
7. Click "Deploy"

### Step 3: Add Secrets

1. In Streamlit Cloud app settings, go to "Secrets"
2. Add your API key:

```toml
GROQ_API_KEY = "your_actual_key_here"
OPENAI_API_KEY = "your_key_here"  # Optional
COHERE_API_KEY = "your_key_here"  # Optional
GEMINI_API_KEY = "your_key_here"  # Optional
LLM_PROVIDER = "groq"
```

### Step 4: Share Your App

Your app will be live at:
```
https://your-username-llm-qa-project.streamlit.app
```

---

## 🚀 Option 2: Deploy to Render.com

### Prerequisites
- GitHub account
- Render account (https://render.com)

### Step 1: Prepare for Deployment

Ensure you have:
- `requirements.txt` (already provided)
- `app.py` (Flask application)
- `Procfile` (instructions below)

### Step 2: Create Procfile

Create a file named `Procfile` (no extension) in your project root:

```
web: gunicorn app:app
```

### Step 3: Push to GitHub

```powershell
git add Procfile
git commit -m "Add Procfile for Render deployment"
git push origin main
```

### Step 4: Deploy on Render

1. Go to https://render.com
2. Sign up and connect GitHub
3. Click "New Web Service"
4. Connect your repository
5. Configure:
   - **Name**: llm-qa-system
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Region**: Choose nearest to you

### Step 5: Add Environment Variables

In Render dashboard:
1. Go to Environment Variables
2. Add:
   ```
   GROQ_API_KEY=your_key_here
   LLM_PROVIDER=groq
   ```

### Step 6: Deploy

Click "Deploy" and wait for completion.

Your app will be live at:
```
https://llm-qa-system.onrender.com
```

---

## 🚀 Option 3: Deploy to PythonAnywhere

### Prerequisites
- PythonAnywhere account (https://www.pythonanywhere.com)

### Step 1: Upload Files

1. Login to PythonAnywhere
2. Go to "Files"
3. Upload all project files or clone from GitHub:
   ```bash
   git clone https://github.com/YOUR_USERNAME/LLM_QA_Project.git
   ```

### Step 2: Create Virtual Environment

In PythonAnywhere console:
```bash
cd /home/your_username/LLM_QA_Project
mkvirtualenv --python=/usr/bin/python3.9 llm-qa
pip install -r requirements.txt
```

### Step 3: Create WSGI File

PythonAnywhere → Web → Add new web app

1. Choose "Flask"
2. Choose Python 3.9
3. Edit WSGI file at `/var/www/yourname_pythonanywhere_com_wsgi.py`:

```python
# Add your project to path
import sys
path = '/home/your_username/LLM_QA_Project'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### Step 4: Configure Virtual Environment

In Web app settings:
- Set virtualenv path: `/home/your_username/.virtualenvs/llm-qa`

### Step 5: Add Environment Variables

Create `.env` file in project directory with your API keys.

Your app will be live at:
```
https://yourname.pythonanywhere.com
```

---

## 🚀 Option 4: Deploy to Vercel (Advanced)

### Prerequisites
- Vercel account (https://vercel.com)
- Node.js installed

### Step 1: Create requirements.txt with Flask

Already done! ✅

### Step 2: Create vercel.json

Create `vercel.json` in project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Step 3: Deploy

```powershell
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Add environment variables when prompted
```

---

## 📝 Create Submission File

Create `LLM_QA_hosted_webGUI_link.txt`:

```
==============================================
LLM Q&A SYSTEM - SUBMISSION DETAILS
==============================================

Student Name: [Your Full Name]
Matric Number: [Your Matric Number]
Institution: Covenant University
Department: Computer Science
Level: 400

==============================================
DEPLOYMENT DETAILS
==============================================

Hosted Application URL:
https://[your-hosted-app-url]

GitHub Repository:
https://github.com/[YOUR_USERNAME]/LLM_QA_Project

Deployment Platform:
Streamlit Cloud / Render / PythonAnywhere / Other

==============================================
FEATURES IMPLEMENTED
==============================================

✅ CLI Application (LLM_QA_CLI.py)
   - Natural language question input
   - NLP preprocessing (lowercasing, tokenization, punctuation removal)
   - Support for multiple LLM providers
   - Interactive command-line interface

✅ Web GUI Application (Flask + HTML/CSS)
   - Modern responsive design
   - Real-time question processing
   - Beautiful result visualization
   - Token display with styling
   - Copy-to-clipboard functionality

✅ NLP Preprocessing
   - Lowercasing
   - Tokenization
   - Punctuation removal
   - Whitespace normalization

✅ Multiple LLM Providers
   - Groq (default, free and fast)
   - OpenAI
   - Cohere
   - Google Gemini

✅ Deployment
   - Successfully deployed to [Platform]
   - Live and accessible online
   - Environment variables configured
   - API keys securely stored

==============================================
FILES SUBMITTED
==============================================

Directory Structure:
LLM_QA_Project/
├── LLM_QA_CLI.py              # CLI Application
├── app.py                      # Flask Web Application
├── streamlit_app.py           # Streamlit Version
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # Documentation
├── SETUP_AND_TESTING.md      # Setup guide
├── DEPLOYMENT.md             # Deployment guide
├── LLM_QA_hosted_webGUI_link.txt
├── templates/
│   └── index.html            # Web GUI HTML
└── static/
    └── style.css             # Web GUI CSS

==============================================
TESTING RESULTS
==============================================

CLI Testing: ✅ PASSED
- Question input: Working
- NLP preprocessing: Working
- Token generation: Working
- LLM response: Working

Web GUI Testing: ✅ PASSED
- Page load: Working
- Form submission: Working
- Result display: Working
- Responsive design: Working

API Testing: ✅ PASSED
- /api/ask endpoint: Working
- /api/health endpoint: Working
- Error handling: Working

==============================================
TECHNOLOGY STACK
==============================================

Backend:
- Python 3.8+
- Flask 3.0.0
- Gunicorn (production server)

Frontend:
- HTML5
- CSS3
- JavaScript (vanilla)
- Font Awesome Icons

LLM Integration:
- Groq API (primary)
- OpenAI API (optional)
- Cohere API (optional)
- Google Gemini API (optional)

NLP:
- NLTK (Natural Language Toolkit)
- Custom tokenization fallback

Other:
- python-dotenv (environment management)
- requests (HTTP library)

==============================================
NOTES
==============================================

1. The application requires an API key from one of the supported
   LLM providers (Groq recommended for free tier).

2. The CLI application can be run locally without web hosting.

3. The Web GUI is hosted online and accessible via the provided URL.

4. Both applications share the same core LLM processing logic,
   ensuring consistent results.

5. The system implements comprehensive NLP preprocessing as
   specified in the project requirements.

6. All code is well-documented with comments and follows
   Python best practices.

==============================================
DATE SUBMITTED: [Current Date]
==============================================
```

---

## ✅ Deployment Checklist

Before deploying:

- [ ] All files created and tested locally
- [ ] requirements.txt updated
- [ ] .env.example properly formatted
- [ ] No API keys in code or GitHub
- [ ] README.md complete
- [ ] Code tested and working
- [ ] Git repository created
- [ ] All changes committed

During deployment:

- [ ] Choose platform (Streamlit recommended for simplicity)
- [ ] Connect GitHub repository
- [ ] Configure environment variables
- [ ] Deploy application
- [ ] Test live application
- [ ] Verify all features working

After deployment:

- [ ] Note the live URL
- [ ] Test all features on live site
- [ ] Create submission file with details
- [ ] Update GitHub with final version
- [ ] Ready for submission

---

## 🔗 Quick Links

### Deployment Platforms
- **Streamlit Cloud**: https://streamlit.io/cloud
- **Render**: https://render.com
- **PythonAnywhere**: https://www.pythonanywhere.com
- **Vercel**: https://vercel.com

### LLM Providers
- **Groq**: https://console.groq.com/
- **OpenAI**: https://platform.openai.com/
- **Cohere**: https://cohere.com/
- **Google Gemini**: https://makersuite.google.com/

### Developer Tools
- **GitHub**: https://github.com
- **Git**: https://git-scm.com/

---

## 🆘 Troubleshooting Deployment

### "Module not found" Error
```
Solution: Ensure all packages in requirements.txt are listed
pip freeze > requirements.txt
```

### "API Key not found"
```
Solution: Check environment variables are set correctly
in platform dashboard, not in .env file
```

### "Port already in use"
```
Solution: Use dynamic port assignment (platform handles this)
For local testing, use: python app.py --port 5001
```

### "Request timeout"
```
Solution: Might be slow LLM API response
Increase timeout in Flask configuration
```

---

## 📊 Performance Tips

1. **Use Groq API** - Fastest free option
2. **Enable caching** - For frequently asked questions
3. **Monitor response times** - Platform dashboards show metrics
4. **Scale vertically** - Upgrade platform tier if needed
5. **Optimize code** - Remove unnecessary processing

---

**Last Updated**: November 2025
**Status**: Ready for Deployment ✅
