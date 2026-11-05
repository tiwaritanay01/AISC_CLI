# scripts/install_windows.ps1
# LabX Remote - Automated Student Installation Script for Windows
# Run in PowerShell: irm https://cli-t0km.onrender.com/install.ps1 | iex

param (
    [string]$InstallDir = "$env:LOCALAPPDATA\Programs\LabX",
    [string]$ReleaseUrl = "https://cli-t0km.onrender.com/downloads/labx.exe"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " LabX Remote - Windows Automated Installer" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Create target installation directory
Write-Host "`n[1/3] Preparing installation directory: $InstallDir" -ForegroundColor Yellow
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

$TargetExe = Join-Path $InstallDir "labx.exe"

# 2. Download executable
Write-Host "`n[2/3] Downloading latest labx.exe from $ReleaseUrl..." -ForegroundColor Yellow
try {
    # If a local build exists, allow copying from local dist for offline setup
    $LocalDist = Join-Path (Split-Path -Parent $PSScriptRoot) "dist\labx.exe"
    if (Test-Path $LocalDist) {
        Write-Host "Found local built binary at $LocalDist. Installing locally..." -ForegroundColor Cyan
        Copy-Item -Path $LocalDist -Destination $TargetExe -Force
    } else {
        Invoke-WebRequest -Uri $ReleaseUrl -OutFile $TargetExe -UseBasicParsing
    }
} catch {
    Write-Error "Failed to retrieve labx.exe: $_"
    exit 1
}

# 3. Add to User PATH if not already present
Write-Host "`n[3/3] Configuring Windows User PATH environment variable..." -ForegroundColor Yellow
$UserPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
$PathEntries = $UserPath -split ";"

if ($PathEntries -notcontains $InstallDir) {
    $NewPath = "$UserPath;$InstallDir"
    [Environment]::SetEnvironmentVariable("Path", $NewPath, [EnvironmentVariableTarget]::User)
    $env:Path = "$env:Path;$InstallDir"
    Write-Host "Added $InstallDir to User PATH." -ForegroundColor Green
} else {
    Write-Host "$InstallDir is already in User PATH." -ForegroundColor Green
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " LABX REMOTE INSTALLED SUCCESSFULLY!" -ForegroundColor Green
Write-Host " Run 'labx' in any new terminal window to begin." -ForegroundColor White
Write-Host " Try:" -ForegroundColor Yellow
Write-Host "   labx list" -ForegroundColor White
Write-Host "   labx download 3" -ForegroundColor White
Write-Host "   labx run 3" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan

