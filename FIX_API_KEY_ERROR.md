# Quick Fix for "Q&A System Not Initialized" Error

## The Problem
Your Render app shows: **"Q&A system not initialized. Please check API configuration."**

This happens because the `GROQ_API_KEY` environment variable is not set on Render.

---

## Solution (Choose One)

### Option 1: Fix on Render (Recommended for Production)

1. **Get Free API Key** (2 minutes)
   - Visit: https://console.groq.com/keys
   - Sign up with any email
   - Click "Create API Key"
   - Copy the key

2. **Add to Render Dashboard** (1 minute)
   - Go to: https://render.com/dashboard
   - Click your service (llm-qa-system)
   - Click **Environment** tab
   - Click **Add Environment Variable**
   - Name: `GROQ_API_KEY`
   - Value: (paste your key from step 1)
   - Click **Save**

3. **Redeploy** (2-3 minutes)
   - Click **Manual Deploy** → **Deploy latest commit**
   - Wait for "Your service is live"
   - Visit your Render URL
   - Should work now! ✅

---

### Option 2: Test Locally First

**Before Render, test on your computer:**

1. **Edit .env file**
   - Open: `.env` in your project folder
   - Replace: `GROQ_API_KEY=your_groq_api_key_here`
   - With: Your actual key from https://console.groq.com/keys
   - Save the file

2. **Run the app** (PowerShell)
   ```powershell
   # Navigate to project folder
   cd "c:\Users\HP\OneDrive\Desktop\...\LLM_QA_Project"
   
   # Run setup script
   .\setup_and_run.ps1
   ```
   
   Or manually:
   ```powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   .\venv\Scripts\Activate.ps1
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the app
   python app.py
   ```

3. **Test**
   - Open browser: http://127.0.0.1:5000
   - Ask a question
   - Should work! ✅

---

## Verify It's Fixed

### Test 1: Health Check
```
Visit: https://your-app.onrender.com/api/health

Should show:
{
  "status": "healthy",
  "provider": "groq",
  "ready": true
}
```

### Test 2: Full App
```
Visit: https://your-app.onrender.com
- Page should load
- Ask a question
- Should get an answer
```

---

## What Changed in the Fix

I improved the error messages to show you exactly what's wrong:

**Before:**
```
Q&A system not initialized. Please check API configuration.
```

**Now:**
```
{
  "error": "Q&A system not initialized",
  "details": "API key for groq not found in environment variables",
  "fix": {
    "on_render": "Add GROQ_API_KEY environment variable in Render dashboard",
    "locally": "Create .env file with GROQ_API_KEY=your_key_here",
    "get_key": "https://console.groq.com/keys"
  }
}
```

Plus:
- Better startup logging in server
- Health check endpoint shows detailed error info
- Setup script for easy local testing
- `.env` file template for local development

---

## Still Not Working?

1. **Check Render Logs**
   - Render Dashboard → Your Service → Logs
   - Look for error messages

2. **Verify Syntax**
   - Make sure `GROQ_API_KEY` value has NO spaces
   - Make sure it's the full key, not partial

3. **Test Health Endpoint**
   - Visit: `https://your-app.onrender.com/api/health`
   - Copy the full error message
   - Check RENDER_TROUBLESHOOTING.md for that specific error

4. **Redeploy**
   - After adding env variable, click **Manual Deploy**
   - Wait for "Your service is live"
   - Try again

---

## Files Updated

- **app.py** - Better error messages and logging
- **setup_and_run.ps1** - Easy local setup script
- **.env** - Template for local development
- **render.yaml** - Explicit Render configuration

All changes are on GitHub → Render will auto-deploy

---

## Next Steps

1. ✅ Get Groq API key (https://console.groq.com/keys)
2. ✅ Add to Render environment (dashboard)
3. ✅ Redeploy on Render
4. ✅ Test your app - should work!

Good luck! 🚀
