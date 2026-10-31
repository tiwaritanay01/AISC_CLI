# scripts/build_windows.ps1
# LabX Remote - Windows Standalone Executable Build Script

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " LabX Remote - Windows Executable Build Pipeline" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

# 1. Check Python Launcher
Write-Host "[1/5] Checking Python environment..." -ForegroundColor Yellow
$PythonCmd = "py"
try {
    & $PythonCmd --version
} catch {
    $PythonCmd = "python"
    & $PythonCmd --version
}

# 2. Check / Install build dependencies
Write-Host "`n[2/5] Ensuring PyInstaller and build packages..." -ForegroundColor Yellow
& $PythonCmd -m pip install --upgrade pip pyinstaller typer rich httpx rapidfuzz

# 3. Compile standalone labx.exe with PyInstaller
Write-Host "`n[3/5] Compiling standalone executable via PyInstaller..." -ForegroundColor Yellow
$DistDir = Join-Path $RepoRoot "dist"
$BuildDir = Join-Path $RepoRoot "build"

& $PythonCmd -m PyInstaller `
    --name labx `
    --onefile `
    --console `
    --clean `
    --collect-all labx `
    --collect-all rich `
    --collect-all typer `
    --collect-all httpx `
    --collect-all rapidfuzz `
    labx/__main__.py

# 4. Verify executable exists
Write-Host "`n[4/5] Verifying generated executable..." -ForegroundColor Yellow
$ExePath = Join-Path $DistDir "labx.exe"

if (Test-Path $ExePath) {
    $ExeSize = (Get-Item $ExePath).Length / 1MB
    Write-Host "[SUCCESS] Executable built successfully: $ExePath ($([math]::Round($ExeSize, 2)) MB)" -ForegroundColor Green

    # Test execution
    Write-Host "`n[5/5] Testing binary invocation..." -ForegroundColor Yellow
    & $ExePath --version
} else {
    Write-Error "[FAIL] labx.exe was not generated in $DistDir"
    exit 1
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " BUILD COMPLETE" -ForegroundColor Green
Write-Host " Location: $ExePath" -ForegroundColor White
Write-Host " To add to PATH permanently:" -ForegroundColor Yellow
Write-Host "   [System.Environment]::SetEnvironmentVariable('Path', `$env:Path + ';$DistDir', [System.EnvironmentVariableTarget]::User)" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan

