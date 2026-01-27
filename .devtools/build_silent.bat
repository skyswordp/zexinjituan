@echo off
set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_101
set PROJECT_DIR=%~dp0
set SRC_DIR=%PROJECT_DIR%src
set CLASSES_DIR=%PROJECT_DIR%WebRoot\WEB-INF\classes
set LIB_DIR=%PROJECT_DIR%WebRoot\WEB-INF\lib

echo Building project...

REM Generate Java file list
dir /s /b "%SRC_DIR%\*.java" > javafile.txt

REM Compile Java sources with debug info
"%JAVA_HOME%\bin\javac.exe" -encoding UTF-8 -g -d "%CLASSES_DIR%" -sourcepath "%SRC_DIR%" -cp "%LIB_DIR%\*" @javafile.txt
if errorlevel 1 (
    echo Build failed!
    exit /b 1
)

REM Copy XML files
for /r "%SRC_DIR%" %%i in (*.xml) do (
    xcopy "%%i" "%CLASSES_DIR%\" /Y /Q >nul 2>&1
)

REM Copy Struts configs
if exist "%SRC_DIR%\struts" (
    copy /Y "%SRC_DIR%\struts\*.xml" "%CLASSES_DIR%\" >nul 2>&1
)

REM Copy root configs
copy /Y "%SRC_DIR%\struts.xml" "%CLASSES_DIR%\" >nul 2>&1
copy /Y "%SRC_DIR%\*.p12" "%CLASSES_DIR%\" >nul 2>&1

echo Build complete!
exit /b 0
