# LabX SE Remote: School Management System - Class Diagram
$title = "Class Diagram"
$topic = "School Management System"
$filename = "school_class.mmd"

$mermaidCode = @'
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
