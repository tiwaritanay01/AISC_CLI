# LabX SE Remote: All 4 Diagrams for Performance Management System
Write-Host "==============================================================" -ForegroundColor White
Write-Host "  LabX SE: All 4 UML & DFD Diagrams for Performance Management System" -ForegroundColor White
Write-Host "==============================================================" -ForegroundColor Gray

$seDir = Join-Path $PWD "SE"
if (-not (Test-Path $seDir)) { New-Item -ItemType Directory -Path $seDir -Force | Out-Null }

Write-Host "  -> Saving Use Case Diagram (performance_usecase.mmd)..." -ForegroundColor White
$code_usecase = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart LR
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef actorStyle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000,stroke-dasharray: 0;

    subgraph SYSTEM ["Performance Management System (System Boundary)"]
        UC01(["UC01: Submit Self-Appraisal & Goals"])
        UC02(["UC02: Review Team KPI Deliverables"])
        UC03(["UC03: Conduct 360-Degree Peer Feedback"])
        UC04(["UC04: Calculate Merit Rating Score"])
        UC05(["UC05: Recommend Bonus / Promotion"])
        UC06(["UC06: Record Disciplinary Action / PIP"])
        UC07(["UC07: Generate Quarterly Performance Analytics"])
    end

    %% Actors
    Employee["<<Actor>>\nEmployee"]:::actorStyle
    Manager["<<Actor>>\nManager"]:::actorStyle
    HRAdmin["<<Actor>>\nHRAdmin"]:::actorStyle

    %% Actor to Use Case Associations
    Employee --> UC01
    Employee --> UC03
    Manager --> UC02
    Manager --> UC04
    Manager --> UC05
    Manager --> UC06
    HRAdmin --> UC04
    HRAdmin --> UC05
    HRAdmin --> UC06
    HRAdmin --> UC07

    %% Include & Extend Relationships
    UC02 -.->|<<include>>| UC01
    UC04 -.->|<<include>>| UC03
    UC05 -.->|<<extend>>| UC04
'@
Set-Content -Path (Join-Path $seDir "performance_usecase.mmd") -Value $code_usecase -Encoding utf8

Write-Host "  -> Saving Class Diagram (performance_class.mmd)..." -ForegroundColor White
$code_class = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
classDiagram
    direction TB

    class Employee {
        -String empId
        -String name
        -String department
        -String designation
        +submitGoals() void
        +viewAppraisal() Report
    }

    class Manager {
        -List~String~ reportees
        +evaluateKPI(String empId) Score
        +approvePromotion() void
    }

    class HRAdmin {
        -String policyAccessLevel
        +finalizeAppraisalCycle() void
        +issueIncrementLetter() Letter
    }

    class Goal {
        -String goalId
        -String description
        -Date targetDate
        -float weightage
        -String status
        +updateProgress(float percent) void
    }

    class AppraisalReview {
        -String reviewId
        -float selfRating
        -float managerRating
        -float peerScore
        -String comments
        +computeCompositeScore() float
    }

    class Reward {
        -String rewardId
        -String type
        -float bonusAmount
        -Date grantedOn
        +disburseReward() void
    }

    Employee <|-- Manager
    Employee <|-- HRAdmin
    Employee "1" --> "*" Goal : sets
    Employee "1" --> "*" AppraisalReview : evaluated by
    Manager "1" --> "*" AppraisalReview : conducts
    AppraisalReview "1" --> "0..1" Reward : triggers
'@
Set-Content -Path (Join-Path $seDir "performance_class.mmd") -Value $code_class -Encoding utf8

Write-Host "  -> Saving Data Flow Diagram (Level 1) (performance_dfd.mmd)..." -ForegroundColor White
$code_dfd = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef entity fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef datastore fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 4 2,color:#000000;

    %% External Entities
    E1["[Entity] Employee"]:::entity
    E2["[Entity] Manager"]:::entity
    E3["[Entity] HRAdmin"]:::entity

    %% Processes (Level 1 DFD)
    P1(["1.0 Goal Setting & Alignment"]):::process
    P2(["2.0 Self & Peer Appraisal"]):::process
    P3(["3.0 Manager Evaluation & Scoring"]):::process
    P4(["4.0 Merit Calibration"]):::process
    P5(["5.0 Rewards & Action Planning"]):::process

    %% Data Stores
    D1[("D1: Employee Roster")]:::datastore
    D2[("D2: Annual Goal Catalog")]:::datastore
    D3[("D3: Review Scores Store")]:::datastore
    D4[("D4: Calibration Matrix")]:::datastore
    D5[("D5: Rewards & PIP Records")]:::datastore

    %% Data Flows
    E1 -->|Quarterly Goals & Milestones| P1
    P1 -->|Save Objectives| D2
    E1 -->|Self-Assessment Ratings| P2
    P2 -->|Store Peer Feedback| D3
    E2 -->|Manager Evaluation Scores| P3
    P3 -->|Consolidated Appraisal| D3
    E3 -->|Bell-Curve Parameters| P4
    P4 -->|Final Scaled Rating| D4
    P4 -->|Bonus & Increment Proposal| P5
    P5 -->|Reward Disbursal & Letters| E1
'@
Set-Content -Path (Join-Path $seDir "performance_dfd.mmd") -Value $code_dfd -Encoding utf8

Write-Host "  -> Saving Activity Diagram (performance_activity.mmd)..." -ForegroundColor White
$code_activity = @'
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff'}}}%%
flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef decision fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef sync fill:#000000,stroke:#000000,stroke-width:1px,color:#ffffff;
    classDef circle fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    StartNode((Start)):::circle
    EndNode((End)):::circle

    subgraph SWIM_Employee ["Employee Swimlane"]
        ACT_1["Draft Key Result Areas (KRAs)"]
        ACT_2["Complete Self-Rating"]
        ACT_3["Attend Appraisal One-on-One"]
    end

    subgraph SWIM_Manager ["Manager Swimlane"]
        ACT_4["Approve KRAs"]
        ACT_5["Rate Performance & Review Evidence"]
        ACT_6["Recommend Band / Hike"]
    end

    subgraph SWIM_HRAdmin ["HRAdmin Swimlane"]
        ACT_7["Initiate Appraisal Cycle"]
        ACT_8["Run Normalization & Bell-Curve"]
        ACT_9["Publish Increment Letters"]
    end

    DEC_1{"Score >= 85%?"}:::decision

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
Set-Content -Path (Join-Path $seDir "performance_activity.mmd") -Value $code_activity -Encoding utf8

try {
    Set-Clipboard -Value $code_usecase
    Write-Host "`n[OK] Use Case Diagram copied to clipboard! (Ctrl + V to paste)" -ForegroundColor White
} catch {}

Write-Host "`n[OK] All 4 diagrams for Performance Management System successfully saved into SE\ directory!" -ForegroundColor White
Write-Host "[*] Created: performance_usecase.mmd, performance_class.mmd, performance_dfd.mmd, performance_activity.mmd" -ForegroundColor Gray
