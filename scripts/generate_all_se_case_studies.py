"""
Master Generator for Software Engineering (SE) Case Studies & UML Diagrams.
Generates all 25 Case Studies from CASE STUDIES.pdf with:
- Use Case Diagram (.mmd)
- Class Diagram (.mmd)
- Data Flow Diagram Level 1 (.mmd)
- Activity Diagram with Swimlanes (.mmd)
- Comprehensive Markdown documentation (README.md)
- PowerShell pinpoint scripts (.ps1) in public/se/
- Master se.ps1 interactive selector
- ZIP distribution archive in public/downloads/se_diagrams.zip
"""

import os
import sys
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
from scripts.se_data import get_all_case_studies
SE_DIR = BASE_DIR / "SE"
PUBLIC_DIR = BASE_DIR / "labx-host" / "public"
SE_PUBLIC = PUBLIC_DIR / "se"
DL_DIR = PUBLIC_DIR / "downloads"

SE_DIR.mkdir(parents=True, exist_ok=True)
SE_PUBLIC.mkdir(parents=True, exist_ok=True)
DL_DIR.mkdir(parents=True, exist_ok=True)

B_AND_W_INIT = "%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%"

def build_usecase_mermaid(cs):
    lines = [
        B_AND_W_INIT,
        "flowchart LR",
        "    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;",
        "    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;",
        "",
        f'    subgraph SYSTEM ["{cs["title"]} (System Boundary)"]'
    ]
    for uc_id, uc_label in cs["usecases"]:
        lines.append(f'        {uc_id}(["{uc_id}: {uc_label}"])')
    lines.append("    end")
    lines.append("")
    lines.append("    %% Actors")
    for actor in cs["actors"]:
        actor_clean = actor.replace(" ", "")
        lines.append(f'    {actor_clean}["<<Actor>>\\n{actor}"]:::actorStyle')
    lines.append("")
    lines.append("    %% Actor to Use Case Associations")
    for actor, ucs in cs.get("actor_map", {}).items():
        actor_clean = actor.replace(" ", "")
        for u in ucs:
            lines.append(f"    {actor_clean} --> {u}")
    lines.append("")
    lines.append("    %% Include & Extend Relationships")
    for src, rel, dest in cs.get("uc_relations", []):
        lines.append(f"    {src} -.->|{rel}| {dest}")
    
    return "\n".join(lines)

def build_class_mermaid(cs):
    lines = [
        B_AND_W_INIT,
        "classDiagram",
        "    direction TB",
        ""
    ]
    for c in cs["classes"]:
        c_name = c["name"]
        lines.append(f"    class {c_name} {{")
        if c.get("abs"):
            lines.append("        <<abstract>>")
        for attr in c.get("attrs", []):
            lines.append(f"        {attr}")
        for op in c.get("ops", []):
            lines.append(f"        {op}")
        lines.append("    }")
        lines.append("")
    
    # Inheritance
    for c in cs["classes"]:
        if "parent" in c:
            lines.append(f"    {c['parent']} <|-- {c['name']}")
    
    # Relationships
    for r in cs.get("class_relations", []):
        src, m1, m2, dest, label = r
        lines.append(f'    {src} "{m1}" --> "{m2}" {dest} : {label}')
    
    return "\n".join(lines)

