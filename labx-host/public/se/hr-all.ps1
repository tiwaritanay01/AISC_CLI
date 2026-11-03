# LabX SE Remote: All 4 Diagrams for HR Management System
Write-Host "Fetching all 4 UML & DFD Diagrams for HR Management System..." -ForegroundColor White
$diags = @("usecase", "class", "dfd", "activity")
foreach ($d in $diags) {
    $url = "https://cli-t0km.onrender.com/se/hr-$d.ps1"
    Invoke-Expression (Invoke-RestMethod $url)
}
Write-Host "`n[OK] All 4 diagrams for HR Management System saved to SE\ folder!" -ForegroundColor White
