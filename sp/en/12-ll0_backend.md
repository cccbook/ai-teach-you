# 12. ll0 Backend——LLVM IR to RISC-V Assembly

## 12.1 What is a Compiler Backend?

Compiler backend is responsible for converting intermediate representation (IR) to target machine code.

```
Frontend (Clang)     Backend (ll0c/llc)
   ↓                ↓
C → IR ──────→ Assembly/Machine Code
```

## 12.2 What is ll0c?

ll0c is LLVM IR to RISC-V assembly converter in cpy0 project.

Location: [_code/cpy0/ll0/](../_code/cpy0/ll0/)

## 12.3 Using ll0c

```bash
# Basic usage
./ll0/ll0c/ll0c input.ll -o output.s

# Or use LLVM's LLC
llc fact.ll -o fact.s --mtriple=riscv64-unknown-elf
```

## 12.4 RISC-V Instruction Set Basics

RISC-V is Reduced Instruction Set Computer:
- Fixed instruction length (32-bit)
- Many registers (32)
- Load/store architecture (memory only via load/store)

### 12.4.1 RISC-V Registers

| Register | Alias | Purpose | Saved |
|---------|-------|---------|-------|
| x0 | zero | Constant 0 | - |
| x1 | ra | Return address | - |
| x2 | sp | Stack pointer | Yes |
| x3 | gp | Global pointer | - |
| x4 | tp | Thread pointer | - |
| x5-x7 | t0-t2 | Temporary | No |
| x8 | s0/fp | Saved / Frame pointer | Yes |
| x9 | s1 | Saved | Yes |
| x10-x17 | a0-a7 | Args/Return | No |
| x18-x27 | s2-s11 | Saved | Yes |
| x28-x31 | t3-t6 | Temporary | No |

### 12.4.2 Basic Instruction Formats

```
R type: rd = rs1 op rs2
+-------+-------+-------+-------+-------+-------+
| 31-25 | 24-20 | 19-15 | 14-12 |  11-7 |  6-0 |
| funct7| rs2   | rs1   | funct3| rd    | opcode|
+-------+-------+-------+-------+-------+-------+

I type: rd = rs1 op imm
+-------+-------+-------+-------+-------+-------+
|  11-10|  9-5  | 4-0   |  12   |  11-7 |  6-0 |
|       | rs2   | rs1   | imm11 | rd    | opcode|
+-------+-------+-------+-------+-------+-------+

S type: mem[rs1+imm] = rs2
+-------+-------+-------+-------+-------+-------+
| 31-25 | 24-20 | 19-15 | 11-7  |  12   |  6-0 |
| imm11 | rs2   | rs1   | imm11 | imm4  | opcode|
+-------+-------+-------+-------+-------+-------+
```

## 12.5 Common RISC-V Instructions

### 12.5.1 Arithmetic Instructions

```asm
# Addition (R type)
add  a0, a0, a1    ; a0 = a0 + a1

# Subtraction
sub  a0, a0, a1    ; a0 = a0 - a1

# Immediate addition (I type)
addi sp, sp, -16   ; sp = sp - 16

# Multiplication (needs M extension)
mul  a0, a0, a1    ; a0 = a0 * a1

# Division (needs M extension)
div  a0, a0, a1    ; a0 = a0 / a1
```

### 12.5.2 Logic Instructions

```asm
# AND
and  a0, a0, a1    ; a0 = a0 & a1
andi a0, a0, 0xFF  ; a0 = a0 & 0xFF

# OR
or   a0, a0, a1    ; a0 = a0 | a1

# XOR
xor  a0, a0, a1    ; a0 = a0 ^ a1
```

### 12.5.3 Shift Instructions

```asm
# Left shift
sll  a0, a0, a1    ; a0 = a0 << a1
slli a0, a0, 2     ; a0 = a0 << 2

# Logical right shift
srl  a0, a0, a1    ; a0 = a0 >> a1
srli a0, a0, 2     ; a0 = a0 >> 2

# Arithmetic right shift (preserves sign)
sra  a0, a0, a1
srai a0, a0, 2
```

### 12.5.4 Comparison Instructions

```asm
# Set on Less Than
slt  a0, a0, a1    ; a0 = (a0 < a1) ? 1 : 0
slti a0, a0, 10    ; a0 = (a0 < 10) ? 1 : 0

# Unsigned comparison
sltu a0, a0, a1
sltiu a0, a0, 10
```

### 12.5.5 Load/Store Instructions

```asm
# Load (I type)
lw   a0, 0(sp)     ; a0 = *((int*)(sp + 0))
lui  a0, 0x10000    ; a0 = 0x10000 << 12

# Store (S type)
sw   a0, 0(sp)     ; *((int*)(sp + 0)) = a0
```

### 12.5.6 Branch Instructions (B type)

