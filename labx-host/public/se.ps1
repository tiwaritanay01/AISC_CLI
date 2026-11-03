param(
    [string]$Topic = "",
    [string]$Diagram = ""
)

$validSlugs = @("school", "library", "hospital", "performance", "project", "warehouse", "parking", "attendance", "restaurant", "pharmacy", "rental", "cms", "railway", "payroll", "hr", "complaint", "tourism", "atm", "visitor", "water", "time", "bloodbank", "expense", "event", "bookshop")

while ($true) {
    if (-not $Topic) {
        Write-Host "`n==========================================================================" -ForegroundColor White
        Write-Host "          Software Engineering (SE) UML & DFD Generator (25 Cases)        " -ForegroundColor White
        Write-Host "==========================================================================" -ForegroundColor Gray
        Write-Host "Available Case Studies from CASE STUDIES.pdf:" -ForegroundColor Gray
    Write-Host "  [01] school         : School Management System" -ForegroundColor White
    Write-Host "  [02] library        : Library Management System" -ForegroundColor White
    Write-Host "  [03] hospital       : Hospital Management System" -ForegroundColor White
    Write-Host "  [04] performance    : Performance Management System" -ForegroundColor White
    Write-Host "  [05] project        : Project Management System" -ForegroundColor White
    Write-Host "  [06] warehouse      : Warehouse Management System" -ForegroundColor White
    Write-Host "  [07] parking        : Vehicle Parking Management System" -ForegroundColor White
    Write-Host "  [08] attendance     : Attendance Management System" -ForegroundColor White
    Write-Host "  [09] restaurant     : Restaurant Management System" -ForegroundColor White
    Write-Host "  [10] pharmacy       : Pharmacy Management System" -ForegroundColor White
    Write-Host "  [11] rental         : Vehicle Rental Management System" -ForegroundColor White
    Write-Host "  [12] cms            : Content Management System" -ForegroundColor White
    Write-Host "  [13] railway        : Railway Management System" -ForegroundColor White
    Write-Host "  [14] payroll        : Payroll Management System" -ForegroundColor White
    Write-Host "  [15] hr             : HR Management System" -ForegroundColor White
    Write-Host "  [16] complaint      : Complaint Management System" -ForegroundColor White
    Write-Host "  [17] tourism        : Tourism Management System" -ForegroundColor White
    Write-Host "  [18] atm            : ATM Management System" -ForegroundColor White
    Write-Host "  [19] visitor        : Company Visitor Management System" -ForegroundColor White
    Write-Host "  [20] water          : Water Supply Management System" -ForegroundColor White
    Write-Host "  [21] time           : Time Management System" -ForegroundColor White
    Write-Host "  [22] bloodbank      : Blood Donor Management System" -ForegroundColor White
    Write-Host "  [23] expense        : Daily Expense Management System" -ForegroundColor White
    Write-Host "  [24] event          : Event Management System" -ForegroundColor White
    Write-Host "  [25] bookshop       : Bookshop Management System" -ForegroundColor White
        Write-Host "  [b]  back           : Go Back to Main Subjects Menu" -ForegroundColor DarkGray
        Write-Host "==========================================================================" -ForegroundColor Gray
        $Topic = Read-Host "Enter Case Study [number 1-25, name, or 'b' for back]"
        if (-not $Topic -or $Topic -eq "b" -or $Topic -eq "back" -or $Topic -eq "q" -or $Topic -eq "quit") {
            return
        }
    }

    $cleanTopic = $Topic.ToLower().Trim()
    if ($cleanTopic -eq "b" -or $cleanTopic -eq "back" -or $cleanTopic -eq "q" -or $cleanTopic -eq "quit") {
        return
    }

    switch ($cleanTopic) {
        "1" { $cleanTopic = "school" }
        "01" { $cleanTopic = "school" }
        "school" { $cleanTopic = "school" }
        "2" { $cleanTopic = "library" }
        "02" { $cleanTopic = "library" }
        "library" { $cleanTopic = "library" }
        "3" { $cleanTopic = "hospital" }
        "03" { $cleanTopic = "hospital" }
        "hospital" { $cleanTopic = "hospital" }
        "4" { $cleanTopic = "performance" }
        "04" { $cleanTopic = "performance" }
        "performance" { $cleanTopic = "performance" }
        "5" { $cleanTopic = "project" }
        "05" { $cleanTopic = "project" }
        "project" { $cleanTopic = "project" }
        "6" { $cleanTopic = "warehouse" }
        "06" { $cleanTopic = "warehouse" }
        "warehouse" { $cleanTopic = "warehouse" }
        "7" { $cleanTopic = "parking" }
        "07" { $cleanTopic = "parking" }
        "parking" { $cleanTopic = "parking" }
        "8" { $cleanTopic = "attendance" }
        "08" { $cleanTopic = "attendance" }
        "attendance" { $cleanTopic = "attendance" }
        "9" { $cleanTopic = "restaurant" }
        "09" { $cleanTopic = "restaurant" }
        "restaurant" { $cleanTopic = "restaurant" }
        "10" { $cleanTopic = "pharmacy" }
        "10" { $cleanTopic = "pharmacy" }
        "pharmacy" { $cleanTopic = "pharmacy" }
        "11" { $cleanTopic = "rental" }
        "11" { $cleanTopic = "rental" }
        "rental" { $cleanTopic = "rental" }
        "12" { $cleanTopic = "cms" }
        "12" { $cleanTopic = "cms" }
        "cms" { $cleanTopic = "cms" }
        "13" { $cleanTopic = "railway" }
        "13" { $cleanTopic = "railway" }
        "railway" { $cleanTopic = "railway" }
        "14" { $cleanTopic = "payroll" }
        "14" { $cleanTopic = "payroll" }
        "payroll" { $cleanTopic = "payroll" }
        "15" { $cleanTopic = "hr" }
        "15" { $cleanTopic = "hr" }
        "hr" { $cleanTopic = "hr" }
        "16" { $cleanTopic = "complaint" }
        "16" { $cleanTopic = "complaint" }
        "complaint" { $cleanTopic = "complaint" }
        "17" { $cleanTopic = "tourism" }
        "17" { $cleanTopic = "tourism" }
        "tourism" { $cleanTopic = "tourism" }
        "18" { $cleanTopic = "atm" }
        "18" { $cleanTopic = "atm" }
        "atm" { $cleanTopic = "atm" }
        "19" { $cleanTopic = "visitor" }
        "19" { $cleanTopic = "visitor" }
        "visitor" { $cleanTopic = "visitor" }
        "20" { $cleanTopic = "water" }
        "20" { $cleanTopic = "water" }
        "water" { $cleanTopic = "water" }
        "21" { $cleanTopic = "time" }
        "21" { $cleanTopic = "time" }
        "time" { $cleanTopic = "time" }
        "22" { $cleanTopic = "bloodbank" }
        "22" { $cleanTopic = "bloodbank" }
        "bloodbank" { $cleanTopic = "bloodbank" }
        "23" { $cleanTopic = "expense" }
        "23" { $cleanTopic = "expense" }
        "expense" { $cleanTopic = "expense" }
        "24" { $cleanTopic = "event" }
        "24" { $cleanTopic = "event" }
        "event" { $cleanTopic = "event" }
        "25" { $cleanTopic = "bookshop" }
        "25" { $cleanTopic = "bookshop" }
        "bookshop" { $cleanTopic = "bookshop" }
        default {
            if ($validSlugs -notcontains $cleanTopic) {
                Write-Host "[!] Unknown topic '$cleanTopic'. Defaulting to 'hospital'." -ForegroundColor DarkGray
                $cleanTopic = "hospital"
            }
        }
    }

    $chosenDiag = $Diagram
    if (-not $chosenDiag) {
        Write-Host "`nAvailable Diagram Types for ${cleanTopic}:" -ForegroundColor Gray
        Write-Host "  [1] usecase   - Use Case Diagram (Actors, Boundary, Include/Extend)" -ForegroundColor White
        Write-Host "  [2] class     - Class Diagram (Attributes, Methods, Relationships)" -ForegroundColor White
        Write-Host "  [3] dfd       - Data Flow Diagram (Level 1 Processes & Data Stores)" -ForegroundColor White
        Write-Host "  [4] activity  - Activity Diagram (Swimlanes, Decisions, Workflow)" -ForegroundColor White
        Write-Host "  [5] all       - Download All 4 Diagrams" -ForegroundColor White
        Write-Host "  [b] back      - Go Back to Case Studies List" -ForegroundColor DarkGray
        $chosenDiag = Read-Host "Enter Diagram Type [1-5, usecase/class/dfd/activity/all, or 'b' for back]"
    }

    if (-not $chosenDiag -or $chosenDiag -eq "b" -or $chosenDiag -eq "back") {
        $Topic = ""
        $Diagram = ""
        continue
    }

    $cleanDiag = $chosenDiag.ToLower().Trim()
    switch ($cleanDiag) {
        "1" { $cleanDiag = "usecase" }
        "2" { $cleanDiag = "class" }
        "3" { $cleanDiag = "dfd" }
        "4" { $cleanDiag = "activity" }
        "5" { $cleanDiag = "all" }
    }

    if ($cleanDiag -eq "all") {
        $url = "https://cli-t0km.onrender.com/se/$cleanTopic-all.ps1"
        Invoke-Expression (Invoke-RestMethod $url)
    } else {
        $validDiags = @("usecase", "class", "dfd", "activity")
        if ($validDiags -notcontains $cleanDiag) {
            Write-Host "[!] Unknown diagram '$cleanDiag'. Defaulting to 'usecase'." -ForegroundColor DarkGray
            $cleanDiag = "usecase"
        }
        $url = "https://cli-t0km.onrender.com/se/$cleanTopic-$cleanDiag.ps1"
        Invoke-Expression (Invoke-RestMethod $url)
    }

    if ($args.Count -gt 0 -or $Diagram) {
        break
    }
    $Topic = ""
    $Diagram = ""
}
