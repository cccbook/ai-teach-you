# 9. Virtual Machine——Stack-Based Instruction Set Architecture

## 9.1 Virtual Machine Introduction

A virtual machine is a software-simulated computer. It has its own instruction set, registers, and memory model, allowing programs to run without actual hardware.

c4 has a **stack-based virtual machine**, meaning:
- Operands are implicitly taken from the stack (no register specification)
- Results are implicitly pushed to the stack
- Suitable for implementing simple languages

## 9.2 c4 VM Architecture

### 9.2.1 Registers

```c
int *pc, *sp, *bp, a, cycle;
// pc: program counter
// sp: stack pointer
// bp: base pointer
// a:  accumulator
// cycle: execution cycle count
```

### 9.2.2 Memory Layout

```c
char *data;   // data segment: string constants, etc.
int *e;       // code segment emission pointer
int *le;      // code segment current pointer
int *sym;     // symbol table
int *sp;      // stack segment pointer
```

### 9.2.3 Stack Usage

```
Low addr ← [ Data ] → [ Code ] → [ Symbol ] → [ Stack ] → High addr
                   ↑
                   e, le point here

sp points to stack top, grows toward low addresses
```

## 9.3 VM Initialization

```c
poolsz = 256*1024;  // 256KB

sym  = malloc(poolsz);  // symbol table
e    = malloc(poolsz);  // code
data = malloc(poolsz);  // data
sp   = malloc(poolsz);  // stack

memset(sym,  0, poolsz);
memset(e,    0, poolsz);
memset(data, 0, poolsz);

lp = p = malloc(poolsz);  // source buffer
```

## 9.4 Instruction Interpreter

```c
cycle = 0;
while (1) {
    i = *pc++;           // fetch instruction, pc advances
    ++cycle;
    
    // execute instruction...
    
    if (i == EXIT) { 
        printf("exit(%d) cycle = %d\n", *sp, cycle); 
        return *sp; 
    }
}
```

## 9.5 Load and Store Instructions

### 9.5.1 LEA - Load Effective Address

```c
else if (i == LEA) 
    a = (int)(bp + *pc++);  // a = bp + offset
```

Use: get local variable address (relative to base pointer)

### 9.5.2 IMM - Load Immediate

```c
else if (i == IMM) 
    a = *pc++;  // a = *pc; pc++
```

### 9.5.3 LI/LC - Load Integer/Char

```c
else if (i == LI) 
    a = *(int *)a;        // a = *((int*)a)
else if (i == LC) 
    a = *(char *)a;       // a = *((char*)a)
```

### 9.5.4 SI/SC - Store Integer/Char

```c
else if (i == SI) 
    *(int *)*sp++ = a;    // *sp = a; sp++
else if (i == SC) 
    a = *(char *)*sp++ = a;  // *sp = (char)a; sp++
```

## 9.6 Stack Instruction

### 9.6.1 PSH - Push to Stack

```c
else if (i == PSH) 
    *--sp = a;  // sp--; *sp = a
```

```
Before:     After:
  sp → [xxx]      sp → [a   ]
            [yyy]           [xxx]
            [zzz]           [yyy]
                          [zzz]
```

## 9.7 Arithmetic Instructions

All binary operations follow same pattern: pop two values, compute, push result to accumulator.

```c
else if (i == ADD) 
    a = *sp++ + a;     // a = *sp + a; sp++

else if (i == SUB) 
    a = *sp++ - a;     // a = *sp - a; sp++

else if (i == MUL) 
    a = *sp++ * a;     // a = *sp * a; sp++

else if (i == DIV) 
    a = *sp++ / a;     // a = *sp / a; sp++
```

Example (calculate `3 + 4`):
```
IMM 3      ; a = 3
PSH        ; sp--; *sp = 3
IMM 4      ; a = 4
ADD        ; a = *sp + a = 3 + 4 = 7; sp++
Result: a = 7
```

## 9.8 Comparison Instructions

```c
else if (i == LT)  a = *sp++ <  a;
else if (i == GT)  a = *sp++ >  a;
else if (i == LE)  a = *sp++ <= a;
else if (i == GE)  a = *sp++ >= a;
else if (i == EQ)  a = *sp++ == a;
else if (i == NE)  a = *sp++ != a;
```

Result is 0 (false) or 1 (true).

## 9.9 Bitwise Instructions

