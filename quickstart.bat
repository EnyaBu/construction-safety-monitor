@echo off
REM Quick Start Script for Construction Safety Monitor (Windows)

echo ============================================
echo    Construction Safety Monitor - Quick Start
echo ============================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Virtual environment activated

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo pip upgraded

REM Install requirements
echo.
echo Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check the error messages above
    pause
    exit /b 1
)

echo All dependencies installed successfully

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo .env file created
    echo.
    echo WARNING: Please edit .env and add your Gemini API key!
    echo Get your API key from: https://makersuite.google.com/app/apikey
)

REM Create necessary directories
if not exist results mkdir results
if not exist examples\sample_videos mkdir examples\sample_videos

echo.
echo ============================================
echo Setup complete!
echo.
echo Next steps:
echo 1. Add your Gemini API key to .env file
echo 2. Run the web app: streamlit run app.py
echo 3. Or use CLI: python src\main.py --video video.mp4 --sop config\drywall_sop.json
echo.
echo For detailed instructions, see SETUP.md
echo ============================================
echo.
pause
