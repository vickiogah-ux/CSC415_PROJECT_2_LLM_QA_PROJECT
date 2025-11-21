# LLM Q&A System Setup and Run Script for Windows PowerShell

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "LLM Q&A System - Setup & Run" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (!(Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ .env file created from .env.example" -ForegroundColor Green
        Write-Host ""
        Write-Host "📝 IMPORTANT: Edit .env file and add your Groq API key:" -ForegroundColor Yellow
        Write-Host "   1. Open: .env" -ForegroundColor White
        Write-Host "   2. Replace: GROQ_API_KEY=your_groq_api_key_here" -ForegroundColor White
        Write-Host "   3. Get free key: https://console.groq.com/keys" -ForegroundColor White
        Write-Host ""
        Write-Host "Press Enter once you've added your API key to continue..."
        Read-Host
    } else {
        Write-Host "❌ .env.example not found!" -ForegroundColor Red
        Write-Host "Creating default .env file..." -ForegroundColor Yellow
        @"
# LLM Q&A System Environment Variables
GROQ_API_KEY=your_groq_api_key_here
LLM_PROVIDER=groq
FLASK_DEBUG=False
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_ENV=development
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✅ Default .env file created" -ForegroundColor Green
        Write-Host ""
        Write-Host "📝 Please edit .env and add your Groq API key" -ForegroundColor Yellow
        Write-Host "Get free key: https://console.groq.com/keys" -ForegroundColor White
        exit 1
    }
}

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Cyan
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (!$pythonCmd) {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from: https://www.python.org" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Python found: $($pythonCmd.Source)" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Virtual environment exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Display startup info
Write-Host "================================================" -ForegroundColor Green
Write-Host "Starting Flask Application" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Server starting..." -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 Web Interface: http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host "💚 Health Check:  http://127.0.0.1:5000/api/health" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Run the Flask app
python app.py

# Deactivate virtual environment on exit
deactivate