```c
else if (i == AND) a = *sp++ &  a;
else if (i == OR)  a = *sp++ |  a;
else if (i == XOR) a = *sp++ ^  a;
else if (i == SHL) a = *sp++ << a;
else if (i == SHR) a = *sp++ >> a;
else if (i == MOD) a = *sp++ %  a;
```

## 9.10 Control Flow Instructions

### 9.10.1 JMP - Unconditional Jump

```c
else if (i == JMP) 
    pc = (int *)*pc;  // pc = *pc
```

### 9.10.2 BZ/BNZ - Conditional Jump

```c
else if (i == BZ)  
    pc = a ? pc + 1 : (int *)*pc;  // if (a == 0) pc = *pc

else if (i == BNZ) 
    pc = a ? (int *)*pc : pc + 1;  // if (a != 0) pc = *pc
```

### 9.10.3 JSR - Jump to Subroutine

```c
else if (i == JSR) { 
    *--sp = (int)(pc + 1);  // save return address
    pc = (int *)*pc;        // jump
}
```

## 9.11 Function Call Instructions

### 9.11.1 ENT - Enter Function

```c
else if (i == ENT) { 
    *--sp = (int)bp;   // save old base pointer
    bp = sp;           // set new base pointer
    sp = sp - *pc++;   // allocate local space
}
```

Equivalent to x86-64:
```asm
push rbp
mov rbp, rsp
sub rsp, frame_size
```

### 9.11.2 LEV - Leave Function

```c
else if (i == LEV) { 
    sp = bp;           // restore stack
    bp = (int *)*sp++; // restore base pointer
    pc = (int *)*sp++; // return
}
```

Equivalent to:
```asm
mov rsp, rbp
pop rbp
ret
```

### 9.11.3 ADJ - Adjust Stack

```c
else if (i == ADJ) 
    sp = sp + *pc++;  // cleanup caller's stack frame arguments
```

## 9.12 Function Call Example

Calling `printf("Hello")`:

```
Initial stack: [unused space...]
           [return addr]  ← pushed by JSR before
           [old bp]       ← pushed by ENT
           [local space]
sp →

After ENT frame_size:
sp → [local space...]

After printf:
PRTF

After ADJ 1:
sp = sp + 1  ; cleanup argument

After LEV:
return to caller
```

## 9.13 System Calls

### 9.13.1 PRTF - printf

```c
else if (i == PRTF) { 
    t = sp + pc[1];    // get argument pointer
    a = printf((char *)t[-1], t[-2], t[-3], t[-4], t[-5], t[-6]); 
}
```

Supports up to 6 arguments, format string at `t[-1]`.

### 9.13.2 MALC - malloc

```c
else if (i == MALC) 
    a = (int)malloc(*sp);  // allocate memory
```

### 9.13.3 EXIT

```c
else if (i == EXIT) { 
    printf("exit(%d) cycle = %d\n", *sp, cycle); 
    return *sp; 
}
```

## 9.14 Complete Execution Example

Source:
```c
int main() {
    return 2 + 3;
}
```

Execution trace:

| Step | Instruction | pc | a | sp | Stack |
|------|------------|-----|---|-----|-------|
| 1 | ENT 0 | +1 | - | - | ... |
| 2 | IMM 2 | +2 | 2 | - | ... |
| 3 | PSH | - | 2 | -1 | [2] |
| 4 | IMM 3 | +1 | 3 | -1 | [2] |
| 5 | ADD | - | 5 | 0 | [] |
| 6 | LEV | - | 5 | - | return |

## 9.15 Debug Mode

Use `-d` option to trace execution:

```bash
./c4 -d hello.c
```

Output:
```
1> ENT
2> IMM 10
3> PSH
4> IMM 5
5> GT
6> BZ
...
```

## 9.16 Summary

In this chapter we learned:
- c4 stack-based VM architecture
- Register roles: pc, sp, bp, a
- Load/store instructions: LEA, IMM, LI, LC, SI, SC
- Arithmetic instructions: ADD, SUB, MUL, DIV, MOD
- Comparison and bitwise instructions
- Control flow: JMP, BZ, BNZ, JSR
- Function call: ENT, LEV, ADJ
- System calls: PRTF, MALC, EXIT

## 9.17 Exercises

1. Use `-d` to trace hello.c execution
2. Manually execute a simple program (calculate 10!)
3. Research why binary ops need PSH first then compute
4. Implement a simple stack-based VM (like simplified WebAssembly)
5. Compare stack-based vs register-based architecture pros/cons
