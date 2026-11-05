param([string]$Choice = "")

if (-not $Choice) {
    Write-Host "==============================================================" -ForegroundColor White
    Write-Host "               AISC Practicals Delivery Tool                  " -ForegroundColor White
    Write-Host "==============================================================" -ForegroundColor Gray
    Write-Host "  [all]   Pull ALL 12 AISC Practicals (Complete bundle)" -ForegroundColor Gray
    Write-Host "  [1-12]  Pull a specific Practical by serial number" -ForegroundColor Gray
    Write-Host "==============================================================" -ForegroundColor Gray
    $Choice = Read-Host "Enter choice [all or 1-12, default: all]"
}

if (-not $Choice -or $Choice -eq "all") {
    $zip = Join-Path $PWD "aisc_temp.zip"
    Write-Host "Downloading all 12 AISC Practicals from LabX Remote..." -ForegroundColor White
    Invoke-WebRequest "https://nirpin.vercel.app/downloads/aisc_experiments.zip" -OutFile $zip -UseBasicParsing
    Expand-Archive $zip -DestinationPath $PWD -Force
    Remove-Item $zip -Force
    Write-Host "[OK] All 12 AISC Practicals extracted into current directory!" -ForegroundColor White
} else {
    $num = [int]$Choice
    if ($num -ge 1 -and $num -le 12) {
        $scriptUrl = "https://nirpin.vercel.app/a$num.ps1"
        Invoke-Expression (Invoke-RestMethod $scriptUrl)
    } else {
        Write-Host "[!] Invalid practical number: $Choice (Please enter 1-12 or 'all')" -ForegroundColor DarkGray
    }
}
