# LabX SE Remote: All 4 Diagrams for Performance Management System
Write-Host "Fetching all 4 UML & DFD Diagrams for Performance Management System..." -ForegroundColor White
$diags = @("usecase", "class", "dfd", "activity")
foreach ($d in $diags) {
    $url = "https://cli-t0km.onrender.com/se/performance-$d.ps1"
    Invoke-Expression (Invoke-RestMethod $url)
}
Write-Host "`n[OK] All 4 diagrams for Performance Management System saved to SE\ folder!" -ForegroundColor White
