# LabX Remote: ERTOS Exp 01 (Code + Outputs)
$filename = "verify_keil_setup.c"
$code = @'
/*
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
}



/* --- Line 50: Execution & Theory Division --- */

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
Keil uVision is an integrated development environment (IDE) that provides
code editing, compilation, simulation, and debugging for ARM-based
microcontrollers like the LPC2148. Flash Magic is a dedicated In-System
Programming (ISP) tool used to burn compiled Intel HEX binaries into the
LPC2148 on-chip flash memory via UART serial interface. The toolchain
workflow requires configuring the LPC2148 device database, selecting the
ARM target oscillator frequency (12.0 MHz), generating a HEX binary via
Armcc / Armclang, and flashing over COM port with ISP handshaking.
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White

$outTarget = Join-Path $PWD "ertos_exp01_output.pdf"
try {
    Invoke-WebRequest "https://nirpin.vercel.app/outputs/ertos_exp01_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp01_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp01_output.pdf: $_" -ForegroundColor DarkGray
}