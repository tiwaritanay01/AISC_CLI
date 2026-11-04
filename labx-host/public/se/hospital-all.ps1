# LabX SE Remote: All 4 Diagrams for Hospital Management System
Write-Host "==============================================================" -ForegroundColor White
Write-Host "  LabX SE: All 4 UML & DFD Diagrams for Hospital Management System" -ForegroundColor White
Write-Host "==============================================================" -ForegroundColor Gray

$seDir = Join-Path $PWD "SE"
if (-not (Test-Path $seDir)) { New-Item -ItemType Directory -Path $seDir -Force | Out-Null }

Write-Host "  -> Saving Use Case Diagram (hospital_usecase.mmd)..." -ForegroundColor White
$code_usecase = @'
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
Set-Content -Path (Join-Path $seDir "hospital_usecase.mmd") -Value $code_usecase -Encoding utf8

Write-Host "  -> Saving Class Diagram (hospital_class.mmd)..." -ForegroundColor White
$code_class = @'
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
Set-Content -Path (Join-Path $seDir "hospital_class.mmd") -Value $code_class -Encoding utf8

Write-Host "  -> Saving Data Flow Diagram (Level 1) (hospital_dfd.mmd)..." -ForegroundColor White
$code_dfd = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] Patient"]:::entity
    E2["[Entity] Receptionist"]:::entity
    E3["[Entity] Doctor"]:::entity
    E4["[Entity] Administrator"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Patient Intake & Triage"]):::process
    P2(["2.0 Appointment Booking"]):::process
    P3(["3.0 Clinical Consultation & EMR"]):::process
    P4(["4.0 Pharmacy & Diagnostics"]):::process
    P5(["5.0 Billing & Discharge"]):::process

    %% Data Stores
    D1[("D1: Patient Database")]:::datastore
    D2[("D2: Doctor Duty Roster")]:::datastore
    D3[("D3: Medical Records Store")]:::datastore
    D4[("D4: Pharmacy Stock")]:::datastore
    D5[("D5: Financial Accounts")]:::datastore

    %% Data Flows
    E1 -->|Personal Details| P1
    P1 -->|Save Patient Details| D1
    E2 -->|Slot Booking Request| P2
    P2 -->|Check Doctor Availability| D2
    E3 -->|Clinical Notes & Rx| P3
    P3 -->|Append EMR| D3
    P3 -->|Medicine Dispense Order| P4
    P4 -->|Deduct Drug Stock| D4
    P4 -->|Drug Bill Items| P5
    P5 -->|Settlement Receipt| E1
'@
Set-Content -Path (Join-Path $seDir "hospital_dfd.mmd") -Value $code_dfd -Encoding utf8

Write-Host "  -> Saving Activity Diagram (hospital_activity.mmd)..." -ForegroundColor White
$code_activity = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef decision fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef sync fill:#000000,stroke:#000000,stroke-width:1px,color:#ffffff;
    classDef circle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    StartNode((Start)):::circle
    EndNode((End)):::circle

    subgraph SWIM_Patient ["Patient Swimlane"]
        ACT_1["Arrive & Request Appointment"]
        ACT_2["Undergo Examination"]
        ACT_3["Pay Hospital Bill"]
    end

    subgraph SWIM_Receptionist ["Receptionist Swimlane"]
        ACT_4["Check Slot & Issue Token"]
        ACT_5["Forward to Doctor Room"]
        ACT_6["Print Discharge Slip"]
    end

    subgraph SWIM_Doctor ["Doctor Swimlane"]
        ACT_7["Review Medical History"]
        ACT_8["Prescribe Medicines & Lab"]
        ACT_9["Sign Off Discharge"]
    end

    DEC_1{"Requires Pathology Lab?"}:::decision

    %% Activity Workflow Transitions
    StartNode --> ACT_1
    ACT_1 --> ACT_2
    ACT_2 --> ACT_3
    ACT_3 --> ACT_4
    ACT_4 --> ACT_5
    ACT_5 --> ACT_6
    ACT_6 --> ACT_7
    ACT_7 --> ACT_8
    ACT_8 --> ACT_9
    ACT_9 --> DEC_1
    DEC_1 -->|Approved / Success| EndNode
    DEC_1 -->|Rejected / Needs Revision| ACT_1
'@
Set-Content -Path (Join-Path $seDir "hospital_activity.mmd") -Value $code_activity -Encoding utf8

try {
    Set-Clipboard -Value $code_usecase
    Write-Host "`n[OK] Use Case Diagram copied to clipboard! (Ctrl + V to paste)" -ForegroundColor White
} catch {}

Write-Host "`n[OK] All 4 diagrams for Hospital Management System successfully saved into SE\ directory!" -ForegroundColor White
Write-Host "[*] Created: hospital_usecase.mmd, hospital_class.mmd, hospital_dfd.mmd, hospital_activity.mmd" -ForegroundColor Gray
