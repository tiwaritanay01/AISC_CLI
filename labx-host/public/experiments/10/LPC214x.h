/* LPC214x.h - Hardware Register Definitions for Philips/NXP LPC2148 ARM7TDMI */
#ifndef LPC214X_H
#define LPC214X_H

#define IODIR0   (*((volatile unsigned long *) 0xE0028008))
#define IOPIN0   (*((volatile unsigned long *) 0xE0028000))
#define IOSET0   (*((volatile unsigned long *) 0xE0028004))
#define IOCLR0   (*((volatile unsigned long *) 0xE002800C))

#define PINSEL0  (*((volatile unsigned long *) 0xE002C000))
#define PINSEL1  (*((volatile unsigned long *) 0xE002C004))

#endif
