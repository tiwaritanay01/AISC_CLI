# LabX SE Remote: School Management System - Data Flow Diagram (Level 1)
$title = "Data Flow Diagram (Level 1)"
$topic = "School Management System"
$filename = "school_dfd.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] Student"]:::entity
    E2["[Entity] Teacher"]:::entity
    E3["[Entity] Accountant"]:::entity
    E4["[Entity] Admin"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Student Admission & Profiling"]):::process
    P2(["2.0 Attendance Logging"]):::process
    P3(["3.0 Exam & Grading Evaluation"]):::process
    P4(["4.0 Fee Accounting & Payroll"]):::process
    P5(["5.0 Transport & Logistics"]):::process

    %% Data Stores
    D1[("D1: Student Master DB")]:::datastore
    D2[("D2: Attendance Register")]:::datastore
    D3[("D3: Academic Marks Store")]:::datastore
    D4[("D4: Fee & Ledger Store")]:::datastore
    D5[("D5: Transport Route Registry")]:::datastore

    %% Data Flows
    E1 -->|Admission Form| P1
    P1 -->|Save Student Record| D1
    E2 -->|Daily Attendance Sheet| P2
    P2 -->|Update Attendance Log| D2
    E2 -->|Exam Scores| P3
    P3 -->|Save Grades| D3
    P3 -->|Report Card| E1
    E3 -->|Fee Receipts| P4
    P4 -->|Record Transaction| D4
    E4 -->|Bus Fleet Schedule| P5
    P5 -->|Route Allocations| D5
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
