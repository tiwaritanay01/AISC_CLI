# LabX SE Remote: Hospital Management System - Activity Diagram (Swimlanes)
$title = "Activity Diagram (Swimlanes)"
$topic = "Hospital Management System"
$filename = "hospital_activity.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000'}}}%%
flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef decision fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef sync fill:#000000,stroke:#000000,stroke-width:1px,color:#ffffff;
    classDef circle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    Start((Start)):::circle

    subgraph SWIMLANE_PATIENT ["Patient Swimlane"]
        A1["Arrive at Hospital / Request Appointment"]
        A2["Provide Symptoms & Medical History"]
        A3["Undergo Diagnostic Tests"]
        A4["Make Payment (Cash / Insurance / Card)"]
    end

    subgraph SWIMLANE_RECEPTION ["Receptionist Swimlane"]
        B1{"Registered Patient?"}:::decision
        B2["Create New Patient Profile in Database"]
        B3["Verify Doctor Slot & Assign Token"]
    end

    subgraph SWIMLANE_DOCTOR ["Doctor Swimlane"]
        C1["Call Token & Examine Patient"]
        C2{"Requires Lab Tests?"}:::decision
        C3["Issue Lab Requisition Order"]
        C4["Analyze Results & Prescribe Medication"]
        C5["Update EMR Database"]
    end

    subgraph SWIMLANE_BILLING ["Billing & Pharmacy Swimlane"]
        Fork1[=== Parallel Split ===]:::sync
        D1["Dispense Medicines from Pharmacy"]
        D2["Calculate Total Invoice Bill"]
        Join1[=== Parallel Join ===]:::sync
        D3["Generate Receipt & Discharge Summary"]
    end

    EndNode((End)):::circle

    Start --> A1
    A1 --> B1
    B1 -->|No| B2
    B2 --> B3
    B1 -->|Yes| B3
    B3 --> C1
    C1 --> A2
    A2 --> C2
    C2 -->|Yes| C3
    C3 --> A3
    A3 --> C4
    C2 -->|No| C4
    C4 --> C5

    C5 --> Fork1
    Fork1 --> D1
    Fork1 --> D2
    D1 --> Join1
    D2 --> Join1

    Join1 --> A4
    A4 --> D3
    D3 --> EndNode

'@

# 1. Output to console
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

# 3. Save to local SE directory
$seDir = Join-Path $PWD "SE"
if (-not (Test-Path $seDir)) { New-Item -ItemType Directory -Path $seDir -Force | Out-Null }
$outFile = Join-Path $seDir $filename
Set-Content -Path $outFile -Value $mermaidCode -Encoding utf8
Write-Host "[OK] Saved local file: SE\$filename" -ForegroundColor White
Write-Host "[*] Tip: Paste into Notion, GitHub Markdown, or https://mermaid.live" -ForegroundColor Gray
