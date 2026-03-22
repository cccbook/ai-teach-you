# 14. rv0 Virtual Machine——RISC-V Instruction Set Simulator

## 14.1 Virtual Machine Introduction

A virtual machine is a software-implemented CPU that can execute a specific instruction set's programs.

```
+------------------+       +------------------+
|   rv0vm         |       |   QEMU          |
| (Educational simplified) |       | (Industrial simulator) |
+------------------+       +------------------+
| - Basic instruction support |       | - Complete ISA support |
| - Educational purpose      |       | - Performance optimized  |
| - Easy to understand      |       | - Device emulation        |
+------------------+       +------------------+
```

## 14.2 rv0vm Architecture

Location: [_code/cpy0/rv0/rv0vm.c](../_code/cpy0/rv0/rv0vm.c)

### 14.2.1 Memory Model

```c
#define MEM_SIZE (128 * 1024)  // 128KB memory

static uint8_t mem[MEM_SIZE];  // memory

// Load program into memory
void load_program(const char *filename, uint64_t entry) {
    FILE *fp = fopen(filename, "rb");
    fread(&mem[entry], 1, MEM_SIZE - entry, fp);
    fclose(fp);
}
```

### 14.2.2 Registers

```c
static uint64_t reg[32];  // 32 general purpose registers
// x0 = 0 (always 0)
// x1 = ra (return address)
// x2 = sp (stack pointer)
// ...
```

### 14.2.3 PC and Fetch-Decode-Execute

```c
static uint64_t pc = 0;
static uint64_t halted = 0;

while (!halted) {
    uint32_t inst = fetch(pc);    // fetch instruction
    decode_and_execute(inst);     // decode and execute
    pc += 4;                      // PC advances
}
```

## 14.3 Instruction Decoding

RISC-V instruction decoding:

```c
uint32_t inst = *(uint32_t *)&mem[pc];

int opcode = inst & 0x7F;
int rd     = (inst >> 7) & 0x1F;
int funct3 = (inst >> 12) & 0x7;
int rs1    = (inst >> 15) & 0x1F;
int rs2    = (inst >> 20) & 0x1F;
int funct7 = (inst >> 25) & 0x7F;
int imm_i  = (int32_t)(inst & 0xFFFFF000) >> 20;  // I type immediate
```

## 14.4 Instruction Execution

### 14.4.1 LUI (Load Upper Immediate)

```c
case 0x37:  // LUI
    reg[rd] = (uint64_t)(int32_t)(inst & 0xFFFFF000);
    break;
```
```
LUI x5, 0x12345
x5 = 0x12345000
```

### 14.4.2 AUIPC (Add Upper Immediate to PC)

```c
case 0x17:  // AUIPC
    reg[rd] = pc + (int64_t)(int32_t)(inst & 0xFFFFF000);
    break;
```

### 14.4.3 JAL (Jump and Link)

```c
case 0x6F:  // JAL
    {
        int imm = ((inst >> 31) & 0x1) << 20 |
                  ((inst >> 12) & 0xFF) << 12 |
                  ((inst >> 20) & 0x1) << 11 |
                  ((inst >> 21) & 0x3FF) << 1;
        imm = (int32_t)(imm << 11) >> 11;  // sign extend
        reg[rd] = pc + 4;
        pc = pc + imm - 4;  // will be +4'd at loop end
    }
    break;
```

### 14.4.4 JALR (Jump and Link Register)

```c
case 0x67:  // JALR
    {
        int imm = imm_i;
        uint64_t target = (reg[rs1] + imm) & ~1ULL;
        reg[rd] = pc + 4;
        pc = target - 4;  // will be +4'd
    }
    break;
```

### 14.4.5 Branch Instructions

```c
case 0x63:  // branch instructions
    {
        int imm = ((inst >> 31) & 0x1) << 12 |
                  ((inst >> 25) & 0x3F) << 5 |
                  ((inst >> 8) & 0xF) << 1 |
                  ((inst >> 7) & 0x1) << 11;
        imm = (int32_t)(imm << 19) >> 19;
        
        int taken = 0;
        switch (funct3) {
            case 0: taken = (reg[rs1] == reg[rs2]); break;  // BEQ
            case 1: taken = (reg[rs1] != reg[rs2]); break;  // BNE
            case 4: taken = ((int64_t)reg[rs1] < (int64_t)reg[rs2]); break;  // BLT
            case 5: taken = ((int64_t)reg[rs1] >= (int64_t)reg[rs2]); break;  // BGE
            // ...
        }
        if (taken) pc = pc + imm - 4;
    }
    break;
```

### 14.4.6 Load Instructions

```c
case 0x03:  // load instructions
    {
        uint64_t addr = reg[rs1] + imm_i;
        switch (funct3) {
            case 0:  // LB
                reg[rd] = (int8_t)mem[addr];
                break;
            case 1:  // LH
                reg[rd] = *(int16_t *)&mem[addr];
                break;
            case 2:  // LW
                reg[rd] = *(int32_t *)&mem[addr];
                break;
            case 3:  // LD
                reg[rd] = *(int64_t *)&mem[addr];
                break;
            case 4:  // LBU
                reg[rd] = mem[addr];
                break;
            // ...
        }
    }
    break;
```

### 14.4.7 Store Instructions

