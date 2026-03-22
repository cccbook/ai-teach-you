# 13. rv0 Assembler——Assembly to Object File

## 13.1 What is an Assembler?

An assembler converts human-readable assembly into machine code (object file).

```
Assembly (.s)     Object file (.o)
   ↓              ↓
Text instructions ──→ Binary machine code
```

## 13.2 rv0as Introduction

rv0as is the RISC-V assembler in cpy0 project.

Location: [_code/cpy0/rv0/rv0as.c](../_code/cpy0/rv0/rv0as.c)

## 13.3 Object File Format

Object file contains:
- **Machine code**: actual instruction bytes
- **Symbol table**: function, variable names and locations
- **Relocation info**: addresses not yet determined

## 13.4 RISC-V Instruction Encoding Review

### 13.4.1 R Type (Integer Register Operations)

```
31        25:20  19:15  14:12  11:7   6:0
+---------+------+------+-------+------+-----+
| funct7  | rs2  | rs1  | funct3| rd   |opcode|
+---------+------+------+-------+------+-----+
```

Example: `add x5, x6, x7`
- opcode = 0110011 (0x33)
- funct3 = 000
- funct7 = 0000000
- rd = 00101 (5)
- rs1 = 00110 (6)
- rs2 = 00111 (7)

Encoding: 0x00F70733

### 13.4.2 I Type (Immediate Operations, Load)

```
31                20:12  11:7   6:0
+------------------+------+------+-----+
| immediate[11:0] | rs1  | rd   |opcode|
+------------------+------+------+-----+
```

Example: `addi x5, x6, 10`
- opcode = 0010011 (0x13)
- funct3 = 000
- rd = 00101 (5)
- rs1 = 00110 (6)
- imm = 10

### 13.4.3 S Type (Store)

```
31        25:20  19:15  11:7        6:0
+---------+------+------+----------+-----+
| imm[11:5]| rs2 | rs1  | imm[4:0]|opcode|
+---------+------+------+----------+-----+
```

### 13.4.4 B Type (Branch)

```
31        25:20  19:15  11:8 7  6:0
+---------+------+------+-----+----+-----+
|imm[12]|imm[10:5]| rs2 | rs1 |imm[4:1]| opcode|
+---------+------+------+-----+----+-----+
```

### 13.4.5 U Type (Upper Immediate)

```
31                    11:7   6:0
+---------------------+-------+-----+
| immediate[31:12]    | rd    |opcode|
+---------------------+-------+-----+
```

### 13.4.6 J Type (Jump)

```
31        25:20  19:12  11:8 7  6:0
+---------+------+-------+-----+----+-----+
|imm[20]|imm[10:1]|imm[11]|imm[19:12]| opcode|
+---------+------+-------+-----+----+-----+
```

## 13.5 rv0as Design

### 13.5.1 Lexical Analysis

```c
// Parse register
int parse_reg(char *s) {
    if (s[0] == 'x' || s[0] == 'z') {
        return atoi(s + 1);  // x0-x31
    }
    // ...
}

// Parse immediate (decimal, hex)
long long parse_imm(char *s) {
    if (s[0] == '0' && s[1] == 'x')
        return strtoll(s + 2, NULL, 16);
    return atoll(s);
}
```

### 13.5.2 Instruction Parsing

```c
// Parse add instruction
case OP_ADD:
    check_args(3);
    r_type(0x33, 0, 0, rd(), rs1(), rs2());
    break;

// Parse addi instruction
case OP_ADDI:
    check_args(3);
    i_type(0x13, 0, rd(), rs1(), imm());
    break;
```

### 13.5.3 Instruction Encoding Functions

```c
void r_type(int opcode, int funct3, int funct7, int rd, int rs1, int rs2) {
    emit((funct7 << 25) | (rs2 << 20) | (rs1 << 15) | 
         (funct3 << 12) | (rd << 7) | opcode);
}

void i_type(int opcode, int funct3, int rd, int rs1, int imm) {
    emit(((imm & 0xFFF) << 20) | (rs1 << 15) | 
         (funct3 << 12) | (rd << 7) | opcode);
}

void sb_type(int opcode, int funct3, int rs1, int rs2, int imm) {
    int enc = ((imm & 0x1000) << 19) |
              ((imm & 0x7E0) << 20) |
              (rs2 << 20) | (rs1 << 15) |
              ((imm & 0xF) << 8) |
              ((imm & 0x800) >> 7) |
              opcode;
    emit(enc);
}
```

