param(
    [string]$Topic = "",
    [string]$Diagram = ""
)

if (-not $Topic) {
    Write-Host "==============================================================" -ForegroundColor White
    Write-Host "     Software Engineering (SE) UML & Diagram Generator       " -ForegroundColor White
    Write-Host "==============================================================" -ForegroundColor Gray
    Write-Host "Available Case Studies:" -ForegroundColor Gray
    Write-Host "  [hospital]   Hospital Management System" -ForegroundColor White
    Write-Host "  [library]    Library Management System" -ForegroundColor White
    Write-Host "  [atm]        ATM Management System" -ForegroundColor White
    Write-Host "  [school]     School Management System" -ForegroundColor White
    Write-Host "  [railway]    Railway Management System" -ForegroundColor White
    Write-Host "==============================================================" -ForegroundColor Gray
    $Topic = Read-Host "Enter Case Study (default: hospital)"
    if (-not $Topic) { $Topic = "hospital" }
}

$cleanTopic = $Topic.ToLower().Trim()
if ($cleanTopic -ne "hospital") {
    Write-Host "[*] Defaulting to available implementation: Hospital Management System" -ForegroundColor DarkGray
    $cleanTopic = "hospital"
}

if (-not $Diagram) {
    Write-Host "`nAvailable Diagram Types:" -ForegroundColor Gray
    Write-Host "  [1] usecase   - Use Case Diagram (Actors, Boundary, Include/Extend)" -ForegroundColor White
    Write-Host "  [2] class     - Class Diagram (Attributes, Methods, Relationships)" -ForegroundColor White
    Write-Host "  [3] dfd       - Data Flow Diagram (Level 0 & Level 1 Processes & Stores)" -ForegroundColor White
    Write-Host "  [4] activity  - Activity Diagram (Swimlanes, Decisions, Fork/Join)" -ForegroundColor White
    Write-Host "  [5] all       - Generate & Save All 4 Diagrams" -ForegroundColor White
    $Diagram = Read-Host "Enter Diagram Type [usecase / class / dfd / activity / all, default: usecase]"
    if (-not $Diagram) { $Diagram = "usecase" }
}

$cleanDiag = $Diagram.ToLower().Trim()
switch ($cleanDiag) {
    "1" { $cleanDiag = "usecase" }
    "2" { $cleanDiag = "class" }
    "3" { $cleanDiag = "dfd" }
    "4" { $cleanDiag = "activity" }
    "5" { $cleanDiag = "all" }
}

if ($cleanDiag -eq "all") {
    foreach ($d in @("usecase", "class", "dfd", "activity")) {
        $url = "https://cli-t0km.onrender.com/se/hospital-$d.ps1"
        Invoke-Expression (Invoke-RestMethod $url)
    }
} else {
    $validDiags = @("usecase", "class", "dfd", "activity")
    if ($validDiags -notcontains $cleanDiag) {
        Write-Host "[!] Unknown diagram type: $cleanDiag. Defaulting to 'usecase'." -ForegroundColor DarkGray
        $cleanDiag = "usecase"
    }
    $url = "https://cli-t0km.onrender.com/se/hospital-$cleanDiag.ps1"
    Invoke-Expression (Invoke-RestMethod $url)
}
