$zip = Join-Path $PWD "ertos_temp.zip"
Write-Host "Downloading 10 Embedded Systems & RTOS experiments from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://aisccli.netlify.app/downloads/ertos.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 10 ES & RTOS experiments extracted to current directory!" -ForegroundColor White
