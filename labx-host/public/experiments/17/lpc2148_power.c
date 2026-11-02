#include <LPC214x.h>

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
}

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
To implement power management techniques in the LPC2148 embedded
controller by configuring its power-saving modes to reduce power
consumption. Power management in the LPC2148 is controlled via the PCON
(Power Control) and PCONP (Power Control for Peripherals) registers.
LPC2148 supports Idle Mode (PCON=0x01) where the CPU clock stops while
peripherals continue running, and Power Down Mode (PCON=0x02) where both
CPU and oscillator are halted. An external interrupt (EINT0 on P0.16) is
configured via the Vectored Interrupt Controller (VIC) to wake the
microcontroller from low-power state, toggle a status LED, and resume
operation.
============================================================================
*/
