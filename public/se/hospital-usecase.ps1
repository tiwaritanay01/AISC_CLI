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
        UC01(["UC01: Register / Login Patient"])
        UC02(["UC02: Book / Reschedule Appointment"])
        UC03(["UC03: Verify Doctor Availability"])
        UC04(["UC04: View & Update EMR Medical Records"])
        UC05(["UC05: Generate Diagnosis & Prescription"])
        UC06(["UC06: Order Lab Diagnostic Tests"])
        UC07(["UC07: Process Discharge & Invoicing"])
        UC08(["UC08: Manage Pharmacy & Inventory"])
        UC09(["UC09: Manage Hospital Staff & System Roles"])
    end

    %% Actors
    Patient["<<Actor>>\nPatient"]:::actorStyle
    Receptionist["<<Actor>>\nReceptionist"]:::actorStyle
    Doctor["<<Actor>>\nDoctor"]:::actorStyle
    Administrator["<<Actor>>\nAdministrator"]:::actorStyle

    %% Actor to Use Case Associations
    Patient --> UC01
    Patient --> UC02
    Receptionist --> UC01
    Receptionist --> UC02
    Receptionist --> UC07
    Doctor --> UC04
    Doctor --> UC05
    Administrator --> UC07
    Administrator --> UC08
    Administrator --> UC09

    %% Include & Extend Relationships
    UC02 -.->|<<include>>| UC03
    UC05 -.->|<<extend>>| UC06
    UC07 -.->|<<include>>| UC08
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
