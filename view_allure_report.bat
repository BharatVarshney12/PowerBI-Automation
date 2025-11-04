@echo off
REM ============================================================================
REM Quick Allure Report Viewer
REM ============================================================================
REM Opens the existing Allure report or generates a new one if needed
REM ============================================================================

echo ============================================================================
echo ALLURE REPORT VIEWER
echo ============================================================================
echo.

REM Check if Allure is installed
where allure >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Allure CLI not found!
    echo.
    echo Please install Allure CLI:
    echo   scoop install allure
    echo   OR download from: https://github.com/allure-framework/allure2/releases
    echo.
    pause
    exit /b 1
)

REM Check if allure-results exists
if not exist "reports\allure-results" (
    echo [ERROR] No Allure results found!
    echo.
    echo Please run generate_allure_report.bat first to create the report.
    echo.
    pause
    exit /b 1
)

echo Opening Allure report server...
echo.
echo Press Ctrl+C to stop the server when done.
echo.

REM Serve the report (this will open in browser)
allure serve reports\allure-results

pause
