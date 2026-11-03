# LabX SE Remote: Time Management System - Data Flow Diagram (Level 1)
$title = "Data Flow Diagram (Level 1)"
$topic = "Time Management System"
$filename = "time_dfd.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] Employee"]:::entity
    E2["[Entity] TeamLead"]:::entity
    E3["[Entity] OperationsManager"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Employee Authentication"]):::process
    P2(["2.0 Time Service Request Processing"]):::process
    P3(["3.0 Verification & Scheduling"]):::process
    P4(["4.0 Financial Settlement"]):::process
    P5(["5.0 Analytics & Master DB Update"]):::process

    %% Data Stores
    D1[("D1: Time Master Registry")]:::datastore
    D2[("D2: Active Transactions")]:::datastore
    D3[("D3: Verification Logs")]:::datastore
    D4[("D4: Ledger & Payments")]:::datastore
    D5[("D5: System Archives")]:::datastore

    %% Data Flows
    E1 -->|Registration Credentials| P1
    P1 -->|Save Verified User| D1
    E1 -->|Service Request Input| P2
    P2 -->|Record Transaction Intent| D2
    E3 -->|Verification Decision| P3
    P3 -->|Update Compliance Status| D3
    P3 -->|Billing Breakdown| P4
    P4 -->|Payment Confirmation| D4
    P4 -->|Official Receipt| E1
    P5 -->|Quarterly Audit Summary| E3
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
