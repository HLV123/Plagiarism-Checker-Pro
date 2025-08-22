@echo off
title Plagiarism Checker Pro - Installation
color 0A

echo.
echo ========================================
echo   PLAGIARISM CHECKER PRO - INSTALLER
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] Python is installed
python --version

echo.
echo [INFO] Installing required packages...
echo.

REM Install requirements
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [WARNING] Some packages may have failed to install
    echo Trying alternative installation method...
    echo.
    pip install requests urllib3 certifi
)

echo.
echo [INFO] Verifying installation...
python -c "import requests; print('✓ requests installed')" 2>nul || echo "✗ requests installation failed"
python -c "import tkinter; print('✓ tkinter available')" 2>nul || echo "✗ tkinter not available"

echo.
echo ========================================
echo   INSTALLATION COMPLETE
echo ========================================
echo.
echo Next steps:
echo 1. Configure your API keys in config.py
echo 2. Run the application with: python main.py
echo 3. Or use the provided run.bat file
echo.
echo For help, please refer to the documentation
echo.
pause