# 24. Timer Interrupts——Preemptive Scheduling

## 24.1 Why Preemptive Scheduling?

Problems with cooperative multitasking:
- Tasks may never yield CPU
- System may become unresponsive

Advantages of preemptive multitasking:
- OS can force task switching
- Fairer CPU allocation
- Better system responsiveness

## 24.2 RISC-V Interrupt Mechanism

### 24.2.1 Interrupt Types

| Type | Name | Description |
|------|------|-------------|
| Synchronous | Exception | Occurs during instruction execution |
| Asynchronous | Interrupt | Triggered by external device |

Asynchronous interrupts:
- **Machine Timer Interrupt** (mti): Timer interrupt
- **Machine Software Interrupt** (msi): Software interrupt
- **Machine External Interrupt** (mei): External interrupt

### 24.2.2 Key CSRs

| CSR | Name | Purpose |
|-----|------|---------|
| mstatus | Machine Status | Global interrupt enable |
| mie | Machine Interrupt Enable | Per-type interrupt enable |
| mtvec | Machine Trap Vector | Trap handler vector address |
| mip | Machine Interrupt Pending | Pending interrupt flags |
| mepc | Machine Exception PC | PC when exception occurred |
| mcause | Machine Cause | Exception/interrupt cause |

### 24.2.3 mstatus Register

```
Bit 3: MIE - Machine Interrupt Enable
       1 = Enable machine mode interrupts
       0 = Disable machine mode interrupts

Bit 7: MPIE - Machine Previous Interrupt Enable
       Saves MIE value before entering interrupt
```

### 24.2.4 mie Register

```
Bit 3: MTIE - Machine Timer Interrupt Enable
Bit 7: MSIE - Machine Software Interrupt Enable  
Bit 11: MEIE - Machine External Interrupt Enable
```

### 24.2.5 mcause Register

```
Bit 31: Interrupt flag
        1 = Asynchronous interrupt
        0 = Synchronous exception

Bits 0-30: Exception/interrupt code
        3 = Machine Software Interrupt
        7 = Machine Timer Interrupt
        11 = Machine External Interrupt
```

## 24.3 Timer Setup

### 24.3.1 RISC-V Timer

RISC-V uses two CSRs:
- **mtime**: Timer count (64-bit)
- **mtimecmp**: Timer compare value (64-bit)

When `mtime >= mtimecmp`, a timer interrupt is triggered.

### 24.3.2 Timer Register Addresses

On QEMU virt platform:
```
#define CLINT_BASE 0x2000000
#define MTIME       (CLINT_BASE + 0xBFF8)  // Timer count
#define MTIMECMP    (CLINT_BASE + 0x4000)  // Compare value
```

### 24.3.3 Timer Initialization

```c
// timer.h
extern void timer_init(void);
extern void timer_handler(void);
extern void timer_load(int interval);

// timer.c
#define CLINT_BASE 0x2000000
#define MTIME       ((uint64_t*) (CLINT_BASE + 0xBFF8))
#define MTIMECMP    ((uint64_t*) (CLINT_BASE + 0x4000))

void timer_init(void) {
    timer_load(100000);  // Set initial interval
}

void timer_load(int interval) {
    // Set next interrupt time
    *MTIMECMP = *MTIME + interval;
}
```

## 24.4 Interrupt Handling

### 24.4.1 trap.s - Trap Vector

```asm
.align 4
.globl trap_vector
trap_vector:
    # Save context to task stack
    sw ra, 0(sp)
    sw sp, 4(sp)
    # ... other registers
    sw s11, 52(sp)
    
    # Call C handler
    csrr a0, mepc          ; Get exception PC
    csrr a1, mcause         ; Get exception cause
    jal ra, trap_handler
    
    # Restore context
    lw ra, 0(sp)
    lw sp, 4(sp)
    # ... other registers
    lw s11, 52(sp)
    
    mret                    ; Return from interrupt
```

### 24.4.2 trap.c - Trap Handler

