# LabX SE Remote: Library Management System - Data Flow Diagram (Level 1)
$title = "Data Flow Diagram (Level 1)"
$topic = "Library Management System"
$filename = "library_dfd.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] Member"]:::entity
    E2["[Entity] Librarian"]:::entity
    E3["[Entity] Admin"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Catalog Search & Indexing"]):::process
    P2(["2.0 Book Issue & Verification"]):::process
    P3(["3.0 Return & Overdue Assessment"]):::process
    P4(["4.0 Reservation Management"]):::process
    P5(["5.0 Inventory & Acquisition"]):::process

    %% Data Stores
    D1[("D1: Book Catalog Store")]:::datastore
    D2[("D2: Member Directory")]:::datastore
    D3[("D3: Active Loans Store")]:::datastore
    D4[("D4: Fines & Ledger")]:::datastore
    D5[("D5: Reservations Queue")]:::datastore

    %% Data Flows
    E1 -->|Search Query (Title/ISBN)| P1
    P1 -->|Catalog Query| D1
    E1 -->|Borrow Request| P2
    P2 -->|Check Eligibility & Limits| D2
    P2 -->|Record Loan| D3
    E1 -->|Return Book| P3
    P3 -->|Close Loan Record| D3
    P3 -->|Compute Fine Details| D4
    E2 -->|New Title Metadata| P5
    P5 -->|Insert Stock| D1
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
