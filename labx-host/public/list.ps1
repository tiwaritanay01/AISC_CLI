$cat = Invoke-RestMethod "https://aisccli.netlify.app/catalog.json"
Write-Host "`n==== AISC & Embedded Systems / RTOS Laboratory Experiments ====" -ForegroundColor White
$cat.experiments | Format-Table @{Label="Lab"; Expression={$_.subject}}, @{Label="Exp"; Expression={"#" + ("{0:D2}" -f $_.lab_serial)}}, @{Label="Title"; Expression={$_.title}}, @{Label="Language"; Expression={$_.language}}
Write-Host "Quick commands:" -ForegroundColor White
Write-Host "  Pull ERTOS Exp 2 (Code + Output) : irm https://aisccli.netlify.app/e2.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All ERTOS experiments       : irm https://aisccli.netlify.app/ertos.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All 22 experiments          : irm https://aisccli.netlify.app/all.ps1 | iex`n" -ForegroundColor Gray
