@echo off
REM PowerBI Automation - Setup and Run Script

echo ========================================
echo PowerBI Automation Framework (POM)
echo ========================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [2/4] Installing Playwright browsers...
playwright install chromium

echo.
echo [3/4] Running tests...
pytest

echo.
echo [4/4] Opening Allure report...
allure serve reports\allure-results

pause
