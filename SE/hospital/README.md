# Hospital Management System - Software Engineering (SE) Specification

## 1. Case Study Overview
The Hospital Management System manages hospital operations ranging from patient registration and appointment scheduling to billing, pharmacy inventory, and Electronic Medical Records (EMR). It serves four primary stakeholder modules: **Patient**, **Receptionist**, **Doctor**, and **Administrator**.

---

## 2. Use Case Diagram (Black & White UML Standard)
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["Hospital Management System (System Boundary)"]
        UC1([UC-01: Register / Login Patient])
        UC2([UC-02: Book / Reschedule Appointment])
        UC3([UC-03: Verify Doctor Availability])
        UC4([UC-04: View & Update EMR Medical Records])
        UC5([UC-05: Generate Diagnosis & Prescription])
        UC6([UC-06: Order Lab Diagnostic Tests])
        UC7([UC-07: Process Discharge & Invoicing])
        UC8([UC-08: Process Insurance & Payment])
        UC9([UC-09: Manage Pharmacy & Drug Inventory])
        UC10([UC-10: Manage Hospital Staff & System Roles])
    end

    Patient["<<Actor>>\nPatient"]:::actorStyle
    Receptionist["<<Actor>>\nReceptionist"]:::actorStyle
    Doctor["<<Actor>>\nDoctor"]:::actorStyle
    Admin["<<Actor>>\nAdministrator"]:::actorStyle

    Patient --> UC1
    Patient --> UC2

    Receptionist --> UC1
    Receptionist --> UC2
    Receptionist --> UC7

    Doctor --> UC4
    Doctor --> UC5

    Admin --> UC9
    Admin --> UC10
    Admin --> UC7

    UC2 -.->|<<include>>| UC3
    UC5 -.->|<<extend>>| UC6
    UC7 -.->|<<include>>| UC8
```

---

## 3. Class Diagram (UML Structure)
```mermaid
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

    User <|-- Patient
    User <|-- Doctor
    User <|-- Receptionist
    User <|-- Administrator

    Patient "1" --> "*" Appointment : books
    Doctor "1" --> "*" Appointment : conducts
    Patient "1" *-- "1..*" MedicalRecord_EMR : owns
    Doctor "1" --> "*" MedicalRecord_EMR : maintains
    MedicalRecord_EMR "1" *-- "1" Prescription : contains
    Appointment "1" --> "1" Bill : generates
    Administrator "1" --> "*" InventoryItem : oversees
    Receptionist "1" --> "*" Bill : issues
```

---

## 4. Data Flow Diagram (Level 1 DFD)
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    E1["[Entity] Patient"]:::entity
    E2["[Entity] Receptionist"]:::entity
    E3["[Entity] Doctor"]:::entity
    E4["[Entity] Administrator"]:::entity

    P1(["1.0 Patient Registration & Verification"]):::process
    P2(["2.0 Appointment Scheduling"]):::process
    P3(["3.0 Clinical Consultation & EMR Update"]):::process
    P4(["4.0 Inventory & Pharmacy Dispensing"]):::process
    P5(["5.0 Billing & Invoice Settlement"]):::process

    D1[("D1: Patient Database")]:::datastore
    D2[("D2: Doctor Roster & Slots")]:::datastore
    D3[("D3: EMR & Medical Histories")]:::datastore
    D4[("D4: Drug & Stock Inventory")]:::datastore
    D5[("D5: Financial & Accounts Store")]:::datastore

    E1 -->|Registration Details| P1
    E2 -->|Walk-in Details| P1
    P1 -->|Store Patient Info| D1
    P1 -->|Patient ID & Card| E1

    E1 -->|Appointment Request| P2
    P2 <-->|Check / Block Slot| D2
    D1 -->|Verify Patient ID| P2
    P2 -->|Appointment Slip| E1
    P2 -->|Daily Patient Queue| E3

    E3 -->|Diagnosis & Lab Notes| P3
    P3 <-->|Read / Write EMR| D3
    P3 -->|Prescription Orders| P4

    P4 <-->|Check Stock / Deduct Items| D4
    E4 -->|Stock Restock Entries| P4
    P4 -->|Medicine Cost Breakdown| P5

    P3 -->|Consultation Charges| P5
    P5 <-->|Record Ledger & Invoices| D5
    P5 -->|Final Itemized Invoice| E1
    E1 -->|Payment Settlement| P5
    P5 -->|Revenue & Audit Summary| E4
```

---

## 5. Activity Diagram (Workflow with Swimlanes)
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000'}}}%%
flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef decision fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef sync fill:#000000,stroke:#000000,stroke-width:1px,color:#ffffff;
    classDef circle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    Start((Start)):::circle

    subgraph SWIMLANE_PATIENT ["Patient Swimlane"]
        A1["Arrive at Hospital / Request Appointment"]
        A2["Provide Symptoms & Medical History"]
        A3["Undergo Diagnostic Tests"]
        A4["Make Payment (Cash / Insurance / Card)"]
    end

    subgraph SWIMLANE_RECEPTION ["Receptionist Swimlane"]
        B1{"Registered Patient?"}:::decision
        B2["Create New Patient Profile in Database"]
        B3["Verify Doctor Slot & Assign Token"]
    end

    subgraph SWIMLANE_DOCTOR ["Doctor Swimlane"]
        C1["Call Token & Examine Patient"]
        C2{"Requires Lab Tests?"}:::decision
        C3["Issue Lab Requisition Order"]
        C4["Analyze Results & Prescribe Medication"]
        C5["Update EMR Database"]
    end

    subgraph SWIMLANE_BILLING ["Billing & Pharmacy Swimlane"]
        Fork1[=== Parallel Split ===]:::sync
        D1["Dispense Medicines from Pharmacy"]
        D2["Calculate Total Invoice Bill"]
        Join1[=== Parallel Join ===]:::sync
        D3["Generate Receipt & Discharge Summary"]
    end

    EndNode((End)):::circle

    Start --> A1
    A1 --> B1
    B1 -->|No| B2
    B2 --> B3
    B1 -->|Yes| B3
    B3 --> C1
    C1 --> A2
    A2 --> C2
    C2 -->|Yes| C3
    C3 --> A3
    A3 --> C4
    C2 -->|No| C4
    C4 --> C5

    C5 --> Fork1
    Fork1 --> D1
    Fork1 --> D2
    D1 --> Join1
    D2 --> Join1

    Join1 --> A4
    A4 --> D3
    D3 --> EndNode
```