```asm
# Branch equal
beq  a0, a1, .L1   ; if (a0 == a1) goto .L1

# Branch not equal
bne  a0, a1, .L1

# Branch less than (signed)
blt  a0, a1, .L1   ; if (a0 < a1) goto .L1
bge  a0, a1, .L1   ; if (a0 >= a1) goto .L1

# Branch less than (unsigned)
bltu a0, a1, .L1
bgeu a0, a1, .L1
```

### 12.5.7 Jump Instructions (J type)

```asm
# Unconditional jump (J type)
jal  ra, .L1       ; ra = pc + 4; goto .L1

# Jump and Link (function call)
jal  ra, callee    ; ra = pc + 4; goto callee

# Jump Register (R type)
jalr ra, 0(callee) ; ra = pc + 4; goto *callee
ret                 ; jalr x0, 0(ra)
```

## 12.6 LLVM IR to RISC-V Mapping

### 12.6.1 Addition

LLVM IR:
```llvm
%add = add i64 %a, %b
```

RISC-V:
```asm
add a0, a0, a1    ; assuming a = a0, b = a1, result in a0
```

### 12.6.2 Conditional Branch

LLVM IR:
```llvm
%cmp = icmp slt i64 %a, %b
br i1 %cmp, label %then, label %else
```

RISC-V:
```asm
    blt a0, a1, .then    ; if (a < b) goto .then
    j .else
.then:
    ; then block
.else:
    ; else block
```

### 12.6.3 Function Call

LLVM IR:
```llvm
%ret = call i64 @callee(i64 %arg1, i64 %arg2)
```

RISC-V:
```asm
    mv a0, t0       ; move arg to a0
    mv a1, t1       ; move arg to a1
    jal ra, callee  ; call function
    ; return value in a0
```

## 12.7 Calling Conventions

RISC-V calling conventions:

### 12.7.1 Parameter Passing

- First 8 integer args: a0-a7
- More args: via stack
- Return value: a0-a1

### 12.7.2 Register Classification

| Class | Registers | Description |
|------|-----------|-------------|
| Saved (callee-saved) | s0-s11, sp, gp, tp | Function responsible for saving |
| Caller (caller-saved) | t0-t6, a0-a7, ra | Function doesn't need to save |

### 12.7.3 Stack Frame

```asm
; Function entry
frame:
    addi sp, sp, -frame_size   ; allocate stack frame
    sw ra, -4(sp)              ; save return address
    sw s0, -8(sp)              ; save s0

; Function exit
    lw ra, -4(sp)
    lw s0, -8(sp)
    addi sp, sp, frame_size    ; deallocate stack frame
    ret
```

## 12.8 Practical Example

Complete LLVM IR to RISC-V assembly:

LLVM IR:
```llvm
define i64 @fact(i64 %n) {
entry:
  %cmp = icmp sle i64 %n, 1
  br i1 %cmp, label %then, label %else

then:
  ret i64 1

else:
  %sub = sub i64 %n, 1
  %call = call i64 @fact(i64 %sub)
  %mul = mul i64 %n, %call
  ret i64 %mul
}
```

RISC-V Assembly:
```asm
    .text
    .globl fact
    .align 2
fact:
    ; n in a0
    li t0, 1
    ble a0, t0, .LBB0_1   ; if (n <= 1) goto .LBB0_1
    
    ; else branch
    addi sp, sp, -16      ; allocate stack frame
    sw ra, 12(sp)         ; save return address
    sw a0, 8(sp)          ; save n
    
    addi a0, a0, -1        ; n - 1
    jal ra, fact           ; recursive call
    
    lw t0, 8(sp)           ; restore n
    mul a0, t0, a0          ; n * fact(n-1)
    
    lw ra, 12(sp)          ; restore return address
    addi sp, sp, 16        ; deallocate stack frame
    ret
    
.LBB0_1:                  ; then branch
    li a0, 1              ; return 1
    ret
```

## 12.9 Using LLC Tool

LLVM's `llc` tool for testing:

```bash
# Compile IR to RISC-V using LLC
llc -march=riscv64 fact.ll -o fact.s

# Specify ABI
llc -march=riscv64 -mattr=+m,+f,+c fact.ll -o fact.s

# Show optimized assembly
llc -march=riscv64 -O2 fact.ll -o fact_O2.s
```

## 12.10 Summary

In this chapter we learned:
- Compiler backend concept
- RISC-V instruction set basics
- Instruction format types (R, I, S, B, J)
- LLVM IR to RISC-V mapping
- RISC-V calling conventions
- Using ll0c or LLC for conversion

## 12.11 Exercises

1. Use `llc` to compile cpy0 LLVM IR to RISC-V
2. Compare assembly generated at different optimization levels (-O0, -O2)
3. Manually translate a simple LLVM IR function to RISC-V
4. Research RISC-V compressed instruction set (C extension)
5. Implement a simple LLVM IR to x86 backend
