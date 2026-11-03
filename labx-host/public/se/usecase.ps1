# LabX SE Remote: Hospital Management System - Use Case Diagram
$title = "Use Case Diagram"
$topic = "Hospital Management System"
$filename = "hospital_usecase.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["Hospital Management System (System Boundary)"]
        UC1([UC-01: Register / Login Patient])
        UC2([UC-02: Book / Reschedule Appointment])
        UC3([UC-03: Verify Doctor Availability])
        UC4([UC-04: View & Update EMR Medical Records])
        UC5([UC-05: Generate Diagnosis & Prescription])
        UC6([UC-06: Order Lab Diagnostic Tests])
        UC7([UC-07: Process Discharge & Invoicing])
        UC8([UC-08: Process Insurance & Payment])
        UC9([UC-09: Manage Pharmacy & Drug Inventory])
        UC10([UC-10: Manage Hospital Staff & System Roles])
    end

    %% Actors
    Patient["<<Actor>>\nPatient"]:::actorStyle
    Receptionist["<<Actor>>\nReceptionist"]:::actorStyle
    Doctor["<<Actor>>\nDoctor"]:::actorStyle
    Admin["<<Actor>>\nAdministrator"]:::actorStyle

    %% Patient Associations
    Patient --> UC1
    Patient --> UC2

    %% Receptionist Associations
    Receptionist --> UC1
    Receptionist --> UC2
    Receptionist --> UC7

    %% Doctor Associations
    Doctor --> UC4
    Doctor --> UC5

    %% Admin Associations
    Admin --> UC9
    Admin --> UC10
    Admin --> UC7

    %% Include & Extend Relationships
    UC2 -.->|&lt;&lt;include&gt;&gt;| UC3
    UC5 -.->|&lt;&lt;extend&gt;&gt;| UC6
    UC7 -.->|&lt;&lt;include&gt;&gt;| UC8

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
