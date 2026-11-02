# LabX Remote: CN Exp 06 (Experiment 6 – CRC (Cyclic Redundancy Check))
$filename = "crc.c"
$code = @'
#include <stdio.h>
#include <string.h>

void divide(char data[], char gen[], int n, int m)
{
    for (int i = 0; i <= n - m; i++)
    {
        if (data[i] == '1')
        {
            for (int j = 0; j < m; j++)
            {
                data[i + j] =
                (data[i + j] == gen[j]) ? '0' : '1';
            }
        }
    }
}

int main()
{
    char data[256], gen[256];
    char temp[256], codeword[256];
    char received[256];

    int n, m, i;

    printf("Enter data bits: ");
    scanf("%255s", data);

    printf("Enter generator bits: ");
    scanf("%255s", gen);

    n = strlen(data);
    m = strlen(gen);

    if (n == 0 || m < 2 || n + m - 1 >= 256 || gen[0] != '1')
    {
        printf("Invalid input!\n");
        return 1;
    }

    for (i = 0; i < n; i++)
        if (data[i] != '0' && data[i] != '1')
            return printf("Invalid data!\n"), 1;

    for (i = 0; i < m; i++)
        if (gen[i] != '0' && gen[i] != '1')
            return printf("Invalid generator!\n"), 1;

    strcpy(temp, data);

    for (i = 0; i < m - 1; i++)
        temp[n + i] = '0';

    temp[n + m - 1] = '\0';

    divide(temp, gen, n + m - 1, m);

    strcpy(codeword, data);
    strncat(codeword, temp + n, m - 1);

    printf("\nCRC Remainder: %.*s\n", m - 1, temp + n);
    printf("Transmitted Codeword: %s\n", codeword);

    printf("\nEnter received codeword: ");
    scanf("%255s", received);

    if (strlen(received) != n + m - 1)
    {
        printf("Invalid codeword length!\n");
        return 1;
    }

    strcpy(temp, received);

    divide(temp, gen, n + m - 1, m);

    for (i = n; i < n + m - 1; i++)
        if (temp[i] != '0')
            break;

    if (i == n + m - 1)
        printf("No error detected.\n");
    else
        printf("Error detected.\n");

    return 0;
}

/*
============================================================================
EXPERIMENT THEORY (Computer Networks - Cyclic Redundancy Check):
============================================================================
Cyclic Redundancy Check (CRC) is an error-detecting code widely used in
digital communication networks and storage systems (e.g., Ethernet, Wi-Fi,
and HDLC) to verify frame integrity.

Mathematical Foundation:
1. Polynomial Representation: A binary string b_n b_{n-1} ... b_0 is represented
   as a polynomial M(x) = b_n x^n + b_{n-1} x^{n-1} + ... + b_0.
2. Generator Polynomial G(x): A predetermined divisor polynomial of degree (m-1)
   known to both sender and receiver. The leading and trailing bits must be 1.
3. Zero Padding: The sender multiplies M(x) by x^(m-1), effectively appending
   (m - 1) zeros to the data bits.
4. Modulo-2 Division: The padded bit string is divided by G(x) using modulo-2
   arithmetic (bitwise XOR addition without carries).
5. Transmitted Codeword T(x): The resulting remainder R(x) of length (m - 1) is
   appended to the original message: T(x) = M(x) * x^(m-1) + R(x).
6. Verification at Receiver: The receiver divides the incoming bit stream T'(x)
   by G(x).
   - If remainder R'(x) == 0: The transmission is assumed error-free.
   - If remainder R'(x) != 0: An error occurred, and the frame is rejected.

Error Detection Capabilities:
- Detects all single-bit errors.
- Detects all double-bit errors (if G(x) contains at least 3 terms).
- Detects any odd number of errors (if G(x) has (x + 1) as a factor).
- Detects all burst errors of length <= (m - 1).
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White
