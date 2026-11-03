# LabX SE Remote: Hospital Management System - Class Diagram
$title = "Class Diagram"
$topic = "Hospital Management System"
$filename = "hospital_class.mmd"

$mermaidCode = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000'}}}%%
classDiagram
    direction TB

    class User {
        <<abstract>>
        #int userId
        #String name
        #String email
        #String phone
        #String passwordHash
        +login(String email, String pwd) bool
        +logout() void
        +updateProfile() void
    }

    class Patient {
        -String patientId
        -String bloodGroup
        -String emergencyContact
        -Date dob
        +bookAppointment(String doctorId, Date date) Appointment
        +viewMedicalHistory() List~MedicalRecord~
        +payBill(String billId) bool
    }

    class Doctor {
        -String doctorId
        -String specialization
        -String qualification
        -List~String~ availableSlots
        +viewAppointments() List~Appointment~
        +updateEMR(String patientId, String notes) void
        +createPrescription(String patientId) Prescription
    }

    class Receptionist {
        -String staffId
        -String deskNumber
        +registerPatient(Patient p) String
        +scheduleAppointment(Appointment appt) bool
        +generateToken(String patientId) int
    }

    class Administrator {
        -String adminId
        -String department
        +addStaff(User u) bool
        +manageInventory() void
        +generateAuditReport() Report
    }

    class Appointment {
        -String appointmentId
        -Date appointmentDate
        -String timeSlot
        -String status
        +confirm() void
        +cancel() void
        +reschedule(Date newDate) void
    }

    class MedicalRecord_EMR {
        -String recordId
        -Date recordDate
        -String symptoms
        -String diagnosis
        -String labResults
        +addDiagnosis(String diag) void
        +attachReport(String fileUrl) void
    }

    class Prescription {
        -String prescriptionId
        -Date issueDate
        -List~String~ medicineNames
        -String dosageInstructions
        +dispenseMedicines() bool
    }

    class Bill {
        -String billId
        -float consultationFee
        -float medicineCharges
        -float labCharges
        -float totalAmount
        -String paymentStatus
        +calculateTotal() float
        +generateReceipt() String
    }

    class InventoryItem {
        -String itemId
        -String itemName
        -int stockQuantity
        -float unitPrice
        -Date expiryDate
        +restock(int quantity) void
        +deductStock(int quantity) bool
    }

    %% Inheritance (Generalization)
    User <|-- Patient
    User <|-- Doctor
    User <|-- Receptionist
    User <|-- Administrator

    %% Associations & Composition
    Patient "1" --> "*" Appointment : books
    Doctor "1" --> "*" Appointment : conducts
    Patient "1" *-- "1..*" MedicalRecord_EMR : owns
    Doctor "1" --> "*" MedicalRecord_EMR : maintains
    MedicalRecord_EMR "1" *-- "1" Prescription : contains
    Appointment "1" --> "1" Bill : generates
    Administrator "1" --> "*" InventoryItem : oversees
    Receptionist "1" --> "*" Bill : issues

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
