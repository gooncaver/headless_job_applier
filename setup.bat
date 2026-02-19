@echo off
REM Setup script for Headless Job Applier - Windows
REM This script initializes the development environment

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Headless Job Applier - Setup Script
echo ========================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    exit /b 1
)

echo [1/7] Checking Python version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo [2/7] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping creation
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/7] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)
echo.

REM Upgrade pip
echo [4/7] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade pip
    exit /b 1
)
echo.

REM Install dependencies
echo [5/7] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo.

REM Install Playwright browsers
echo [6/7] Installing Playwright browsers...
playwright install chromium
if %errorlevel% neq 0 (
    echo WARNING: Playwright browser installation had issues, continuing anyway...
)
echo.

REM Initialize application
echo [7/7] Initializing application...
python src/main.py setup
if %errorlevel% neq 0 (
    echo ERROR: Application setup failed
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env and fill in your credentials
echo 2. Update input/user_profile.yaml with your information
echo 3. Run: python src/main.py status
echo.
echo To activate the environment in the future:
echo   venv\Scripts\activate.bat
echo.
