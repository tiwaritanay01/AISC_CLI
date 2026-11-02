$zip = Join-Path $PWD "labx_temp.zip"
Write-Host "Downloading all 22 experiments (AISC + Embedded Systems & RTOS) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://aisccli.netlify.app/downloads/labx_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 22 experiments extracted to current directory!" -ForegroundColor White
