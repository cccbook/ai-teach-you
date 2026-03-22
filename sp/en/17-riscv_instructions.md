# 17. RISC-V Instruction Set——The Philosophy of RISC

## 17.1 What is RISC-V?

RISC-V (pronounced "risk-five") is an open-source instruction set architecture (ISA) developed at UC Berkeley.

### Why RISC-V?

- **Open Standard**: Free for anyone to use
- **Simple Design**: Easy to understand and implement
- **Modular**: Choose extensions as needed
- **Supports 32/64/128-bit**
- **Wide ecosystem support**

## 17.2 RISC-V Design Principles

Core principles of RISC (Reduced Instruction Set Computer):

1. **Simplicity**: Uniform instruction formats, simple decoding
2. **Regularity**: All operations work on registers
3. **Make common operations simple**: Dedicated instructions for frequent tasks
4. **Speed comes from good compilers**: Let the compiler optimize

## 17.3 Instruction Formats

RISC-V has 6 basic formats (all 32-bit instructions):

```
R type: register-register operations
+--------+----+--+----+---+----+------+
| 31-25  |24-20|19-15|14-12|11-7|  6-0 |
| funct7 | rs2 | rs1 |funct3| rd |opcode|
+--------+----+--+----+---+----+------+

I type: immediate operations, loads
+--------+------+----+---+----+------+
|  11-0  |19-15 |14-12|11-7|  6-0 |
| imm[11:0]| rs1 |funct3| rd |opcode|
+--------+------+----+---+----+------+

S type: stores
+-------+----+--+----+------+---+----+------+
|31-25|24-20|19-15|11-8 |7|  | 6-0 |
|imm[11:5]|rs2 | rs1 |imm[4:0]|opcode|
+-------+----+--+----+------+---+----+------+

B type: branches (displacement in multiples of 2)
+---------+----+--+----+------+---+----+------+
|31    25|24-20|19-15|11-8 |7|  | 6-0 |
|imm[12]|imm[10:5]|rs2|rs1|imm[4:1]|imm[11]|opcode|
+---------+----+--+----+------+---+----+------+

U type: upper immediates
+----------------+---+----+------+
|    31-12       |11-7|  6-0 |
|  imm[31:12]    | rd |opcode|
+----------------+---+----+------+

J type: jumps (displacement in multiples of 2)
+---------+--------+--+----+---+----+------+
|31    25|24-21|20|19-12|11-8|7|  | 6-0 |
|imm[20]|imm[10:1]|imm[11]|imm[19:12]|imm[11]|opcode|
+---------+--------+--+----+---+----+------+
```

## 17.4 Registers

### 17.4.1 General Purpose Registers (32)

| Register | Alias | Purpose | Saved |
|----------|-------|---------|-------|
| x0 | zero | Constant 0 | - |
| x1 | ra | Return address | - |
| x2 | sp | Stack pointer | Yes |
| x3 | gp | Global pointer | - |
| x4 | tp | Thread pointer | - |
| x5 | t0 | Temporary | No |
| x6 | t1 | Temporary | No |
| x7 | t2 | Temporary | No |
| x8 | s0/fp | Saved/Frame pointer | Yes |
| x9 | s1 | Saved | Yes |
| x10 | a0 | Arg0/Return0 | No |
| x11 | a1 | Arg1/Return1 | No |
| x12 | a2 | Arg2 | No |
| x13 | a3 | Arg3 | No |
| x14 | a4 | Arg4 | No |
| x15 | a5 | Arg5 | No |
| x16 | a6 | Arg6 | No |
| x17 | a7 | Arg7 | No |
| x18-x27 | s2-s11 | Saved | Yes |
| x28-x31 | t3-t6 | Temporary | No |

### 17.4.2 Special Registers

- **PC (Program Counter)**: Stores current instruction address

## 17.5 Integer Instructions (RV32I/RV64I)

### 17.5.1 Arithmetic Instructions

```asm
# Addition
add   a0, a0, a1    ; a0 = a0 + a1
addi  a0, a0, 10    ; a0 = a0 + 10

# Subtraction
sub   a0, a0, a1    ; a0 = a0 - a1

# Negation (no neg instruction, use sub)
neg   a0, a0        ; a0 = 0 - a0
sub   a0, x0, a0    ; equivalent to neg
```

### 17.5.2 Logical Instructions

```asm
and   a0, a0, a1    ; a0 = a0 & a1
andi  a0, a0, 0xFF  ; a0 = a0 & 0xFF

or    a0, a0, a1    ; a0 = a0 | a1
ori   a0, a0, 0xFF  ; a0 = a0 | 0xFF

xor   a0, a0, a1    ; a0 = a0 ^ a1
xori  a0, a0, 0xFF  ; a0 = a0 ^ 0xFF
```

### 17.5.3 Shift Instructions

```asm
# Logical left shift
sll   a0, a0, a1    ; a0 = a0 << a1
slli  a0, a0, 3     ; a0 = a0 << 3

# Logical right shift (zero fill)
srl   a0, a0, a1    ; a0 = a0 >> a1
srli  a0, a0, 3     ; a0 = a0 >> 3

# Arithmetic right shift (sign extend)
sra   a0, a0, a1    ; a0 = a0 >> a1
srai  a0, a0, 3     ; a0 = a0 >> 3
```

