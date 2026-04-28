@echo off
echo ============================================
echo    BBC Food Recipe Scraper
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Starting server at http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app.py

