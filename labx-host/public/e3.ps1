# LabX Remote: ERTOS Exp 03 (Code + Outputs)
$filename = "lpc2148_lcd.c"
$code = @'
/*
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
}

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
A 16x2 alphanumeric LCD display interfaces with the LPC2148 using 8 data
lines (D0-D7) and 3 control lines: RS (Register Select - 0 for command, 1
for data), RW (Read/Write - grounded for write), and EN (Enable -
high-to-low pulse to latch data). Commands initialize display mode (0x38
for 8-bit, 2-line mode), display ON cursor OFF (0x0C), clear screen
(0x01), and set DDRAM address (0x80 line 1, 0xC0 line 2). The LPC2148
drives the LCD by asserting RS, placing data on Port 0, and pulsing EN
with sufficient setup and hold time.
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White

$outTarget = Join-Path $PWD "ertos_exp03_drive_output.pdf"
try {
    Invoke-WebRequest "https://cli-t0km.onrender.com/outputs/ertos_exp03_drive_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp03_drive_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp03_drive_output.pdf: $_" -ForegroundColor DarkGray
}
$outTarget = Join-Path $PWD "ertos_exp03_output.pdf"
try {
    Invoke-WebRequest "https://cli-t0km.onrender.com/outputs/ertos_exp03_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp03_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp03_output.pdf: $_" -ForegroundColor DarkGray
}