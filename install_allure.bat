@echo off
REM ============================================================================
REM Install Allure CLI using Scoop Package Manager
REM ============================================================================

echo ============================================================================
echo ALLURE CLI INSTALLATION
echo ============================================================================
echo.
echo This script will install Allure CLI using Scoop package manager.
echo Scoop is a command-line installer for Windows.
echo.

REM Check if Scoop is already installed
where scoop >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [✓] Scoop is already installed
    goto install_allure
)

echo [!] Scoop is not installed. Installing Scoop first...
echo.

REM Install Scoop
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; irm get.scoop.sh | iex"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to install Scoop
    echo.
    echo Please install manually:
    echo   1. Open PowerShell as Administrator
    echo   2. Run: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo   3. Run: irm get.scoop.sh ^| iex
    echo.
    pause
    exit /b 1
)

echo.
echo [✓] Scoop installed successfully!
echo.

:install_allure

REM Check if Allure is already installed
where allure >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [✓] Allure CLI is already installed
    allure --version
    echo.
    echo Installation complete! You can now run:
    echo   generate_allure_report.bat
    echo.
    pause
    exit /b 0
)

echo Installing Allure CLI...
echo.

scoop install allure

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to install Allure
    echo.
    echo Please try manual installation:
    echo   Download from: https://github.com/allure-framework/allure2/releases
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo SUCCESS! Allure CLI Installed
echo ============================================================================
echo.

allure --version

echo.
echo You can now run:
echo   generate_allure_report.bat - Generate new validation report
echo   view_allure_report.bat     - View existing report
echo.

pause
