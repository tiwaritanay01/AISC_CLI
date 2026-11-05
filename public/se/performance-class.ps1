# LabX SE Remote: Performance Management System - Class Diagram
$title = "Class Diagram"
$topic = "Performance Management System"
$filename = "performance_class.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
classDiagram
    direction TB

    class Employee {
        -String empId
        -String name
        -String department
        -String designation
        +submitGoals() void
        +viewAppraisal() Report
    }

    class Manager {
        -List~String~ reportees
        +evaluateKPI(String empId) Score
        +approvePromotion() void
    }

    class HRAdmin {
        -String policyAccessLevel
        +finalizeAppraisalCycle() void
        +issueIncrementLetter() Letter
    }

    class Goal {
        -String goalId
        -String description
        -Date targetDate
        -float weightage
        -String status
        +updateProgress(float percent) void
    }

    class AppraisalReview {
        -String reviewId
        -float selfRating
        -float managerRating
        -float peerScore
        -String comments
        +computeCompositeScore() float
    }

    class Reward {
        -String rewardId
        -String type
        -float bonusAmount
        -Date grantedOn
        +disburseReward() void
    }

    Employee <|-- Manager
    Employee <|-- HRAdmin
    Employee "1" --> "*" Goal : sets
    Employee "1" --> "*" AppraisalReview : evaluated by
    Manager "1" --> "*" AppraisalReview : conducts
    AppraisalReview "1" --> "0..1" Reward : triggers
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
