param([string]$Subject = "")

$cat = Invoke-RestMethod "https://cli-t0km.onrender.com/catalog.json"

if (-not $Subject) {
    Write-Host "==========================================================================" -ForegroundColor White
    Write-Host "                   LABX - EXPERIMENTS DIRECTORY BY SUBJECT                " -ForegroundColor White
    Write-Host "==========================================================================" -ForegroundColor Gray
    Write-Host "  [1] aisc    - Artificial Intelligence & Soft Computing (12 Practicals)" -ForegroundColor White
    Write-Host "  [2] ertos   - Embedded Systems & Real-Time Operating Systems (10 Exp)" -ForegroundColor White
    Write-Host "  [3] cn      - Computer Networks (7 Experiments & Setups)" -ForegroundColor White
    Write-Host "  [4] se      - Software Engineering (25 UML & DFD Case Studies)" -ForegroundColor White
    Write-Host "  [5] all     - Show All Subjects" -ForegroundColor White
    Write-Host "==========================================================================" -ForegroundColor Gray
    $Subject = Read-Host "Enter subject to list [1-5 or aisc/ertos/cn/se/all, default: all]"
    if (-not $Subject) { $Subject = "all" }
}

$cleanSub = $Subject.ToLower().Trim()
switch ($cleanSub) {
    "1" { $cleanSub = "aisc" }
    "2" { $cleanSub = "ertos" }
    "3" { $cleanSub = "cn" }
    "4" { $cleanSub = "se" }
    "5" { $cleanSub = "all" }
    "es" { $cleanSub = "ertos" }
    "rtos" { $cleanSub = "ertos" }
}

function Show-AISC {
    Write-Host "`n==========================================================================" -ForegroundColor White
    Write-Host "  AISC Laboratory Practicals (Artificial Intelligence & Soft Computing)   " -ForegroundColor White
    Write-Host "==========================================================================" -ForegroundColor Gray
    $items = $cat.experiments | Where-Object { $_.subject -eq "AISC" }
    $items | Format-Table @{Label="#"; Expression={"a" + $_.id}; Width=5}, @{Label="Title"; Expression={$_.title}; Width=52}, @{Label="Pull Command"; Expression={"irm https://cli-t0km.onrender.com/a" + $_.id + ".ps1 | iex"}}
    Write-Host "Quick Pull: irm https://cli-t0km.onrender.com/aisc.ps1 | iex (all or 1-12)`n" -ForegroundColor Gray
}

function Show-ERTOS {
    Write-Host "`n==========================================================================" -ForegroundColor White
    Write-Host "  ES & RTOS Laboratory Experiments (Embedded Systems & LPC2148 / FreeRTOS)" -ForegroundColor White
    Write-Host "==========================================================================" -ForegroundColor Gray
    $items = $cat.experiments | Where-Object { $_.subject -eq "ES_RTOS" }
    $items | Format-Table @{Label="#"; Expression={"e" + $_.lab_serial}; Width=5}, @{Label="Title"; Expression={$_.title}; Width=52}, @{Label="Pull Command (Code + Output)"; Expression={"irm https://cli-t0km.onrender.com/e" + $_.lab_serial + ".ps1 | iex"}}
    Write-Host "Quick Pull All 10: irm https://cli-t0km.onrender.com/ertos.ps1 | iex`n" -ForegroundColor Gray
}

function Show-CN {
    Write-Host "`n==========================================================================" -ForegroundColor White
    Write-Host "  Computer Networks (CN) Laboratory Experiments & Configurations           " -ForegroundColor White
    Write-Host "==========================================================================" -ForegroundColor Gray
    $items = $cat.experiments | Where-Object { $_.subject -eq "CN" }
    $items | Format-Table @{Label="#"; Expression={"cn" + $_.lab_serial}; Width=6}, @{Label="Title"; Expression={$_.title}; Width=52}, @{Label="Pull Command"; Expression={"irm https://cli-t0km.onrender.com/cn" + $_.lab_serial + ".ps1 | iex"}}
    Write-Host "Quick Pull All: irm https://cli-t0km.onrender.com/cn.ps1 | iex`n" -ForegroundColor Gray
}

function Show-SE {
    Write-Host "`n==========================================================================" -ForegroundColor White
    Write-Host "  Software Engineering (SE) Case Studies (UML & Level 1 DFD Diagrams)     " -ForegroundColor White
    Write-Host "==========================================================================" -ForegroundColor Gray
    Write-Host "25 Case Studies available (Use Case, Class, DFD Level 1, Activity Diagrams)." -ForegroundColor Gray
    Write-Host "Quick Commands:" -ForegroundColor Gray
    Write-Host "  Interactive SE Generator : irm https://cli-t0km.onrender.com/se.ps1 | iex" -ForegroundColor White
    Write-Host "  Hospital Management     : & (irm https://cli-t0km.onrender.com/se.ps1) hospital all" -ForegroundColor White
    Write-Host "  School Management       : & (irm https://cli-t0km.onrender.com/se.ps1) school all" -ForegroundColor White
    Write-Host "  ATM Management System   : & (irm https://cli-t0km.onrender.com/se.ps1) atm all" -ForegroundColor White
    Write-Host "  Download All 100 Diagrams: irm https://cli-t0km.onrender.com/downloads/se_diagrams.zip`n" -ForegroundColor Gray
}

if ($cleanSub -eq "aisc") { Show-AISC }
elseif ($cleanSub -eq "ertos") { Show-ERTOS }
elseif ($cleanSub -eq "cn") { Show-CN }
elseif ($cleanSub -eq "se") { Show-SE }
else {
    Show-AISC
    Show-ERTOS
    Show-CN
    Show-SE
}
