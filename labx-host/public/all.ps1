$zip = Join-Path $PWD "labx_temp.zip"
Write-Host "Downloading all 28 experiments (AISC, ES & RTOS, and Computer Networks) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/labx_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 28 experiments extracted to current directory!" -ForegroundColor White
