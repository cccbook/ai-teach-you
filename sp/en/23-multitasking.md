# 23. Multitasking——Task Switching and Scheduling

## 23.1 From Single-Task to Multitasking

Single-task systems can only run one program at a time. Multitasking systems can run multiple tasks simultaneously, using fast switching to create the illusion of "simultaneous execution."

```
Single-task:
|----------- task1 -----------|
Time ─────────────────────────→

Multitasking (cooperative):
|---- task1 ----||---- task2 ----||---- task1 ----|
Time ─────────────────────────────────────────────→
```

## 23.2 Cooperative vs Preemptive Multitasking

| Type | Description | Advantage | Disadvantage |
|------|-------------|-----------|--------------|
| Cooperative | Tasks voluntarily yield CPU | Simple | Can be blocked by buggy tasks |
| Preemptive | OS forces switching | Fair and responsive | Complex (needs locks) |

mini-riscv-os 03-MultiTasking is cooperative multitasking.

## 23.3 Task Management Structure

### 23.3.1 Task Control Block (TCB)

```c
// task.h
#define MAX_TASKS 4
#define STACK_SIZE 1024

struct task {
    reg_t sp;              // Stack pointer
    reg_t stack[STACK_SIZE];  // Separate stack
};

struct task tasks[MAX_TASKS];
int taskTop = 0;           // Current task count
```

### 23.3.2 Task Initialization

```c
// user.c
void user_task0(void) {
    lib_puts("Task0: begin\n");
    while (1) {
        lib_puts("Task0: running...\n");
        for (volatile int i = 0; i < 100000; i++);
    }
}

void user_task1(void) {
    lib_puts("Task1: begin\n");
    while (1) {
        lib_puts("Task1: running...\n");
        for (volatile int i = 0; i < 100000; i++);
    }
}

void user_init(void) {
    tasks[0].sp = (reg_t) &tasks[0].stack[STACK_SIZE-1];
    tasks[0].sp = (reg_t) &tasks[1].stack[STACK_SIZE-1];
    
    taskTop = 2;
    
    tasks[0].sp = (reg_t) &tasks[0].stack[STACK_SIZE-1];
    task[1].sp = (reg_t) &tasks[1].stack[STACK_SIZE-1];
}
```

## 23.4 Task Switching

### 23.4.1 Task Jump

```c
// task.h
extern void task_go(struct context *ctx);

void task_go(struct context *ctx) {
    sys_switch(&ctx_os, ctx);
}
```

### 23.4.2 Task Return (Voluntary CPU Yield)

```c
// Call this to return to OS after task completes
extern void os_kernel(void);

void task_exit(void) {
    sys_switch(&ctx_task, &ctx_os);
}
```

## 23.5 Scheduler

### 23.5.1 Round-Robin Scheduling

Round-Robin (time-slice rotation) is the simplest scheduling algorithm:

```c
int current_task = 0;

while (1) {
    lib_puts("OS: Activate next task\n");
    task_go(&tasks[current_task]);  // Switch to task
    lib_puts("OS: Back to OS\n");
    
    // Next task (circular)
    current_task = (current_task + 1) % taskTop;
    lib_puts("\n");
}
```

### 23.5.2 Round-Robin Diagram

```
Task 0 ────────────────── task_go ──────────────────→ return
         (executes for a while then yields)

Task 1 ────────────────── task_go ──────────────────→ return
         (executes for a while then yields)

Task 0 ────────────────── task_go ──────────────────→ return
         ...
```

## 23.6 Problems with Cooperative Multitasking

### 23.6.1 Task Doesn't Yield CPU

If a task enters an infinite loop, OS cannot intervene:

```c
void bad_task(void) {
    while (1) {  // Never calls task_exit!
        // Do work
    }
}
```

### 23.6.2 Task May Forget to Yield

Even if task isn't malicious, it may forget to yield CPU:

```c
void task_with_big_loop(void) {
    for (int i = 0; i < 1000000000; i++) {  // Long computation
        // May forget to yield
    }
    task_exit();
}
```

## 23.7 Complete Task Switching Flow

### 23.7.1 OS Startup

```c
void os_start() {
    lib_puts("OS start\n");
    user_init();  // Initialize tasks
}
```

### 23.7.2 OS Main Loop

```c
int os_main(void) {
    os_start();
    
    int current_task = 0;
    while (1) {
        lib_puts("OS: Activate next task\n");
        task_go(&tasks[current_task]);
        lib_puts("OS: Back to OS\n");
        current_task = (current_task + 1) % taskTop;
        lib_puts("\n");
    }
}
```

### 23.7.3 Task Execution

```c
void user_task0(void) {
    lib_puts("Task0: begin\n");
    while (1) {
        lib_puts("Task0: running...\n");
        // Delay
        for (volatile int i = 0; i < 100000; i++);
        // Task returns to OS
        task_exit();
    }
}
```

## 23.8 Execution Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ os_main()                                              │
│   os_start() → user_init()                            │
│                                                         │
│   while (1) {                                          │
│       task_go(&tasks[current_task]);  ─────────┐       │
│       ...                                      │       │
│       current_task = (current_task + 1) % 2;   │       │
│   }                                             │       │
└─────────────────────────────────────────────────┼───────┘
                                                  │
                              ┌───────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│ sys_switch(&ctx_os, &tasks[current_task])              │
│   1. Save OS context to ctx_os                        │
│   2. Load tasks[current_task] context                 │
│   3. ret → Jump to task                              │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│ user_task0()                                           │
│   lib_puts("Task0: running...")                        │
│   Delay                                                │
│   task_exit() → sys_switch(&ctx_task, &ctx_os)        │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│ sys_switch(&ctx_task, &ctx_os)                         │
│   1. Save task context to ctx_task                   │
│   2. Load ctx_os context                             │
│   3. ret → Return to os_main while loop              │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
                         Return to OS
```

## 23.9 Importance of Delay Function

```c
for (volatile int i = 0; i < 100000; i++);
```

`volatile` is necessary because:
- Prevents compiler from optimizing away the entire loop
- Ensures loop actually executes

## 23.10 Running

```bash
cd _code/mini-riscv-os/03-MultiTasking
make
make qemu
```

Output:
```
OS start
OS: Activate next task
Task0: begin
Task0: running...
OS: Back to OS

OS: Activate next task
Task1: begin
Task1: running...
OS: Back to OS

OS: Activate next task
Task0: running...
OS: Back to OS
...
```

## 23.11 Summary

In this chapter we learned:
- Transition from single-task to multitasking
- Cooperative vs preemptive multitasking
- Task Control Block (TCB) structure
- Round-Robin scheduling algorithm
- Complete task switching flow
- Problems with cooperative multitasking

## 23.12 Exercises

1. Implement priority scheduling (high priority tasks run first)
2. Why need separate task stacks?
3. Implement delay measurement for task CPU yield
4. What happens if a task never calls task_exit?
5. Research "starvation" problem in operating systems
