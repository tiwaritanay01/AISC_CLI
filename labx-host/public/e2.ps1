# LabX Remote: ERTOS Exp 02 (Code + Output PDF)
$filename = "lpc2148_led.c"
$code = @'
/*
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
}

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
The LPC2148 is an ARM7TDMI-S based 32-bit microcontroller with two 32-bit
general-purpose I/O ports (Port 0 and Port 1). GPIO pins are controlled by
registers: PINSEL (Pin Function Select), IOxDIR (Direction register: 1 for
Output, 0 for Input), IOxSET (Set pin high), and IOxCLR (Clear pin low).
An LED connected in active-high or active-low configuration is toggled
with software delay loops. In this experiment, Port 0 pins (P0.10 - P0.17)
drive an 8-LED bar display, demonstrating single-pin blinking, alternating
blinking, and binary counter sequences.
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White

$outTarget = Join-Path $PWD "ertos_exp02_output.pdf"
try {
    Invoke-WebRequest "https://aisccli.netlify.app/outputs/ertos_exp02_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output PDF to: ertos_exp02_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp02_output.pdf: $_" -ForegroundColor DarkGray
}