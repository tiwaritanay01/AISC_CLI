# LabX SE Remote: Hospital Management System - Data Flow Diagram (Level 1)
$title = "Data Flow Diagram (Level 1)"
$topic = "Hospital Management System"
$filename = "hospital_dfd.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] Patient"]:::entity
    E2["[Entity] Receptionist"]:::entity
    E3["[Entity] Doctor"]:::entity
    E4["[Entity] Administrator"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Patient Intake & Triage"]):::process
    P2(["2.0 Appointment Booking"]):::process
    P3(["3.0 Clinical Consultation & EMR"]):::process
    P4(["4.0 Pharmacy & Diagnostics"]):::process
    P5(["5.0 Billing & Discharge"]):::process

    %% Data Stores
    D1[("D1: Patient Database")]:::datastore
    D2[("D2: Doctor Duty Roster")]:::datastore
    D3[("D3: Medical Records Store")]:::datastore
    D4[("D4: Pharmacy Stock")]:::datastore
    D5[("D5: Financial Accounts")]:::datastore

    %% Data Flows
    E1 -->|Personal Details| P1
    P1 -->|Save Patient Details| D1
    E2 -->|Slot Booking Request| P2
    P2 -->|Check Doctor Availability| D2
    E3 -->|Clinical Notes & Rx| P3
    P3 -->|Append EMR| D3
    P3 -->|Medicine Dispense Order| P4
    P4 -->|Deduct Drug Stock| D4
    P4 -->|Drug Bill Items| P5
    P5 -->|Settlement Receipt| E1
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
