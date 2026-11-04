# LabX SE Remote: All 4 Diagrams for Library Management System
Write-Host "==============================================================" -ForegroundColor White
Write-Host "  LabX SE: All 4 UML & DFD Diagrams for Library Management System" -ForegroundColor White
Write-Host "==============================================================" -ForegroundColor Gray

$seDir = Join-Path $PWD "SE"
if (-not (Test-Path $seDir)) { New-Item -ItemType Directory -Path $seDir -Force | Out-Null }

Write-Host "  -> Saving Use Case Diagram (library_usecase.mmd)..." -ForegroundColor White
$code_usecase = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["Library Management System (System Boundary)"]
        UC01(["UC01: Search Online Catalog (OPAC)"])
        UC02(["UC02: Borrow / Issue Book"])
        UC03(["UC03: Return & Inspect Book"])
        UC04(["UC04: Calculate & Collect Overdue Fine"])
        UC05(["UC05: Reserve Unavailable Book"])
        UC06(["UC06: Catalog New Book & Author"])
        UC07(["UC07: Generate Circulation Reports"])
    end

    %% Actors
    StudentMember["<<Actor>>\nStudentMember"]:::actorStyle
    FacultyMember["<<Actor>>\nFacultyMember"]:::actorStyle
    Librarian["<<Actor>>\nLibrarian"]:::actorStyle
    Admin["<<Actor>>\nAdmin"]:::actorStyle

    %% Actor to Use Case Associations
    StudentMember --> UC01
    StudentMember --> UC02
    StudentMember --> UC03
    StudentMember --> UC05
    FacultyMember --> UC01
    FacultyMember --> UC02
    FacultyMember --> UC03
    FacultyMember --> UC05
    Librarian --> UC02
    Librarian --> UC03
    Librarian --> UC04
    Librarian --> UC06
    Librarian --> UC07
    Admin --> UC06
    Admin --> UC07

    %% Include & Extend Relationships
    UC02 -.->|<<include>>| UC01
    UC03 -.->|<<extend>>| UC04
    UC05 -.->|<<extend>>| UC01
'@
Set-Content -Path (Join-Path $seDir "library_usecase.mmd") -Value $code_usecase -Encoding utf8

Write-Host "  -> Saving Class Diagram (library_class.mmd)..." -ForegroundColor White
$code_class = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
classDiagram
    direction TB

    class LibraryUser {
        <<abstract>>
        #String memberId
        #String name
        #int maxBorrowLimit
        +searchCatalog(String query) List~Book~
    }

    class StudentMember {
        -String dept
        -float outstandingFine
        +requestBorrow(Book b) bool
    }

    class FacultyMember {
        -String designation
        -int extendedDays
        +requestBookPurchase(String isbn) void
    }

    class Librarian {
        -String staffId
        -String shift
        +issueBook(String memberId, String isbn) Loan
        +returnBook(String loanId) void
    }

    class Book {
        -String isbn
        -String title
        -String author
        -String publisher
        -int totalCopies
        -int availableCopies
        +checkAvailability() bool
        +updateStock(int qty) void
    }

    class LoanRecord {
        -String loanId
        -Date issueDate
        -Date dueDate
        -Date returnDate
        -float fineAmount
        +calculateOverdueDays() int
    }

    class Reservation {
        -String resId
        -Date reservedOn
        -String status
        +notifyAvailability() void
    }

    LibraryUser <|-- StudentMember
    LibraryUser <|-- FacultyMember
    LibraryUser "1" --> "*" LoanRecord : holds
    Book "1" --> "*" LoanRecord : borrowed in
    LibraryUser "1" --> "*" Reservation : places
    Book "1" --> "*" Reservation : subject of
'@
Set-Content -Path (Join-Path $seDir "library_class.mmd") -Value $code_class -Encoding utf8

Write-Host "  -> Saving Data Flow Diagram (Level 1) (library_dfd.mmd)..." -ForegroundColor White
$code_dfd = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] Member"]:::entity
    E2["[Entity] Librarian"]:::entity
    E3["[Entity] Admin"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Catalog Search & Indexing"]):::process
    P2(["2.0 Book Issue & Verification"]):::process
    P3(["3.0 Return & Overdue Assessment"]):::process
    P4(["4.0 Reservation Management"]):::process
    P5(["5.0 Inventory & Acquisition"]):::process

    %% Data Stores
    D1[("D1: Book Catalog Store")]:::datastore
    D2[("D2: Member Directory")]:::datastore
    D3[("D3: Active Loans Store")]:::datastore
    D4[("D4: Fines & Ledger")]:::datastore
    D5[("D5: Reservations Queue")]:::datastore

    %% Data Flows
    E1 -->|Search Query (Title/ISBN)| P1
    P1 -->|Catalog Query| D1
    E1 -->|Borrow Request| P2
    P2 -->|Check Eligibility & Limits| D2
    P2 -->|Record Loan| D3
    E1 -->|Return Book| P3
    P3 -->|Close Loan Record| D3
    P3 -->|Compute Fine Details| D4
    E2 -->|New Title Metadata| P5
    P5 -->|Insert Stock| D1
'@
Set-Content -Path (Join-Path $seDir "library_dfd.mmd") -Value $code_dfd -Encoding utf8

Write-Host "  -> Saving Activity Diagram (library_activity.mmd)..." -ForegroundColor White
$code_activity = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef decision fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef sync fill:#000000,stroke:#000000,stroke-width:1px,color:#ffffff;
    classDef circle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    StartNode((Start)):::circle
    EndNode((End)):::circle

    subgraph SWIM_Member ["Member Swimlane"]
        ACT_1["Search OPAC Catalog"]
        ACT_2["Present ID & Book at Desk"]
        ACT_3["Return Book & Pay Overdue Fine"]
    end

    subgraph SWIM_Librarian ["Librarian Swimlane"]
        ACT_4["Verify Borrowing Quota"]
        ACT_5["Scan Barcode & Stamp Due Date"]
        ACT_6["Inspect Condition & Calculate Fine"]
    end

    subgraph SWIM_Database_System ["Database System Swimlane"]
        ACT_7["Check Available Copies"]
        ACT_8["Update Loan Status to Active"]
        ACT_9["Clear Member Hold"]
    end

    DEC_1{"Max Books Reached?"}:::decision

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
Set-Content -Path (Join-Path $seDir "library_activity.mmd") -Value $code_activity -Encoding utf8

try {
    Set-Clipboard -Value $code_usecase
    Write-Host "`n[OK] Use Case Diagram copied to clipboard! (Ctrl + V to paste)" -ForegroundColor White
} catch {}

Write-Host "`n[OK] All 4 diagrams for Library Management System successfully saved into SE\ directory!" -ForegroundColor White
Write-Host "[*] Created: library_usecase.mmd, library_class.mmd, library_dfd.mmd, library_activity.mmd" -ForegroundColor Gray
