@echo off
chcp 65001 >nul
echo ========================================
echo Download Apache Tomcat 8.5
echo ========================================
echo.
echo Downloading Tomcat 8.5.100 from Apache official site...
echo URL: https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.100/bin/apache-tomcat-8.5.100-windows-x64.zip
echo.

set DOWNLOAD_DIR=%USERPROFILE%\Downloads
set TOMCAT_ZIP=%DOWNLOAD_DIR%\apache-tomcat-8.5.100.zip
set TOMCAT_DIR=C:\apache-tomcat-8.5.100

echo Download to: %TOMCAT_ZIP%
echo.

powershell -Command "& {Invoke-WebRequest -Uri 'https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.100/bin/apache-tomcat-8.5.100-windows-x64.zip' -OutFile '%TOMCAT_ZIP%'}"

if not exist "%TOMCAT_ZIP%" (
    echo Download failed! Please download manually from:
    echo https://tomcat.apache.org/download-80.cgi
    pause
    exit /b 1
)

echo.
echo Download complete! Extracting to C:\apache-tomcat-8.5.100...
echo.

powershell -Command "& {Expand-Archive -Path '%TOMCAT_ZIP%' -DestinationPath 'C:\' -Force}"

if exist "%TOMCAT_DIR%" (
    echo.
    echo ========================================
    echo Tomcat installed successfully!
    echo Install path: %TOMCAT_DIR%
    echo ========================================
    echo.
    echo Next step: Run "deploy_to_tomcat.bat" to deploy project
    echo.
) else (
    echo Extract failed!
)

pause
