# LabX SE Remote: School Management System - Use Case Diagram
$title = "Use Case Diagram"
$topic = "School Management System"
$filename = "school_usecase.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["School Management System (System Boundary)"]
        UC01(["UC01: Register & Enroll Student"])
        UC02(["UC02: Record Daily Attendance"])
        UC03(["UC03: Generate Timetable & Roster"])
        UC04(["UC04: Publish Examination Marks"])
        UC05(["UC05: Collect Tuition Fees & Invoice"])
        UC06(["UC06: Process Staff Payroll"])
        UC07(["UC07: Manage Bus Transport & Routes"])
        UC08(["UC08: Manage Department Inventory"])
    end

    %% Actors
    Student["<<Actor>>\nStudent"]:::actorStyle
    Teacher["<<Actor>>\nTeacher"]:::actorStyle
    Accountant["<<Actor>>\nAccountant"]:::actorStyle
    SchoolAdmin["<<Actor>>\nSchoolAdmin"]:::actorStyle

    %% Actor to Use Case Associations
    Student --> UC01
    Student --> UC04
    Student --> UC05
    Teacher --> UC02
    Teacher --> UC03
    Teacher --> UC04
    Accountant --> UC05
    Accountant --> UC06
    SchoolAdmin --> UC01
    SchoolAdmin --> UC03
    SchoolAdmin --> UC07
    SchoolAdmin --> UC08

    %% Include & Extend Relationships
    UC01 -.->|<<include>>| UC05
    UC04 -.->|<<extend>>| UC02
    UC05 -.->|<<include>>| UC06
'@

# 1. Output to terminal
Write-Host "==============================================================" -ForegroundColor White
Write-Host "  Software Engineering (SE) Diagram: $title" -ForegroundColor White
Write-Host "  Case Study: $topic" -ForegroundColor Gray
Write-Host "==============================================================" -ForegroundColor Gray
Write-Host $mermaidCode -ForegroundColor Gray

# 2. Copy directly to Windows clipboard
try {
    Set-Clipboard -Value $mermaidCode
    Write-Host "`n[OK] Mermaid.js code copied to clipboard! (Ctrl + V to paste)" -ForegroundColor White
} catch {
    Write-Host "`n[!] Could not auto-copy to clipboard: $_" -ForegroundColor DarkGray
}

# 3. Save to local SE folder
$seDir = Join-Path $PWD "SE"
if (-not (Test-Path $seDir)) { New-Item -ItemType Directory -Path $seDir -Force | Out-Null }
$outFile = Join-Path $seDir $filename
Set-Content -Path $outFile -Value $mermaidCode -Encoding utf8
Write-Host "[OK] Saved local file: SE\$filename" -ForegroundColor White
Write-Host "[*] Tip: Paste into Notion, GitHub Markdown, or https://mermaid.live" -ForegroundColor Gray
