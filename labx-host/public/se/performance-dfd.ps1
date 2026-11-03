# LabX SE Remote: Performance Management System - Data Flow Diagram (Level 1)
$title = "Data Flow Diagram (Level 1)"
$topic = "Performance Management System"
$filename = "performance_dfd.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] Employee"]:::entity
    E2["[Entity] Manager"]:::entity
    E3["[Entity] HRAdmin"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Goal Setting & Alignment"]):::process
    P2(["2.0 Self & Peer Appraisal"]):::process
    P3(["3.0 Manager Evaluation & Scoring"]):::process
    P4(["4.0 Merit Calibration"]):::process
    P5(["5.0 Rewards & Action Planning"]):::process

    %% Data Stores
    D1[("D1: Employee Roster")]:::datastore
    D2[("D2: Annual Goal Catalog")]:::datastore
    D3[("D3: Review Scores Store")]:::datastore
    D4[("D4: Calibration Matrix")]:::datastore
    D5[("D5: Rewards & PIP Records")]:::datastore

    %% Data Flows
    E1 -->|Quarterly Goals & Milestones| P1
    P1 -->|Save Objectives| D2
    E1 -->|Self-Assessment Ratings| P2
    P2 -->|Store Peer Feedback| D3
    E2 -->|Manager Evaluation Scores| P3
    P3 -->|Consolidated Appraisal| D3
    E3 -->|Bell-Curve Parameters| P4
    P4 -->|Final Scaled Rating| D4
    P4 -->|Bonus & Increment Proposal| P5
    P5 -->|Reward Disbursal & Letters| E1
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
