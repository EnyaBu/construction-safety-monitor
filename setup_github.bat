@echo off
REM Automated GitHub Setup Script for Construction Safety Monitor (Windows)

echo ============================================
echo    Construction Safety Monitor - GitHub Setup
echo ============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed
    echo Please install Git from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo Git is installed

REM Check if already a git repository
if exist ".git" (
    echo WARNING: This is already a git repository.
    set /p reinit="Do you want to re-initialize? (y/N): "
    if /i "%reinit%"=="y" (
        rmdir /s /q .git
        echo Removed existing git repository
    ) else (
        echo Keeping existing repository.
        pause
        exit /b 0
    )
)

REM Get GitHub username
echo.
set /p github_username="Enter your GitHub username: "

if "%github_username%"=="" (
    echo ERROR: GitHub username is required!
    pause
    exit /b 1
)

REM Get repository name
echo.
set /p repo_name="Repository name [construction-safety-monitor]: "
if "%repo_name%"=="" set repo_name=construction-safety-monitor

REM Update README
echo.
echo Updating README with your information...
powershell -Command "(gc README.md) -replace 'yourusername', '%github_username%' | Out-File -encoding ASCII README.md"
echo README updated

REM Get user's name for license
echo.
set /p user_name="Your full name (for LICENSE): "

if not "%user_name%"=="" (
    powershell -Command "(gc LICENSE) -replace '\[Your Name\]', '%user_name%' | Out-File -encoding ASCII LICENSE"
    echo LICENSE updated
)

REM Initialize git repository
echo.
echo Initializing git repository...
git init
echo Git repository initialized

REM Create directories
if not exist "examples\sample_videos\brickmasonry" mkdir examples\sample_videos\brickmasonry
type nul > examples\sample_videos\.gitkeep

REM Add all files
echo.
echo Adding files to git...
git add .
echo Files added

REM Create initial commit
echo.
echo Creating initial commit...
git commit -m "Initial commit: Construction Safety Monitor - AI-powered construction safety monitoring - Brick masonry SOP based on Quikrete guide - Video analysis with Gemini API - Semantic similarity with Sentence Transformers - Web interface with Streamlit - Ready for Kaggle dataset integration"
echo Initial commit created

REM Set main branch
git branch -M main

REM Add remote
echo.
echo Adding GitHub remote...
git remote add origin https://github.com/%github_username%/%repo_name%.git
echo Remote added

REM Display next steps
echo.
echo ============================================
echo Setup complete!
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Create the repository on GitHub:
echo    Go to: https://github.com/new
echo    Name: %repo_name%
echo    Description: AI-powered construction safety monitoring system
echo    Keep it PUBLIC for hackathon visibility
echo    DO NOT initialize with README
echo.
echo 2. Push your code to GitHub:
echo    git push -u origin main
echo.
echo    (You'll need to authenticate with GitHub)
echo    (Use Personal Access Token, not password)
echo.
echo 3. Download the Kaggle dataset:
echo    See DATASET.md for instructions
echo.
echo 4. Get your Gemini API key:
echo    Visit: https://makersuite.google.com/app/apikey
echo    Add to .env file
echo.
echo 5. Test the application:
echo    streamlit run app.py
echo.
echo ============================================
echo Repository URL will be:
echo https://github.com/%github_username%/%repo_name%
echo ============================================
echo.
pause
