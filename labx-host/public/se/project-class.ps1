# LabX SE Remote: Project Management System - Class Diagram
$title = "Class Diagram"
$topic = "Project Management System"
$filename = "project_class.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
classDiagram
    direction TB

    class Project {
        -String projId
        -String title
        -Date startDate
        -Date endDate
        -float budget
        -String status
        +calculateProgress() float
        +checkBudgetVariance() float
    }

    class Task {
        -String taskId
        -String title
        -int estHours
        -int actualHours
        -String priority
        -String state
        +assignTo(String devId) void
        +markComplete() void
    }

    class Resource {
        -String resId
        -String name
        -String role
        -float hourlyRate
        +checkAvailability() bool
    }

    class Timesheet {
        -String entryId
        -Date workDate
        -float hoursLogged
        -String comments
        +approve() void
    }

    class Milestone {
        -String milestoneId
        -Date targetDate
        -boolean isDelivered
        +verifyDeliverable() bool
    }

    Project "1" --> "*" Task : consists of
    Task "*" --> "1" Resource : assigned to
    Resource "1" --> "*" Timesheet : submits
    Project "1" --> "*" Milestone : tracks
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
