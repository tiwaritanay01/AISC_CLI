# School Management System - Software Engineering (SE) Specification

## 1. Case Study Overview
Manages academic operations: student profiles, admissions, attendance tracking, fee collection, exam schedules, grading, staff payroll, timetables, and transport inventory.

---

## 2. Use Case Diagram (Black & White UML Standard)
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["School Management System (System Boundary)"]
        UC01(["UC01: Register & Enroll Student"])
        UC02(["UC02: Record Daily Attendance"])
        UC03(["UC03: Generate Timetable & Roster"])
        UC04(["UC04: Publish Examination Marks"])
        UC05(["UC05: Collect Tuition Fees & Invoice"])
        UC06(["UC06: Process Staff Payroll"])
        UC07(["UC07: Manage Bus Transport & Routes"])
        UC08(["UC08: Manage Department Inventory"])
    end

    %% Actors
    Student["<<Actor>>\nStudent"]:::actorStyle
    Teacher["<<Actor>>\nTeacher"]:::actorStyle
    Accountant["<<Actor>>\nAccountant"]:::actorStyle
    SchoolAdmin["<<Actor>>\nSchoolAdmin"]:::actorStyle

    %% Actor to Use Case Associations
    Student --> UC01
    Student --> UC04
    Student --> UC05
    Teacher --> UC02
    Teacher --> UC03
    Teacher --> UC04
    Accountant --> UC05
    Accountant --> UC06
    SchoolAdmin --> UC01
    SchoolAdmin --> UC03
    SchoolAdmin --> UC07
    SchoolAdmin --> UC08

    %% Include & Extend Relationships
    UC01 -.->|<<include>>| UC05
    UC04 -.->|<<extend>>| UC02
    UC05 -.->|<<include>>| UC06
```

---

## 3. Class Diagram (UML Structure)
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
classDiagram
    direction TB

    class Person {
        <<abstract>>
        #int id
        #String name
        #String email
        #String phone
        +login() bool
        +logout() void
    }

    class Student {
        -String rollNo
        -String classSection
        -Date dob
        -float feeBalance
        +viewMarks() GradeCard
        +payFee(float amt) Receipt
    }

    class Teacher {
        -String empId
        -String department
        -List~String~ subjects
        +markAttendance(Class c) void
        +enterGrades(Exam e) void
    }

    class SchoolAdmin {
        -String adminId
        -String role
        +createTimetable() Timetable
        +manageTransport() void
    }

    class Course {
        -String courseCode
        -String title
        -int credits
        +getSyllabus() String
    }

    class AttendanceRecord {
        -Date date
        -String status
        -String remarks
        +calculatePercentage() float
    }

    class FeePayment {
        -String receiptId
        -float amount
        -Date paidOn
        -String mode
        +generateReceipt() Receipt
    }

    class TransportRoute {
        -String busNo
        -String driverName
        -List~String~ stops
        +trackGPS() Coordinates
    }

    Person <|-- Student
    Person <|-- Teacher
    Person <|-- SchoolAdmin
    Student "*" --> "1" Course : enrolled in
    Teacher "1" --> "*" Course : instructs
    Student "1" --> "*" AttendanceRecord : has
    Student "1" --> "*" FeePayment : makes
    Student "*" --> "1" TransportRoute : assigned to
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
    E1["[Entity] Student"]:::entity
    E2["[Entity] Teacher"]:::entity
    E3["[Entity] Accountant"]:::entity
    E4["[Entity] Admin"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Student Admission & Profiling"]):::process
    P2(["2.0 Attendance Logging"]):::process
    P3(["3.0 Exam & Grading Evaluation"]):::process
    P4(["4.0 Fee Accounting & Payroll"]):::process
    P5(["5.0 Transport & Logistics"]):::process

    %% Data Stores
    D1[("D1: Student Master DB")]:::datastore
    D2[("D2: Attendance Register")]:::datastore
    D3[("D3: Academic Marks Store")]:::datastore
    D4[("D4: Fee & Ledger Store")]:::datastore
    D5[("D5: Transport Route Registry")]:::datastore

    %% Data Flows
    E1 -->|Admission Form| P1
    P1 -->|Save Student Record| D1
    E2 -->|Daily Attendance Sheet| P2
    P2 -->|Update Attendance Log| D2
    E2 -->|Exam Scores| P3
    P3 -->|Save Grades| D3
    P3 -->|Report Card| E1
    E3 -->|Fee Receipts| P4
    P4 -->|Record Transaction| D4
    E4 -->|Bus Fleet Schedule| P5
    P5 -->|Route Allocations| D5
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

    subgraph SWIM_Student ["Student Swimlane"]
        ACT_1["Submit Admission & Docs"]
        ACT_2["Attend Classes"]
        ACT_3["Pay Term Fees"]
    end

    subgraph SWIM_Teacher ["Teacher Swimlane"]
        ACT_4["Verify Documents"]
        ACT_5["Mark Attendance & Conduct Exams"]
        ACT_6["Submit Marks"]
    end

    subgraph SWIM_Administration ["Administration Swimlane"]
        ACT_7["Generate Fee Challan"]
        ACT_8["Calculate Payroll"]
        ACT_9["Issue Final Report Card"]
    end

    DEC_1{"Documents Valid?"}:::decision

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