def build_dfd_mermaid(cs):
    lines = [
        B_AND_W_INIT,
        "flowchart TD",
        "    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;",
        "    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;",
        "    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;",
        "",
        "    %% External Entities"
    ]
    for i, ent in enumerate(cs["dfd_entities"], 1):
        lines.append(f'    E{i}["[Entity] {ent}"]:::entity')
    
    lines.append("")
    lines.append("    %% Processes (Level 1 DFD)")
    for i, proc in enumerate(cs["dfd_processes"], 1):
        lines.append(f'    P{i}(["{proc}"]):::process')
    
    lines.append("")
    lines.append("    %% Data Stores")
    for i, store in enumerate(cs["dfd_stores"], 1):
        lines.append(f'    D{i}[("{store}")]:::datastore')
    
    lines.append("")
    lines.append("    %% Data Flows")
    for flow in cs.get("dfd_flows", []):
        src, label, dest = flow
        # Match identifiers
        s_id = src
        for idx, ent in enumerate(cs["dfd_entities"], 1):
            if ent == src: s_id = f"E{idx}"
        for idx, proc in enumerate(cs["dfd_processes"], 1):
            if proc.startswith(src): s_id = f"P{idx}"
        for idx, st in enumerate(cs["dfd_stores"], 1):
            if st.startswith(src): s_id = f"D{idx}"
        
        d_id = dest
        for idx, ent in enumerate(cs["dfd_entities"], 1):
            if ent == dest: d_id = f"E{idx}"
        for idx, proc in enumerate(cs["dfd_processes"], 1):
            if proc.startswith(dest): d_id = f"P{idx}"
        for idx, st in enumerate(cs["dfd_stores"], 1):
            if st.startswith(dest): d_id = f"D{idx}"
        
        lines.append(f"    {s_id} -->|{label}| {d_id}")
    
    return "\n".join(lines)

def build_activity_mermaid(cs):
    lines = [
        B_AND_W_INIT,
        "flowchart TD",
        "    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;",
        "    classDef decision fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;",
        "    classDef sync fill:#000000,stroke:#000000,stroke-width:1px,color:#ffffff;",
        "    classDef circle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;",
        "",
        "    StartNode((Start)):::circle",
        "    EndNode((End)):::circle",
        ""
    ]
    node_counter = 1
    lane_nodes = {}
    for lane_name, steps in cs.get("swimlanes", []):
        safe_lane = lane_name.replace(" ", "_")
        lines.append(f'    subgraph SWIM_{safe_lane} ["{lane_name} Swimlane"]')
        lane_nodes[lane_name] = []
        for step in steps:
            nid = f"ACT_{node_counter}"
            node_counter += 1
            lines.append(f'        {nid}["{step}"]')
            lane_nodes[lane_name].append(nid)
        lines.append("    end")
        lines.append("")
    
    # Decisions
    for dec_id, (d_name, cond, true_branch, false_branch) in enumerate(cs.get("decisions", []), 1):
        did = f"DEC_{dec_id}"
        lines.append(f'    {did}{{"{cond}"}}:::decision')
    
    lines.append("")
    lines.append("    %% Activity Workflow Transitions")
    all_lanes = list(lane_nodes.keys())
    if all_lanes:
        first_node = lane_nodes[all_lanes[0]][0]
        lines.append(f"    StartNode --> {first_node}")
        
        # Connect sequential steps within lanes and across lanes
        prev = first_node
        for l in all_lanes:
            for n in lane_nodes[l]:
                if n != first_node:
                    lines.append(f"    {prev} --> {n}")
                    prev = n
        
        # Connect to decision if present
        if cs.get("decisions"):
            lines.append(f"    {prev} --> DEC_1")
            lines.append(f"    DEC_1 -->|Approved / Success| EndNode")
            lines.append(f"    DEC_1 -->|Rejected / Needs Revision| {first_node}")
        else:
            lines.append(f"    {prev} --> EndNode")
    
    return "\n".join(lines)

def make_ps1_content(cs, diag_key, title, filename, code):
    return f"""# LabX SE Remote: {cs['title']} - {title}
$title = "{title}"
$topic = "{cs['title']}"
$filename = "{filename}"

$mermaidCode = @'
{code}
'@

# 1. Output to terminal
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

# 3. Save to local SE folder
$seDir = Join-Path $PWD "SE"
if (-not (Test-Path $seDir)) {{ New-Item -ItemType Directory -Path $seDir -Force | Out-Null }}
$outFile = Join-Path $seDir $filename
Set-Content -Path $outFile -Value $mermaidCode -Encoding utf8
Write-Host "[OK] Saved local file: SE\\$filename" -ForegroundColor White
Write-Host "[*] Tip: Paste into Notion, GitHub Markdown, or https://mermaid.live" -ForegroundColor Gray
"""

