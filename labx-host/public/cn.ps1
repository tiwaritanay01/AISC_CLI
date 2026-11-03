$zip = Join-Path $PWD "cn_temp.zip"
Write-Host "Downloading Computer Networks (CN) Experiments from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/cn.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] Computer Networks experiments extracted into CN/ folder!" -ForegroundColor White
