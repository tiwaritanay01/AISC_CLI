# LabX SE Remote: Hospital Management System - Class Diagram
$title = "Class Diagram"
$topic = "Hospital Management System"
$filename = "hospital_class.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
classDiagram
    direction TB

    class User {
        <<abstract>>
        #int userId
        #String name
        #String phone
        +login() bool
        +logout() void
    }

    class Patient {
        -String patientId
        -String bloodGroup
        -Date dob
        +bookAppointment() Appointment
        +payBill() bool
    }

    class Doctor {
        -String doctorId
        -String specialization
        +examinePatient() void
        +prescribeDrugs() void
    }

    class Receptionist {
        -String deskId
        +registerWalkIn() String
        +assignToken() int
    }

    class Administrator {
        -String role
        +auditSystem() Report
        +manageStock() void
    }

    class Appointment {
        -String apptId
        -Date apptDate
        -String slot
        -String status
        +confirm() void
        +cancel() void
    }

    class MedicalRecord {
        -String recordId
        -String diagnosis
        -String labFindings
        +attachLabResult() void
    }

    class Bill {
        -String billId
        -float consultationFee
        -float medicineTotal
        -float total
        +settleInvoice() void
    }

    User <|-- Patient
    User <|-- Doctor
    User <|-- Receptionist
    User <|-- Administrator
    Patient "1" --> "*" Appointment : schedules
    Doctor "1" --> "*" Appointment : consults
    Patient "1" --> "*" MedicalRecord : possesses
    Appointment "1" --> "1" Bill : incurs
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
