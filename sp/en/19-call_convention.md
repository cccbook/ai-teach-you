# 19. Calling Conventions——Stack Frames and Register Usage

## 19.1 Why Calling Conventions?

Calling conventions define:
- How parameters are passed
- How return values are returned
- Which registers must be saved
- How the stack is maintained

Unified calling conventions ensure different compilers and modules can call each other.

## 19.2 RISC-V Calling Convention (ELF psABI)

### 19.2.1 Parameter Passing

Integer/pointer arguments (first 8):
```
a0 = first argument
a1 = second argument
...
a7 = eighth argument
```

More than 8 arguments: passed via stack (pushed by caller)

Floating-point arguments:
- Use fa0-fa7 if function has "double" or "float" parameters
- Otherwise use a0-a7

### 19.2.2 Return Values

```
a0 = first return value
a1 = second return value (if needed)
```

### 19.2.3 Register Classification

| Category | Registers | Description |
|----------|-----------|-------------|
| Callee-saved | s0-s11, sp, gp, tp | **Callee** is responsible |
| Caller-saved | t0-t6, a0-a7, ra | **Caller** handles |

### 19.2.4 Stack Alignment

- At entry: `sp mod 16 = 0` (16-byte aligned)
- Before `call/jal`: `sp mod 16 = 0`

## 19.3 Complete Example

### 19.3.1 C Program

```c
long long sum3(long long a, long long b, long long c) {
    return a + b + c;
}

long long main() {
    return sum3(10, 20, 30);
}
```

### 19.3.2 Assembly Analysis

```asm
sum3:
    # Function entry
    addi    sp, sp, -16      ; allocate stack frame (16-byte aligned)
    sd      ra, 8(sp)         ; save return address
    sd      s0, 0(sp)         ; save frame pointer (optional)
    
    # Function body
    # a = a0, b = a1, c = a2
    add     a0, a0, a1        ; a = a + b
    add     a0, a0, a2        ; a = a + c
    # Return value already in a0
    
    # Function exit
    ld      ra, 8(sp)         ; restore return address
    ld      s0, 0(sp)         ; restore s0
    addi    sp, sp, 16        ; deallocate stack frame
    
    jalr    x0, 0(ra)         ; return (ret pseudo-instruction)

main:
    addi    sp, sp, -16      ; allocate stack frame
    sd      ra, 8(sp)         ; save main's return address
    
    # Set arguments
    li      a0, 10            ; first argument
    li      a1, 20            ; second argument
    li      a2, 30            ; third argument
    
    jal     ra, sum3          ; call sum3
    
    # Here a0 = sum3's return value (60)
    
    ld      ra, 8(sp)         ; restore return address
    addi    sp, sp, 16        ; deallocate stack frame
    li      a0, 0             ; main return value
    jalr    x0, 0(ra)         ; return
```

## 19.4 Stack Frame Structure

### 19.4.1 Typical Stack Frame

```
High Address
+------------------+
|  Argument 8      |  ← Caller pushes (if needed)
+------------------+
|  Argument 7      |
+------------------+
|  ...             |
+------------------+
|  Argument N      |
+------------------+ <- sp' (new sp after call)
|  Saved ra        |  ← auto pushed after jal (software convention)
+------------------+
|  Saved s0 (fp)  |  ← callee-saved
+------------------+ <- fp (frame pointer)
|  Local var 1     |
+------------------+
|  Local var 2     |
+------------------+
|  ...             |
+------------------+ <- sp (current)
Low Address
```

### 19.4.2 Frame Pointer Omission

Modern compilers often omit frame pointer (`-fno-omit-frame-pointer` vs `-fomit-frame-pointer`):

```asm
# With frame pointer
sum3:
    addi    sp, sp, -8
    sd      ra, 0(sp)
    addi    fp, sp, 8      ; fp = sp + 8
    # ... use fp to access locals
    ld      ra, 0(sp)
    addi    sp, sp, 8
    ret

# Without frame pointer (more compact)
sum3:
    addi    sp, sp, -8
    sd      ra, 0(sp)
    # ... use sp + offset to access locals
    ld      ra, 0(sp)
    addi    sp, sp, 8
    ret
```

## 19.5 Complex Parameter Passing

### 19.5.1 Struct Members

```c
struct Point {
    long long x;
    long long y;
};

long long dist(struct Point p) {
    return p.x * p.x + p.y * p.y;
}
```

Because `Point` occupies 16 bytes (2 int64s), a0 and a1 are used:

```asm
dist:
    # a0 = p.x (loaded by caller)
    # a1 = p.y (loaded by caller)
    mul     a0, a0, a0
    mul     a1, a1, a1
    add     a0, a0, a1
    ret
```

