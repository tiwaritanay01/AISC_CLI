import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
HOST_PUBLIC = BASE_DIR / "labx-host" / "public"
SE_PUBLIC = HOST_PUBLIC / "se"
SE_DIR = BASE_DIR / "SE"

SE_PUBLIC.mkdir(parents=True, exist_ok=True)

# Read the Hospital Mermaid files
uc_code = (SE_DIR / "hospital" / "hospital_usecase.mmd").read_text(encoding="utf-8")
class_code = (SE_DIR / "hospital" / "hospital_class.mmd").read_text(encoding="utf-8")
dfd_code = (SE_DIR / "hospital" / "hospital_dfd.mmd").read_text(encoding="utf-8")
act_code = (SE_DIR / "hospital" / "hospital_activity.mmd").read_text(encoding="utf-8")

DIAGRAMS = {
    "usecase": {
        "title": "Use Case Diagram",
        "case": "Hospital Management System",
        "filename": "hospital_usecase.mmd",
        "code": uc_code
    },
    "class": {
        "title": "Class Diagram",
        "case": "Hospital Management System",
        "filename": "hospital_class.mmd",
        "code": class_code
    },
    "dfd": {
        "title": "Data Flow Diagram (Level 1 DFD)",
        "case": "Hospital Management System",
        "filename": "hospital_dfd.mmd",
        "code": dfd_code
    },
    "activity": {
        "title": "Activity Diagram (Swimlanes)",
        "case": "Hospital Management System",
        "filename": "hospital_activity.mmd",
        "code": act_code
    }
}

def make_ps1_content(diag_key, info):
    code_escaped = info["code"].replace("'", "''")
    return f"""# LabX SE Remote: {info['case']} - {info['title']}
$title = "{info['title']}"
$topic = "{info['case']}"
$filename = "{info['filename']}"

$mermaidCode = @'
{info['code']}
'@

# 1. Output to console
Write-Host "==============================================================" -ForegroundColor White
Write-Host "  Software Engineering (SE) Diagram: $title" -ForegroundColor White
Write-Host "  Case Study: $topic" -ForegroundColor Gray
Write-Host "==============================================================" -ForegroundColor Gray
Write-Host $mermaidCode -ForegroundColor Gray

# 2. Copy directly to Windows clipboard
try {{
    Set-Clipboard -Value $mermaidCode
    Write-Host "`n[OK] Mermaid.js code copied to clipboard! (Ctrl + V to paste)" -ForegroundColor White
}} catch {{
    Write-Host "`n[!] Could not auto-copy to clipboard: $_" -ForegroundColor DarkGray
}}

# 3. Save to local SE directory
$seDir = Join-Path $PWD "SE"
if (-not (Test-Path $seDir)) {{ New-Item -ItemType Directory -Path $seDir -Force | Out-Null }}
$outFile = Join-Path $seDir $filename
Set-Content -Path $outFile -Value $mermaidCode -Encoding utf8
Write-Host "[OK] Saved local file: SE\\$filename" -ForegroundColor White
Write-Host "[*] Tip: Paste into Notion, GitHub Markdown, or https://mermaid.live" -ForegroundColor Gray
"""

# Generate pinpoint scripts
for key, info in DIAGRAMS.items():
    ps1_text = make_ps1_content(key, info)
    (SE_PUBLIC / f"hospital-{key}.ps1").write_text(ps1_text, encoding="utf-8")
    (SE_PUBLIC / f"{key}.ps1").write_text(ps1_text, encoding="utf-8")

# Universal / Interactive se.ps1 script
se_master_ps1 = """param(
    [string]$Topic = "",
    [string]$Diagram = ""
)

if (-not $Topic) {
    Write-Host "==============================================================" -ForegroundColor White
    Write-Host "     Software Engineering (SE) UML & Diagram Generator       " -ForegroundColor White
    Write-Host "==============================================================" -ForegroundColor Gray
    Write-Host "Available Case Studies:" -ForegroundColor Gray
    Write-Host "  [hospital]   Hospital Management System" -ForegroundColor White
    Write-Host "  [library]    Library Management System" -ForegroundColor White
    Write-Host "  [atm]        ATM Management System" -ForegroundColor White
    Write-Host "  [school]     School Management System" -ForegroundColor White
    Write-Host "  [railway]    Railway Management System" -ForegroundColor White
    Write-Host "==============================================================" -ForegroundColor Gray
    $Topic = Read-Host "Enter Case Study (default: hospital)"
    if (-not $Topic) { $Topic = "hospital" }
}

$cleanTopic = $Topic.ToLower().Trim()
if ($cleanTopic -ne "hospital") {
    Write-Host "[*] Defaulting to available implementation: Hospital Management System" -ForegroundColor DarkGray
    $cleanTopic = "hospital"
}

if (-not $Diagram) {
    Write-Host "`nAvailable Diagram Types:" -ForegroundColor Gray
    Write-Host "  [1] usecase   - Use Case Diagram (Actors, Boundary, Include/Extend)" -ForegroundColor White
    Write-Host "  [2] class     - Class Diagram (Attributes, Methods, Relationships)" -ForegroundColor White
    Write-Host "  [3] dfd       - Data Flow Diagram (Level 0 & Level 1 Processes & Stores)" -ForegroundColor White
    Write-Host "  [4] activity  - Activity Diagram (Swimlanes, Decisions, Fork/Join)" -ForegroundColor White
    Write-Host "  [5] all       - Generate & Save All 4 Diagrams" -ForegroundColor White
    $Diagram = Read-Host "Enter Diagram Type [usecase / class / dfd / activity / all, default: usecase]"
    if (-not $Diagram) { $Diagram = "usecase" }
}

$cleanDiag = $Diagram.ToLower().Trim()
switch ($cleanDiag) {
    "1" { $cleanDiag = "usecase" }
    "2" { $cleanDiag = "class" }
    "3" { $cleanDiag = "dfd" }
    "4" { $cleanDiag = "activity" }
    "5" { $cleanDiag = "all" }
}

if ($cleanDiag -eq "all") {
    foreach ($d in @("usecase", "class", "dfd", "activity")) {
        $url = "https://cli-t0km.onrender.com/se/hospital-$d.ps1"
        Invoke-Expression (Invoke-RestMethod $url)
    }
} else {
    $validDiags = @("usecase", "class", "dfd", "activity")
    if ($validDiags -notcontains $cleanDiag) {
        Write-Host "[!] Unknown diagram type: $cleanDiag. Defaulting to 'usecase'." -ForegroundColor DarkGray
        $cleanDiag = "usecase"
    }
    $url = "https://cli-t0km.onrender.com/se/hospital-$cleanDiag.ps1"
    Invoke-Expression (Invoke-RestMethod $url)
}
"""

(HOST_PUBLIC / "se.ps1").write_text(se_master_ps1, encoding="utf-8")
print("SE scripts generated successfully in labx-host/public/se/ and labx-host/public/se.ps1")

