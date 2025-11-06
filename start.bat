@echo off
REM Quick Start Script for Jaremis Character Server (Windows)

echo Starting Jaremis Character Server...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements_character.txt
echo.

REM Start server
echo Starting server on http://localhost:10000
echo.
echo Press Ctrl+C to stop the server
echo Open browser: http://localhost:10000
echo.

python character_server.py

pause
