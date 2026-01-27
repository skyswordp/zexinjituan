@echo off
chcp 65001 >nul
echo ========================================
echo 本地编译部署脚本
echo ========================================

set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_101
set PROJECT_DIR=%~dp0
set SRC_DIR=%PROJECT_DIR%src
set CLASSES_DIR=%PROJECT_DIR%WebRoot\WEB-INF\classes
set LIB_DIR=%PROJECT_DIR%WebRoot\WEB-INF\lib

echo.
echo [1/5] 清理旧的编译文件...
if exist "%CLASSES_DIR%\com" rd /s /q "%CLASSES_DIR%\com"
if exist "%CLASSES_DIR%\cn" rd /s /q "%CLASSES_DIR%\cn"

echo [2/5] 生成 Java 文件列表...
dir /s /b "%SRC_DIR%\*.java" > javafile.txt

echo [3/5] 编译 Java 源文件...
"%JAVA_HOME%\bin\javac.exe" -encoding UTF-8 -d "%CLASSES_DIR%" -sourcepath "%SRC_DIR%" -cp "%LIB_DIR%\*" @javafile.txt
if errorlevel 1 (
    echo 编译失败！
    pause
    exit /b 1
)

echo [4/5] 复制配置文件...
rem 复制所有 XML 文件
for /r "%SRC_DIR%" %%i in (*.xml) do (
    xcopy "%%i" "%CLASSES_DIR%\" /Y /Q >nul 2>&1
)

rem 复制 Struts 配置
if exist "%SRC_DIR%\struts" (
    copy /Y "%SRC_DIR%\struts\*.xml" "%CLASSES_DIR%\" >nul 2>&1
)

rem 复制根目录配置
copy /Y "%SRC_DIR%\struts.xml" "%CLASSES_DIR%\" >nul 2>&1
copy /Y "%SRC_DIR%\*.p12" "%CLASSES_DIR%\" >nul 2>&1

echo [5/5] 编译完成！
echo.
echo WebRoot 目录已准备就绪，可以部署到 Tomcat
echo 编译输出: %CLASSES_DIR%
echo.
echo ========================================
echo 提示：
echo 1. 如果使用 Docker: docker build -t png:local .
echo 2. 如果使用 Tomcat: 将 WebRoot 复制到 webapps/CODE
echo ========================================
pause
