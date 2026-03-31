# 22. Privilege Mode Switching——Context Switch Basics

## 22.1 What is Context Switch?

Context Switch is the process where the OS switches the CPU from one task to another.

```
Task A                          Task B
   │                               │
   │  ┌─────────────────────┐      │
   │  │ 1. Save task A state │      │
   │  │ 2. Load task B state │      │
   │  └─────────────────────┘      │
   │                               │
   ↓                               ↓
CPU executes Task A             CPU executes Task B
```

## 22.2 Task State

Task state includes:
- **Program Counter (PC)**: Next instruction to execute
- **Stack Pointer (SP)**: Task's stack top
- **General registers**: s0-s11 (saved registers)

## 22.3 Code Structure

### 22.3.1 Structure Definitions (os.h)

```c
#include "riscv.h"

extern int os_main(void);
```

### 22.3.2 Context Structure (riscv.h)

Defined in riscv.h:
```c
struct context {
    reg_t ra;
    reg_t sp;
    reg_t s0;
    reg_t s1;
    // ... s2-s11
};
```

### 22.3.3 Task Code (user.c)

```c
void user_task0(void) {
    lib_puts("Task0: Context Switch Success !\n");
    while (1) {}
}
```

### 22.3.4 OS Main Program (os.c)

```c
#include "os.h"

#define STACK_SIZE 1024
reg_t task0_stack[STACK_SIZE];  // Task's stack
struct context ctx_os;           // OS context
struct context ctx_task;         // Task context

extern void sys_switch();

void user_task0(void) {
    lib_puts("Task0: Context Switch Success !\n");
    while (1) {}
}

int os_main(void) {
    lib_puts("OS start\n");
    
    // Initialize task context
    ctx_task.ra = (reg_t) user_task0;           ; Return address = task entry
    ctx_task.sp = (reg_t) &task0_stack[STACK_SIZE-1]; Stack top
    
    // Switch to task
    sys_switch(&ctx_os, &ctx_task);
    
    return 0;
}
```

## 22.4 Context Switch Implementation

### 22.4.1 sys.s - Assembly

```asm
# ============ Macro Definitions ==================
.macro ctx_save base
    sw ra, 0(\base)     ; Save return address
    sw sp, 4(\base)     ; Save stack pointer
    sw s0, 8(\base)     ; Save s0
    sw s1, 12(\base)    ; Save s1
    # ... s2-s11 same treatment
    sw s11, 52(\base)
.endm

.macro ctx_load base
    lw ra, 0(\base)     ; Restore return address
    lw sp, 4(\base)     ; Restore stack pointer
    lw s0, 8(\base)     ; Restore s0
    lw s1, 12(\base)    ; Restore s1
    # ... s2-s11 same treatment
    lw s11, 52(\base)
.endm
# =========================================

# Context Switch Function
# void sys_switch(struct context *old, struct context *new);
#
# Save current state to old, load new state

.globl sys_switch
.align 4
sys_switch:
    ctx_save a0          ; Save old context (a0 = old)
    ctx_load a1          ; Load new context (a1 = new)
    ret                  ; Return, effectively jump to new->ra
```

## 22.5 Switch Flow Diagram

```
                     sys_switch(&ctx_os, &ctx_task)
                                     │
                                     ↓
                         ┌───────────────────────┐
                         │ ctx_save(ctx_os)      │
                         │   Save ra → ctx_os.ra │
                         │   Save sp → ctx_os.sp │
                         │   Save s0 → ctx_os.s0 │
                         │   ...                 │
                         └───────────────────────┘
                                     │
                                     ↓
                         ┌───────────────────────┐
                         │ ctx_load(ctx_task)    │
                         │   Restore ra = ctx_task.ra │
                         │   Restore sp = ctx_task.sp │
                         │   Restore s0 = ctx_task.s0 │
                         │   ...                 │
                         └───────────────────────┘
                                     │
                                     ↓
                                 ret
                                     │
                                     ↓
                     Jump to ctx_task.ra = user_task0
                                     │
                                     ↓
                         user_task0() starts executing
```

## 22.6 Why Save These Registers?

RISC-V calling convention:
- **Caller-saved** (t0-t6, a0-a7, ra): Caller is responsible
- **Callee-saved** (s0-s11): Callee is responsible

`sys_switch` is a regular function call, the compiler will:
- Caller-saved: Since it's called via `call` instruction, ra is already saved automatically
- Callee-saved: If we want to preserve these values, we must save them manually

We save s0-s11 because tasks may use them, and task switching shouldn't destroy these values.

## 22.7 Task Stack

### 22.7.1 Stack Allocation

```
High Address
+------------------+  ← task0_stack[STACK_SIZE-1]
|  (stack top)      |  ← ctx_task.sp points here
|  ...             |
|  (stack grows down) |
|  ...             |
|                  |
+------------------+  ← task0_stack[0]
Low Address
```

### 22.7.2 Why Separate Stacks for Tasks?

If task and OS share a stack:
- When task function returns, it will return to OS code
- When task calls functions, it will pollute OS stack
- Nested calls cause confusion

## 22.8 Execution Flow Analysis

### Initial State
```
ctx_os:  (uninitialized)
ctx_task: {
    ra = user_task0,    // Task entry
    sp = &task0_stack[STACK_SIZE-1],
    s0-s11 = 0
}
```

### Execute sys_switch

1. Save current state:
```
ctx_os: {
    ra = (address after sys_switch returns),
    sp = (current sp),
    s0-s11 = (current values)
}
```

2. Load task state:
```
sp = &task0_stack[STACK_SIZE-1]  // Switch stack
ra = user_task0                    // Set return address
s0-s11 = 0                         // Initialize to 0
```

3. Execute ret instruction:
```
pc = ra = user_task0  // Jump to user_task0
```

## 22.9 Comparison with xv6

xv6-riscv's `swtch.S` is almost identical:

```asm
# xv6-riscv/swtch.S
.globl swtch
swtch:
    sd ra, 0(a0)
    sd sp, 8(a0)
    sd s0, 16(a0)
    # ... other s registers
    ld ra, 0(a1)
    ld sp, 8(a1)
    ld s0, 16(a1)
    # ... other s registers
    ret
```

Main differences:
- xv6 uses 64-bit (`sd`/`ld`)
- mini-riscv-os uses 32-bit (`sw`/`lw`)

## 22.10 Running

```bash
cd _code/mini-riscv-os/02-ContextSwitch
make
make qemu
```

Output:
```
OS start
Task0: Context Switch Success !
```

## 22.11 Summary

In this chapter we learned:
- Concept of Context Switch
- Task state components (PC, SP, s0-s11)
- Context structure definition
- sys_switch function implementation
- Need for separate task stacks
- Complete flow from OS to task switching

## 22.12 Exercises

1. Why does sys_switch save ra? What's the use?
2. Try adding s0 save and restore
3. Modify program for Task A and Task B to switch back and forth
4. Why can't we just save/restore sp?
5. Research C's `setjmp`/`longjmp` and their relationship to context switch
