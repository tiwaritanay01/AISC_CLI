# LabX SE Remote: All 4 Diagrams for ATM Management System
Write-Host "==============================================================" -ForegroundColor White
Write-Host "  LabX SE: All 4 UML & DFD Diagrams for ATM Management System" -ForegroundColor White
Write-Host "==============================================================" -ForegroundColor Gray

$seDir = Join-Path $PWD "SE"
if (-not (Test-Path $seDir)) { New-Item -ItemType Directory -Path $seDir -Force | Out-Null }

Write-Host "  -> Saving Use Case Diagram (atm_usecase.mmd)..." -ForegroundColor White
$code_usecase = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["ATM Management System (System Boundary)"]
        UC01(["UC01: Register & Authenticate BankCustomer"])
        UC02(["UC02: Search & View ATM Items"])
        UC03(["UC03: Create New Booking / Request"])
        UC04(["UC04: Process Verification & Approvals"])
        UC05(["UC05: Generate Invoice & Process Payment"])
        UC06(["UC06: Update Central Records & Inventory"])
        UC07(["UC07: Generate Operational & Audit Reports"])
    end

    %% Actors
    BankCustomer["<<Actor>>\nBankCustomer"]:::actorStyle
    ATMHardwareController["<<Actor>>\nATMHardwareController"]:::actorStyle
    BankCoreServer["<<Actor>>\nBankCoreServer"]:::actorStyle
    CashTechnician["<<Actor>>\nCashTechnician"]:::actorStyle

    %% Actor to Use Case Associations
    BankCustomer --> UC01
    BankCustomer --> UC02
    BankCustomer --> UC03
    BankCustomer --> UC05
    ATMHardwareController --> UC02
    ATMHardwareController --> UC03
    ATMHardwareController --> UC04
    ATMHardwareController --> UC06
    CashTechnician --> UC04
    CashTechnician --> UC06
    CashTechnician --> UC07

    %% Include & Extend Relationships
    UC03 -.->|<<include>>| UC02
    UC04 -.->|<<include>>| UC03
    UC05 -.->|<<include>>| UC04
    UC07 -.->|<<extend>>| UC06
'@
Set-Content -Path (Join-Path $seDir "atm_usecase.mmd") -Value $code_usecase -Encoding utf8

Write-Host "  -> Saving Class Diagram (atm_class.mmd)..." -ForegroundColor White
$code_class = @'
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

    class BankCustomerProfile {
        -String regNumber
        -Date joinDate
        +submitRequest() String
        +viewStatus() void
    }

    class CashTechnicianProfile {
        -String accessLevel
        -String badgeId
        +verifyEntry() bool
        +generateSummary() Report
    }

    class ATMRecord {
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

    BaseUser <|-- BankCustomerProfile
    BaseUser <|-- CashTechnicianProfile
    BankCustomerProfile "1" --> "*" ATMRecord : initiates
    CashTechnicianProfile "1" --> "*" ATMRecord : moderates
    ATMRecord "1" --> "1" TransactionPayment : settled by
'@
Set-Content -Path (Join-Path $seDir "atm_class.mmd") -Value $code_class -Encoding utf8

Write-Host "  -> Saving Data Flow Diagram (Level 1) (atm_dfd.mmd)..." -ForegroundColor White
$code_dfd = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] BankCustomer"]:::entity
    E2["[Entity] ATMHardwareController"]:::entity
    E3["[Entity] CashTechnician"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 BankCustomer Authentication"]):::process
    P2(["2.0 ATM Service Request Processing"]):::process
    P3(["3.0 Verification & Scheduling"]):::process
    P4(["4.0 Financial Settlement"]):::process
    P5(["5.0 Analytics & Master DB Update"]):::process

    %% Data Stores
    D1[("D1: ATM Master Registry")]:::datastore
    D2[("D2: Active Transactions")]:::datastore
    D3[("D3: Verification Logs")]:::datastore
    D4[("D4: Ledger & Payments")]:::datastore
    D5[("D5: System Archives")]:::datastore

    %% Data Flows
    E1 -->|Registration Credentials| P1
    P1 -->|Save Verified User| D1
    E1 -->|Service Request Input| P2
    P2 -->|Record Transaction Intent| D2
    E3 -->|Verification Decision| P3
    P3 -->|Update Compliance Status| D3
    P3 -->|Billing Breakdown| P4
    P4 -->|Payment Confirmation| D4
    P4 -->|Official Receipt| E1
    P5 -->|Quarterly Audit Summary| E3
'@
Set-Content -Path (Join-Path $seDir "atm_dfd.mmd") -Value $code_dfd -Encoding utf8

Write-Host "  -> Saving Activity Diagram (atm_activity.mmd)..." -ForegroundColor White
$code_activity = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef decision fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef sync fill:#000000,stroke:#000000,stroke-width:1px,color:#ffffff;
    classDef circle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    StartNode((Start)):::circle
    EndNode((End)):::circle

    subgraph SWIM_BankCustomer ["BankCustomer Swimlane"]
        ACT_1["Initiate Online Service Request"]
        ACT_2["Provide Documentation & Details"]
        ACT_3["Make Digital / Cash Payment"]
    end

    subgraph SWIM_ATMHardwareController ["ATMHardwareController Swimlane"]
        ACT_4["Review Inward Application"]
        ACT_5["Validate Against Policy Guidelines"]
        ACT_6["Forward for Final Approval"]
    end

    subgraph SWIM_CashTechnician ["CashTechnician Swimlane"]
        ACT_7["Audit Compliance"]
        ACT_8["Authorize Service Allocation"]
        ACT_9["Dispatch Confirmation & Receipt"]
    end

    DEC_1{"Meets Eligibility Criteria?"}:::decision

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
Set-Content -Path (Join-Path $seDir "atm_activity.mmd") -Value $code_activity -Encoding utf8

try {
    Set-Clipboard -Value $code_usecase
    Write-Host "`n[OK] Use Case Diagram copied to clipboard! (Ctrl + V to paste)" -ForegroundColor White
} catch {}

Write-Host "`n[OK] All 4 diagrams for ATM Management System successfully saved into SE\ directory!" -ForegroundColor White
Write-Host "[*] Created: atm_usecase.mmd, atm_class.mmd, atm_dfd.mmd, atm_activity.mmd" -ForegroundColor Gray
