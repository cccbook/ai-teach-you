# 30. Memory Management——Paging and Swapping

## 30.1 Paging Basics

Paging divides virtual memory into fixed-size chunks (pages):

```
Virtual Memory                    Physical Memory
┌──────────────┐            ┌──────────────┐
│ Page 0       │ ────────→ │ Frame 3     │
│ Page 1       │ ────────→ │ Frame 1     │
│ Page 2       │ ────────→ │ Frame 5     │
│ Page 3       │            │ Frame 2     │
└──────────────┘            └──────────────┘
      4KB                        4KB
```

## 30.2 RISC-V Paging

### 30.2.1 Page Size

xv6 uses 4KB pages (Sv39).

### 30.2.2 Page Table Entry (PTE)

```c
// Page table entry format
#define PTE_V  0x001  // Valid
#define PTE_R  0x002  // Read
#define PTE_W  0x004  // Write
#define PTE_X  0x008  // Execute
#define PTE_U  0x010  // User
#define PTE_G  0x020  // Global
#define PTE_A  0x040  // Accessed
#define PTE_D  0x080  // Dirty
```

### 30.2.3 Three-Level Paging

```
VPN[2] (9 bits) ──→ Second level page directory (512 entries)
VPN[1] (9 bits) ──→ First level page directory (512 entries)
VPN[0] (9 bits) ──→ Page frame number (PPN)
Offset (12 bits) ──→ Page offset
```

## 30.3 xv6 Page Table Management

### 30.3.1 Create Process Page Table

```c
pagetable_t
proc_pagetable(struct proc *p) {
    pagetable_t pagetable;
    
    // Allocate first-level page directory
    pagetable = uvmcreate();
    if (pagetable == 0) return 0;
    
    // Map trampoline page (for interrupts)
    if (mappages(pagetable, TRAMPOLINE, PGSIZE, 
                 (uint64)trampoline, PTE_R | PTE_X) < 0) {
        uvmfree(pagetable, 0);
        return 0;
    }
    
    // Map trap frame page
    if (mappages(pagetable, TRAPFRAME, PGSIZE, 
                 (uint64)p->tf, PTE_R | PTE_W) < 0) {
        // ...
    }
    
    return pagetable;
}
```

### 30.3.2 uvmcreate

```c
pagetable_t
uvmcreate(void) {
    pagetable_t pagetable;
    pagetable = (pagetable_t) kalloc();
    if (pagetable == 0) return 0;
    memset(pagetable, 0, PGSIZE);
    return pagetable;
}
```

## 30.4 Memory Allocation

### 30.4.1 sbrk

```c
int
sys_sbrk(void) {
    int addr;
    int n;
    
    if (argint(0, &n) < 0) return -1;
    
    addr = myproc()->sz;
    if (n < 0) {
        if (growproc(n) < 0) return -1;
    } else if (growproc(n) < 0) {
        return -1;
    }
    return addr;
}

int
growproc(int n) {
    uint64 sz = p->sz;
    if (n > 0) {
        if ((sz = uvmalloc(p->pagetable, sz, sz + n)) == 0) {
            return -1;
        }
    } else if (n < 0) {
        sz = uvmdealloc(p->pagetable, sz, sz + n);
    }
    p->sz = sz;
    return 0;
}
```

## 30.5 Page Fault Handling

### 30.5.1 Trap Handling

```c
void
usertrap(void) {
    // ...
    if (r_scause() == 8) {
        // System call
        syscall();
    } else if (r_scause() == 13 || r_scause() == 15) {
        // Load/Store page fault
        uint64 va = r_stval();
        if (va >= p->sz || 
            (r_scause() == 15 && !uva_to_pa(p->pagetable, va))) {
            p->killed = 1;
        }
    }
    // ...
}
```

## 30.6 Kernel and User Space

### 30.6.1 Memory Layout

```
┌────────────────────────────────────────┐
│ USYSCALL (TRAPFRAME)                  │ 0x3fffff000
├────────────────────────────────────────┤
│                                        │
│     User space                         │ 0 ... p->sz
│                                        │
├────────────────────────────────────────┤
│     Gap                                │
├────────────────────────────────────────┤
│                                        │
│     Kernel space                       │ 0x80000000 ...
│                                        │
└────────────────────────────────────────┘
```

### 30.6.2 Kernel Page Table

Kernel has separate page table:
- Maps all physical memory
- Inaccessible to applications

## 30.7 Copy-on-Write (COW)

xv6 doesn't implement COW, but the concept is:

### 30.7.1 fork() Optimization

```c
// Original fork:
uvmcopy(p->pagetable, np->pagetable, p->sz);  ; Full copy

// COW fork:
// 1. Copy page table only, not data
// 2. Set both parent and child page tables to read-only
// 3. Page fault on write
// 4. Page fault handler: allocate new page, copy, set writable
```

## 30.8 Swapping

xv6 doesn't implement swapping. If there's not enough memory, it results in out-of-memory errors.

## 30.9 Summary

In this chapter we learned:
- Basic concepts of paging
- RISC-V Sv39 paging mechanism
- xv6 page table management
- sbrk() and growproc()
- Page fault handling
- Kernel/user space separation

## 30.10 Exercises

1. Research Sv48 and Sv57 paging
2. Implement Copy-on-Write fork
3. Implement mmap() system call
4. Compare paging and segmentation
5. Research TLB flush strategies
