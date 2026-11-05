# Warehouse Management System - Software Engineering (SE) Specification

## 1. Case Study Overview
Automates inbound pallet receiving, rack put-away, FIFO/LIFO pick-pack-ship, inventory cycle counts, and freight dispatch.

---

## 2. Use Case Diagram (Black & White UML Standard)
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["Warehouse Management System (System Boundary)"]
        UC01(["UC01: Register & Authenticate WarehouseWorker"])
        UC02(["UC02: Search & View Warehouse Items"])
        UC03(["UC03: Create New Booking / Request"])
        UC04(["UC04: Process Verification & Approvals"])
        UC05(["UC05: Generate Invoice & Process Payment"])
        UC06(["UC06: Update Central Records & Inventory"])
        UC07(["UC07: Generate Operational & Audit Reports"])
    end

    %% Actors
    WarehouseWorker["<<Actor>>\nWarehouseWorker"]:::actorStyle
    Picker["<<Actor>>\nPicker"]:::actorStyle
    Dispatcher["<<Actor>>\nDispatcher"]:::actorStyle
    LogisticsManager["<<Actor>>\nLogisticsManager"]:::actorStyle

    %% Actor to Use Case Associations
    WarehouseWorker --> UC01
    WarehouseWorker --> UC02
    WarehouseWorker --> UC03
    WarehouseWorker --> UC05
    Picker --> UC02
    Picker --> UC03
    Picker --> UC04
    Picker --> UC06
    LogisticsManager --> UC04
    LogisticsManager --> UC06
    LogisticsManager --> UC07

    %% Include & Extend Relationships
    UC03 -.->|<<include>>| UC02
    UC04 -.->|<<include>>| UC03
    UC05 -.->|<<include>>| UC04
    UC07 -.->|<<extend>>| UC06
```

---

## 3. Class Diagram (UML Structure)
```mermaid
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

    class WarehouseWorkerProfile {
        -String regNumber
        -Date joinDate
        +submitRequest() String
        +viewStatus() void
    }

    class LogisticsManagerProfile {
        -String accessLevel
        -String badgeId
        +verifyEntry() bool
        +generateSummary() Report
    }

    class WarehouseRecord {
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

    BaseUser <|-- WarehouseWorkerProfile
    BaseUser <|-- LogisticsManagerProfile
    WarehouseWorkerProfile "1" --> "*" WarehouseRecord : initiates
    LogisticsManagerProfile "1" --> "*" WarehouseRecord : moderates
    WarehouseRecord "1" --> "1" TransactionPayment : settled by
```

---

## 4. Data Flow Diagram (Level 1 DFD)
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] WarehouseWorker"]:::entity
    E2["[Entity] Picker"]:::entity
    E3["[Entity] LogisticsManager"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 WarehouseWorker Authentication"]):::process
    P2(["2.0 Warehouse Service Request Processing"]):::process
    P3(["3.0 Verification & Scheduling"]):::process
    P4(["4.0 Financial Settlement"]):::process
    P5(["5.0 Analytics & Master DB Update"]):::process

    %% Data Stores
    D1[("D1: Warehouse Master Registry")]:::datastore
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
```

---

## 5. Activity Diagram (Workflow with Swimlanes)
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef decision fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef sync fill:#000000,stroke:#000000,stroke-width:1px,color:#ffffff;
    classDef circle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    StartNode((Start)):::circle
    EndNode((End)):::circle

    subgraph SWIM_WarehouseWorker ["WarehouseWorker Swimlane"]
        ACT_1["Initiate Online Service Request"]
        ACT_2["Provide Documentation & Details"]
        ACT_3["Make Digital / Cash Payment"]
    end

    subgraph SWIM_Picker ["Picker Swimlane"]
        ACT_4["Review Inward Application"]
        ACT_5["Validate Against Policy Guidelines"]
        ACT_6["Forward for Final Approval"]
    end

    subgraph SWIM_LogisticsManager ["LogisticsManager Swimlane"]
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
```