### 19.5.2 Large Structs

Structs larger than 16 bytes:
- Caller allocates memory
- Pass pointer in a0 (as implicit first argument)
- Remaining space uses a1, a2...

```c
struct Big {
    long long a, b, c, d;
};

void init(struct Big *p) {
    p->a = 1;
    p->b = 2;
    // ...
}
```

### 19.5.3 Variadic Functions

```c
int sum(int count, ...) {
    va_list args;
    va_start(args, count);
    int total = 0;
    for (int i = 0; i < count; i++) {
        total += va_arg(args, int);
    }
    va_end(args);
    return total;
}
```

va_list is typically implemented as a stack pointer array.

## 19.6 Recursive Functions

### 19.6.1 Fibonacci Sequence

```c
long long fib(long long n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
```

```asm
fib:
    # Stack frame allocation
    addi    sp, sp, -24     ; 24 bytes
    sd      ra, 16(sp)       ; save return address
    sd      s0, 8(sp)        ; save s0
    addi    s0, sp, 24       ; set frame pointer
    
    # Save parameter to stack (optional, needed for nested calls)
    sd      a0, -16(s0)      ; save n
    
    # if (n <= 1)
    li      t0, 1
    ble     a0, t0, .Lbase   ; if (n <= 1) goto .Lbase
    
    # fib(n-1)
    ld      a0, -16(s0)
    addi    a0, a0, -1
    jal     ra, fib          ; call fib(n-1)
    # Return value in a0 (result1)
    sd      a0, -24(s0)      ; save result1
    
    # fib(n-2)
    ld      a0, -16(s0)
    addi    a0, a0, -2
    jal     ra, fib          ; call fib(n-2)
    # Return value in a0 (result2)
    
    # Add result1
    ld      t0, -24(s0)
    add     a0, a0, t0       ; a0 = result2 + result1
    
    j       .Lreturn

.Lbase:
    # return n
    ld      a0, -16(s0)      ; a0 = n

.Lreturn:
    # Stack frame deallocation
    ld      ra, 16(sp)       ; restore ra
    ld      s0, 8(sp)        ; restore s0
    addi    sp, sp, 24        ; deallocate stack frame
    ret
```

## 19.7 Leaf vs Non-Leaf Functions

### 19.7.1 Leaf Functions

Leaf functions are functions that don't call other functions:

```asm
# Optimized version (assuming t0, t1 are caller-saved)
leaf_func:
    # Can use t0-t6 here, no need to save
    add     a0, a0, a1
    # Can return directly if not using stack
    ret
```

### 19.7.2 Non-Leaf Functions

Non-leaf functions call other functions:

```asm
non_leaf:
    addi    sp, sp, -8       ; must save ra
    sd      ra, 0(sp)
    jal     other_func
    ld      ra, 0(sp)
    addi    sp, sp, 8
    ret
```

## 19.8 Register Save Responsibility

### 19.8.1 Caller-Saved Registers

Don't need to save before use, may have changed after calling other functions:
```
t0-t6 (7 registers)
a0-a7 (8 registers)
ra (return address)
```

### 19.8.2 Callee-Saved Registers

Must save before use, must restore before return:
```
s0-s11 (12 registers)
sp (stack pointer)
gp, tp (per ABI)
```

```asm
example:
    addi    sp, sp, -16      ; allocate space
    sd      s0, 8(sp)        ; save s0
    sd      s1, 0(sp)        ; save s1
    
    # Use s0, s1...
    
    ld      s0, 8(sp)        ; restore s0
    ld      s1, 0(sp)        ; restore s1
    addi    sp, sp, 16        ; restore sp
    ret
```

## 19.9 Stack Overflow Detection

### 19.9.1 Manual Detection

```c
void *get_sp() {
    long long dummy;
    return &dummy;
}

void safe_function() {
    void *sp_start = get_sp();
    // ... use stack ...
    void *sp_end = get_sp();
    if (sp_end > sp_start + STACK_LIMIT) {
        // Stack overflow!
    }
}
```

### 19.9.2 GCC Stack Protection

```bash
gcc -fstack-protector -S foo.c
```

Inserts stack canary detection.

## 19.10 Summary

In this chapter we learned:
- RISC-V calling convention basics
- Parameter passing (first 8 use a0-a7)
- Return value passing (a0-a1)
- Register save responsibility (callee vs caller saved)
- Stack frame structure and alignment
- Leaf and non-leaf functions
- Recursive function implementation

## 19.11 Exercises

1. Write a recursive function and analyze the generated assembly
2. Implement a function call with 10 arguments
3. Compare assembly with/without frame pointer
4. Research variadic function (`va_start`) implementation
5. Trace a system call stack in mini-riscv-os or xv6
