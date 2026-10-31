$zip = Join-Path $PWD "labx_temp.zip"
Write-Host "Downloading all 12 AISC experiments from LabX Remote..." -ForegroundColor Cyan
Invoke-WebRequest "https://aisccli.netlify.app/downloads/labx_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 12 experiments extracted to current directory!" -ForegroundColor Green
