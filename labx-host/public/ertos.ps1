$zip = Join-Path $PWD "ertos_temp.zip"
Write-Host "Downloading all 10 Embedded Systems & RTOS experiments (Code + All Output Images & PDFs) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/ertos.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 10 ES & RTOS experiments with code and authentic outputs extracted to current directory!" -ForegroundColor White
