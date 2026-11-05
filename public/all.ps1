$zip = Join-Path $PWD "labx_temp.zip"
Write-Host "Downloading all 29 experiments (AISC, ES & RTOS, and Computer Networks) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-ashen-two.vercel.app/downloads/labx_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 29 experiments extracted to current directory!" -ForegroundColor White
