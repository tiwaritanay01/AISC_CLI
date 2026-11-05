# LabX SE Remote: Library Management System - Class Diagram
$title = "Class Diagram"
$topic = "Library Management System"
$filename = "library_class.mmd"

$mermaidCode = @'
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