### 17.5.4 Comparison Instructions

```asm
# Set less than (signed)
slt   a0, a0, a1    ; a0 = (a0 < a1) ? 1 : 0
slti  a0, a0, 10    ; a0 = (a0 < 10) ? 1 : 0

# Set less than (unsigned)
sltu  a0, a0, a1    ; a0 = (a0 < a1) ? 1 : 0
sltiu a0, a0, 10    ; a0 = (a0 < 10) ? 1 : 0
```

## 17.6 Load and Store

RISC-V is a **load/store architecture** - memory can only be accessed through dedicated instructions.

```asm
# Loads
lw   a0, 0(sp)      ; a0 = *((int*)(sp + 0))
lb   a0, 0(sp)      ; a0 = *((int8*)(sp + 0)) (signed)
lbu  a0, 0(sp)      ; a0 = *((uint8*)(sp + 0)) (unsigned)
lhu  a0, 0(sp)      ; a0 = *((uint16*)(sp + 0)) (unsigned)

# Stores
sw   a0, 0(sp)      ; *((int*)(sp + 0)) = a0
sb   a0, 0(sp)      ; *((int8*)(sp + 0)) = a0
sh   a0, 0(sp)      ; *((int16*)(sp + 0)) = a0

# No direct memory-to-memory instructions!
# Must: load → operate → store
```

## 17.7 Branch Instructions

```asm
# Unconditional equal/unequal
beq  a0, a1, label   ; if (a0 == a1) goto label
bne  a0, a1, label   ; if (a0 != a1) goto label

# Signed comparisons
blt  a0, a1, label   ; if (a0 < a1) goto label (signed)
bge  a0, a1, label   ; if (a0 >= a1) goto label (signed)

# Unsigned comparisons
bltu a0, a1, label   ; if (a0 < a1) goto label (unsigned)
bgeu a0, a1, label   ; if (a0 >= a1) goto label (unsigned)

# Combined conditions (require multiple instructions)
bgt  a0, a1, label   ; if (a0 > a1) goto label
                        ; slt t0, a1, a0
                        ; bne t0, x0, label
```

## 17.8 Jump Instructions

```asm
# Jump and link
jal  ra, label       ; ra = pc + 4; goto label

# Jump and link register
jalr ra, 0(a0)       ; ra = pc + 4; goto *a0

# Return (pseudo-instruction)
ret                  ; jalr x0, 0(ra)
```

## 17.9 Upper Immediate Instructions

```asm
# Load upper immediate
lui  a0, 0x12345     ; a0 = 0x12345000

# Add upper immediate to PC
auipc a0, 0x12345    ; a0 = pc + 0x12345000

# Combine with addi for large immediates
lui  a0, 0x12345
addi a0, a0, 0x678   ; a0 = 0x12345678
```

## 17.10 Pseudo-Instructions

RISC-V assembly provides many pseudo-instructions for convenience:

```asm
# No operation
nop                  ; addi x0, x0, 0

# Load immediate
li   a0, 42          ; expands to lui + addi
li   a0, 0x12345678  ; lui + addi

# Move
mv   a0, a1          ; addi a0, a1, 0

# Clear
clr  a0              ; xor a0, a0, a0
```

## 17.11 RISC-V Extensions

RISC-V is modular - you can choose different extensions:

| Extension | Name | Contents |
|----------|------|----------|
| M | Multiply/Divide | mul, div, rem |
| F | Single-precision Float | flw, fsw, fadd.s |
| D | Double-precision Float | fld, fsd, fadd.d |
| A | Atomic Operations | amoadd, amoswap |
| C | Compressed Instructions | 16-bit instructions |
| G | General | Base + M, F, D, A |

Full notation: `RV64IMAFDC` = RV64GC

## 17.12 Practical Example

### C Program

```c
long long add(long long a, long long b) {
    return a + b;
}
```

### RISC-V Assembly (O0)

```asm
add:
    # Function entry
    addi sp, sp, -16    ; allocate stack frame
    sd ra, 8(sp)         ; save return address
    sd a0, 0(sp)         ; save a (for return value)
    
    # a1 is already b
    
    # Addition
    add a0, a0, a1
    
    # Function exit
    ld ra, 8(sp)         ; restore return address
    addi sp, sp, 16      ; deallocate stack frame
    ret
```

## 17.13 Summary

In this chapter we learned:
- RISC-V design principles
- 6 instruction formats (R, I, S, B, U, J)
- 32 general-purpose register purposes
- Integer arithmetic, logical, and shift instructions
- Load/store instructions
- Branch and jump instructions
- Upper immediate instructions
- Pseudo-instructions and extensions

## 17.14 Exercises

1. Write RISC-V assembly to implement `factorial(10)`
2. Research the difference between `blt` and `bltu`
3. Why doesn't RISC-V have a `neg` instruction? How do you implement it?
4. Use `lui` + `addi` to load `0xDEADBEEF` into a register
5. Compare RISC-V and ARMv8 instruction format differences
