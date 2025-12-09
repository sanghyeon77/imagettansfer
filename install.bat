@echo off
echo ============================================================
echo Installation Script - Video Auto Capture System
echo ============================================================
echo.

echo [1/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
echo OK: Python found
python --version
echo.

echo [2/4] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [3/4] Installing required packages...
echo.
echo Installing Flask...
python -m pip install Flask==3.0.0
echo.
echo Installing moviepy...
python -m pip install moviepy==1.0.3
echo.
echo Installing discord-webhook...
python -m pip install discord-webhook==1.3.0
echo.
echo Installing Werkzeug...
python -m pip install Werkzeug==3.0.1
echo.

echo [4/4] Checking FFMPEG...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: FFMPEG is not installed!
    echo.
    echo Install FFMPEG using one of these methods:
    echo.
    echo Method 1 - Chocolatey (Recommended):
    echo   1. Run PowerShell as Administrator
    echo   2. choco install ffmpeg
    echo.
    echo Method 2 - Manual:
    echo   1. Download from https://github.com/BtbN/FFmpeg-Builds/releases
    echo   2. Extract to C:\ffmpeg
    echo   3. Add C:\ffmpeg\bin to PATH
    echo.
    echo Please install FFMPEG and run this script again.
    echo.
) else (
    echo OK: FFMPEG found
    ffmpeg -version 2>&1 | findstr "version"
)
echo.

echo ============================================================
echo Installed packages:
echo ============================================================
python -m pip list | findstr /i "Flask moviepy discord Werkzeug"
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo To start the server:
echo    python app.py
echo.
echo Then open in browser:
echo    http://127.0.0.1:5000
echo.
echo Your Discord Webhook URL:
echo    https://discordapp.com/api/webhooks/1437610959303606343/fRXM_sVUEZUP9GgZSH5qOxBMeA2PdCBzUFsjIB4Wap3ow7rylZ5kS6GkINuyK9Wfiyyb
echo.
pause
