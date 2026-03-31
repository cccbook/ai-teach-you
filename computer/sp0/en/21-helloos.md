# 21. First OS——UART and Hello World

## 21.1 Building an OS from Scratch

An operating system is software that manages hardware resources and provides services to applications. This book uses the mini-riscv-os project to build a micro operating system on RISC-V from scratch.

Source code location: [_code/mini-riscv-os/](../_code/mini-riscv-os/)

## 21.2 Stage Overview

mini-riscv-os is divided into 10 stages:

| Stage | Directory | Content |
|-------|----------|---------|
| 01 | HelloOs | First OS, UART output |
| 02 | ContextSwitch | Switching from OS to task |
| 03 | MultiTasking | Cooperative multitasking |
| 04 | TimerInterrupt | Timer interrupt |
| 05 | Preemptive | Preemptive scheduling |
| 06 | Spinlock | Spinlock |
| 07 | ExternalInterrupt | External interrupt |
| 08 | BlockDeviceDriver | Block device driver |
| 09 | MemoryAllocator | Memory allocation |
| 10 | SystemCall | System call |

## 21.3 First OS Structure

### 21.3.1 Startup File start.s

```asm
.equ STACK_SIZE, 8192

.global _start

_start:
    csrr a0, mhartid        ; Read Hart ID
    bnez a0, park           ; If not hart 0, go to park
    
    la   sp, stacks + STACK_SIZE  ; Set stack pointer
    j    os_main             ; Jump to OS main

park:
    wfi                      ; Wait for Interrupt
    j park

stacks:
    .skip STACK_SIZE         ; Allocate stack space
```

Key points:
- `csrr a0, mhartid`: Read current CPU core ID
- On multi-core systems, only hart 0 runs the OS
- Other cores enter park loop waiting
- `wfi`: Wait for timer interrupt to save power

### 21.3.2 Main Program os.c

```c
#include <stdint.h>

#define UART        0x10000000
#define UART_THR    (uint8_t*)(UART+0x00)  // Transmit Holding Register
#define UART_LSR    (uint8_t*)(UART+0x05)  // Line Status Register
#define UART_LSR_EMPTY_MASK 0x40           // Transmitter empty flag

int lib_putc(char ch) {
    // Wait for UART to be ready
    while ((*UART_LSR & UART_LSR_EMPTY_MASK) == 0);
    return *UART_THR = ch;
}

void lib_puts(char *s) {
    while (*s) lib_putc(*s++);
}

int os_main(void) {
    lib_puts("Hello OS!\n");
    while (1) {}  // Infinite loop
    return 0;
}
```

## 21.4 RISC-V Privilege Modes

RISC-V has three privilege modes (high to low):

| Mode | Name | Purpose |
|------|------|---------|
| M Mode | Machine | Highest privilege, Bootloader, BIOS |
| S Mode | Supervisor | OS kernel |
| U Mode | User | User programs |

mini-riscv-os runs in Machine Mode because it's a bare-metal system.

### 21.4.1 Control and Status Registers (CSR)

Important CSRs for M Mode:

| CSR | Name | Purpose |
|-----|------|---------|
| mhartid | Hart ID | CPU core ID |
| mstatus | Machine Status | Interrupt status |
| mtvec | Machine Trap Vector | Trap handler vector |
| mie | Machine Interrupt Enable | Interrupt enable |
| mip | Machine Interrupt Pending | Pending interrupt |
| mepc | Machine Exception PC | Exception PC |
| mcause | Machine Cause | Exception/interrupt cause |

## 21.5 UART Device

### 21.5.1 What is UART?

UART (Universal Asynchronous Receiver-Transmitter) is a serial communication protocol.

QEMU's Virt platform maps UART to memory address `0x10000000`.

### 21.5.2 UART Registers

| Address | Name | Description |
|---------|------|-------------|
| 0x00 | THR | Transmit Holding Register (write character to send) |
| 0x05 | LSR | Line Status Register (read status) |

LSR bit 6 (UART_LSR_EMPTY_MASK): When 1, transmitter is empty, can send next character.

### 21.5.3 Character Output Flow

```
CPU                    UART                    Terminal
  |                      |                      |
  |─── Write THR ───────→|                      |
  |                      |─── Serial bits ─────→|
  |                      |                      |
  |←── Poll LSR ─────────|                      |
  |                      |                      |
```

## 21.6 Linker Script os.ld

```ld
OUTPUT_ARCH(riscv)
OUTPUT_FORMAT("elf32-littleriscv", "elf32-littleriscv", "elf32-littleriscv")

ENTRY(_start)

SECTIONS {
    . = 0x80000000;
    .text : { *(.text) }
    .data : { *(.data) }
    .bss  : { *(.bss) }
}
```

Key points:
- `ENTRY(_start)`: Program entry point
- `. = 0x80000000`: Code starts at this address (where QEMU expects it)
- All sections arranged from this address

## 21.7 Makefile

```makefile
CC = riscv64-unknown-elf-gcc
CFLAGS = -nostdlib -fno-builtin -mcmodel=medany -march=rv32ima -mabi=ilp32

QEMU = qemu-system-riscv32
QFLAGS = -nographic -smp 4 -machine virt -bios none

all: os.elf

os.elf: start.s os.c
    $(CC) $(CFLAGS) -T os.ld -o os.elf $^

qemu:
    $(QEMU) $(QFLAGS) -kernel os.elf

clean:
    rm -f *.elf
```

Key compilation options:
- `-nostdlib`: Don't link standard library (we're an OS, no standard library)
- `-fno-builtin`: Don't use builtin functions
- `-mcmodel=medany`: Use any address code model
- `-march=rv32ima`: Target architecture (32-bit, M, A, I extensions)
- `-mabi=ilp32`: 32-bit ABI (integer/pointer are 32-bit)

## 21.8 Running and Testing

### 21.8.1 Build

```bash
cd _code/mini-riscv-os/01-HelloOs
make
```

### 21.8.2 Run in QEMU

```bash
make qemu
```

Output:
```
Hello OS!
```

### 21.8.3 Exit QEMU

Press `Ctrl-A` then `X`.

## 21.9 Boot Flow

```
┌─────────────────────────────────────────────────────────┐
│  QEMU loads os.elf                                       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  _start (start.s)                                       │
│    1. Read mhartid                                      │
│    2. Non-0 harts go to park                          │
│    3. Hart 0 sets sp and jumps to os_main             │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  os_main (os.c)                                        │
│    1. Call lib_puts("Hello OS!\n")                     │
│    2. Infinite loop                                    │
└─────────────────────────────────────────────────────────┘
```

## 21.10 Summary

In this chapter we learned:
- mini-riscv-os stage structure
- RISC-V privilege modes (M/S/U Mode)
- Control and Status Registers (CSR)
- UART device and serial communication
- Basic linker script structure
- Makefile compilation options
- First OS from scratch

## 21.11 Exercises

1. Modify `os.c` to output your name
2. Add a `lib_puti` function to output numbers
3. Implement `printf` function (support %d, %x, %s)
4. Why poll LSR? How to use interrupts instead?
5. Research QEMU's `-machine virt` platform memory layout
