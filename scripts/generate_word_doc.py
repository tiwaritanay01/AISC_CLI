"""Script to generate a Word Document (.docx) summarizing the ES & RTOS submissions."""

import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets the background color of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding in twips."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = Document()

    # Set page margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles & Fonts
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(45, 55, 72)

    # Document Header / Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("Embedded Systems & Real-Time Operating Systems (ES & RTOS)")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(26, 54, 93) # Navy

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Laboratory Submissions: Technical Summary & Architectural Analysis")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(14)
    run_sub.font.color.rgb = RGBColor(43, 108, 176) # Slate Blue

    # Metadata Box (Table with left accent border)
    meta_table = doc.add_table(rows=1, cols=1)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_cell = meta_table.cell(0, 0)
    meta_cell.width = Inches(6.5)
    set_cell_background(meta_cell, "F0F4F8")
    set_cell_margins(meta_cell, top=140, bottom=140, left=180, right=180)

    # Add left accent border to meta box
    tcPr = meta_cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="2B6CB0"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)

    meta_p = meta_cell.paragraphs[0]
    meta_p.paragraph_format.space_after = Pt(2)
    r = meta_p.add_run("STUDENT & CURRICULUM PROFILE\n")
    r.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(43, 108, 176)

    meta_lines = [
        ("Student Reference", "Tanay Tiwari (VU1F2425005)"),
        ("Academic Batch", "Division A, Batch A"),
        ("Source Package", "ES_RTOS_DIV_A_BATCH_A_Submissions.zip (10 Experiments)"),
        ("Target Microcontrollers", "NXP LPC2148 (ARM7TDMI-S) & ATmega328P (Arduino UNO)"),
        ("Development Environments", "Keil µVision, Flash Magic ISP, Proteus VSM, Arduino IDE with FreeRTOS Kernel")
    ]
    for label, val in meta_lines:
        mp = meta_cell.add_paragraph()
        mp.paragraph_format.space_before = Pt(1)
        mp.paragraph_format.space_after = Pt(1)
        lbl_r = mp.add_run(f"• {label}: ")
        lbl_r.bold = True
        lbl_r.font.size = Pt(10)
        lbl_r.font.color.rgb = RGBColor(26, 54, 93)
        val_r = mp.add_run(val)
        val_r.font.size = Pt(10)
        val_r.font.color.rgb = RGBColor(74, 85, 104)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 1: Executive Overview
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    hr1 = h1.add_run("1. Executive Curriculum Overview")
    hr1.bold = True
    hr1.font.size = Pt(15)
    hr1.font.color.rgb = RGBColor(26, 54, 93)

    p_intro = doc.add_paragraph(
        "The laboratory curriculum encapsulated within ES_RTOS_DIV_A_BATCH_A_Submissions.zip represents an end-to-end "
        "practical study of modern embedded firmware design, bridging bare-metal hardware control and real-time operating system "
        "multitasking. The 10 experiments are structured into two fundamental engineering paradigms:"
    )
    p_intro.paragraph_format.space_after = Pt(6)

    p_part1 = doc.add_paragraph()
    p_part1.paragraph_format.space_after = Pt(4)
    r = p_part1.add_run("Part I: Bare-Metal Firmware Engineering on ARM7 (NXP LPC2148)\n")
    r.bold = True
    r.font.color.rgb = RGBColor(43, 108, 176)
    p_part1.add_run(
        "Direct register-level memory-mapped I/O manipulation without an underlying operating system. Covers clock tree configuration, "
        "GPIO pin direction and atomic state latches (PINSEL, IO0DIR, IO0SET, IO0CLR), HD44780 LCD driver protocol, asynchronous serial "
        "framing (UART0 divisor latches), low-power state transitions (PCON Idle mode with Vectored Interrupt Controller wake-up), "
        "and deterministic finite state machines (Traffic Light Controller)."
    )

    p_part2 = doc.add_paragraph()
    p_part2.paragraph_format.space_after = Pt(12)
    r = p_part2.add_run("Part II: Preemptive Real-Time Operating Systems (FreeRTOS on ATmega328P)\n")
    r.bold = True
    r.font.color.rgb = RGBColor(5, 150, 105) # Green
    p_part2.add_run(
        "Real-time kernel porting, task state machines, and multitasking. Binds hardware tick timers to the FreeRTOS scheduler, "
        "replaces single-threaded superloops with independent prioritized task stacks, and implements race-free inter-process "
        "communication (IPC) using Binary Semaphores (event signaling), Counting Semaphores (resource tokens), Mutexes (shared serial bus protection), "
        "and thread-safe FIFO Message Queues."
    )

    # Section 2: Detailed Breakdown of All 10 Experiments
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    hr2 = h2.add_run("2. Detailed Experiment-by-Experiment Analysis")
    hr2.bold = True
    hr2.font.size = Pt(15)
    hr2.font.color.rgb = RGBColor(26, 54, 93)

    experiments = [
        {
            "num": "Experiment 01",
            "title": "Installation and Verification of Keil µVision & Flash Magic Toolchains",
            "platform": "NXP LPC2148 (ARM7TDMI-S) • Keil µVision • Flash Magic ISP",
            "aim": "Installation of Keil µVision IDE and Flash Magic ISP utility, setting up ARM project targets, and verifying firmware compilation and flashing workflows.",
            "concepts": [
                ("Toolchain Workflow", "Configures Keil µVision for the ARM7TDMI-S core, setting on-chip RAM/ROM boundaries (IRAM1: 0x40000000, IROM1: 0x00000000) and enabling automatic Intel HEX binary generation upon compilation."),
                ("Startup Architecture", "Links Startup.s assembly bootstrap to initialize exception vector tables, stack pointers for different CPU modes (SVC, IRQ, FIQ, User), and Phase Locked Loop (PLL0) multipliers."),
                ("ISP Bootloader Flashing", "Uses Flash Magic over USB-to-UART bridging. Controls DTR and RTS hardware handshaking lines to automatically reset the microcontroller and force the on-chip bootloader into ISP mode for burning hex files.")
            ]
        },
        {
            "num": "Experiment 02",
            "title": "Interfacing of LED with LPC2148 Microcontroller",
            "platform": "NXP LPC2148 (ARM7TDMI-S) • Embedded C",
            "aim": "Interfacing an array of LEDs to LPC2148 GPIO Port 0 pins and programming blinking patterns and binary ripple counters.",
            "concepts": [
                ("Pin Function Multiplexing", "Configures PINSEL0 bits [31:20] as '00' to assign pins P0.10 through P0.17 to general-purpose input/output (GPIO) mode."),
                ("Direction Control", "Sets corresponding bits in IO0DIR (IO0DIR |= 0x000FF000) to establish digital output drive capability."),
                ("Atomic Set & Clear", "Utilizes IO0SET to write logic HIGH and IO0CLR to write logic LOW. This atomic hardware operation avoids read-modify-write hazards on concurrent pin ports."),
                ("Working Logic", "A calibrated software delay loop provides human-visible persistence of vision while the microcontroller cycles through synchronous blinking and an 8-bit binary counter (0 to 255).")
            ]
        },
        {
            "num": "Experiment 03",
            "title": "Interfacing 16x2 Alphanumeric LCD with LPC2148",
            "platform": "NXP LPC2148 (ARM7TDMI-S) • Embedded C",
            "aim": "Interfacing a 16x2 HD44780-compatible alphanumeric LCD display to LPC2148 in 8-bit mode and rendering formatted text strings.",
            "concepts": [
                ("Bus Connections", "Data lines D0-D7 connected to P0.0-P0.7. Control lines Register Select (RS) on P0.8, Read/Write (RW) on P0.9 (tied LOW for write), and Enable (EN) on P0.10."),
                ("Control Strobe Protocol", "Commands (RS=0) and Data (RS=1) are placed onto Port 0, followed by a HIGH-to-LOW falling-edge pulse on EN with setup/hold timing to latch bytes into the HD44780 registers."),
                ("Initialization Commands", "Executes 0x38 (8-bit bus, 2 display lines, 5x7 font), 0x0C (Display ON, cursor OFF), 0x06 (auto-increment DDRAM address without display shift), and 0x01 (Clear display memory)."),
                ("Memory Addressing", "Transmits custom alphanumeric character strings to Line 1 (DDRAM base 0x80) and Line 2 (DDRAM base 0xC0).")
            ]
        },
        {
            "num": "Experiment 04",
            "title": "Serial Communication Using UART0 on LPC2148",
            "platform": "NXP LPC2148 (ARM7TDMI-S) • Embedded C",
            "aim": "Configuring UART0 on LPC2148 for full-duplex asynchronous serial communication at 9600 baud rate with 8-N-1 framing.",
            "concepts": [
                ("Peripheral Pin Routing", "Writes 0x05 to PINSEL0 bits [3:0] to map internal UART0 peripheral signals to P0.0 (TXD0) and P0.1 (RXD0)."),
                ("Baud Rate Divisor Calculation", "Formula: Divisor = PCLK / (16 * BaudRate). With PCLK = 15 MHz and Baud = 9600, Divisor = 15,000,000 / (16 * 9600) = 97.65. Sets U0DLM = 0, U0DLL = 97 while DLAB=1 in U0LCR."),
                ("Framing & Line Control", "Clears DLAB bit and sets U0LCR = 0x03 to lock baud divisors and configure standard 8 data bits, 1 stop bit, no parity framing."),
                ("Register Polling", "Transmissions poll Transmit Holding Register Empty (THRE, bit 5 of U0LSR) before writing to U0THR. Receptions poll Receiver Data Ready (RDR, bit 0 of U0LSR) before reading from U0RBR.")
            ]
        },
        {
            "num": "Experiment 05",
            "title": "Power Management & Low-Power Modes in LPC2148",
            "platform": "NXP LPC2148 (ARM7TDMI-S) • Embedded C",
            "aim": "Implementing power reduction techniques in LPC2148 by configuring CPU Idle mode and waking the core via external interrupts.",
            "concepts": [
                ("Power Modes (PCON)", "Writing 0x01 to the Power Control (PCON) register places the ARM7 core into Idle Mode. The CPU clock halts to eliminate dynamic switching losses, while peripheral clocks remain energized."),
                ("External Interrupt (EINT0)", "Configures P0.16 as External Interrupt 0 in PINSEL1. Configures EXTMODE and EXTPOLAR for falling-edge trigger sensitivity."),
                ("Vectored Interrupt Controller", "Programs VICVectAddr0 with eint0_isr address and unmasks interrupt slot 14 in VICIntEnable."),
                ("Wake-Up Flow", "Upon button press on P0.16, the VIC resumes core clocking, executes the ISR, clears the EXTINT flag, sets wakeup_flag, toggles the status LED, and re-enters sleep.")
            ]
        },
        {
            "num": "Experiment 06",
            "title": "Task Synchronization Using Binary & Counting Semaphores in FreeRTOS",
            "platform": "Arduino UNO (ATmega328P) • FreeRTOS (C++)",
            "aim": "Demonstrating task synchronization and shared resource access control using Binary and Counting Semaphores under FreeRTOS.",
            "concepts": [
                ("Binary Semaphore Signaling", "Created via xSemaphoreCreateBinary(). Used as a synchronization event flag between a Producer task and a Consumer task. The consumer blocks via xSemaphoreTake(sem, portMAX_DELAY) without CPU busy-waiting until the producer issues xSemaphoreGive()."),
                ("Counting Semaphore Resource Pooling", "Created via xSemaphoreCreateCounting(3, 0). Tracks 3 available shared resource tokens. Worker tasks take tokens to perform bounded work; once tokens reach 0, requesting tasks block until tokens are returned."),
                ("RTOS Efficiency", "Eliminates CPU polling loops, maximizing power efficiency and real-time response by shifting idle tasks to the Blocked state.")
            ]
        },
        {
            "num": "Experiment 07",
            "title": "Porting FreeRTOS to Arduino Development Board & Task Scheduling",
            "platform": "Arduino UNO (ATmega328P) • FreeRTOS (C++)",
            "aim": "Porting the FreeRTOS real-time kernel to an 8-bit AVR microcontroller and implementing concurrent scheduled tasks.",
            "concepts": [
                ("Kernel Porting & System Tick", "Binds the FreeRTOS timer tick interrupt to AVR Timer 1, generating a periodic 1 ms tick. This tick drives the FreeRTOS preemptive scheduler."),
                ("Task Creation (xTaskCreate)", "Allocates private stack memory (128 bytes) and task control blocks (TCBs) for TaskBlink1 (fast blink, 250 ms period) and TaskBlink2 (slow heartbeat, 1000 ms period)."),
                ("Cooperative Delay (vTaskDelay)", "Tasks yield control using vTaskDelay(pdMS_TO_TICKS(ms)), placing the task into the Blocked list and allowing the kernel to switch context to other Ready tasks without starvation.")
            ]
        },
        {
            "num": "Experiment 08",
            "title": "Creating Multiple Tasks with Priority Preemption in FreeRTOS",
            "platform": "Arduino UNO (ATmega328P) • FreeRTOS (C++)",
            "aim": "Creating multiple concurrent tasks with distinct priority levels to observe priority preemption and task state transitions.",
            "concepts": [
                ("Priority Tiers", "Instantiates three tasks: TaskHighPriority (Priority 3, urgent alarm monitor), TaskMediumPriority (Priority 2, periodic sensor sampling), and TaskLowPriority (Priority 1, background heartbeat)."),
                ("Preemptive Context Switching", "The FreeRTOS scheduler guarantees that the highest-priority Ready task always holds the CPU. Whenever the Priority 3 task unblocks, the scheduler suspends the running lower-priority task, saving its registers on its private stack."),
                ("Task State Transitions", "Illustrates deterministic transitions between Running, Ready, Blocked (waiting on timer), and Suspended states.")
            ]
        },
        {
            "num": "Experiment 09",
            "title": "Multitasking Real-Time IPC (Message Queue, Event Group & Mutex)",
            "platform": "Arduino UNO (ATmega328P) • FreeRTOS (C++)",
            "aim": "Developing a real-time application demonstrating Inter-Process Communication using FreeRTOS Message Queues, Mutexes, and Event Groups.",
            "concepts": [
                ("FIFO Message Queue", "xQueueCreate(5, sizeof(SensorPacket)) allocates a thread-safe FIFO buffer. Producer task copies telemetry structs into the queue (xQueueSend); Consumer task unblocks when packets arrive (xQueueReceive), preventing race conditions."),
                ("Mutex Semaphore Bus Guard", "xSemaphoreCreateMutex() guards the shared UART Serial port. Prevents concurrent tasks from corrupting or interleaving print statements by enforcing mutually exclusive serial bus access."),
                ("Event Groups", "Coordinates multi-task synchronization milestones using bitwise flags (xEventGroupSetBits, xEventGroupWaitBits).")
            ]
        },
        {
            "num": "Experiment 10",
            "title": "Design & Implementation of Real-Time Traffic Light Controller on LPC2148",
            "platform": "NXP LPC2148 (ARM7TDMI-S) • Embedded C",
            "aim": "Design and implementation of a real-time traffic light junction controller finite state machine (FSM) on LPC2148 GPIOs.",
            "concepts": [
                ("Hardware Actuators", "Red LED on P0.10, Yellow LED on P0.11, Green LED on P0.12 configured as digital outputs via PINSEL0 and IO0DIR."),
                ("Deterministic State Machine", "Executes cyclic traffic sequence: RED (Stop: 500 units) -> GREEN (Go: 500 units) -> YELLOW (Caution: 200 units) -> RED."),
                ("Atomic Bitmask Safety", "Enforces single-light activation using IO0CLR = ALL_LEDS followed by IO0SET = signal, preventing conflicting simultaneous signals (e.g. Green and Red at the same time).")
            ]
        }
    ]

    for exp in experiments:
        # Experiment Heading
        eh = doc.add_paragraph()
        eh.paragraph_format.space_before = Pt(12)
        eh.paragraph_format.space_after = Pt(2)
        r_num = eh.add_run(f"[{exp['num']}] ")
        r_num.bold = True
        r_num.font.size = Pt(12)
        r_num.font.color.rgb = RGBColor(43, 108, 176)

        r_title = eh.add_run(exp['title'])
        r_title.bold = True
        r_title.font.size = Pt(12)
        r_title.font.color.rgb = RGBColor(26, 54, 93)

        # Platform badge line
        ep = doc.add_paragraph()
        ep.paragraph_format.space_after = Pt(4)
        rp = ep.add_run(f"Target Architecture: {exp['platform']}")
        rp.font.size = Pt(9.5)
        rp.font.italic = True
        rp.font.color.rgb = RGBColor(113, 128, 150)

        # Aim
        p_aim = doc.add_paragraph()
        p_aim.paragraph_format.space_after = Pt(4)
        ra_lbl = p_aim.add_run("Aim / Objective: ")
        ra_lbl.bold = True
        ra_lbl.font.size = Pt(10.5)
        ra_val = p_aim.add_run(exp['aim'])
        ra_val.font.size = Pt(10.5)

        # Concepts bullets
        for clabel, cdesc in exp['concepts']:
            cp = doc.add_paragraph(style='List Bullet')
            cp.paragraph_format.space_before = Pt(1)
            cp.paragraph_format.space_after = Pt(2)
            c_lbl = cp.add_run(f"{clabel}: ")
            c_lbl.bold = True
            c_lbl.font.size = Pt(10)
            c_lbl.font.color.rgb = RGBColor(45, 55, 72)
            c_desc = cp.add_run(cdesc)
            c_desc.font.size = Pt(10)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Section 3: Summary Matrix Table
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)
    hr3 = h3.add_run("3. Curriculum Summary Matrix")
    hr3.bold = True
    hr3.font.size = Pt(15)
    hr3.font.color.rgb = RGBColor(26, 54, 93)

    table_data = [
        ("Exp #", "Experiment Title", "Target Platform", "Language", "Key Technical Concept"),
        ("01", "Keil & Flash Magic Setup", "LPC2148 ARM7", "C / Assembly", "Toolchains, Hex generation, ISP handshaking"),
        ("02", "LED Interfacing & Patterns", "LPC2148 ARM7", "Embedded C", "GPIO registers (PINSEL0, IO0DIR, IO0SET, IO0CLR)"),
        ("03", "16x2 Alphanumeric LCD", "LPC2148 ARM7", "Embedded C", "HD44780 8-bit bus, command/data latching, DDRAM"),
        ("04", "UART0 Serial Communication", "LPC2148 ARM7", "Embedded C", "Baud rate divisor, 9600-8-N-1, THRE/RDR polling"),
        ("05", "Power Management Modes", "LPC2148 ARM7", "Embedded C", "PCON Idle mode, VIC, External Interrupt (EINT0)"),
        ("06", "Semaphores & Task Sync", "ATmega328P / UNO", "FreeRTOS (C++)", "Binary Semaphore (signaling), Counting Semaphore (pool)"),
        ("07", "FreeRTOS Kernel Porting", "ATmega328P / UNO", "FreeRTOS (C++)", "AVR Timer 1 tick, task creation, cooperative vTaskDelay"),
        ("08", "Multi-Tasking & Preemption", "ATmega328P / UNO", "FreeRTOS (C++)", "Priority tiers (1, 2, 3), preemptive context switching"),
        ("09", "Inter-Process Communication", "ATmega328P / UNO", "FreeRTOS (C++)", "FIFO Message Queues, Mutex Serial guard, Event Groups"),
        ("10", "Real-Time Traffic Light FSM", "LPC2148 ARM7", "Embedded C", "Finite State Machine, atomic bitmask clearance, safety")
    ]

    matrix_table = doc.add_table(rows=len(table_data), cols=5)
    matrix_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    matrix_table.autofit = False

    col_widths = [Inches(0.6), Inches(1.8), Inches(1.2), Inches(1.1), Inches(1.8)]

    for row_idx, row in enumerate(matrix_table.rows):
        is_header = (row_idx == 0)
        # Repeat header row on multiple pages
        if is_header:
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths[col_idx]
            text = table_data[row_idx][col_idx]
            cell.paragraphs[0].text = text
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)

            run = p.runs[0]
            if is_header:
                run.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_background(cell, "1A365D") # Navy
            else:
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(45, 55, 72)
                bg_color = "F7FAFC" if (row_idx % 2 == 1) else "FFFFFF"
                set_cell_background(cell, bg_color)

            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

            # Cell borders
            c_tcPr = cell._tc.get_or_add_tcPr()
            bdr = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/></w:tcBorders>')
            c_tcPr.append(bdr)

    # Save destinations
    out_workspace = Path(r"c:\dev\CLI_AISC\ES_RTOS_Submissions_Summary.docx")
    out_brain = Path(r"C:\Users\tiwar\.gemini\antigravity\brain\79357858-e1a8-4a71-8f92-585dec25b7a7\ES_RTOS_Submissions_Summary.docx")
    out_downloads = Path(r"C:\Users\tiwar\Downloads\ES_RTOS_Submissions_Summary.docx")

    for dest in [out_workspace, out_brain, out_downloads]:
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            doc.save(str(dest))
            print(f"Saved Word document to: {dest}")
        except Exception as e:
            print(f"Could not save to {dest}: {e}")

if __name__ == "__main__":
    create_document()

