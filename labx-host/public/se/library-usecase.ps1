# LabX SE Remote: Library Management System - Use Case Diagram
$title = "Use Case Diagram"
$topic = "Library Management System"
$filename = "library_usecase.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["Library Management System (System Boundary)"]
        UC01(["UC01: Search Online Catalog (OPAC)"])
        UC02(["UC02: Borrow / Issue Book"])
        UC03(["UC03: Return & Inspect Book"])
        UC04(["UC04: Calculate & Collect Overdue Fine"])
        UC05(["UC05: Reserve Unavailable Book"])
        UC06(["UC06: Catalog New Book & Author"])
        UC07(["UC07: Generate Circulation Reports"])
    end

    %% Actors
    StudentMember["<<Actor>>\nStudentMember"]:::actorStyle
    FacultyMember["<<Actor>>\nFacultyMember"]:::actorStyle
    Librarian["<<Actor>>\nLibrarian"]:::actorStyle
    Admin["<<Actor>>\nAdmin"]:::actorStyle

    %% Actor to Use Case Associations
    StudentMember --> UC01
    StudentMember --> UC02
    StudentMember --> UC03
    StudentMember --> UC05
    FacultyMember --> UC01
    FacultyMember --> UC02
    FacultyMember --> UC03
    FacultyMember --> UC05
    Librarian --> UC02
    Librarian --> UC03
    Librarian --> UC04
    Librarian --> UC06
    Librarian --> UC07
    Admin --> UC06
    Admin --> UC07

    %% Include & Extend Relationships
    UC02 -.->|<<include>>| UC01
    UC03 -.->|<<extend>>| UC04
    UC05 -.->|<<extend>>| UC01
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
