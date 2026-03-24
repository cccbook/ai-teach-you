# 14. rv0 虛擬機——RISC-V 指令集模擬器

## 14.1 虛擬機簡介

虛擬機是一個軟體實現的 CPU，可以執行特定指令集的程式。

```
+------------------+       +------------------+
|   rv0vm         |       |   QEMU          |
| (教學用簡化版)   |       | (工業級模擬器)    |
+------------------+       +------------------+
| - 基本指令支援   |       | - 完整 ISA 支援  |
| - 教學目的      |       | - 效能優化       |
| - 易於理解      |       | - 設備模擬       |
+------------------+       +------------------+
```

## 14.2 rv0vm 架構

位置：[_code/cpy0/rv0/rv0vm.c](../_code/cpy0/rv0/rv0vm.c)

### 14.2.1 記憶體模型

```c
#define MEM_SIZE (128 * 1024)  // 128KB 記憶體

static uint8_t mem[MEM_SIZE];  // 記憶體

// 載入程式到記憶體
void load_program(const char *filename, uint64_t entry) {
    FILE *fp = fopen(filename, "rb");
    fread(&mem[entry], 1, MEM_SIZE - entry, fp);
    fclose(fp);
}
```

### 14.2.2 暫存器

```c
static uint64_t reg[32];  // 32 個通用暫存器
// x0 = 0 (永遠是 0)
// x1 = ra (返回位址)
// x2 = sp (堆疊指標)
// ...
```

### 14.2.3 PC 和 fetch-decode-execute

```c
static uint64_t pc = 0;
static uint64_t halted = 0;

while (!halted) {
    uint32_t inst = fetch(pc);    // 取指令
    decode_and_execute(inst);     // 解碼並執行
    pc += 4;                      // PC 前進
}
```

## 14.3 指令解碼

RISC-V 指令的解碼：

```c
uint32_t inst = *(uint32_t *)&mem[pc];

int opcode = inst & 0x7F;
int rd     = (inst >> 7) & 0x1F;
int funct3 = (inst >> 12) & 0x7;
int rs1    = (inst >> 15) & 0x1F;
int rs2    = (inst >> 20) & 0x1F;
int funct7 = (inst >> 25) & 0x7F;
int imm_i  = (int32_t)(inst & 0xFFFFF000) >> 20;  // I 型立即數
```

## 14.4 各類指令執行

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
        imm = (int32_t)(imm << 11) >> 11;  // 符號擴展
        reg[rd] = pc + 4;
        pc = pc + imm - 4;  // PC 會在迴圈末尾 +4
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
        pc = target - 4;  // 會被 +4 抵消
    }
    break;
```

### 14.4.5 分支指令

```c
case 0x63:  // 分支指令
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

### 14.4.6 載入指令

```c
case 0x03:  // 載入指令
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
            case 5:  // LHU
                reg[rd] = *(uint16_t *)&mem[addr];
                break;
            case 6:  // LWU
                reg[rd] = *(uint32_t *)&mem[addr];
                break;
        }
    }
    break;
```

### 14.4.7 儲存指令

```c
case 0x23:  // 儲存指令
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

### 14.4.8 算術邏輯指令

```c
case 0x33:  // R 類型算術指令
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
        case 5: reg[rd] = funct7 == 0x00 ? 
                          (reg[rs1] >> reg[rs2]) :           // SRL
                          ((int64_t)reg[rs1] >> reg[rs2]);   // SRA
                 break;
        case 6: reg[rd] = reg[rs1] | reg[rs2]; break;        // OR
        case 7: reg[rd] = reg[rs1] & reg[rs2]; break;        // AND
    }
    break;
```

### 14.4.9 I 型算術指令

```c
case 0x13:  // I 型算術指令
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

## 14.5 系統呼叫

```c
case 0x73:  // ECALL
    switch (reg[17]) {  // a7 = 系統呼叫號
        case 64:  // write
            // sbrk 或其他
            break;
        case 93:  // exit
            halted = 1;
            exit_code = reg[10];  // a0 = 退出碼
            break;
    }
    break;
```

## 14.6 使用 rv0vm

```bash
# 基本用法
./rv0/rv0vm fact.o

# 指定入口點
./rv0/rv0vm -e 0x1000 fact.o

# 顯示執行追蹤
./rv0/rv0vm -d fact.o
```

## 14.7 完整執行範例

### 程式碼：fact.c

```c
long long fact(long long n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
}

long long main() {
    return fact(10);
}
```

### 編譯流程

```bash
# 1. 編譯到 LLVM IR
clang -S -emit-llvm --target=riscv64 fact.c -o fact.ll

# 2. 轉換到 RISC-V 組語
llc -march=riscv64 fact.ll -o fact.s

# 3. 組譯到目的檔
./rv0/rv0as fact.s -o fact.o

# 4. 用虛擬機執行
./rv0/rv0vm fact.o
```

### 輸出

```
Result: 3628800
Exit code: 0
```

## 14.8 rv0objdump 反組譯工具

位置：[_code/cpy0/rv0/rv0objdump.c](../_code/cpy0/rv0/rv0objdump.c)

```bash
# 反組譯目的檔
./rv0/rv0objdump fact.o

# 使用 LLVM 的 objdump
llvm-objdump -d fact.o --arch-name=riscv64
riscv64-unknown-elf-objdump -d fact.o
```

## 14.9 與 QEMU 比較

| 功能 | rv0vm | QEMU |
|------|-------|------|
| 複雜度 | ~500 行 | ~100 萬行 |
| 效能 | 慢 | 快 |
| 設備模擬 | 無 | 完整 |
| 作業系統 | 無 | 可以 |
| 除錯支援 | 基本 | 完整 |
| 用途 | 教學 | 生產 |

## 14.10 小結

本章節我們學習了：
- 虛擬機的基本概念
- rv0vm 的架構設計
- RISC-V 指令的解碼和執行
- 各類指令的實現
- 系統呼叫處理
- 使用 rv0vm 執行程式
- rv0objdump 反組譯工具

## 14.11 習題

1. 為 rv0vm 添加 `MRET` 指令支援（機器模式返回）
2. 實現一個簡單的效能分析功能
3. 添加對 `fence` 指令的支持
4. 比較 rv0vm 和 QEMU 的效能差異
5. 為 rv0vm 添加簡單的除錯模式（顯示每條指令）
