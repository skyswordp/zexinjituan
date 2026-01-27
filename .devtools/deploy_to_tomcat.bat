@echo off
chcp 65001 >nul
echo ========================================
echo Deploy to Tomcat
echo ========================================

set TOMCAT_DIR=C:\apache-tomcat-8.5.100
set PROJECT_DIR=%~dp0
set WEBAPP_DIR=%TOMCAT_DIR%\webapps\CODE

if not exist "%TOMCAT_DIR%" (
    echo ERROR: Tomcat not found at %TOMCAT_DIR%
    echo Please run "download_tomcat.bat" first or install Tomcat manually
    pause
    exit /b 1
)

echo.
echo [1/3] Compiling project...
call "%PROJECT_DIR%build.bat"

echo.
echo [2/3] Deploying to Tomcat...
if exist "%WEBAPP_DIR%" (
    echo Removing old deployment...
    rd /s /q "%WEBAPP_DIR%"
)

echo Copying WebRoot to %WEBAPP_DIR%...
xcopy /E /I /Y "%PROJECT_DIR%WebRoot" "%WEBAPP_DIR%"

echo.
echo [3/3] Starting Tomcat...
cd /d "%TOMCAT_DIR%\bin"

echo Stopping Tomcat if running...
call shutdown.bat 2>nul
timeout /t 3 /nobreak >nul

echo Starting Tomcat...
start "Tomcat Server" cmd /c "catalina.bat run"

echo.
echo ========================================
echo Deployment complete!
echo.
echo Tomcat is starting...
echo Wait 10-15 seconds, then access:
echo http://localhost:8080/CODE/
echo ========================================
echo.
echo Press any key to open browser...
pause >nul

timeout /t 10 /nobreak >nul
start http://localhost:8080/CODE/
