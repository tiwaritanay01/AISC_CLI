$zip = Join-Path $PWD "aisc_temp.zip"
Write-Host "Downloading 12 AISC experiments from LabX Remote..." -ForegroundColor Cyan
Invoke-WebRequest "https://aisccli.netlify.app/downloads/aisc_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 12 AISC experiments extracted to current directory!" -ForegroundColor Green
