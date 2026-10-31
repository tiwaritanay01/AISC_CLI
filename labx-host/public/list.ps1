$cat = Invoke-RestMethod "https://aisccli.netlify.app/catalog.json"
Write-Host "`n==== AISC Laboratory Experiments (LabX Remote) ====" -ForegroundColor Cyan
$cat.experiments | Format-Table @{Label="ID"; Expression={"Exp " + ("{0:D2}" -f $_.id)}}, @{Label="Title"; Expression={$_.title}}, @{Label="Language"; Expression={$_.language}}
Write-Host "Quick commands:" -ForegroundColor Yellow
Write-Host "  Pull all experiments : irm https://aisccli.netlify.app/all.ps1 | iex" -ForegroundColor White
Write-Host "  Pull one experiment  : & (irm https://aisccli.netlify.app/get.ps1) <id>`n" -ForegroundColor White
