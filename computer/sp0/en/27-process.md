# 27. Process Management——fork, exec, and wait

## 27.1 UNIX Process Model

One of the core concepts of UNIX is "everything is a file" and "every program is a process."

### 27.1.1 Process System Calls

| System Call | Description |
|-------------|-------------|
| fork() | Create new process (clone current process) |
| exec() | Execute new program (replace current process) |
| wait() | Wait for child process to exit |
| exit() | End current process |

## 27.2 fork() Implementation

fork() creates a new process:

```c
// kernel/sysproc.c
int
sys_fork(void) {
    return fork();
}

// kernel/proc.c
int
fork(void) {
    struct proc *np;
    
    // Allocate new process
    np = allocproc();
    
    // Copy user memory
    if (uvmcopy(p->pagetable, np->pagetable, p->sz) < 0) {
        freeproc(np);
        release(&np->lock);
        return -1;
    }
    np->sz = p->sz;
    
    // Copy user register state
    *np->tf = *p->tf;
    
    // Child has different return value
    np->tf->a0 = 0;  ; fork() returns 0 to child
    
    // Set new process name
    safestrcpy(np->name, p->name, sizeof(p->name));
    
    np->state = RUNNABLE;
    
    return np->pid;  ; Parent returns child's PID
}
```

### 27.2.1 What fork() Does

1. Allocate new proc structure
2. Allocate new kernel stack
3. Copy user page table
4. Copy register state (tf)
5. Child: fork() returns 0
6. Parent: fork() returns child PID

## 27.3 exec() Implementation

exec() executes a new program:

```c
// kernel/sysfile.c
int
sys_exec(void) {
    char path[MAXPATH];
    char *argv[MAXARG];
    
    // Get path and arguments
    if (argstr(0, path) < 0 || argint(1, (int*)&argv) < 0) {
        return -1;
    }
    
    return exec(path, argv);
}

// kernel/proc.c
int
exec(char *path, char **argv) {
    struct inode *ip;
    struct proghdr ph;
    pagetable_t pagetable;
    
    // Read ELF file
    ip = namei(path);
    el = (struct elfhdr*)pgroot;
    if (readi(ip, 0, (uint64)el, 0, sizeof(*el)) != sizeof(*el))
        goto bad;
    
    // Load each program segment
    for (i=0, off=sizeof(*el); i<el->phnum; i++) {
        readi(ip, 0, (uint64)ph, off, sizeof(ph));
        if (ph.type != ELF_PROG_LOAD) continue;
        if (ph.vaddr + ph.memsz < ph.vaddr) goto bad;
        if (ph.vaddr % PGSIZE != 0) goto bad;
        
        // Allocate and copy memory
        if ((sz = uvmalloc(pagetable, sz, ph.vaddr + ph.memsz)) == 0) goto bad;
    }
    
    // Set new page table
    p->pagetable = pagetable;
    p->sz = sz;
    
    // Set program entry
    p->tf->epc = el->entry;
    
    return 0;
}
```

### 27.2.2 What exec() Does

1. Read ELF file
2. Verify ELF format
3. Create new page table
4. Load each program segment into memory
5. Set program entry point
6. Set command line arguments

## 27.4 wait() Implementation

wait() waits for child process to exit:

```c
// kernel/proc.c
int
wait(uint64 addr) {
    struct proc *p;
    int havekids, pid;
    
    for (;;) {
        // Find a process with children
        havekids = 0;
        for (p = proc; p < &proc[NPROC]; p++) {
            acquire(&p->lock);
            if (p->parent == current) {
                havekids = 1;
                if (p->state == ZOMBIE) {
                    // Found terminated child
                    pid = p->pid;
                    if (addr && copyout(current->pagetable, addr, &p->xstate, sizeof(p->xstate)) < 0) {
                        release(&p->lock);
                        return -1;
                    }
                    freeproc(p);
                    release(&p->lock);
                    return pid;
                }
            }
            release(&p->lock);
        }
        
        // No children, return error
        if (!havekids) return -1;
        
        // Sleep, waiting for child
        sleep(current, &wait_lock);
    }
}
```

## 27.5 Process States

```c
enum procstate {
    UNUSED,      // Unused
    USED,        // Allocated
    SLEEPING,    // Sleeping (waiting for I/O)
    RUNNABLE,    // Runnable (in memory)
    RUNNING,     // Running
    ZOMBIE       // Zombie (terminated, waiting for parent to reap)
};
```

## 27.6 Process Lifecycle

```
        fork()                   exit()
UNUSED ─────→ USED ─────→ SLEEPING ─────┐
    ↑            ↓              ↑        │
    │         exec()            │        │
    │            ↓               │        │
    │         RUNNABLE ───→ RUNNING ────┤
    │              ↑                       │
    │              │sched()                │
    │              └───────────────────────┤
    │                                     ↓
    │        ┌──────────────────────────┐ │
    │        │          ZOMBIE          │ │
    │        └──────────────────────────┘ │
    │                  ↑                 │
    └──────────────────┴────────────────┘
                    wait()
```

## 27.7 Typical Usage Patterns

### 27.7.1 How Shell Works

```c
// Simplified shell
if (fork() == 0) {
    // Child: execute command
    exec(cmd, argv);
    exit(1);  ; If exec fails
} else {
    // Parent: wait for command to finish
    wait(0);
}
```

### 27.7.2 Pipes

```c
// Pipe implementation uses fork
int p[2];
pipe(p);

if (fork() == 0) {
    // Child: write to pipe
    close(1);      ; Close stdout
    dup(p[1]);     ; Copy write end to stdout
    close(p[0]);   ; Close read end
    close(p[1]);   ; Close write end
    exec(cmd1);
} else {
    // Parent: read from pipe
    close(0);      ; Close stdin
    dup(p[0]);     ; Copy read end to stdin
    close(p[0]);   ; Close read end
    close(p[1]);   ; Close write end
    wait(0);
    exec(cmd2);
}
```

## 27.8 Summary

In this chapter we learned:
- UNIX process model
- fork() implementation (clone process)
- exec() implementation (execute new program)
- wait() implementation (wait for child)
- Process state machine
- Process lifecycle

## 27.9 Exercises

1. Implement a simple shell
2. Research why fork() returns different values
3. Implement pipe() system call
4. Research necessity of ZOMBIE state
5. Implement dup() system call
