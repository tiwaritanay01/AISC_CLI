# LabX Remote: ERTOS Exp 04 (Code + Outputs)
$filename = "lpc2148_uart.c"
$code = @'
/*
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
    UART0_SendString("\r\n==========================================\r\n");
    UART0_SendString(" LabX Remote: LPC2148 UART0 Communication\r\n");
    UART0_SendString(" Serial Port Initialized at 9600 Baud (8-N-1)\r\n");
    UART0_SendString("==========================================\r\n");
    UART0_SendString("Type characters in terminal to echo back:\r\n");

    while (1) {
        char ch = UART0_ReceiveChar();
        UART0_SendChar(ch);     // Echo back received character
        if (ch == '\r') {
            UART0_SendChar('\n');
        }
    }
    return 0;
}

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
LPC2148 features two asynchronous serial ports (UART0 and UART1). UART
communication requires setting the baud rate generator using U0LCR (Line
Control Register, DLAB=1), U0DLL, and U0DLM divider latches based on PCLK
(Peripheral Clock). Data transmission occurs by polling the Transmit
Holding Register Empty (THRE) flag in U0LSR and writing bytes to U0THR.
Data reception polls the Receiver Data Ready (RDR) flag and reads from
U0RBR. Setting word length to 8 bits, 1 stop bit, and no parity
establishes standard 9600-8-N-1 serial framing.
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White

$outTarget = Join-Path $PWD "ertos_exp04_drive_output.pdf"
try {
    Invoke-WebRequest "https://cli-t0km.onrender.com/outputs/ertos_exp04_drive_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp04_drive_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp04_drive_output.pdf: $_" -ForegroundColor DarkGray
}
$outTarget = Join-Path $PWD "ertos_exp04_output.pdf"
try {
    Invoke-WebRequest "https://cli-t0km.onrender.com/outputs/ertos_exp04_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp04_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp04_output.pdf: $_" -ForegroundColor DarkGray
}