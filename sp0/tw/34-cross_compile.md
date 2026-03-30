# 34. 交叉編譯——在 x86 上編譯 RISC-V 程式

## 34.1 什麼是交叉編譯？

交叉編譯是在一台機器上為另一種架構編譯程式：

```
主機 (x86_64) ──────→ 目標 (RISC-V)
  執行 gcc             執行編譯後的程式
```

## 34.2 為什麼需要交叉編譯？

- **嵌入式系統**：沒有足夠資源編譯
- **開發效率**：主機比目標快很多
- **多目標支援**：一次編譯，多個目標

## 34.3 RISC-V 工具鏈

### 34.3.1 安裝

```bash
# macOS
brew tap riscv/riscv
brew install riscv-gnu-toolchain

# Ubuntu/Debian
sudo apt install gcc-riscv64-unknown-elf
```

### 34.3.2 工具

```bash
riscv64-unknown-elf-gcc    # C 編譯器
riscv64-unknown-elf-g++    # C++ 編譯器
riscv64-unknown-elf-as     # 組譯器
riscv64-unknown-elf-ld     # 連結器
riscv64-unknown-elf-objdump # 反組譯器
riscv64-unknown-elf-readelf # ELF 分析
```

## 34.4 基本交叉編譯

### 34.4.1 編譯到 RISC-V

```bash
riscv64-unknown-elf-gcc hello.c -o hello.rv
```

### 34.4.2 指定 ABI 和 ISA

```bash
riscv64-unknown-elf-gcc \
    -march=rv64gc \        # ISA (G=IMAFDC)
    -mabi=lp64d \          # ABI
    hello.c -o hello.rv
```

### 34.4.3 與 cpy0 工具鏈比較

```bash
# 使用 RISC-V GCC
riscv64-unknown-elf-gcc -S hello.c -o hello.s

# 使用 clang
clang --target=riscv64 -march=rv64g -mabi=lp64d \
    -S hello.c -o hello.s
```

## 34.5 無標準庫編譯

### 34.5.1 裸機程式

```bash
riscv64-unknown-elf-gcc \
    -nostdlib \
    -march=rv32ima \
    -mabi=ilp32 \
    hello.c -o hello.elf
```

### 34.5.2 新libc (Newlib)

```bash
# Newlib 提供標準庫的簡化實現
riscv64-unknown-elf-gcc \
    -march=rv64gc \
    -mabi=lp64d \
    hello.c -o hello.elf
```

## 34.6 在 QEMU 上執行

### 34.6.1 32 位元

```bash
qemu-system-riscv32 -kernel hello.elf -nographic
```

### 34.6.2 64 位元

```bash
qemu-system-riscv64 -kernel hello.elf -nographic
```

## 34.7 除錯

### 34.7.1 GDB 除錯

```bash
# 啟動 QEMU 等待 GDB
qemu-system-riscv64 -kernel hello.elf -gdb tcp::1234 -S

# 另一個終端
riscv64-unknown-elf-gdb hello.elf
(gdb) target remote localhost:1234
(gdb) load
(gdb) break main
(gdb) continue
```

## 34.8 小結

本章節我們學習了：
- 交叉編譯的概念
- RISC-V 工具鏈的安裝
- 基本交叉編譯命令
- 無標準庫編譯
- 在 QEMU 上執行
- 除錯設定

## 34.9 習題

1. 在你的系統上安裝 RISC-V 工具鏈
2. 為 mini-riscv-os 交叉編譯一個程式
3. 研究不同 ABI 的差異
4. 實現遠端除錯流程
5. 比較 riscv64-unknown-elf-gcc 和 clang 的輸出
