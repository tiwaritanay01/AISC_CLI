# LabX SE Remote: Project Management System - Data Flow Diagram (Level 1)
$title = "Data Flow Diagram (Level 1)"
$topic = "Project Management System"
$filename = "project_dfd.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] ProjectManager"]:::entity
    E2["[Entity] TeamMember"]:::entity
    E3["[Entity] Client"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Project Charter & Scope Creation"]):::process
    P2(["2.0 Task Decomposition & Scheduling"]):::process
    P3(["3.0 Execution & Timesheet Logging"]):::process
    P4(["4.0 Milestone Tracking & QA"]):::process
    P5(["5.0 Billing & Governance Reporting"]):::process

    %% Data Stores
    D1[("D1: Project Registry")]:::datastore
    D2[("D2: Task & Backlog Store")]:::datastore
    D3[("D3: Resource Pool")]:::datastore
    D4[("D4: Timesheet Logs")]:::datastore
    D5[("D5: Financials & Budget Store")]:::datastore

    %% Data Flows
    E1 -->|Scope & Budget| P1
    P1 -->|New Project Baseline| D1
    E1 -->|Task Breakdown (WBS)| P2
    P2 -->|Save Tasks & Deadlines| D2
    E2 -->|Daily Hours & Status| P3
    P3 -->|Commit Timesheets| D4
    P3 -->|Sprint Burndown Delta| P4
    P4 -->|Milestone Verification| E3
    P5 -->|Budget Utilization Dashboard| E1
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
