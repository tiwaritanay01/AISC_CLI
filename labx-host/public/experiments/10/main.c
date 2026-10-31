/*
 * Experiment 10: ARM7 LPC2148 GPIO LED Flasher
 * Target: NXP LPC2148 (ARM7TDMI-S)
 * Frequency: 60 MHz (12 MHz Crystal + PLL)
 */
#include "LPC214x.h"

#define LED_PIN (1 << 10)  /* P0.10 connected to LED */

void delay_ms(unsigned int count) {
    volatile unsigned int i, j;
    for (i = 0; i < count; i++) {
        for (j = 0; j < 3000; j++) {
            /* Assembly NOP or busy wait */
        }
    }
}

int main(void) {
    /* Set P0.10 as GPIO */
    PINSEL0 &= ~(0x3 << 20);

    /* Set P0.10 as Output */
    IODIR0 |= LED_PIN;

    while (1) {
        IOSET0 = LED_PIN;   /* Turn LED ON */
        delay_ms(500);

        IOCLR0 = LED_PIN;   /* Turn LED OFF */
        delay_ms(500);
    }

    return 0;
}
