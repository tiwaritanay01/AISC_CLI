# LabX SE Remote: All 4 Diagrams for Project Management System
Write-Host "==============================================================" -ForegroundColor White
Write-Host "  LabX SE: All 4 UML & DFD Diagrams for Project Management System" -ForegroundColor White
Write-Host "==============================================================" -ForegroundColor Gray

$seDir = Join-Path $PWD "SE"
if (-not (Test-Path $seDir)) { New-Item -ItemType Directory -Path $seDir -Force | Out-Null }

Write-Host "  -> Saving Use Case Diagram (project_usecase.mmd)..." -ForegroundColor White
$code_usecase = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["Project Management System (System Boundary)"]
        UC01(["UC01: Create Project & Define Scope"])
        UC02(["UC02: Breakdown Work Breakdown Structure (WBS)"])
        UC03(["UC03: Assign Tasks & Allocate Resources"])
        UC04(["UC04: Log Timesheet & Update Progress"])
        UC05(["UC05: Track Sprint Burndown & Milestones"])
        UC06(["UC06: Review Deliverables & Signoff"])
        UC07(["UC07: Generate Project Health & Budget Reports"])
    end

    %% Actors
    TeamMember["<<Actor>>\nTeamMember"]:::actorStyle
    ProjectManager["<<Actor>>\nProjectManager"]:::actorStyle
    Client["<<Actor>>\nClient"]:::actorStyle
    Executive["<<Actor>>\nExecutive"]:::actorStyle

    %% Actor to Use Case Associations
    TeamMember --> UC04
    TeamMember --> UC05
    ProjectManager --> UC01
    ProjectManager --> UC02
    ProjectManager --> UC03
    ProjectManager --> UC05
    ProjectManager --> UC07
    Client --> UC06
    Client --> UC07
    Executive --> UC07

    %% Include & Extend Relationships
    UC02 -.->|<<include>>| UC01
    UC03 -.->|<<include>>| UC02
    UC05 -.->|<<extend>>| UC04
'@
Set-Content -Path (Join-Path $seDir "project_usecase.mmd") -Value $code_usecase -Encoding utf8

Write-Host "  -> Saving Class Diagram (project_class.mmd)..." -ForegroundColor White
$code_class = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
classDiagram
    direction TB

    class Project {
        -String projId
        -String title
        -Date startDate
        -Date endDate
        -float budget
        -String status
        +calculateProgress() float
        +checkBudgetVariance() float
    }

    class Task {
        -String taskId
        -String title
        -int estHours
        -int actualHours
        -String priority
        -String state
        +assignTo(String devId) void
        +markComplete() void
    }

    class Resource {
        -String resId
        -String name
        -String role
        -float hourlyRate
        +checkAvailability() bool
    }

    class Timesheet {
        -String entryId
        -Date workDate
        -float hoursLogged
        -String comments
        +approve() void
    }

    class Milestone {
        -String milestoneId
        -Date targetDate
        -boolean isDelivered
        +verifyDeliverable() bool
    }

    Project "1" --> "*" Task : consists of
    Task "*" --> "1" Resource : assigned to
    Resource "1" --> "*" Timesheet : submits
    Project "1" --> "*" Milestone : tracks
'@
Set-Content -Path (Join-Path $seDir "project_class.mmd") -Value $code_class -Encoding utf8

Write-Host "  -> Saving Data Flow Diagram (Level 1) (project_dfd.mmd)..." -ForegroundColor White
$code_dfd = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] ProjectManager"]:::entity
    E2["[Entity] TeamMember"]:::entity
    E3["[Entity] Client"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Project Charter & Scope Creation"]):::process
    P2(["2.0 Task Decomposition & Scheduling"]):::process
    P3(["3.0 Execution & Timesheet Logging"]):::process
    P4(["4.0 Milestone Tracking & QA"]):::process
    P5(["5.0 Billing & Governance Reporting"]):::process

    %% Data Stores
    D1[("D1: Project Registry")]:::datastore
    D2[("D2: Task & Backlog Store")]:::datastore
    D3[("D3: Resource Pool")]:::datastore
    D4[("D4: Timesheet Logs")]:::datastore
    D5[("D5: Financials & Budget Store")]:::datastore

    %% Data Flows
    E1 -->|Scope & Budget| P1
    P1 -->|New Project Baseline| D1
    E1 -->|Task Breakdown (WBS)| P2
    P2 -->|Save Tasks & Deadlines| D2
    E2 -->|Daily Hours & Status| P3
    P3 -->|Commit Timesheets| D4
    P3 -->|Sprint Burndown Delta| P4
    P4 -->|Milestone Verification| E3
    P5 -->|Budget Utilization Dashboard| E1
'@
Set-Content -Path (Join-Path $seDir "project_dfd.mmd") -Value $code_dfd -Encoding utf8

Write-Host "  -> Saving Activity Diagram (project_activity.mmd)..." -ForegroundColor White
$code_activity = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef decision fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef sync fill:#000000,stroke:#000000,stroke-width:1px,color:#ffffff;
    classDef circle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    StartNode((Start)):::circle
    EndNode((End)):::circle

    subgraph SWIM_ProjectManager ["ProjectManager Swimlane"]
        ACT_1["Create Project Charter"]
        ACT_2["Allocate Team Resources"]
        ACT_3["Review Milestone Progress"]
    end

    subgraph SWIM_TeamMember ["TeamMember Swimlane"]
        ACT_4["Pick Backlog Task"]
        ACT_5["Execute Code / Design"]
        ACT_6["Log Daily Timesheet Hours"]
    end

    subgraph SWIM_Client ["Client Swimlane"]
        ACT_7["Approve Sprint Goals"]
        ACT_8["Review Demo Deliverable"]
        ACT_9["Signoff Milestone Acceptance"]
    end

    DEC_1{"Deliverable Meets DoD?"}:::decision

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
Set-Content -Path (Join-Path $seDir "project_activity.mmd") -Value $code_activity -Encoding utf8

try {
    Set-Clipboard -Value $code_usecase
    Write-Host "`n[OK] Use Case Diagram copied to clipboard! (Ctrl + V to paste)" -ForegroundColor White
} catch {}

Write-Host "`n[OK] All 4 diagrams for Project Management System successfully saved into SE\ directory!" -ForegroundColor White
Write-Host "[*] Created: project_usecase.mmd, project_class.mmd, project_dfd.mmd, project_activity.mmd" -ForegroundColor Gray
