# LabX SE Remote: Vehicle Parking Management System - Class Diagram
$title = "Class Diagram"
$topic = "Vehicle Parking Management System"
$filename = "parking_class.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
classDiagram
    direction TB

    class BaseUser {
        <<abstract>>
        #String userId
        #String name
        #String contact
        #String status
        +login() bool
        +logout() void
    }

    class DriverProfile {
        -String regNumber
        -Date joinDate
        +submitRequest() String
        +viewStatus() void
    }

    class AdminProfile {
        -String accessLevel
        -String badgeId
        +verifyEntry() bool
        +generateSummary() Report
    }

    class VehicleRecord {
        -String recordId
        -Date recordDate
        -float feeAmount
        -String state
        +approve() void
        +cancel() void
        +calculateTotals() float
    }

    class TransactionPayment {
        -String txnId
        -Date timestamp
        -float amount
        -String paymentType
        +execute() bool
        +printReceipt() Receipt
    }

    BaseUser <|-- DriverProfile
    BaseUser <|-- AdminProfile
    DriverProfile "1" --> "*" VehicleRecord : initiates
    AdminProfile "1" --> "*" VehicleRecord : moderates
    VehicleRecord "1" --> "1" TransactionPayment : settled by
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
