# LabX Remote: ERTOS Exp 10 (Code + Outputs)
$filename = "lpc2148_traffic.c"
$code = @'
#include <LPC214x.h>

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
}

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
A traffic light control system is a type of embedded application that
helps manage how cars move through intersections. It uses red, yellow, and
green lights in a certain order to keep traffic moving safely and prevent
accidents. A real-time traffic light control system was created using the
LPC2148 embedded controller. GPIO pins were configured as outputs to
control the red, yellow, and green LEDs, and a programmed sequence was
executed using IO0DIR, IO0SET, and IO0CLR with calibrated delay routines.
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White

$outTarget = Join-Path $PWD "ertos_exp10_drive_output.pdf"
try {
    Invoke-WebRequest "https://nirpin.vercel.app/outputs/ertos_exp10_drive_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp10_drive_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp10_drive_output.pdf: $_" -ForegroundColor DarkGray
}
$outTarget = Join-Path $PWD "ertos_exp10_output.pdf"
try {
    Invoke-WebRequest "https://nirpin.vercel.app/outputs/ertos_exp10_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp10_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp10_output.pdf: $_" -ForegroundColor DarkGray
}