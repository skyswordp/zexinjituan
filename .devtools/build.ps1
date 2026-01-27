$JAVA_HOME = "C:\Program Files\Java\jdk1.8.0_101"
$DEVTOOLS_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_DIR = Join-Path (Split-Path -Parent $DEVTOOLS_DIR) "png"
$SRC_DIR = Join-Path $PROJECT_DIR "src"
$CLASSES_DIR = Join-Path $PROJECT_DIR "WebRoot\WEB-INF\classes"
$LIB_DIR = Join-Path $PROJECT_DIR "WebRoot\WEB-INF\lib"
$JAVAFILE = Join-Path $DEVTOOLS_DIR "javafile.txt"

Write-Host "Building project..." -ForegroundColor Cyan

# Generate Java file list
$javaFiles = Get-ChildItem -Path $SRC_DIR -Filter *.java -Recurse | Select-Object -ExpandProperty FullName
$javaFiles | Out-File -FilePath $JAVAFILE -Encoding ASCII

# Compile with debug info
& "$JAVA_HOME\bin\javac.exe" -encoding UTF-8 -g -d $CLASSES_DIR -sourcepath $SRC_DIR -cp "$LIB_DIR\*" "@$JAVAFILE"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

# Copy XML files
Get-ChildItem -Path $SRC_DIR -Filter *.xml -Recurse | ForEach-Object {
    Copy-Item $_.FullName -Destination $CLASSES_DIR -Force -ErrorAction SilentlyContinue
}

# Copy properties files
Get-ChildItem -Path $SRC_DIR -Filter *.properties -Recurse | ForEach-Object {
    Copy-Item $_.FullName -Destination $CLASSES_DIR -Force -ErrorAction SilentlyContinue
}

# Copy Struts configs
$strutsDir = Join-Path $SRC_DIR "struts"
if (Test-Path $strutsDir) {
    Get-ChildItem -Path $strutsDir -Filter *.xml | ForEach-Object {
        Copy-Item $_.FullName -Destination $CLASSES_DIR -Force
    }
}

# Copy root configs
Copy-Item (Join-Path $SRC_DIR "struts.xml") -Destination $CLASSES_DIR -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $SRC_DIR -Filter *.p12 | ForEach-Object {
    Copy-Item $_.FullName -Destination $CLASSES_DIR -Force -ErrorAction SilentlyContinue
}

Write-Host "Build complete!" -ForegroundColor Green
exit 0
