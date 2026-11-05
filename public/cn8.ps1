# LabX Remote: CN Exp 08 (Experiment 8 – Checksum Error Detection)
$filename = "checksum.c"
$code = @'
#include <stdio.h>
#include <string.h>

int readBinary()
{
    char bits[20];
    int value = 0;

    scanf("%19s", bits);

    if (strlen(bits) != 8)
        return -1;

    for (int i = 0; i < 8; i++)
    {
        if (bits[i] != '0' && bits[i] != '1')
            return -1;

        value = value * 2 + (bits[i] - '0');
    }

    return value;
}

void printBinary(int value)
{
    for (int i = 7; i >= 0; i--)
        printf("%d", (value >> i) & 1);
}

int add(int sum, int value)
{
    sum += value;

    while (sum > 255)
        sum = (sum & 255) + (sum >> 8);

    return sum;
}

int main()
{
    int n, i, data[20];
    int sum = 0, checksum;
    int received, verify = 0;

    printf("Enter number of 8-bit data words: ");
    scanf("%d", &n);

    if (n < 1 || n > 20)
    {
        printf("Invalid number of words!\n");
        return 1;
    }

    printf("Enter %d binary data words:\n", n);

    for (i = 0; i < n; i++)
    {
        data[i] = readBinary();

        if (data[i] < 0)
        {
            printf("Invalid 8-bit data!\n");
            return 1;
        }

        sum = add(sum, data[i]);
    }

    checksum = (~sum) & 255;

    printf("\nChecksum: ");
    printBinary(checksum);

    printf("\n\nEnter received data words:\n");

    for (i = 0; i < n; i++)
    {
        received = readBinary();

        if (received < 0)
        {
            printf("Invalid received data!\n");
            return 1;
        }

        verify = add(verify, received);
    }

    printf("Enter received checksum: ");

    received = readBinary();

    if (received < 0)
    {
        printf("Invalid checksum!\n");
        return 1;
    }

    verify = add(verify, received);

    printf("\nReceiver Sum: ");
    printBinary(verify);

    if (verify == 255)
        printf("\nNo error detected.\n");
    else
        printf("\nError detected.\n");

    return 0;
}

/*
============================================================================
HOW TO RUN THIS EXPERIMENT:
============================================================================
Requirements: GCC (MinGW / MSYS2 / build-essential) or Clang.

1. Compilation:
   Windows:   gcc checksum.c -o checksum.exe
   Linux/Mac: gcc checksum.c -o checksum

2. Execution:
   Windows:   .\checksum.exe
   Linux/Mac: ./checksum

3. Sample Run:
   Enter number of 8-bit data words: 2
   Enter 2 binary data words:
   10101001
   00111100
   -> Output:
      Checksum: 00011001
   Enter received data words:
   10101001
   00111100
   Enter received checksum:
   00011001
   -> Output:
      Receiver Sum: 11111111
      No error detected.
============================================================================
EXPERIMENT THEORY (Computer Networks - Checksum Error Detection):
============================================================================
The Checksum algorithm is an error-detection technique widely deployed at the
Transport layer (TCP, UDP) and Network layer (IPv4 header) of the Internet
protocol suite.

Mathematical Foundation (One's Complement Arithmetic):
1. Word Segmentation:
   The message is divided into fixed-width k-bit words (here, 8-bit bytes;
   in TCP/IP, 16-bit words).
2. One's Complement Addition:
   All words are summed using one's complement addition. In binary arithmetic,
   if an addition produces an overflow carry bit past the k-th bit (sum > 255),
   that carry bit must be wrapped around and added to the least significant bit
   (end-around carry: `(sum & 255) + (sum >> 8)`).
3. Checksum Generation:
   The sender inverts all bits of the accumulated sum (bitwise NOT / complement:
   `(~sum) & 0xFF`). This inverted value is the Checksum and is appended to
   the data transmission.
4. Receiver Verification:
   The receiver sums all received data words PLUS the received checksum word
   using the identical one's complement arithmetic.
5. Error Decision:
   - If no corruption occurred: Sum + (~Sum) = all 1s (0xFF or 255 in 8-bit).
     Inverting the receiver sum produces all 0s (0x00).
   - If any bit changed during transmission: The sum will not equal all 1s,
     and an error is reported.
============================================================================
*/


'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White
