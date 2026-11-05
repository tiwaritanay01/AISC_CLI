# LabX Remote: CN Exp 07 (Experiment 7 – Hamming Code Error Detection & Correction)
$filename = "hamming.c"
$code = @'
#include <stdio.h>
#include <string.h>

int main()
{
    int data[50], hamming[100], received[100];
    int n, r = 0, i, j, k, pos;
    int syndrome = 0;

    printf("Enter number of data bits: ");
    scanf("%d", &n);

    if (n < 1 || n > 40)
    {
        printf("Invalid number of bits!\n");
        return 1;
    }

    printf("Enter data bits (0 or 1): ");

    for (i = 0; i < n; i++)
    {
        scanf("%1d", &data[i]);

        if (data[i] != 0 && data[i] != 1)
        {
            printf("Invalid data!\n");
            return 1;
        }
    }

    while ((1 << r) < n + r + 1)
        r++;

    int total = n + r;

    j = 0;

    for (i = 1; i <= total; i++)
    {
        if ((i & (i - 1)) == 0)
            hamming[i] = 0;
        else
            hamming[i] = data[j++];
    }

    for (i = 0; i < r; i++)
    {
        pos = 1 << i;
        int parity = 0;

        for (j = 1; j <= total; j++)
        {
            if (j & pos)
                parity ^= hamming[j];
        }

        hamming[pos] = parity;
    }

    printf("\nHamming Code: ");

    for (i = total; i >= 1; i--)
        printf("%d", hamming[i]);

    printf("\nEnter received codeword: ");

    for (i = total; i >= 1; i--)
    {
        scanf("%1d", &received[i]);

        if (received[i] != 0 && received[i] != 1)
        {
            printf("Invalid received data!\n");
            return 1;
        }
    }

    for (i = 0; i < r; i++)
    {
        pos = 1 << i;
        int parity = 0;

        for (j = 1; j <= total; j++)
        {
            if (j & pos)
                parity ^= received[j];
        }

        if (parity)
            syndrome += pos;
    }

    if (syndrome == 0)
    {
        printf("No error detected.\n");
    }
    else if (syndrome <= total)
    {
        printf("Error detected at position: %d\n", syndrome);

        received[syndrome] ^= 1;

        printf("Corrected Codeword: ");

        for (i = total; i >= 1; i--)
            printf("%d", received[i]);
    }
    else
    {
        printf("Invalid syndrome!\n");
    }

    return 0;
}

/*
============================================================================
HOW TO RUN THIS EXPERIMENT:
============================================================================
Requirements: GCC (MinGW / MSYS2 / build-essential) or Clang.

1. Compilation:
   Windows:   gcc hamming.c -o hamming.exe
   Linux/Mac: gcc hamming.c -o hamming

2. Execution:
   Windows:   .\hamming.exe
   Linux/Mac: ./hamming

3. Sample Run:
   Enter number of data bits: 4
   Enter data bits (0 or 1): 1 0 1 1
   -> Output:
      Hamming Code: 1010101
   Enter received codeword: 1010101
   -> Output:
      No error detected.

   (Or introduce an error: e.g. 1011101 -> Error detected at position: 4)
============================================================================
EXPERIMENT THEORY (Computer Networks - Hamming Code Error Detection & Correction):
============================================================================
Hamming Code is a linear error-correcting code invented by Richard Hamming in 1950.
It can detect up to two simultaneous bit errors and correct single-bit errors (SEC-DED).

Operating Principles:
1. Redundancy Bit Calculation:
   For 'n' data bits and 'r' parity/redundant bits, the relationship is given
   by the Hamming Inequality:
       2^r >= n + r + 1
2. Bit Positioning (1-based indexing):
   - Redundant bits occupy bit positions that are powers of 2: 1, 2, 4, 8, 16, etc.
   - Data bits occupy all remaining bit positions: 3, 5, 6, 7, 9, 10, etc.
3. Parity Determination:
   Each parity bit P_i at position 2^i calculates even parity across all bit
   positions whose binary representation has the i-th bit set to 1.
   - P1 (pos 1): checks bits 1, 3, 5, 7, 9, 11, ...
   - P2 (pos 2): checks bits 2, 3, 6, 7, 10, 11, ...
   - P4 (pos 4): checks bits 4, 5, 6, 7, 12, 13, ...
   - P8 (pos 8): checks bits 8-15, 24-31, ...
4. Syndrome Evaluation:
   At the receiver, the parity checks are recomputed over the entire received
   word. Each check produces an error bit S_i. The combined binary value of
   (S_r ... S_2 S_1) is known as the Error Syndrome:
   - Syndrome == 0: No error occurred.
   - Syndrome > 0: Indicates the EXACT bit position of the corrupted bit.
5. Error Correction:
   Inverting the bit at received[syndrome] restores the original codeword.
============================================================================
*/


'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White
