# 13. rv0 組譯器——組語到目標檔

## 13.1 什麼是組譯器？

組譯器（Assembler）將人類可讀的組語翻譯成機器碼（目的檔）。

```
組語 (.s)     目的檔 (.o)
   ↓              ↓
文字指令 ──→ 二進位機器碼
```

## 13.2 rv0as 簡介

rv0as 是 cpy0 專案中的 RISC-V 組譯器。

位置：[_code/cpy0/rv0/rv0as.c](../_code/cpy0/rv0/rv0as.c)

## 13.3 目的檔格式

目的檔包含：
- **機器碼**：實際的指令位元組
- **符號表**：函式、變數的名稱和位置
- **重定位資訊**：尚未確定的位址

## 13.4 RISC-V 指令編碼回顧

### 13.4.1 R 類型（整數暫存器運算）

```
31        25:20  19:15  14:12  11:7   6:0
+---------+------+------+-------+------+-----+
| funct7  | rs2  | rs1  | funct3| rd   |opcode|
+---------+------+------+-------+------+-----+
```

範例：`add x5, x6, x7`
- opcode = 0110011 (0x33)
- funct3 = 000
- funct7 = 0000000
- rd = 00101 (5)
- rs1 = 00110 (6)
- rs2 = 00111 (7)

編碼結果：0x00F70733

### 13.4.2 I 類型（立即數運算、載入）

```
31                20:12  11:7   6:0
+------------------+------+------+-----+
| immediate[11:0] | rs1  | rd   |opcode|
+------------------+------+------+-----+
```

範例：`addi x5, x6, 10`
- opcode = 0010011 (0x13)
- funct3 = 000
- rd = 00101 (5)
- rs1 = 00110 (6)
- imm = 10

### 13.4.3 S 類型（儲存）

```
31        25:20  19:15  11:7        6:0
+---------+------+------+----------+-----+
| imm[11:5]| rs2 | rs1  | imm[4:0]|opcode|
+---------+------+------+----------+-----+
```

### 13.4.4 B 類型（分支）

```
31        25:20  19:15  11:8 7  6:0
+---------+------+------+-----+----+-----+
|imm[12]|imm[10:5]| rs2 | rs1 |imm[4:1]| opcode|
+---------+------+------+-----+----+-----+
```

### 13.4.5 U 類型（上位立即數）

```
31                    11:7   6:0
+---------------------+-------+-----+
| immediate[31:12]    | rd    |opcode|
+---------------------+-------+-----+
```

### 13.4.6 J 類型（跳躍）

```
31        25:20  19:12  11:8 7  6:0
+---------+------+-------+-----+----+-----+
|imm[20]|imm[10:1]|imm[11]|imm[19:12]| opcode|
+---------+------+-------+-----+----+-----+
```

## 13.5 rv0as 的設計

### 13.5.1 詞彙分析

```c
// 解析暫存器
int parse_reg(char *s) {
    if (s[0] == 'x' || s[0] == 'z') {
        return atoi(s + 1);  // x0-x31
    }
    // ...
}

// 解析立即數（支援十進位、十六進位）
long long parse_imm(char *s) {
    if (s[0] == '0' && s[1] == 'x')
        return strtoll(s + 2, NULL, 16);
    return atoll(s);
}
```

### 13.5.2 指令解析

```c
// 解析 add 指令
case OP_ADD:
    check_args(3);
    r_type(0x33, 0, 0, rd(), rs1(), rs2());
    break;

// 解析 addi 指令
case OP_ADDI:
    check_args(3);
    i_type(0x13, 0, rd(), rs1(), imm());
    break;
```

### 13.5.3 指令編碼函式

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

## 13.6 支援的指令

rv0as 支援基本的 RISC-V 指令：

### 算術指令
- add, addi, sub
- mul, div, rem
- and, andi, or, ori, xor, xori
- sll, slli, srl, srli

### 比較指令
- slt, slti, sltu, sltiu

### 負載/儲存
- lw, sw
- lb, lbu, sb

### 分支
- beq, bne, blt, bge, bltu, bgeu

### 跳躍
- jal, jalr
- ret (擴充)

### 其他
- lui, auipc
- ecall, ebreak
- nop

## 13.7 標籤和重定位

### 13.7.1 定義標籤

```asm
loop:
    addi t0, t0, 1
    blt t0, t1, loop
```

### 13.7.2 解析標籤

```c
// 第一次掃描：收集標籤
if (label_exists(label)) {
    addr = labels[label];
} else {
    // 延遲解析
    add_reloc(label, current_addr);
}

// 第二次掃描：解析重定位
for (reloc in relocs) {
    target = labels[reloc.name];
    patch(reloc.addr, target - reloc.pc);
}
```

## 13.8 使用 rv0as

```bash
# 基本用法
./rv0/rv0as fact.s -o fact.o

# 或者使用 clang 的內建組譯器
clang -c fact.s -o fact.o --target=riscv64
```

## 13.9 完整範例

### 輸入：fact.s

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

### 輸出：fact.o（二進位）

rv0as 會生成：
1. 機器碼段（二進位或 ELF）
2. 符號表
3. 重定位表

## 13.10 ELF 目的檔格式

如果生成 ELF 格式的目的檔：

```
+-------------------+
| ELF Header        |
+-------------------+
| Section Header    |
| Table             |
+-------------------+
| .text section     |  機器碼
+-------------------+
| .data section     |  已初始化資料
+-------------------+
| .symtab           |  符號表
+-------------------+
| .rel.text         |  重定位表
+-------------------+
```

### 13.10.1 符號表條目

```c
struct Elf64_Sym {
    Elf64_Word    st_name;   // 符號名
    unsigned char st_info;   // 綁定+類型
    unsigned char st_other;  // 其他
    Elf64_Half    st_shndx; // 所在段
    Elf64_Addr    st_value;  // 值/位址
    Elf64_Xword   st_size;  // 大小
};
```

### 13.10.2 重定位條目

```c
struct Elf64_Rela {
    Elf64_Addr    r_offset;  // 需修正的位址
    Elf64_Xword   r_info;    // 符號+類型
    Elf64_Sxword  r_addend;  // 加數
};
```

## 13.11 objdump 反組譯

可以使用 rv0objdump 或標準 objdump 來查看：

```bash
# 使用 rv0objdump
./rv0/rv0objdump fact.o

# 或使用 riscv64-unknown-elf-objdump
riscv64-unknown-elf-objdump -d fact.o

# 查看符號表
riscv64-unknown-elf-objdump -t fact.o

# 查看重定位表
riscv64-unknown-elf-objdump -r fact.o
```

## 13.12 小結

本章節我們學習了：
- 組譯器的基本功能
- RISC-V 指令編碼格式
- rv0as 的設計和實現
- 支援的 RISC-V 指令
- 標籤和重定位
- ELF 目的檔格式
- 使用 objdump 反組譯

## 13.13 習題

1. 為 rv0as 添加 `not` 指令支援
2. 研究 RISC-V 的壓縮指令 (C 擴展)
3. 為 rv0as 添加對 `.data` 段的支持
4. 實現一個簡單的 x86 組譯器
5. 使用 `objdump -d` 反組譯一個 C 程式