def generate_all():
    case_studies = get_all_case_studies()
    print(f"Generating Software Engineering UML Diagrams for all {len(case_studies)} Case Studies...")

    all_case_names = []

    for cs in case_studies:
        slug = cs["slug"]
        cs_dir = SE_DIR / slug
        cs_dir.mkdir(parents=True, exist_ok=True)
        all_case_names.append((slug, cs["title"]))

        # Build 4 diagrams
        uc_code = build_usecase_mermaid(cs)
        class_code = build_class_mermaid(cs)
        dfd_code = build_dfd_mermaid(cs)
        act_code = build_activity_mermaid(cs)

        # Write .mmd files
        (cs_dir / f"{slug}_usecase.mmd").write_text(uc_code, encoding="utf-8")
        (cs_dir / f"{slug}_class.mmd").write_text(class_code, encoding="utf-8")
        (cs_dir / f"{slug}_dfd.mmd").write_text(dfd_code, encoding="utf-8")
        (cs_dir / f"{slug}_activity.mmd").write_text(act_code, encoding="utf-8")

        # Write README.md for case study
        readme = f"""# {cs['title']} - Software Engineering (SE) Specification

## 1. Case Study Overview
{cs['desc']}

---

## 2. Use Case Diagram (Black & White UML Standard)
```mermaid
{uc_code}
```

---

## 3. Class Diagram (UML Structure)
```mermaid
{class_code}
```

---

## 4. Data Flow Diagram (Level 1 DFD)
```mermaid
{dfd_code}
```

---

## 5. Activity Diagram (Workflow with Swimlanes)
```mermaid
{act_code}
```
"""
        (cs_dir / "README.md").write_text(readme, encoding="utf-8")

        # Generate PowerShell pinpoint scripts in public/se/
        diags = [
            ("usecase", "Use Case Diagram", f"{slug}_usecase.mmd", uc_code),
            ("class", "Class Diagram", f"{slug}_class.mmd", class_code),
            ("dfd", "Data Flow Diagram (Level 1)", f"{slug}_dfd.mmd", dfd_code),
            ("activity", "Activity Diagram", f"{slug}_activity.mmd", act_code)
        ]

        for d_key, d_title, d_fname, d_code in diags:
            ps1_text = make_ps1_content(cs, d_key, d_title, d_fname, d_code)
            (SE_PUBLIC / f"{slug}-{d_key}.ps1").write_text(ps1_text, encoding="utf-8")

        # All-in-one script for this specific case study
        all_ps1 = f"""# LabX SE Remote: All 4 Diagrams for {cs['title']}
Write-Host "Fetching all 4 UML & DFD Diagrams for {cs['title']}..." -ForegroundColor White
$diags = @("usecase", "class", "dfd", "activity")
foreach ($d in $diags) {{
    $url = "https://cli-t0km.onrender.com/se/{slug}-$d.ps1"
    Invoke-Expression (Invoke-RestMethod $url)
}}
Write-Host "`n[OK] All 4 diagrams for {cs['title']} saved to SE\\ folder!" -ForegroundColor White
"""
        (SE_PUBLIC / f"{slug}-all.ps1").write_text(all_ps1, encoding="utf-8")

    # Generate master se.ps1 interactive selector supporting all 25 case studies
    options_menu = []
    case_switches = []
    for idx, (s, title) in enumerate(all_case_names, 1):
        options_menu.append(f'    Write-Host "  [{idx:02d}] {s:<14} : {title}" -ForegroundColor White')
        case_switches.append(f'        "{idx}" {{ $cleanTopic = "{s}" }}')
        case_switches.append(f'        "{idx:02d}" {{ $cleanTopic = "{s}" }}')
        case_switches.append(f'        "{s}" {{ $cleanTopic = "{s}" }}')

    menu_str = "\n".join(options_menu)
    switches_str = "\n".join(case_switches)

    master_se_script = f"""param(
    [string]$Topic = "",
    [string]$Diagram = ""
)

$validSlugs = @({', '.join(f'"{s}"' for s, _ in all_case_names)})

if (-not $Topic) {{
    Write-Host "==========================================================================" -ForegroundColor White
    Write-Host "          Software Engineering (SE) UML & DFD Generator (25 Cases)        " -ForegroundColor White
    Write-Host "==========================================================================" -ForegroundColor Gray
    Write-Host "Available Case Studies from CASE STUDIES.pdf:" -ForegroundColor Gray
{menu_str}
    Write-Host "==========================================================================" -ForegroundColor Gray
    $Topic = Read-Host "Enter Case Study [number 1-25 or name, default: hospital]"
    if (-not $Topic) {{ $Topic = "hospital" }}
}}

$cleanTopic = $Topic.ToLower().Trim()
switch ($cleanTopic) {{
{switches_str}
    default {{
        if ($validSlugs -notcontains $cleanTopic) {{
            Write-Host "[!] Unknown topic '$cleanTopic'. Defaulting to 'hospital'." -ForegroundColor DarkGray
            $cleanTopic = "hospital"
        }}
    }}
}}

if (-not $Diagram) {{
    Write-Host "`nAvailable Diagram Types for ${{cleanTopic}}:" -ForegroundColor Gray
    Write-Host "  [1] usecase   - Use Case Diagram (Actors, Boundary, Include/Extend)" -ForegroundColor White
    Write-Host "  [2] class     - Class Diagram (Attributes, Methods, Relationships)" -ForegroundColor White
    Write-Host "  [3] dfd       - Data Flow Diagram (Level 1 Processes & Data Stores)" -ForegroundColor White
    Write-Host "  [4] activity  - Activity Diagram (Swimlanes, Decisions, Workflow)" -ForegroundColor White
    Write-Host "  [5] all       - Download All 4 Diagrams" -ForegroundColor White
    $Diagram = Read-Host "Enter Diagram Type [1-5 or usecase/class/dfd/activity/all, default: usecase]"
    if (-not $Diagram) {{ $Diagram = "usecase" }}
}}

$cleanDiag = $Diagram.ToLower().Trim()
switch ($cleanDiag) {{
    "1" {{ $cleanDiag = "usecase" }}
    "2" {{ $cleanDiag = "class" }}
    "3" {{ $cleanDiag = "dfd" }}
    "4" {{ $cleanDiag = "activity" }}
    "5" {{ $cleanDiag = "all" }}
}}

if ($cleanDiag -eq "all") {{
    $url = "https://cli-t0km.onrender.com/se/$cleanTopic-all.ps1"
    Invoke-Expression (Invoke-RestMethod $url)
}} else {{
    $validDiags = @("usecase", "class", "dfd", "activity")
    if ($validDiags -notcontains $cleanDiag) {{
        Write-Host "[!] Unknown diagram '$cleanDiag'. Defaulting to 'usecase'." -ForegroundColor DarkGray
        $cleanDiag = "usecase"
    }}
    $url = "https://cli-t0km.onrender.com/se/$cleanTopic-$cleanDiag.ps1"
    Invoke-Expression (Invoke-RestMethod $url)
}}
"""
    (PUBLIC_DIR / "se.ps1").write_text(master_se_script, encoding="utf-8")

    # Build ZIP archive of all SE diagrams
    zip_path = DL_DIR / "se_diagrams.zip"
    print(f"Building complete SE archive at {zip_path}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(SE_DIR):
            for f in files:
                full_p = Path(root) / f
                rel_p = full_p.relative_to(SE_DIR)
                zf.write(full_p, arcname=f"SE/{rel_p}".replace("\\", "/"))

    print(f"Success! Generated {len(case_studies)} SE case studies (100 total diagrams)!")

if __name__ == "__main__":
    generate_all()
