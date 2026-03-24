# 31. Scheduler——CFS and Real-Time Scheduling

## 31.1 Scheduling Basics

The scheduler decides which process runs next:

```
┌─────────────────────────────────────────────────────────┐
│                    Scheduler                            │
│  ┌─────────────────────────────────────────────────┐  │
│  │ 1. Select highest priority process               │  │
│  │ 2. If same priority, Round-Robin                │  │
│  │ 3. When time slice expires, move to lower priority│ │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 31.2 xv6 Scheduler

### 31.2.1 scheduler()

```c
void
scheduler(void) {
    struct proc *p;
    
    for (;;) {
        // Enable interrupts
        intr_on();
        
        for (p = proc; p < &proc[NPROC]; p++) {
            acquire(&p->lock);
            if (p->state == RUNNABLE) {
                // Select this process
                p->state = RUNNING;
                p->pid = // ...
                
                // Switch to process
                swtch(&c->context, &p->context);
                
                // After process returns, continue loop
            }
            release(&p->lock);
        }
    }
}
```

## 31.3 Context Switch

### 31.3.1 swtch.S

```asm
.globl swtch
swtch:
    sd ra, 0(a0)
    sd sp, 8(a0)
    sd s0, 16(a0)
    sd s1, 24(a0)
    // ... save other s registers
    ld ra, 0(a1)
    ld sp, 8(a1)
    ld s0, 16(a1)
    ld s1, 24(a1)
    // ... restore other s registers
    ret
```

## 31.4 Scheduling Triggers

### 31.4.1 When Does Scheduling Happen?

1. **Timer interrupt**: Time slice expires, forcibly yield CPU
2. **Blocking**: Process calls sleep() waiting for I/O
3. **Yielding**: Process voluntarily calls yield()

### 31.4.2 yield()

```c
void
yield(void) {
    struct proc *p = myproc();
    acquire(&p->lock);
    p->state = RUNNABLE;
    sched();
    release(&p->lock);
}
```

### 31.4.3 sched()

```c
void
sched(void) {
    int intena;
    struct proc *p = myproc();
    
    if (p->state == RUNNING)
        panic("sched running");
    if (intr_get())
        panic("sched interruptible");
    
    intena = mycpu()->noff;
    if (intena == 1 && mycpu()->intena)
        panic("sched interruptible");
    
    if (p->state == RUNNABLE)
        p->ctime = ticks;  ; Record wait start time
    
    swtch(&p->context, &c->context);
}
```

## 31.5 Time Slice

### 31.5.1 Timer Interrupt

```c
void
clockintr(void) {
    if ((r_scause() == 0x80000000 || r_scause() == 0x80000005) &&
        ticks % TICK == 0) {
        if (cpuid() == 0) {
            // Update clock
        }
        // Send software interrupt to all CPUs
    }
}
```

### 31.5.2 Preemption

```c
void
usertrap(void) {
    // ...
    if (r_scause() == 0x80000007) {
        // Timer interrupt
        if (cpuid() == 0)
            clockintr();
        intr_on();
        
        // Force yield CPU
        yield();
    }
    // ...
}
```

## 31.6 Sleep and Wakeup

### 31.6.1 sleep()

```c
void
sleep(void *chan, struct spinlock *lk) {
    struct proc *p = myproc();
    
    // Must hold lock or already hold p->lock
    acquire(&p->lock);
    release(lk);
    
    p->chan = chan;      ; Channel to wait on
    p->state = SLEEPING; ; Set to sleeping
    sched();              ; Yield CPU
    
    // After waking, clear state
    p->chan = 0;
    
    release(&p->lock);
    acquire(lk);
}
```

### 31.6.2 wakeup()

```c
void
wakeup(void *chan) {
    struct proc *p;
    
    for (p = proc; p < &proc[NPROC]; p++) {
        if (p != myproc()) {
            acquire(&p->lock);
            if (p->state == SLEEPING && p->chan == chan) {
                p->state = RUNNABLE;  ; Wake up
            }
            release(&p->lock);
        }
    }
}
```

## 31.7 Typical Sleep Pattern

```c
// Disk I/O wait
void
bread(void) {
    acquire(&bache.lock);
    while (b->flags & B_DIRTY) {
        sleep(b, &bache.lock);
    }
    // ...
}
```

## 31.8 Comparison with Linux CFS

| Feature | xv6 | Linux CFS |
|---------|-----|-----------|
| Scheduling algorithm | Simple round-robin | Completely Fair Scheduler |
| Time slice | Fixed | Dynamic |
| Priority | Fixed | Dynamic adjustment |
| Implementation complexity | Low | High |

## 31.9 Summary

In this chapter we learned:
- How xv6 scheduler works
- scheduler() implementation
- How swtch works
- Scheduling triggers
- Time slice and timer interrupts
- sleep() and wakeup()
- Comparison with Linux CFS

## 31.10 Exercises

1. Implement multi-level feedback queue scheduling
2. Implement O(1) scheduler
3. Research real-time scheduling (SCHED_FIFO, SCHED_RR)
4. Implement fair scheduling (equal time slice per process)
5. Research NUMA system scheduling considerations
