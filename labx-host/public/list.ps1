$cat = Invoke-RestMethod "https://cli-t0km.onrender.com/catalog.json"
Write-Host "`n==== AISC, Embedded Systems / RTOS & Computer Networks Experiments ====" -ForegroundColor White
$cat.experiments | Format-Table @{Label="Lab"; Expression={$_.subject}}, @{Label="Exp"; Expression={"#" + ("{0:D2}" -f $_.lab_serial)}}, @{Label="Title"; Expression={$_.title}}, @{Label="Language"; Expression={$_.language}}
Write-Host "Quick commands:" -ForegroundColor White
Write-Host "  Pull AISC Practical (e.g. 1)     : irm https://cli-t0km.onrender.com/a1.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull AISC Interactive (all/1-12) : irm https://cli-t0km.onrender.com/aisc.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull ERTOS Exp 2 (Code + Output) : irm https://cli-t0km.onrender.com/e2.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All ERTOS (Code + Outputs)  : irm https://cli-t0km.onrender.com/ertos.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All Computer Networks (CN)  : irm https://cli-t0km.onrender.com/cn.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull CN Java Socket Programming  : irm https://cli-t0km.onrender.com/cnsocket.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull CN Dijkstra Algorithm       : irm https://cli-t0km.onrender.com/dijkstra.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull CN GNS3 Static Routing      : irm https://cli-t0km.onrender.com/staticrouting.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All experiments             : irm https://cli-t0km.onrender.com/all.ps1 | iex`n" -ForegroundColor Gray
