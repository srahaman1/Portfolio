@echo off
REM Finance App Launcher for Windows
REM Double-click this file to run the application

echo ====================================
echo Personal Finance Calculator
echo ====================================
echo.
echo Starting application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    echo.
    pip install -r requirements.txt
    echo.
)

REM Run the application
python finance_app.py

pause