## 13.6 Supported Instructions

rv0as supports basic RISC-V instructions:

### Arithmetic
- add, addi, sub
- mul, div, rem
- and, andi, or, ori, xor, xori
- sll, slli, srl, srli

### Comparison
- slt, slti, sltu, sltiu

### Load/Store
- lw, sw
- lb, lbu, sb

### Branch
- beq, bne, blt, bge, bltu, bgeu

### Jump
- jal, jalr
- ret (pseudo)

### Other
- lui, auipc
- ecall, ebreak
- nop

## 13.7 Labels and Relocation

### 13.7.1 Defining Labels

```asm
loop:
    addi t0, t0, 1
    blt t0, t1, loop
```

### 13.7.2 Resolving Labels

```c
// First pass: collect labels
if (label_exists(label)) {
    addr = labels[label];
} else {
    // Defer resolution
    add_reloc(label, current_addr);
}

// Second pass: resolve relocations
for (reloc in relocs) {
    target = labels[reloc.name];
    patch(reloc.addr, target - reloc.pc);
}
```

## 13.8 Using rv0as

```bash
# Basic usage
./rv0/rv0as fact.s -o fact.o

# Or use clang's built-in assembler
clang -c fact.s -o fact.o --target=riscv64
```

## 13.9 Complete Example

### Input: fact.s

```asm
    .text
    .globl fact
    .align 2

fact:
    li t0, 1
    ble a0, t0, .LBB0_1
    
    addi sp, sp, -16
    sw ra, 12(sp)
    sw a0, 8(sp)
    
    addi a0, a0, -1
    jal ra, fact
    
    lw t0, 8(sp)
    mul a0, t0, a0
    
    lw ra, 12(sp)
    addi sp, sp, 16
    ret

.LBB0_1:
    li a0, 1
    ret
```

### Output: fact.o (binary)

rv0as generates:
1. Machine code segment (binary or ELF)
2. Symbol table
3. Relocation table

## 13.10 ELF Object File Format

For ELF format object files:

```
+-------------------+
| ELF Header        |
+-------------------+
| Section Header    |
| Table             |
+-------------------+
| .text section     |  Machine code
+-------------------+
| .data section     |  Initialized data
+-------------------+
| .symtab           |  Symbol table
+-------------------+
| .rel.text         |  Relocation table
+-------------------+
```

### 13.10.1 Symbol Table Entry

```c
struct Elf64_Sym {
    Elf64_Word    st_name;   // symbol name
    unsigned char st_info;   // binding+type
    unsigned char st_other;  // other
    Elf64_Half    st_shndx; // containing section
    Elf64_Addr    st_value;  // value/address
    Elf64_Xword   st_size;  // size
};
```

### 13.10.2 Relocation Entry

```c
struct Elf64_Rela {
    Elf64_Addr    r_offset;  // address needing fixup
    Elf64_Xword   r_info;    // symbol+type
    Elf64_Sxword  r_addend;  // addend
};
```

## 13.11 objdump Disassembly

Use rv0objdump or standard objdump:

```bash
# Use rv0objdump
./rv0/rv0objdump fact.o

# Or use riscv64-unknown-elf-objdump
riscv64-unknown-elf-objdump -d fact.o

# View symbol table
riscv64-unknown-elf-objdump -t fact.o

# View relocation table
riscv64-unknown-elf-objdump -r fact.o
```

## 13.12 Summary

In this chapter we learned:
- Assembler basics
- RISC-V instruction encoding formats
- rv0as design and implementation
- Supported RISC-V instructions
- Labels and relocation
- ELF object file format
- Using objdump for disassembly

## 13.13 Exercises

1. Add `not` instruction support to rv0as
2. Research RISC-V compressed instructions (C extension)
3. Add `.data` section support to rv0as
4. Implement a simple x86 assembler
5. Use `objdump -d` to disassemble a C program
