# Troubleshooting: Render Deployment Issues

## The Problem: "Application Won't Load on Render"

Your app may deploy successfully but show errors like:
- Blank page
- 503 Service Unavailable
- 500 Internal Server Error
- Connection timeout

## Common Causes & Solutions

### 1. **Missing API Key (Most Common)**

**Symptom**: Page loads but shows "Q&A system not initialized" error

**Solution**:
1. Go to your Render dashboard
2. Open your service settings
3. Click "Environment" tab
4. Add these variables:
   ```
   GROQ_API_KEY = your_actual_key_here
   LLM_PROVIDER = groq
   ```
5. Click "Deploy" to redeploy with the new environment variables

**Get a Free Groq API Key**:
- Visit: https://console.groq.com/keys
- Sign up with email
- Generate an API key
- Copy it and paste in Render dashboard

### 2. **Check Render Logs**

**To see what went wrong**:
1. In Render dashboard, open your service
2. Click "Logs" tab at the top
3. Look for error messages like:
   - `ModuleNotFoundError: No module named 'flask'`
   - `API key for groq not found in environment variables`
   - `Port already in use`

### 3. **Procfile Issues**

Your `Procfile` should contain:
```
web: gunicorn app:app
```

Make sure:
- File is named exactly `Procfile` (no `.txt` extension)
- It's in the **project root** (same level as `app.py`)
- No extra spaces or lines

### 4. **Build Command Issues**

If you see: `No module named 'gunicorn'`

**Solution**: Add to `requirements.txt`:
```
gunicorn==21.2.0
```

Then:
```bash
git add requirements.txt
git commit -m "Add gunicorn"
git push
```

And redeploy on Render.

### 5. **Port Configuration**

Flask on Render **must** listen on the PORT Render provides.

Your `app.py` already does this correctly:
```python
port = int(os.getenv('PORT', os.getenv('FLASK_PORT', 5000)))
```

No changes needed unless you get port errors.

### 6. **Static Files Not Loading (CSS/Images)**

**Symptom**: Page loads but looks broken (no styling)

**Solution**:
1. Verify folder structure:
```
LLM_QA_Project/
├── app.py
├── Procfile
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    └── style.css
```

2. The `templates` and `static` folders **must** be in the same directory as `app.py`

3. In your HTML, use Flask's `url_for`:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

### 7. **Deployment Steps Checklist**

1. ✅ Commit all changes to GitHub
```bash
git add .
git commit -m "Fix: Render deployment"
git push origin main
```

2. ✅ Go to Render.com dashboard
3. ✅ Select your service
4. ✅ Click "Manual Deploy" → "Deploy latest commit"
5. ✅ Wait for build to complete (check Logs)
6. ✅ Once "Your service is live" appears, test your URL

### 8. **Test Your Deployment**

```bash
# Get your Render URL (looks like: https://llm-qa-system.onrender.com)

# Test health check:
curl https://your-app.onrender.com/api/health

# Should return:
# {"status": "healthy", "provider": "groq"}
```

If it returns "misconfigured", you're missing the API key!

### 9. **Complete Environment Variables List**

Render → Your Service → Environment

Add these (minimum):
```
GROQ_API_KEY = your_key_here
LLM_PROVIDER = groq
FLASK_ENV = production
```

Optional (for other LLM providers):
```
OPENAI_API_KEY = your_key_here
COHERE_API_KEY = your_key_here
GEMINI_API_KEY = your_key_here
```

### 10. **If Still Not Working: Debug Mode**

Temporarily add to Render environment:
```
FLASK_DEBUG = true
```

Then check logs again. This will show more detailed error messages.

**IMPORTANT**: Remove `FLASK_DEBUG = true` after debugging for security!

---

## Quick Fixes (Try These First)

### Fix 1: API Key Not Set
```
Dashboard → Environment → Add GROQ_API_KEY → Deploy
```

### Fix 2: Cache Issues
```
Dashboard → Settings → Clear Build Cache → Manual Deploy
```

### Fix 3: Stale Build
```
git push (any commit) → Render auto-rebuilds
OR
Dashboard → Manual Deploy
```

### Fix 4: Health Check Verification
```
Go to: https://your-app.onrender.com/api/health
Should show: {"status":"healthy","provider":"groq"}
```

---

## File Checklist for Render

Must exist in GitHub repo root:
- ✅ `app.py` (Flask application)
- ✅ `requirements.txt` (with gunicorn)
- ✅ `Procfile` (with no extension)
- ✅ `templates/index.html` (HTML template)
- ✅ `static/style.css` (CSS styling)
- ✅ `.gitignore` (exclude `.env`)
- ✅ `render.yaml` (optional, for extra config)

Must NOT be in repo:
- ❌ `.env` file (use Render dashboard instead)
- ❌ Any file with actual API keys

---

## Contact Support

If issues persist:

1. **Check Render Logs**: Dashboard → Logs
2. **Verify GitHub Push**: All changes on `main` branch
3. **Test Locally First**:
   ```bash
   pip install -r requirements.txt
   python app.py
   # Should work on http://localhost:5000
   ```
4. **Review This Guide**: Most issues covered above

---

## Common Error Messages & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `No module named 'gunicorn'` | gunicorn not in requirements.txt | Add gunicorn to requirements.txt |
| `API key for groq not found` | GROQ_API_KEY not set on Render | Add environment variable in dashboard |
| `Module not found 'flask'` | requirements.txt not installed | Check Procfile and requirements.txt |
| `Address already in use` | Port conflict (shouldn't happen on Render) | Change port or clear build cache |
| `Connection refused` | App crashed during startup | Check logs for errors, fix app.py |

---

**Updated**: November 2025
**Status**: Ready to Deploy ✅

---

## Next Steps

1. Get Groq API key: https://console.groq.com/keys
2. Add to Render environment variables
3. Deploy: GitHub push → Render auto-deploys
4. Test: Visit your Render URL
5. If stuck: Follow troubleshooting steps above

Good luck! 🚀
