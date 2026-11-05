# LabX SE Remote: Performance Management System - Use Case Diagram
$title = "Use Case Diagram"
$topic = "Performance Management System"
$filename = "performance_usecase.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["Performance Management System (System Boundary)"]
        UC01(["UC01: Submit Self-Appraisal & Goals"])
        UC02(["UC02: Review Team KPI Deliverables"])
        UC03(["UC03: Conduct 360-Degree Peer Feedback"])
        UC04(["UC04: Calculate Merit Rating Score"])
        UC05(["UC05: Recommend Bonus / Promotion"])
        UC06(["UC06: Record Disciplinary Action / PIP"])
        UC07(["UC07: Generate Quarterly Performance Analytics"])
    end

    %% Actors
    Employee["<<Actor>>\nEmployee"]:::actorStyle
    Manager["<<Actor>>\nManager"]:::actorStyle
    HRAdmin["<<Actor>>\nHRAdmin"]:::actorStyle

    %% Actor to Use Case Associations
    Employee --> UC01
    Employee --> UC03
    Manager --> UC02
    Manager --> UC04
    Manager --> UC05
    Manager --> UC06
    HRAdmin --> UC04
    HRAdmin --> UC05
    HRAdmin --> UC06
    HRAdmin --> UC07

    %% Include & Extend Relationships
    UC02 -.->|<<include>>| UC01
    UC04 -.->|<<include>>| UC03
    UC05 -.->|<<extend>>| UC04
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