```c
reg_t trap_handler(reg_t epc, reg_t cause) {
    reg_t return_pc = epc;
    reg_t cause_code = cause & 0xfff;
    
    if (cause & 0x80000000) {  // Asynchronous interrupt
        switch (cause_code) {
        case 7:  // Timer interrupt
            timer_handler();
            break;
        default:
            lib_puts("Unknown interrupt!\n");
            break;
        }
    } else {  // Synchronous exception
        lib_puts("Sync exception!\n");
    }
    
    return return_pc;
}
```

## 24.5 Timer Interrupt Handler

### 24.5.1 timer_handler

```c
void timer_handler(void) {
    // Set next interrupt
    timer_load(100000);
    
    // On timer interrupt, force switch to OS
    // OS scheduler will select next task
}
```

## 24.6 Preemptive Scheduling Integration

### 24.6.1 trap.c Complete Implementation

```c
reg_t trap_handler(reg_t epc, reg_t cause) {
    reg_t return_pc = epc;
    reg_t cause_code = cause & 0xfff;
    
    if (cause & 0x80000000) {
        switch (cause_code) {
        case 3:  // Software interrupt
            lib_puts("Software interrupt!\n");
            break;
        case 7:  // Timer interrupt
            lib_puts("Timer interrupt!\n");
            timer_handler();
            // Return to OS instead of task
            return_pc = (reg_t)&os_kernel;
            break;
        case 11:  // External interrupt
            lib_puts("External interrupt!\n");
            break;
        }
    }
    return return_pc;
}
```

### 24.6.2 trap_init

```c
void trap_init(void) {
    // Set trap vector
    w_mtvec((reg_t)trap_vector);
    
    // Enable timer interrupt
    w_mstatus(r_mstatus() | MSTATUS_MIE);
    w_mie(r_mie() | MIE_MTIE);  // Enable machine timer interrupt
}
```

## 24.7 Preemptive Scheduling Flow

```
                    Timer interrupt triggers
                          │
                          ↓
              ┌───────────────────────────┐
              │ trap_vector (asm)        │
              │   Save task context       │
              └───────────────────────────┘
                          │
                          ↓
              ┌───────────────────────────┐
              │ trap_handler (C)        │
              │   timer_handler()       │
              │   return_pc = os_kernel │
              └───────────────────────────┘
                          │
                          ↓
              ┌───────────────────────────┐
              │ Restore context (asm)   │
              │ mret → return to os_kernel │
              └───────────────────────────┘
                          │
                          ↓
              ┌───────────────────────────┐
              │ os_kernel()              │
              │   Schedule next task      │
              │   task_go(&tasks[next])  │
              └───────────────────────────┘
```

## 24.8 Comparison with Cooperative Scheduling

| Feature | Cooperative | Preemptive |
|---------|-------------|------------|
| Switch timing | Tasks voluntarily yield | Timer interrupt |
| Fairness | Unfair | Fair |
| Complexity | Simple | Complex |
| Responsiveness | Low | High |

## 24.9 Running

```bash
cd _code/mini-riscv-os/04-TimerInterrupt
make
make qemu
```

Or preemptive scheduling:
```bash
cd _code/mini-riscv-os/05-Preemptive
make
make qemu
```

## 24.10 mret Instruction

`mret` is the instruction for returning from machine mode interrupt:

```asm
mret
```

Equivalent to:
```
mepc = pc
mstatus.MPIE → mstatus.MIE  ; Restore interrupt status
pc = mepc                     ; Jump back to PC where interrupt occurred
```

## 24.11 Summary

In this chapter we learned:
- RISC-V interrupt mechanism
- mstatus, mie, mcause and other CSRs
- Timer setup (mtime/mtimecmp)
- Interrupt vector handling
- trap_handler implementation
- Preemptive scheduling flow

## 24.12 Exercises

1. Implement dynamic time slice adjustment
2. Why save and restore all s registers?
3. Research interrupt nesting possibilities and implementation
4. Implement CPU time accounting per task
5. Compare RISC-V interrupt mechanism with ARM Cortex-M
