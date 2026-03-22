# 26. Boot Process——From BIOS to Kernel

## 26.1 Boot Flow Overview

xv6 boot flow:

```
QEMU loads kernel/kernel
         ↓
  entry.S (kernel entry)
         ↓
  start.c (machine mode setup)
         ↓
  main.c (kernel initialization)
         ↓
  user init (first user process)
```

## 26.2 Kernel Entry (entry.S)

```asm
# kernel/entry.S
    .section .text
    .globl _entry
_entry:
    # Set up registers
    la sp, bootstacktop    ; Set stack
    tail main              ; Jump to main
    .section .data
    .globl bootstack
bootstack:
    .space 4096 * 4       ; 4KB kernel stack
    .globl bootstacktop
bootstacktop:
```

## 26.3 Kernel Initialization (start.c)

Before C code runs, setup is required:

```c
// kernel/start.c
void start() {
    // Set up machine mode timer
    // ...
    
    // Enable MIE for timer interrupt
    w_mie(r_mie() | MIE_MEIE | MIE_MTIE | MIE_MSIE);
    
    // Set return to S mode
    unsigned long x = r_mstatus();
    x &= ~MSTATUS_MPP_MASK;  ; Clear MPP
    x |= MSTATUS_MPP_S;       ; Set MPP to Supervisor
    w_mstatus(x);
    
    // Set mepc to main
    w_mepc((uint64_t)main);
    
    // Set up paging
    w_satp(MAKE_SATP(kernel_pagetable));
    
    // Flush TLB
    sfence_vma();
    
    // Return to S mode, will jump to main()
    asm volatile("mret");
}
```

## 26.4 Main Initialization (main.c)

```c
// kernel/main.c
extern char end[];  // Kernel end address

int main() {
    // Initialize various subsystems
    consoleinit();    ; Console
    printfinit();     ; printf
    pinit();          ; Process table
    binit();          ; Block I/O
    loginit();        ; Logging
    fileinit();       ; File table
    fsinit();         ; File system
    
    // Read boot parameters
    binit();
    
    // Boot process
    userinit();
    
    // Scheduler
    scheduler();
}
```

## 26.5 First User Process

```c
// kernel/proc.c
void userinit(void) {
    struct proc *p = allocproc();
    
    // Set up initial code
    p->pagetable = proc_pagetable(p);
    
    // Copy initcode to process space
    uvminit(p->pagetable, initcode, sizeof(initcode));
    p->sz = PGSIZE;
    
    // Set user stack
    p->tf->sp = PGSIZE;
    
    // Set entry point
    p->tf->epc = 0;  ; Start from address 0
    
    safestrcpy(p->name, "initcode", sizeof(p->name));
    p->state = RUNNABLE;
}
```

## 26.6 Scheduler

```c
// scheduler() selects next process to run
void scheduler(void) {
    struct proc *p;
    
    for (;;) {
        // Find runnable process
        for (p = proc; p < &proc[NPROC]; p++) {
            acquire(&p->lock);
            if (p->state == RUNNABLE) {
                p->state = RUNNING;
                p->pid = ...;
                
                // Switch to process
                swtch(&c->context, &p->context);
                
                // After process returns, continue searching
            }
            release(&p->lock);
        }
    }
}
```

## 26.7 Interrupt Return to User

```c
// kernel/trampoline.S
.globl uservec
uservec:
    # Save user state
    # ...
    ret

.globl userret
userret:
    # Restore user state
    # ...
    sret
```

## 26.8 Summary

In this chapter we learned:
- xv6 boot flow
- Kernel entry point setup
- Machine mode to supervisor mode transition
- Kernel initialization sequence
- First user process creation
- How scheduler works

## 26.9 Exercises

1. Trace xv6 boot log
2. Research meaning of mstatus.MPP
3. Why trampoline page is needed?
4. Analyze how scheduler() implements Round-Robin
5. Research how xv6 initializes page tables
