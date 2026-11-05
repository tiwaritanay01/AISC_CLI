param([string]$Subject = "", [string]$Item = "")

$cat = Invoke-RestMethod "https://nirpin.vercel.app/catalog.json"

function Show-Header {
    param([string]$Title)
    Write-Host "`n==========================================================================" -ForegroundColor White
    Write-Host "  $Title" -ForegroundColor White
    Write-Host "==========================================================================" -ForegroundColor Gray
}

while ($true) {
    if (-not $Subject) {
        Write-Host "`n==========================================================================" -ForegroundColor White
        Write-Host "                   LABX - INTERACTIVE EXPERIMENT DIRECTORY                " -ForegroundColor White
        Write-Host "==========================================================================" -ForegroundColor Gray
        Write-Host "  [1] aisc    - Artificial Intelligence & Soft Computing (12 Practicals)" -ForegroundColor White
        Write-Host "  [2] ertos   - Embedded Systems & Real-Time Operating Systems (10 Exp)" -ForegroundColor White
        Write-Host "  [3] cn      - Computer Networks (7 Experiments & Configurations)" -ForegroundColor White
        Write-Host "  [4] se      - Software Engineering (25 UML & DFD Case Studies)" -ForegroundColor White
        Write-Host "  [5] all     - Display Overview of All Subjects" -ForegroundColor White
        Write-Host "  [q] quit    - Exit" -ForegroundColor DarkGray
        Write-Host "==========================================================================" -ForegroundColor Gray
        $Subject = Read-Host "Select Subject [1-5 or aisc/ertos/cn/se/all, 'q' to quit]"
    }

    if (-not $Subject -or $Subject -eq "q" -or $Subject -eq "quit") {
        break
    }

    $cleanSub = $Subject.ToLower().Trim()
    switch ($cleanSub) {
        "1" { $cleanSub = "aisc" }
        "2" { $cleanSub = "ertos" }
        "3" { $cleanSub = "cn" }
        "4" { $cleanSub = "se" }
        "5" { $cleanSub = "all" }
        "es" { $cleanSub = "ertos" }
        "rtos" { $cleanSub = "ertos" }
    }

    if ($cleanSub -eq "aisc") {
        Show-Header "AISC Laboratory Practicals (Artificial Intelligence & Soft Computing)"
        Write-Host "  [01]  Case Study on AI Agents & PEAS Properties" -ForegroundColor White
        Write-Host "  [02]  Informed Search - A* Algorithm for 15-Puzzle Problem" -ForegroundColor White
        Write-Host "  [03]  Uninformed Search - Depth First Iterative Deepening (DFID)" -ForegroundColor White
        Write-Host "  [04]  Implementation of Alpha-Beta Pruning Algorithm" -ForegroundColor White
        Write-Host "  [05]  Single Layer Perceptron (SLP) for Binary Classification" -ForegroundColor White
        Write-Host "  [06]  Supervised Learning using Multi-Layer Perceptron (MLP)" -ForegroundColor White
        Write-Host "  [07]  Unsupervised Learning using K-Means Clustering" -ForegroundColor White
        Write-Host "  [08]  Associative Memory Network (Hopfield Network)" -ForegroundColor White
        Write-Host "  [09]  Implementation of Fuzzy Membership Functions" -ForegroundColor White
        Write-Host "  [10]  Fuzzy Control System Simulation (Fan Speed Controller)" -ForegroundColor White
        Write-Host "  [11]  Optimization using Genetic Algorithm & Simulated Annealing" -ForegroundColor White
        Write-Host "  [12]  AI Agent for Automation using n8n Workflow Architecture" -ForegroundColor White
        Write-Host "  [all] Pull ALL 12 AISC Practicals into current directory" -ForegroundColor Gray
        Write-Host "==========================================================================" -ForegroundColor Gray
        
        $pick = if ($Item) { $Item } else { Read-Host "Enter practical to pull [1-12, 'all', or 'b' for back]" }
        if ($pick -and $pick -ne "b" -and $pick -ne "back") {
            if ($pick -eq "all") {
                irm https://nirpin.vercel.app/aisc.ps1 | iex
            } else {
                $num = [int]$pick
                if ($num -ge 1 -and $num -le 12) {
                    $url = "https://nirpin.vercel.app/a$num.ps1"
                    Invoke-Expression (Invoke-RestMethod $url)
                }
            }
        }
    }
    elseif ($cleanSub -eq "ertos") {
        Show-Header "ES & RTOS Laboratory Experiments (Embedded Systems & FreeRTOS)"
        Write-Host "  [01]  Installation of Keil uVision & Flash Magic Verification" -ForegroundColor White
        Write-Host "  [02]  Interfacing of LED with Embedded Core (LPC 2148)" -ForegroundColor White
        Write-Host "  [03]  Interfacing of LCD with Embedded Core (LPC 2148)" -ForegroundColor White
        Write-Host "  [04]  Serial Communication (UART0/1 between Controller & Devices)" -ForegroundColor White
        Write-Host "  [05]  Power Management Techniques & Power-Saving Modes (LPC2148)" -ForegroundColor White
        Write-Host "  [06]  Binary Semaphore & Counting Semaphore for Task Synchronization" -ForegroundColor White
        Write-Host "  [07]  FreeRTOS Porting to Arduino / STM32 Development Board" -ForegroundColor White
        Write-Host "  [08]  Multitasking Capabilities using FreeRTOS on Arduino Uno" -ForegroundColor White
        Write-Host "  [09]  Multitasking Real-Time IPC (Message Queue, Event Groups)" -ForegroundColor White
        Write-Host "  [10]  Real-Time Traffic Light Control System Implementation" -ForegroundColor White
        Write-Host "  [all] Pull ALL 10 ERTOS Experiments (Code + Hardware Output Photos & PDFs)" -ForegroundColor Gray
        Write-Host "==========================================================================" -ForegroundColor Gray
        
        $pick = if ($Item) { $Item } else { Read-Host "Enter experiment to pull [1-10, 'all', or 'b' for back]" }
        if ($pick -and $pick -ne "b" -and $pick -ne "back") {
            if ($pick -eq "all") {
                irm https://nirpin.vercel.app/ertos.ps1 | iex
            } else {
                $num = [int]$pick
                if ($num -ge 1 -and $num -le 10) {
                    $url = "https://nirpin.vercel.app/e$num.ps1"
                    Invoke-Expression (Invoke-RestMethod $url)
                }
            }
        }
    }
    elseif ($cleanSub -eq "cn") {
        Show-Header "Computer Networks (CN) Laboratory Experiments & Setups"
        Write-Host "  [06]  CRC (Cyclic Redundancy Check Error Detection in C)" -ForegroundColor White
        Write-Host "  [07]  Hamming Code Error Detection & Single-Bit Correction in C" -ForegroundColor White
        Write-Host "  [08]  Checksum Error Detection (One's Complement 8-Bit Sum in C)" -ForegroundColor White
        Write-Host "  [09]  Client-Server Socket Programming in Java (TCPServer & TCPClient)" -ForegroundColor White
        Write-Host "  [10]  Dijkstra's Shortest Path Routing Algorithm (Link-State OSPF in C)" -ForegroundColor White
        Write-Host "  [11]  Static Routing Configuration in GNS3 (Router & Host Setup)" -ForegroundColor White
        Write-Host "  [12]  Dynamic Routing Configuration using RIP v2 in GNS3" -ForegroundColor White
        Write-Host "  [all] Pull Entire CN Suite into CN/ Directory" -ForegroundColor Gray
        Write-Host "==========================================================================" -ForegroundColor Gray
        
        $pick = if ($Item) { $Item } else { Read-Host "Enter experiment to pull [6-12, 'all', or 'b' for back]" }
        if ($pick -and $pick -ne "b" -and $pick -ne "back") {
            if ($pick -eq "all") {
                irm https://nirpin.vercel.app/cn.ps1 | iex
            } else {
                $cleanPick = $pick.ToLower().Replace("cn", "").Trim()
                $num = [int]$cleanPick
                if ($num -ge 6 -and $num -le 12) {
                    $url = "https://nirpin.vercel.app/cn$num.ps1"
                    Invoke-Expression (Invoke-RestMethod $url)
                }
            }
        }
    }
    elseif ($cleanSub -eq "se") {
        irm https://nirpin.vercel.app/se.ps1 | iex
    }
    else {
        Show-Header "All Laboratory Experiments Overview"
        $cat.experiments | Format-Table @{Label="Lab"; Expression={$_.subject}; Width=10}, @{Label="Exp #"; Expression={"#" + ("{0:D2}" -f $_.lab_serial)}; Width=8}, @{Label="Title"; Expression={$_.title}; Width=50}, @{Label="Language"; Expression={$_.language}}
    }

    if ($args.Count -gt 0 -or $Item) {
        break
    }
    $Subject = ""
    $Item = ""
}
