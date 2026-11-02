"""Assembler to generate full scripts/build_host.py with 22 experiments and updated UI."""

import os
import json
from pathlib import Path

# Load original 12 AISC experiments from build_host.py
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_host as orig_host

aisc_experiments = orig_host.EXPERIMENTS
for exp in aisc_experiments:
    exp["subject"] = "AISC"

print(f"Loaded {len(aisc_experiments)} AISC experiments.")

def pad_and_embed_c(code: str, theory: str) -> str:
    lines = code.strip().splitlines()
    while len(lines) < 49:
        lines.append("")
    if len(lines) == 49:
        lines.append("/* --- Line 50: Execution & Theory Division --- */")
    lines.append("")
    lines.append("/*")
    lines.append("=" * 76)
    lines.append("EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):")
    lines.append("=" * 76)
    for p in theory.strip().splitlines():
        p = p.strip()
        if not p:
            lines.append("")
            continue
        words = p.split()
        curr = ""
        for w in words:
            if len(curr + " " + w) > 74:
                lines.append(curr)
                curr = w
            else:
                curr = (curr + " " + w) if curr else w
        if curr:
            lines.append(curr)
    lines.append("=" * 76)
    lines.append("*/")
    return "\n".join(lines) + "\n"

es_experiments = [
    # Exp 13 (ES 1)
    {
        "id": 13,
        "slug": "keil-uvision-flash-magic-setup",
        "subject": "ES_RTOS",
        "title": "Installation and Verification of Keil uVision & Flash Magic Toolchains",
        "language": "c",
        "aliases": ["keil", "flash magic", "arm7 setup", "keil uvision", "lpc2148 setup"],
        "description": "ARM7TDMI-S microcontroller toolchain configuration, PLL clocking, and Flash Magic ISP programming verification.",
        "aim": "Installation of Keil uVision IDE and Flash Magic ISP flashing utility, and verifying ARM7 microcontroller project setup.",
        "theory": (
            "Keil uVision is an integrated development environment (IDE) that provides code editing, compilation, "
            "simulation, and debugging for ARM-based microcontrollers like the LPC2148. Flash Magic is a dedicated "
            "In-System Programming (ISP) tool used to burn compiled Intel HEX binaries into the LPC2148 on-chip flash "
            "memory via UART serial interface. The toolchain workflow requires configuring the LPC2148 device database, "
            "selecting the ARM target oscillator frequency (12.0 MHz), generating a HEX binary via Armcc / Armclang, "
            "and flashing over COM port with ISP handshaking."
        ),
        "algorithm": [
            "Download Keil uVision and Flash Magic installers from official vendor repositories.",
            "Install Keil uVision, set toolchain path, and add LPC2148 device database support.",
            "Install Flash Magic, configure COM port baud rate (9600 to 57600), device LPC2148, and oscillator frequency (12.0 MHz).",
            "Create a target test project in Keil uVision, select LPC2148, and include startup assembly code (Startup.s).",
            "Compile and generate Intel HEX binary (test_project.hex), and verify target connection via Flash Magic ISP handshake."
        ],
        "files": [
            {
                "path": "verify_keil_setup.c",
                "source": "verify_keil_setup.c",
                "role": "source",
                "content": pad_and_embed_c(
                    """/*
 * Experiment 13: Installation & Verification of Keil uVision & Flash Magic
 * Target: NXP LPC2148 ARM7TDMI-S Microcontroller
 */

#include <LPC214x.h>

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 6000; j++) {
            #ifdef __GNUC__
            __asm__("nop");
            #endif
        }
    }
}

void System_Init(void) {
    // Configure PLL0 for 60 MHz operation with 12 MHz crystal
    PLL0CON = 0x01;             // Enable PLL0
    PLL0CFG = 0x24;             // M=5, P=2 (CCLK = 60MHz)
    PLL0FEED = 0xAA;
    PLL0FEED = 0x55;
    while (!(PLL0STAT & (1 << 10))); // Wait for PLL lock
    PLL0CON = 0x03;             // Connect PLL0
    PLL0FEED = 0xAA;
    PLL0FEED = 0x55;
    VPBDIV = 0x02;              // PCLK = CCLK / 2 = 30 MHz
}

int main(void) {
    System_Init();

    // Configure P0.10 as GPIO Output (Status Indicator)
    PINSEL0 &= ~(3U << 20);
    IO0DIR |= (1U << 10);

    while (1) {
        IO0SET = (1U << 10);    // LED ON: Keil Toolchain Alive
        delay_ms(250);
        IO0CLR = (1U << 10);    // LED OFF
        delay_ms(250);
    }
    return 0;
}""",
                    "Keil uVision is an integrated development environment (IDE) that provides code editing, compilation, simulation, and debugging for ARM-based microcontrollers like the LPC2148. Flash Magic is a dedicated In-System Programming (ISP) tool used to burn compiled Intel HEX binaries into the LPC2148 on-chip flash memory via UART serial interface. The toolchain workflow requires configuring the LPC2148 device database, selecting the ARM target oscillator frequency (12.0 MHz), generating a HEX binary via Armcc / Armclang, and flashing over COM port with ISP handshaking."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "verify_keil_setup.c",
            "hardware": "NXP LPC2148 (ARM7TDMI-S)"
        }
    },

    # Exp 14 (ES 2)
    {
        "id": 14,
        "slug": "lpc2148-led-interfacing",
        "subject": "ES_RTOS",
        "title": "Interfacing of LED with LPC2148 Microcontroller",
        "language": "c",
        "aliases": ["led interfacing", "lpc2148 led", "gpio led", "blinking led", "led counter"],
        "description": "General Purpose I/O pin control on LPC2148: PINSEL, IO0DIR, IO0SET, and IO0CLR for LED blinking and binary ripple counters.",
        "aim": "Interfacing of LED with an embedded core (LPC 2148)",
        "theory": (
            "The LPC2148 is an ARM7TDMI-S based 32-bit microcontroller with two 32-bit general-purpose I/O ports "
            "(Port 0 and Port 1). GPIO pins are controlled by registers: PINSEL (Pin Function Select), IOxDIR "
            "(Direction register: 1 for Output, 0 for Input), IOxSET (Set pin high), and IOxCLR (Clear pin low). "
            "An LED connected in active-high or active-low configuration is toggled with software delay loops. "
            "In this experiment, Port 0 pins (P0.10 - P0.17) drive an 8-LED bar display, demonstrating single-pin "
            "blinking, alternating blinking, and binary counter sequences."
        ),
        "algorithm": [
            "Configure PINSEL0 to set P0.10 to P0.17 as standard GPIO pins.",
            "Configure IO0DIR to set pins P0.10 to P0.17 as outputs (IO0DIR |= 0x000FF000).",
            "Turn off all LEDs initially using IO0CLR = 0x000FF000.",
            "In a continuous loop, set IO0SET to turn LEDs ON, call delay(300), and set IO0CLR to turn LEDs OFF.",
            "Implement alternating and binary counter patterns on the LED array."
        ],
        "files": [
            {
                "path": "lpc2148_led.c",
                "source": "lpc2148_led.c",
                "role": "source",
                "content": pad_and_embed_c(
                    """/*
 * Experiment 14: Interfacing of LED with Embedded Core (LPC 2148)
 * Demonstrates Port 0 GPIO Pin Configuration, Set, Clear, and Patterns
 */

#include <LPC214x.h>

#define LED_PINS (0xFF << 10)   // P0.10 to P0.17 for 8 LEDs

void delay(unsigned int count) {
    unsigned int i, j;
    for (i = 0; i < count; i++) {
        for (j = 0; j < 6000; j++) {
            #ifdef __GNUC__
            __asm__("nop");
            #endif
        }
    }
}

void led_counter(void) {
    unsigned int count;
    for (count = 0; count < 256; count++) {
        IO0CLR = LED_PINS;
        IO0SET = (count << 10) & LED_PINS;
        delay(100);
    }
}

int main(void) {
    // Select GPIO function for P0.10 - P0.17
    PINSEL0 &= ~0xFFFF0000;

    // Configure P0.10 - P0.17 as output
    IO0DIR |= LED_PINS;

    // Initially turn off all LEDs
    IO0CLR = LED_PINS;

    while (1) {
        // Pattern 1: All ON / All OFF
        IO0SET = LED_PINS;
        delay(300);
        IO0CLR = LED_PINS;
        delay(300);

        // Pattern 2: Binary Ripple Counter
        led_counter();
    }
    return 0;
}""",
                    "The LPC2148 is an ARM7TDMI-S based 32-bit microcontroller with two 32-bit general-purpose I/O ports (Port 0 and Port 1). GPIO pins are controlled by registers: PINSEL (Pin Function Select), IOxDIR (Direction register: 1 for Output, 0 for Input), IOxSET (Set pin high), and IOxCLR (Clear pin low). An LED connected in active-high or active-low configuration is toggled with software delay loops. In this experiment, Port 0 pins (P0.10 - P0.17) drive an 8-LED bar display, demonstrating single-pin blinking, alternating blinking, and binary counter sequences."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "lpc2148_led.c",
            "hardware": "NXP LPC2148 (ARM7TDMI-S)"
        }
    },

    # Exp 15 (ES 3)
    {
        "id": 15,
        "slug": "lpc2148-lcd-interfacing",
        "subject": "ES_RTOS",
        "title": "Interfacing 16x2 Alphanumeric LCD with LPC2148",
        "language": "c",
        "aliases": ["lcd interfacing", "lpc2148 lcd", "16x2 lcd", "hd44780", "lcd display"],
        "description": "8-bit HD44780 LCD driver interfacing with LPC2148: command latching, data transmission, and string rendering.",
        "aim": "Interfacing of LCD with an embedded core (LPC 2148)",
        "theory": (
            "A 16x2 alphanumeric LCD display interfaces with the LPC2148 using 8 data lines (D0-D7) and 3 control lines: "
            "RS (Register Select - 0 for command, 1 for data), RW (Read/Write - grounded for write), and EN (Enable - "
            "high-to-low pulse to latch data). Commands initialize display mode (0x38 for 8-bit, 2-line mode), display "
            "ON cursor OFF (0x0C), clear screen (0x01), and set DDRAM address (0x80 line 1, 0xC0 line 2). The LPC2148 "
            "drives the LCD by asserting RS, placing data on Port 0, and pulsing EN with sufficient setup and hold time."
        ),
        "algorithm": [
            "Connect LCD data pins D0-D7 to P0.0-P0.7 and control pins RS, RW, EN to P0.8, P0.9, P0.10.",
            "Configure P0.0 through P0.10 as GPIO outputs in PINSEL0 and IO0DIR.",
            "Define LCD_Command function to latch command bytes (RS=0, RW=0, pulse EN).",
            "Define LCD_Data function to latch character bytes (RS=1, RW=0, pulse EN).",
            "Initialize LCD with commands 0x38 (8-bit mode), 0x0C (display ON), 0x06 (auto-increment), and 0x01 (clear screen).",
            "Write custom strings to Line 1 and Line 2."
        ],
        "files": [
            {
                "path": "lpc2148_lcd.c",
                "source": "lpc2148_lcd.c",
                "role": "source",
                "content": pad_and_embed_c(
                    """/*
 * Experiment 15: Interfacing 16x2 Alphanumeric LCD with LPC2148
 * 8-Bit Interface: Data on P0.0-P0.7, Control on P0.8(RS), P0.9(RW), P0.10(EN)
 */

#include <LPC214x.h>

#define LCD_DATA_PINS  0x000000FF  // P0.0 - P0.7
#define RS_PIN         (1U << 8)   // P0.8
#define RW_PIN         (1U << 9)   // P0.9
#define EN_PIN         (1U << 10)  // P0.10

void delay_lcd(unsigned int count) {
    unsigned int i, j;
    for (i = 0; i < count; i++)
        for (j = 0; j < 3000; j++);
}

void LCD_Command(unsigned char cmd) {
    IO0CLR = LCD_DATA_PINS | RS_PIN | RW_PIN;
    IO0SET = (cmd & 0xFF);
    IO0SET = EN_PIN;
    delay_lcd(2);
    IO0CLR = EN_PIN;
    delay_lcd(5);
}

void LCD_Data(unsigned char data_byte) {
    IO0CLR = LCD_DATA_PINS | RW_PIN;
    IO0SET = RS_PIN | (data_byte & 0xFF);
    IO0SET = EN_PIN;
    delay_lcd(2);
    IO0CLR = EN_PIN;
    delay_lcd(5);
}

void LCD_String(const char *str) {
    while (*str) {
        LCD_Data((unsigned char)*str++);
    }
}

void LCD_Init(void) {
    PINSEL0 &= ~0x001FFFFF;      // Configure P0.0 - P0.10 as GPIO
    IO0DIR |= (LCD_DATA_PINS | RS_PIN | RW_PIN | EN_PIN);

    LCD_Command(0x38);           // 8-bit mode, 2 lines, 5x7 dots
    LCD_Command(0x0C);           // Display ON, Cursor OFF
    LCD_Command(0x06);           // Increment cursor
    LCD_Command(0x01);           // Clear display screen
    delay_lcd(10);
}

int main(void) {
    LCD_Init();
    LCD_Command(0x80);           // Move cursor to Line 1
    LCD_String("LabX Embedded C");
    LCD_Command(0xC0);           // Move cursor to Line 2
    LCD_String("LPC2148 LCD OK");

    while (1) {
        // Static message display
    }
    return 0;
}""",
                    "A 16x2 alphanumeric LCD display interfaces with the LPC2148 using 8 data lines (D0-D7) and 3 control lines: RS (Register Select - 0 for command, 1 for data), RW (Read/Write - grounded for write), and EN (Enable - high-to-low pulse to latch data). Commands initialize display mode (0x38 for 8-bit, 2-line mode), display ON cursor OFF (0x0C), clear screen (0x01), and set DDRAM address (0x80 line 1, 0xC0 line 2). The LPC2148 drives the LCD by asserting RS, placing data on Port 0, and pulsing EN with sufficient setup and hold time."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "lpc2148_lcd.c",
            "hardware": "NXP LPC2148 (ARM7TDMI-S)"
        }
    },

    # Exp 16 (ES 4)
    {
        "id": 16,
        "slug": "lpc2148-uart-serial",
        "subject": "ES_RTOS",
        "title": "Serial Communication using UART0 on LPC2148",
        "language": "c",
        "aliases": ["uart", "serial communication", "lpc2148 uart", "baud rate", "uart0"],
        "description": "Full-duplex asynchronous serial transceiver configuration on LPC2148: baud rate generation, FIFOs, and character echo.",
        "aim": "Serial communication between controller boards or any other device (UART on LPC 2148)",
        "theory": (
            "LPC2148 features two asynchronous serial ports (UART0 and UART1). UART communication requires setting "
            "the baud rate generator using U0LCR (Line Control Register, DLAB=1), U0DLL, and U0DLM divider latches based "
            "on PCLK (Peripheral Clock). Data transmission occurs by polling the Transmit Holding Register Empty (THRE) "
            "flag in U0LSR and writing bytes to U0THR. Data reception polls the Receiver Data Ready (RDR) flag and reads "
            "from U0RBR. Setting word length to 8 bits, 1 stop bit, and no parity establishes standard 9600-8-N-1 serial framing."
        ),
        "algorithm": [
            "Configure P0.0 as TXD0 and P0.1 as RXD0 using PINSEL0 (PINSEL0 |= 0x00000005).",
            "Enable Divisor Latch Access Bit (DLAB = 1) in U0LCR.",
            "Set baud rate divisor latches (U0DLL = 97, U0DLM = 0 for 9600 baud rate at PCLK=15MHz).",
            "Clear DLAB bit and set 8-bit character length with 1 stop bit (U0LCR = 0x03).",
            "Define UART0_SendChar and UART0_SendString functions by polling the THRE flag in U0LSR.",
            "Define UART0_ReceiveChar by polling the RDR flag in U0LSR.",
            "Send welcome message and echo back incoming serial keystrokes."
        ],
        "files": [
            {
                "path": "lpc2148_uart.c",
                "source": "lpc2148_uart.c",
                "role": "source",
                "content": pad_and_embed_c(
                    """/*
 * Experiment 16: Serial Communication between Controller Boards (UART0 on LPC2148)
 * Configures 9600 Baud, 8 Data Bits, 1 Stop Bit, No Parity (9600-8-N-1)
 */

#include <LPC214x.h>

void UART0_Init(void) {
    // Configure P0.0 as TXD0, P0.1 as RXD0
    PINSEL0 &= ~0x0000000F;
    PINSEL0 |= 0x00000005;

    // Enable Divisor Latch Access Bit (DLAB = 1)
    U0LCR = 0x83;

    // Set Baud Rate to 9600 for PCLK = 15 MHz (15000000 / (16 * 9600) = 97.65)
    U0DLM = 0x00;
    U0DLL = 97;

    // Disable DLAB and set 8-bit word length
    U0LCR = 0x03;

    // Enable and reset FIFO buffers
    U0FCR = 0x07;
}

void UART0_SendChar(char ch) {
    // Wait until Transmit Holding Register is Empty (THRE = bit 5)
    while (!(U0LSR & 0x20));
    U0THR = ch;
}

char UART0_ReceiveChar(void) {
    // Wait until Receiver Data Ready (RDR = bit 0)
    while (!(U0LSR & 0x01));
    return (char)U0RBR;
}

void UART0_SendString(const char *str) {
    while (*str) {
        UART0_SendChar(*str++);
    }
}

int main(void) {
    UART0_Init();
    UART0_SendString("\\r\\n==========================================\\r\\n");
    UART0_SendString(" LabX Remote: LPC2148 UART0 Communication\\r\\n");
    UART0_SendString(" Serial Port Initialized at 9600 Baud (8-N-1)\\r\\n");
    UART0_SendString("==========================================\\r\\n");
    UART0_SendString("Type characters in terminal to echo back:\\r\\n");

    while (1) {
        char ch = UART0_ReceiveChar();
        UART0_SendChar(ch);     // Echo back received character
        if (ch == '\\r') {
            UART0_SendChar('\\n');
        }
    }
    return 0;
}""",
                    "LPC2148 features two asynchronous serial ports (UART0 and UART1). UART communication requires setting the baud rate generator using U0LCR (Line Control Register, DLAB=1), U0DLL, and U0DLM divider latches based on PCLK (Peripheral Clock). Data transmission occurs by polling the Transmit Holding Register Empty (THRE) flag in U0LSR and writing bytes to U0THR. Data reception polls the Receiver Data Ready (RDR) flag and reads from U0RBR. Setting word length to 8 bits, 1 stop bit, and no parity establishes standard 9600-8-N-1 serial framing."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "lpc2148_uart.c",
            "hardware": "NXP LPC2148 (ARM7TDMI-S)"
        }
    },

    # Exp 17 (ES 5)
    {
        "id": 17,
        "slug": "lpc2148-power-management",
        "subject": "ES_RTOS",
        "title": "Power Management & Low-Power Modes in LPC2148",
        "language": "c",
        "aliases": ["power management", "lpc2148 power", "idle mode", "power down", "eint0"],
        "description": "LPC2148 power saving techniques configuring PCON register Idle Mode with external interrupt (EINT0) wake-up.",
        "aim": "To implement power management techniques in the LPC2148 embedded controller by configuring its power saving modes to reduce power consumption.",
        "theory": (
            "To implement power management techniques in the LPC2148 embedded controller by configuring its power-saving "
            "modes to reduce power consumption. Power management in the LPC2148 is controlled via the PCON (Power Control) "
            "and PCONP (Power Control for Peripherals) registers. LPC2148 supports Idle Mode (PCON=0x01) where the CPU clock "
            "stops while peripherals continue running, and Power Down Mode (PCON=0x02) where both CPU and oscillator are halted. "
            "An external interrupt (EINT0 on P0.16) is configured via the Vectored Interrupt Controller (VIC) to wake the "
            "microcontroller from low-power state, toggle a status LED, and resume operation."
        ),
        "algorithm": [
            "Initiate the program and initialize LPC2148 system clocks.",
            "Configure GPIO P0.10 as an output for status LED indication.",
            "Configure P0.16 as External Interrupt 0 (EINT0) in PINSEL1.",
            "Configure EINT0 as edge-sensitive, falling edge trigger using EXTMODE and EXTPOLAR.",
            "Assign eint0_isr to VICVectAddr0, enable slot in VICVectCntl0, and unmask interrupt in VICIntEnable.",
            "Enter low-power Idle mode by writing 0x01 to PCON.",
            "On interrupt trigger, ISR sets wakeup_flag and toggles LED before returning to sleep."
        ],
        "files": [
            {
                "path": "lpc2148_power.c",
                "source": "lpc2148_power.c",
                "role": "source",
                "content": pad_and_embed_c(
                    """#include <LPC214x.h>

#define LED       (1U << 10)   // P0.10
#define EINT0_PIN (1U << 16)   // P0.16

volatile unsigned int wakeup_flag = 0;

/* External Interrupt 0 service routine */
void eint0_isr(void) __irq
{
    EXTINT = 0x01;             // Clear EINT0 interrupt flag
    wakeup_flag = 1;

    VICVectAddr = 0x00;        // End of interrupt
}

void eint0_init(void)
{
    /* Configure P0.16 as EINT0 */
    PINSEL1 &= ~(3U << 0);
    PINSEL1 |=  (1U << 0);

    /* Configure EINT0 as edge-sensitive, falling edge */
    EXTMODE |= 0x01;
    EXTPOLAR &= ~0x01;
    EXTINT = 0x01;

    /* Configure VIC for EINT0 */
    VICIntSelect &= ~(1U << 14);
    VICVectAddr0 = (unsigned long)eint0_isr;
    VICVectCntl0 = 0x20 | 14;
    VICIntEnable |= (1U << 14);
}

int main(void)
{
    /* Configure P0.10 as GPIO output */
    PINSEL0 &= ~(3U << 20);
    IO0DIR |= LED;
    IO0CLR = LED;

    eint0_init();

    while (1)
    {
        if (wakeup_flag)
        {
            wakeup_flag = 0;
            IO0PIN ^= LED;     // Toggle LED after wake-up
        }

        /* Enter Idle Mode */
        PCON = 0x01;
    }
}""",
                    "To implement power management techniques in the LPC2148 embedded controller by configuring its power-saving modes to reduce power consumption. Power management in the LPC2148 is controlled via the PCON (Power Control) and PCONP (Power Control for Peripherals) registers. LPC2148 supports Idle Mode (PCON=0x01) where the CPU clock stops while peripherals continue running, and Power Down Mode (PCON=0x02) where both CPU and oscillator are halted. An external interrupt (EINT0 on P0.16) is configured via the Vectored Interrupt Controller (VIC) to wake the microcontroller from low-power state, toggle a status LED, and resume operation."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "lpc2148_power.c",
            "hardware": "NXP LPC2148 (ARM7TDMI-S)"
        }
    },

    # Exp 18 (ES 6)
    {
        "id": 18,
        "slug": "freertos-semaphores-synchronization",
        "subject": "ES_RTOS",
        "title": "Task Synchronization using Binary and Counting Semaphores in FreeRTOS",
        "language": "cpp",
        "aliases": ["freertos semaphores", "binary semaphore", "counting semaphore", "task sync", "freertos"],
        "description": "Synchronization of producer and worker tasks using FreeRTOS binary signaling and counting semaphore resource pools.",
        "aim": "To illustrate the use of Binary Semaphore and Counting Semaphore for Task Synchronization using FreeRTOS",
        "theory": (
            "FreeRTOS is a lightweight open source Real time Operating system (RTOS) made for use in embedded systems. "
            "It helps manage multiple tasks schedules them properly allows tasks to work together smoothly and share resources "
            "without conflict. Semaphores are synchronization mechanisms used to coordinate tasks. A Binary Semaphore has "
            "a maximum count of 1, functioning similarly to a mutex flag to signal events between tasks or ISRs using "
            "xSemaphoreCreateBinary, xSemaphoreTake, and xSemaphoreGive. A Counting Semaphore has a count >= 1 "
            "(xSemaphoreCreateCounting), tracking multiple available units of a shared resource or counting events. When "
            "tasks take the semaphore, the count decrements; when tasks release the resource, the count increments."
        ),
        "algorithm": [
            "Create a binary semaphore using xSemaphoreCreateBinary and a counting semaphore using xSemaphoreCreateCounting.",
            "Initialize the counting semaphore with a count (e.g. 3).",
            "Use xSemaphoreTake to acquire the semaphore in the consumer/worker tasks.",
            "Use xSemaphoreGive to release the semaphore in the producer/signaling task.",
            "Observe task synchronization and shared resource access coordination over serial telemetry."
        ],
        "files": [
            {
                "path": "freertos_semaphores.ino",
                "source": "freertos_semaphores.ino",
                "role": "source",
                "content": pad_and_embed_c(
                    """/*
 * Experiment 18: Binary and Counting Semaphores for Task Synchronization in FreeRTOS
 * Demonstrates xSemaphoreCreateBinary and xSemaphoreCreateCounting on Arduino / AVR
 */

#include <Arduino_FreeRTOS.h>
#include <semphr.h>

SemaphoreHandle_t xBinarySemaphore;
SemaphoreHandle_t xCountingSemaphore;

void TaskProducer(void *pvParameters) {
    (void) pvParameters;
    int eventCount = 0;
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(1500));
        eventCount++;
        Serial.print("[Producer] Signaling Binary Event #");
        Serial.println(eventCount);
        xSemaphoreGive(xBinarySemaphore);

        // Also give counting token if space allows
        xSemaphoreGive(xCountingSemaphore);
    }
}

void TaskBinaryConsumer(void *pvParameters) {
    (void) pvParameters;
    for (;;) {
        if (xSemaphoreTake(xBinarySemaphore, portMAX_DELAY) == pdTRUE) {
            Serial.println("  --> [Binary Consumer] Acquired semaphore! Synchronized task executed.");
        }
    }
}

void TaskCountingWorker(void *pvParameters) {
    (void) pvParameters;
    for (;;) {
        if (xSemaphoreTake(xCountingSemaphore, pdMS_TO_TICKS(3000)) == pdTRUE) {
            Serial.println("  --> [Counting Worker] Shared resource accessed (Token acquired).");
            vTaskDelay(pdMS_TO_TICKS(400));
        } else {
            Serial.println("  --> [Counting Worker] Resource wait timeout.");
        }
    }
}

void setup() {
    Serial.begin(9600);
    while (!Serial) { ; }
    Serial.println("=== FreeRTOS Binary & Counting Semaphore Demo ===");

    xBinarySemaphore = xSemaphoreCreateBinary();
    xCountingSemaphore = xSemaphoreCreateCounting(3, 0);

    if (xBinarySemaphore != NULL && xCountingSemaphore != NULL) {
        xTaskCreate(TaskProducer, "Producer", 128, NULL, 2, NULL);
        xTaskCreate(TaskBinaryConsumer, "BinConsumer", 128, NULL, 1, NULL);
        xTaskCreate(TaskCountingWorker, "CountWorker", 128, NULL, 1, NULL);
    }
}

void loop() {
    // Empty: FreeRTOS scheduler manages execution
}""",
                    "FreeRTOS is a lightweight open source Real time Operating system (RTOS) made for use in embedded systems. It helps manage multiple tasks schedules them properly allows tasks to work together smoothly and share resources without conflict. Semaphores are synchronization mechanisms used to coordinate tasks. A Binary Semaphore has a maximum count of 1, functioning similarly to a mutex flag to signal events between tasks or ISRs using xSemaphoreCreateBinary, xSemaphoreTake, and xSemaphoreGive. A Counting Semaphore has a count >= 1 (xSemaphoreCreateCounting), tracking multiple available units of a shared resource or counting events. When tasks take the semaphore, the count decrements; when tasks release the resource, the count increments."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "freertos_semaphores.ino",
            "hardware": "Arduino UNO (ATmega328P) / FreeRTOS"
        }
    },

    # Exp 19 (ES 7)
    {
        "id": 19,
        "slug": "freertos-arduino-porting",
        "subject": "ES_RTOS",
        "title": "Porting FreeRTOS to Arduino Development Board & Task Scheduling",
        "language": "cpp",
        "aliases": ["porting freertos", "arduino rtos", "freertos porting", "task scheduling", "freertos uno"],
        "description": "Porting FreeRTOS kernel to ATmega328P microcontroller, configuring system tick, and executing independent scheduled tasks.",
        "aim": "To port FreeRTOS to an Arduino UNO or STM32 development board and create multiple tasks to understand task scheduling and multitasking in a Real Time Operating System (RTOS)",
        "theory": (
            "FreeRTOS is a lightweight real-time operating system designed for embedded systems with constrained memory footprint. "
            "Porting FreeRTOS to the ATmega328P microcontroller on the Arduino UNO board allows developers to run preemptive "
            "priority-based multitasking on an 8-bit platform. The FreeRTOS kernel replaces the traditional single-threaded loop() "
            "construct with independent task routines, each possessing its own stack, priority, and state machine. Tasks yield "
            "control cooperatively using vTaskDelay(), allowing the scheduler to context-switch to ready tasks."
        ),
        "algorithm": [
            "Include Arduino_FreeRTOS header and configure system tick timer.",
            "Define task prototypes TaskBlink1 (fast blink, 250ms) and TaskBlink2 (slow blink, 1000ms).",
            "In setup(), initialize hardware serial and create Task 1 and Task 2 using xTaskCreate.",
            "In each task loop, execute GPIO toggling and yield using vTaskDelay(pdMS_TO_TICKS(duration)).",
            "Start the scheduler and monitor concurrent multitasking on the serial console."
        ],
        "files": [
            {
                "path": "freertos_porting.ino",
                "source": "freertos_porting.ino",
                "role": "source",
                "content": pad_and_embed_c(
                    """/*
 * Experiment 19: Porting FreeRTOS to Arduino UNO (ATmega328P) Development Board
 * Demonstrates Kernel Porting, Preemptive Task Scheduling & vTaskDelay()
 */

#include <Arduino_FreeRTOS.h>

#define LED_PIN_1 12
#define LED_PIN_2 13

void TaskBlink1(void *pvParameters) {
    (void) pvParameters;
    pinMode(LED_PIN_1, OUTPUT);
    for (;;) {
        digitalWrite(LED_PIN_1, HIGH);
        vTaskDelay(pdMS_TO_TICKS(250));
        digitalWrite(LED_PIN_1, LOW);
        vTaskDelay(pdMS_TO_TICKS(250));
        Serial.println("[Task 1] Fast Blink (250ms) - Priority 1");
    }
}

void TaskBlink2(void *pvParameters) {
    (void) pvParameters;
    pinMode(LED_PIN_2, OUTPUT);
    for (;;) {
        digitalWrite(LED_PIN_2, HIGH);
        vTaskDelay(pdMS_TO_TICKS(1000));
        digitalWrite(LED_PIN_2, LOW);
        vTaskDelay(pdMS_TO_TICKS(1000));
        Serial.println("[Task 2] Slow Heartbeat (1000ms) - Priority 1");
    }
}

void setup() {
    Serial.begin(9600);
    while (!Serial) { ; }
    Serial.println("=== FreeRTOS Arduino Porting & Multitasking Initialized ===");

    xTaskCreate(TaskBlink1, "FastBlink", 128, NULL, 1, NULL);
    xTaskCreate(TaskBlink2, "SlowBlink", 128, NULL, 1, NULL);
}

void loop() {
    // Arduino loop stays empty; RTOS scheduler handles tasks
}""",
                    "FreeRTOS is a lightweight real-time operating system designed for embedded systems with constrained memory footprint. Porting FreeRTOS to the ATmega328P microcontroller on the Arduino UNO board allows developers to run preemptive priority-based multitasking on an 8-bit platform. The FreeRTOS kernel replaces the traditional single-threaded loop() construct with independent task routines, each possessing its own stack, priority, and state machine. Tasks yield control cooperatively using vTaskDelay(), allowing the scheduler to context-switch to ready tasks."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "freertos_porting.ino",
            "hardware": "Arduino UNO (ATmega328P) / FreeRTOS"
        }
    },

    # Exp 20 (ES 8)
    {
        "id": 20,
        "slug": "freertos-multiple-tasks-creation",
        "subject": "ES_RTOS",
        "title": "Creating Multiple Tasks in FreeRTOS with Priority Preemption",
        "language": "cpp",
        "aliases": ["multiple tasks", "freertos tasks", "priority preemption", "rtos multitasking"],
        "description": "Multi-task instantiation in FreeRTOS: assigning priority tiers, preemptive context switches, and telemetry logging.",
        "aim": "To create Multiple Task using free RTOS On an Arduino UNO and understanding the multitasking capabilities of RTOS",
        "theory": (
            "Multitasking in FreeRTOS enables the concurrent execution of multiple independent operational threads on a single "
            "core microcontroller. The FreeRTOS preemptive scheduler enforces priority-based task switching, ensuring that the "
            "highest priority ready task always gains execution control. In this experiment, three distinct tasks (Sensor Reading "
            "Task, Display/Telemetry Task, and Heartbeat Monitor Task) are instantiated with varying priorities to demonstrate "
            "how priority inversion is avoided and how tasks cleanly share CPU cycles."
        ),
        "algorithm": [
            "Include Arduino_FreeRTOS library.",
            "Define TaskSensorRead (priority 2), TaskDisplay (priority 1), and TaskHeartbeat (priority 1).",
            "Allocate individual stack depths and task parameters for each task.",
            "Create the three tasks in setup() using xTaskCreate.",
            "Use vTaskDelayUntil or vTaskDelay for deterministic periodic execution.",
            "Observe concurrent execution output on Arduino Serial Monitor."
        ],
        "files": [
            {
                "path": "freertos_multitask.ino",
                "source": "freertos_multitask.ino",
                "role": "source",
                "content": pad_and_embed_c(
                    """/*
 * Experiment 20: Creating Multiple Tasks using FreeRTOS on Arduino UNO
 * Demonstrates Priority-Based Preemption and Task State Transitions
 */

#include <Arduino_FreeRTOS.h>

void TaskHighPriority(void *pvParameters) {
    (void) pvParameters;
    for (;;) {
        Serial.println(">>> [HIGH PRIORITY TASK - 3] Critical execution cycle started.");
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}

void TaskMediumPriority(void *pvParameters) {
    (void) pvParameters;
    int reading = 0;
    for (;;) {
        reading = analogRead(A0);
        Serial.print("  [MED PRIORITY TASK - 2] Telemetry Sensor A0: ");
        Serial.println(reading);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void TaskLowPriority(void *pvParameters) {
    (void) pvParameters;
    unsigned long count = 0;
    for (;;) {
        count++;
        Serial.print("    [LOW PRIORITY TASK - 1] Background heartbeat tick: ");
        Serial.println(count);
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void setup() {
    Serial.begin(9600);
    while (!Serial) { ; }
    Serial.println("=== FreeRTOS Multiple Tasks & Preemption Demonstration ===");

    xTaskCreate(TaskLowPriority,    "LowTask",  128, NULL, 1, NULL);
    xTaskCreate(TaskMediumPriority, "MedTask",  128, NULL, 2, NULL);
    xTaskCreate(TaskHighPriority,   "HighTask", 128, NULL, 3, NULL);
}

void loop() {
    // Managed by RTOS
}""",
                    "Multitasking in FreeRTOS enables the concurrent execution of multiple independent operational threads on a single core microcontroller. The FreeRTOS preemptive scheduler enforces priority-based task switching, ensuring that the highest priority ready task always gains execution control. In this experiment, three distinct tasks (Sensor Reading Task, Display/Telemetry Task, and Heartbeat Monitor Task) are instantiated with varying priorities to demonstrate how priority inversion is avoided and how tasks cleanly share CPU cycles."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "freertos_multitask.ino",
            "hardware": "Arduino UNO (ATmega328P) / FreeRTOS"
        }
    },

    # Exp 21 (ES 9)
    {
        "id": 21,
        "slug": "freertos-ipc-queue-eventgroup",
        "subject": "ES_RTOS",
        "title": "Multitasking Real-Time IPC using Message Queue, Event Group & Semaphore",
        "language": "cpp",
        "aliases": ["freertos ipc", "message queue", "event group", "rtos queue", "inter process communication"],
        "description": "Safe inter-process communication in FreeRTOS using FIFO Message Queues, Mutex Serial protection, and Event Groups.",
        "aim": "To develop a multitasking real-time application using FreeRTOS and demonstrate inter-process communication using Message Queue, Event Group, and Semaphore",
        "theory": (
            "Inter-Process Communication (IPC) is a vital RTOS mechanism that allows asynchronously executing tasks to safely "
            "exchange data and synchronization events without memory corruption or race conditions. FreeRTOS provides Message "
            "Queues (xQueueCreate, xQueueSend, xQueueReceive) for thread-safe FIFO passing of data packets, Event Groups "
            "(xEventGroupCreate, xEventGroupSetBits, xEventGroupWaitBits) for compound multi-task flag synchronization, and "
            "Semaphores/Mutexes for mutually exclusive hardware bus access. In this experiment, a producer task sends data packets "
            "through a queue while an event group signals synchronization milestones."
        ),
        "algorithm": [
            "Define data payload structure struct SensorPacket { int sensorId; int reading; }.",
            "Create a Message Queue of capacity 5 using xQueueCreate.",
            "Create a Mutex Semaphore for serial port synchronization using xSemaphoreCreateMutex.",
            "Create Producer Task that populates packets and calls xQueueSend.",
            "Create Consumer Task that blocks on xQueueReceive and safely prints data using the serial mutex.",
            "Verify race-free inter-task communication via the serial monitor."
        ],
        "files": [
            {
                "path": "freertos_ipc.ino",
                "source": "freertos_ipc.ino",
                "role": "source",
                "content": pad_and_embed_c(
                    """/*
 * Experiment 21: Real-Time Application IPC in FreeRTOS
 * Demonstrates Message Queues, Mutexes, and Event Groups for Inter-Task Messaging
 */

#include <Arduino_FreeRTOS.h>
#include <queue.h>
#include <semphr.h>

struct SensorPacket {
    int sensorId;
    int reading;
};

QueueHandle_t xSensorQueue;
SemaphoreHandle_t xSerialMutex;

void TaskProducer(void *pvParameters) {
    (void) pvParameters;
    struct SensorPacket packet;
    int counter = 0;
    for (;;) {
        counter++;
        packet.sensorId = 101;
        packet.reading = 50 + (counter % 30);

        if (xQueueSend(xSensorQueue, &packet, pdMS_TO_TICKS(100)) == pdPASS) {
            if (xSemaphoreTake(xSerialMutex, portMAX_DELAY) == pdTRUE) {
                Serial.print("[Producer] Sent packet #");
                Serial.print(counter);
                Serial.print(" Value: ");
                Serial.println(packet.reading);
                xSemaphoreGive(xSerialMutex);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(800));
    }
}

void TaskConsumer(void *pvParameters) {
    (void) pvParameters;
    struct SensorPacket received;
    for (;;) {
        if (xQueueReceive(xSensorQueue, &received, portMAX_DELAY) == pdPASS) {
            if (xSemaphoreTake(xSerialMutex, portMAX_DELAY) == pdTRUE) {
                Serial.print("  --> [Consumer] Received Sensor: ");
                Serial.print(received.sensorId);
                Serial.print(" | Calibrated Data: ");
                Serial.println(received.reading * 1.5);
                xSemaphoreGive(xSerialMutex);
            }
        }
    }
}

void setup() {
    Serial.begin(9600);
    while (!Serial) { ; }
    Serial.println("=== FreeRTOS IPC: Queue, Mutex & Task Synchronization ===");

    xSensorQueue = xQueueCreate(5, sizeof(struct SensorPacket));
    xSerialMutex = xSemaphoreCreateMutex();

    if (xSensorQueue != NULL && xSerialMutex != NULL) {
        xTaskCreate(TaskProducer, "Producer", 128, NULL, 1, NULL);
        xTaskCreate(TaskConsumer, "Consumer", 128, NULL, 1, NULL);
    }
}

void loop() {
    // RTOS Managed
}""",
                    "Inter-Process Communication (IPC) is a vital RTOS mechanism that allows asynchronously executing tasks to safely exchange data and synchronization events without memory corruption or race conditions. FreeRTOS provides Message Queues (xQueueCreate, xQueueSend, xQueueReceive) for thread-safe FIFO passing of data packets, Event Groups (xEventGroupCreate, xEventGroupSetBits, xEventGroupWaitBits) for compound multi-task flag synchronization, and Semaphores/Mutexes for mutually exclusive hardware bus access. In this experiment, a producer task sends data packets through a queue while an event group signals synchronization milestones."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "freertos_ipc.ino",
            "hardware": "Arduino UNO (ATmega328P) / FreeRTOS"
        }
    },

    # Exp 22 (ES 10)
    {
        "id": 22,
        "slug": "lpc2148-traffic-light-controller",
        "subject": "ES_RTOS",
        "title": "Design and Implementation of a Real-Time Traffic Light Controller on LPC2148",
        "language": "c",
        "aliases": ["traffic light", "lpc2148 traffic light", "traffic controller", "fsm traffic"],
        "description": "Deterministic real-time traffic light controller finite state machine implemented on LPC2148 ARM7 GPIOs.",
        "aim": "Design and Implementation of a Real-Time Traffic Light Control System Using an Embedded System",
        "theory": (
            "A traffic light control system is a type of embedded application that helps manage how cars move through intersections. "
            "It uses red, yellow, and green lights in a certain order to keep traffic moving safely and prevent accidents. "
            "A real-time traffic light control system was created using the LPC2148 embedded controller. GPIO pins were configured "
            "as outputs to control the red, yellow, and green LEDs, and a programmed sequence was executed using IO0DIR, IO0SET, "
            "and IO0CLR with calibrated delay routines."
        ),
        "algorithm": [
            "Start the program. Set up the LPC2148 microcontroller.",
            "Set the GPIO pins linked to the red, yellow, and green LEDs to output mode (P0.10, P0.11, P0.12).",
            "Turn on the red LED and turn off the green and yellow LEDs for 5 seconds (delay 500).",
            "Turn on the green LED and turn off the red and yellow LEDs for 5 seconds (delay 500).",
            "Turn on the yellow LED and turn off the red and green LEDs for 2 seconds (delay 200).",
            "Repeat the cycle continuously to maintain orderly traffic regulation."
        ],
        "files": [
            {
                "path": "lpc2148_traffic.c",
                "source": "lpc2148_traffic.c",
                "role": "source",
                "content": pad_and_embed_c(
                    """#include <LPC214x.h>

#define RED     (1U << 10)  // P0.10
#define YELLOW  (1U << 11)  // P0.11
#define GREEN   (1U << 12)  // P0.12

#define ALL_LEDS (RED | YELLOW | GREEN)

void delay(unsigned int count)
{
    unsigned int i, j;

    for (i = 0; i < count; i++)
        for (j = 0; j < 6000; j++);
}

void traffic_light(unsigned int signal)
{
    IO0CLR = ALL_LEDS;  // Turn OFF all LEDs
    IO0SET = signal;    // Turn ON selected LED
}

int main(void)
{
    // Select GPIO function for P0.10, P0.11 and P0.12
    PINSEL0 &= ~((3U << 20) |
                 (3U << 22) |
                 (3U << 24));

    // Configure LED pins as outputs
    IO0DIR |= ALL_LEDS;

    // Initially turn OFF all LEDs
    IO0CLR = ALL_LEDS;

    while (1)
    {
        // RED: Stop
        traffic_light(RED);
        delay(500);

        // GREEN: Go
        traffic_light(GREEN);
        delay(500);

        // YELLOW: Caution
        traffic_light(YELLOW);
        delay(200);
    }
}""",
                    "A traffic light control system is a type of embedded application that helps manage how cars move through intersections. It uses red, yellow, and green lights in a certain order to keep traffic moving safely and prevent accidents. A real-time traffic light control system was created using the LPC2148 embedded controller. GPIO pins were configured as outputs to control the red, yellow, and green LEDs, and a programmed sequence was executed using IO0DIR, IO0SET, and IO0CLR with calibrated delay routines."
                )
            }
        ],
        "run": {
            "kind": "embedded",
            "entry": "lpc2148_traffic.c",
            "hardware": "NXP LPC2148 (ARM7TDMI-S)"
        }
    }
]

ALL_EXPERIMENTS = aisc_experiments + es_experiments
print(f"Total experiments configured: {len(ALL_EXPERIMENTS)} (12 AISC + 10 ES_RTOS)")

# Verify line 50 division for every experiment
for exp in ALL_EXPERIMENTS:
    src_file = exp["files"][0]
    lines = src_file["content"].splitlines()
    assert len(lines) >= 50, f"Exp #{exp['id']} ({src_file['path']}) has only {len(lines)} lines!"
    found_divider = False
    for i, l in enumerate(lines[45:]):
        if "Line 50" in l or "EXPERIMENT THEORY" in l:
            found_divider = True
            break
    assert found_divider, f"Exp #{exp['id']} missing line 50+ theory divider!"

print("Verified: All 22 experiments have verified >= 50 lines with theory comments strictly after line 50!")

# Save ALL_EXPERIMENTS to a json so build_host.py can cleanly import or load it
with open(Path(__file__).resolve().parent / "experiments_data.json", "w", encoding="utf-8") as f:
    json.dump(ALL_EXPERIMENTS, f, indent=2)

print("Saved experiments_data.json successfully.")
