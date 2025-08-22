@echo off
title Plagiarism Checker Pro
color 0B

echo.
echo ========================================
echo   PLAGIARISM CHECKER PRO - LAUNCHER  
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python from https://python.org
    echo or run install.bat first
    echo.
    pause
    exit /b 1
)

echo [INFO] Python detected: 
python --version
echo.

REM Check if required files exist
if not exist "config.py" (
    echo [ERROR] config.py not found!
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

if not exist "gui.py" (
    echo [ERROR] gui.py not found!
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

REM Install requirements if needed
if exist "requirements.txt" (
    echo [INFO] Checking dependencies...
    pip install -r requirements.txt --quiet --disable-pip-version-check
)

echo [INFO] Starting Plagiarism Checker Pro...
echo [INFO] Please wait while the application loads...
echo.
echo ==========================================
echo   APPLICATION RUNNING - DO NOT CLOSE
echo ==========================================
echo.

REM Run the application
python main.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo [ERROR] Application encountered an error
    echo Please check the error messages above
    echo.
) else (
    echo.
    echo [INFO] Application closed successfully
)

echo.
echo Thank you for using Plagiarism Checker Pro!
pause