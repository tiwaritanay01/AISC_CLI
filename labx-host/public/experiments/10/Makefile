# Makefile for ARM7 LPC2148 using GNU Arm Embedded Toolchain
CC = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy
CFLAGS = -mcpu=arm7tdmi -O2 -Wall

all: main.hex

main.elf: main.c
	$(CC) $(CFLAGS) -o main.elf main.c

main.hex: main.elf
	$(OBJCOPY) -O ihex main.elf main.hex

clean:
	rm -f *.elf *.hex *.o
