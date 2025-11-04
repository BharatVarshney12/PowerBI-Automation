@echo off
REM ============================================================================
REM PowerBI Validation with Allure Report Generation
REM ============================================================================
REM This script runs the complete PowerBI validation workflow and generates
REM a beautiful Allure HTML report for stakeholder review.
REM ============================================================================

echo ============================================================================
echo POWERBI VALIDATION WITH ALLURE REPORTING
echo ============================================================================
echo.

REM Clean old Allure results
if exist "reports\allure-results" (
    echo Cleaning old Allure results...
    rmdir /s /q "reports\allure-results"
)

mkdir reports\allure-results 2>nul

echo.
echo ============================================================================
echo STEP 1: Running Validation Tests with Pytest
echo ============================================================================
echo.

REM Run pytest with Allure reporting
pytest test_validation_allure.py --alluredir=reports/allure-results -v --tb=short

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Some tests failed. Check the results above.
    echo.
)

echo.
echo ============================================================================
echo STEP 2: Generating Allure HTML Report
echo ============================================================================
echo.

REM Check if Allure is installed
where allure >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Allure CLI not found!
    echo.
    echo Please install Allure CLI to generate HTML reports:
    echo.
    echo Option 1 - Using Scoop:
    echo   scoop install allure
    echo.
    echo Option 2 - Manual Download:
    echo   Download from: https://github.com/allure-framework/allure2/releases
    echo   Extract and add to PATH
    echo.
    echo Option 3 - Using npm:
    echo   npm install -g allure-commandline
    echo.
    echo Allure results have been saved in: reports\allure-results
    echo You can generate the report later with: allure serve reports\allure-results
    echo.
    pause
    exit /b 1
)

REM Generate Allure report
allure generate reports\allure-results -o reports\allure-report --clean

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to generate Allure report
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo SUCCESS! Allure Report Generated
echo ============================================================================
echo.
echo Report Location: reports\allure-report\index.html
echo.
echo Opening Allure report in browser...
echo.

REM Open report in default browser
start "" "reports\allure-report\index.html"

echo.
echo ============================================================================
echo VALIDATION COMPLETED
echo ============================================================================
echo.
echo Next Steps:
echo   1. Review the Allure report in your browser
echo   2. Check validation_reports\ folder for detailed Excel reports
echo   3. Share the Allure HTML report with stakeholders
echo.
echo To view the report again later, run: allure open reports\allure-report
echo.

pause