```c
case 0x23:  // store instructions
    {
        uint64_t addr = reg[rs1] + ((int32_t)((inst >> 25) << 5) | ((inst >> 7) & 0x1F));
        switch (funct3) {
            case 0:  // SB
                mem[addr] = reg[rs2] & 0xFF;
                break;
            case 1:  // SH
                *(uint16_t *)&mem[addr] = reg[rs2] & 0xFFFF;
                break;
            case 2:  // SW
                *(uint32_t *)&mem[addr] = reg[rs2] & 0xFFFFFFFF;
                break;
            case 3:  // SD
                *(uint64_t *)&mem[addr] = reg[rs2];
                break;
        }
    }
    break;
```

### 14.4.8 Arithmetic Instructions

```c
case 0x33:  // R type arithmetic
    switch (funct3) {
        case 0:  // ADD/SUB
            reg[rd] = funct7 == 0x20 ? 
                       reg[rs1] - reg[rs2] : 
                       reg[rs1] + reg[rs2];
            break;
        case 1: reg[rd] = reg[rs1] << reg[rs2]; break;      // SLL
        case 2: reg[rd] = (int64_t)reg[rs1] < (int64_t)reg[rs2]; break;  // SLT
        case 3: reg[rd] = reg[rs1] < reg[rs2]; break;        // SLTU
        case 4: reg[rd] = reg[rs1] ^ reg[rs2]; break;        // XOR
        case 5: reg[rd] = funct7 == 0 ? 
                          (reg[rs1] >> reg[rs2]) :           // SRL
                          ((int64_t)reg[rs1] >> reg[rs2]);   // SRA
                 break;
        case 6: reg[rd] = reg[rs1] | reg[rs2]; break;        // OR
        case 7: reg[rd] = reg[rs1] & reg[rs2]; break;        // AND
    }
    break;
```

### 14.4.9 I Type Arithmetic

```c
case 0x13:  // I type arithmetic
    switch (funct3) {
        case 0: reg[rd] = reg[rs1] + imm_i; break;          // ADDI
        case 1: reg[rd] = reg[rs1] << (imm_i & 0x3F); break;  // SLLI
        case 2: reg[rd] = (int64_t)reg[rs1] < imm_i; break;  // SLTI
        case 3: reg[rd] = reg[rs1] < (uint64_t)imm_i; break; // SLTIU
        case 4: reg[rd] = reg[rs1] ^ imm_i; break;           // XORI
        case 5: reg[rd] = funct7 == 0 ? 
                          (reg[rs1] >> (imm_i & 0x3F)) :     // SRLI
                          ((int64_t)reg[rs1] >> (imm_i & 0x3F));  // SRAI
                 break;
        case 6: reg[rd] = reg[rs1] | imm_i; break;           // ORI
        case 7: reg[rd] = reg[rs1] & imm_i; break;           // ANDI
    }
    break;
```

## 14.5 System Calls

```c
case 0x73:  // ECALL
    switch (reg[17]) {  // a7 = syscall number
        case 64:  // write
            // sbrk or other
            break;
        case 93:  // exit
            halted = 1;
            exit_code = reg[10];  // a0 = exit code
            break;
    }
    break;
```

## 14.6 Using rv0vm

```bash
# Basic usage
./rv0/rv0vm fact.o

# Specify entry point
./rv0/rv0vm -e 0x1000 fact.o

# Show execution trace
./rv0/rv0vm -d fact.o
```

## 14.7 Complete Execution Example

### Code: fact.c

```c
long long fact(long long n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
}

long long main() {
    return fact(10);
}
```

### Compilation Flow

```bash
# 1. Compile to LLVM IR
clang -S -emit-llvm --target=riscv64 fact.c -o fact.ll

# 2. Translate to RISC-V assembly
llc -march=riscv64 fact.ll -o fact.s

# 3. Assemble to object file
./rv0/rv0as fact.s -o fact.o

# 4. Execute with VM
./rv0/rv0vm fact.o
```

### Output

```
Result: 3628800
Exit code: 0
```

## 14.8 rv0objdump Disassembly Tool

Location: [_code/cpy0/rv0/rv0objdump.c](../_code/cpy0/rv0/rv0objdump.c)

```bash
# Disassemble object file
./rv0/rv0objdump fact.o

# Use LLVM's objdump
llvm-objdump -d fact.o --arch-name=riscv64
riscv64-unknown-elf-objdump -d fact.o
```

## 14.9 Comparison with QEMU

| Feature | rv0vm | QEMU |
|---------|--------|------|
| Complexity | ~500 lines | ~1 million lines |
| Performance | Slow | Fast |
| Device emulation | None | Complete |
| OS support | None | Can boot OS |
| Debug support | Basic | Complete |
| Use case | Teaching | Production |

## 14.10 Summary

In this chapter we learned:
- Virtual machine basics
- rv0vm architecture design
- RISC-V instruction decoding and execution
- Each instruction type implementation
- System call handling
- Using rv0vm to execute programs
- rv0objdump disassembly tool

## 14.11 Exercises

1. Add `MRET` instruction support to rv0vm (machine mode return)
2. Implement simple profiling functionality
3. Add support for `fence` instruction
4. Compare rv0vm and QEMU performance difference
5. Add simple debug mode to rv0vm (show each instruction)
