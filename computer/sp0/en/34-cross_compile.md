# 34. Cross-Compilation——Compiling RISC-V on x86

## 34.1 What is Cross-Compilation?

Cross-compilation is compiling programs for another architecture on one machine:

```
Host (x86_64) ──────→ Target (RISC-V)
  Run gcc             Run compiled program
```

## 34.2 Why Cross-Compilation?

- **Embedded systems**: Not enough resources to compile
- **Development efficiency**: Host is much faster than target
- **Multi-target support**: Compile once, run on multiple targets

## 34.3 RISC-V Toolchain

### 34.3.1 Installation

```bash
# macOS
brew tap riscv/riscv
brew install riscv-gnu-toolchain

# Ubuntu/Debian
sudo apt install gcc-riscv64-unknown-elf
```

### 34.3.2 Tools

```bash
riscv64-unknown-elf-gcc    # C compiler
riscv64-unknown-elf-g++    # C++ compiler
riscv64-unknown-elf-as     # Assembler
riscv64-unknown-elf-ld     # Linker
riscv64-unknown-elf-objdump # Disassembler
riscv64-unknown-elf-readelf # ELF analyzer
```

## 34.4 Basic Cross-Compilation

### 34.4.1 Compile to RISC-V

```bash
riscv64-unknown-elf-gcc hello.c -o hello.rv
```

### 34.4.2 Specify ABI and ISA

```bash
riscv64-unknown-elf-gcc \
    -march=rv64gc \        # ISA (G=IMAFDC)
    -mabi=lp64d \          # ABI
    hello.c -o hello.rv
```

### 34.4.3 Compare with cpy0 Toolchain

```bash
# Using RISC-V GCC
riscv64-unknown-elf-gcc -S hello.c -o hello.s

# Using clang
clang --target=riscv64 -march=rv64g -mabi=lp64d \
    -S hello.c -o hello.s
```

## 34.5 No Standard Library Compilation

### 34.5.1 Bare Metal Program

```bash
riscv64-unknown-elf-gcc \
    -nostdlib \
    -march=rv32ima \
    -mabi=ilp32 \
    hello.c -o hello.elf
```

### 34.5.2 Newlib

```bash
# Newlib provides simplified standard library implementation
riscv64-unknown-elf-gcc \
    -march=rv64gc \
    -mabi=lp64d \
    hello.c -o hello.elf
```

## 34.6 Running on QEMU

### 34.6.1 32-bit

```bash
qemu-system-riscv32 -kernel hello.elf -nographic
```

### 34.6.2 64-bit

```bash
qemu-system-riscv64 -kernel hello.elf -nographic
```

## 34.7 Debugging

### 34.7.1 GDB Debugging

```bash
# Start QEMU waiting for GDB
qemu-system-riscv64 -kernel hello.elf -gdb tcp::1234 -S

# Another terminal
riscv64-unknown-elf-gdb hello.elf
(gdb) target remote localhost:1234
(gdb) load
(gdb) break main
(gdb) continue
```

## 34.8 Summary

In this chapter we learned:
- Cross-compilation concept
- RISC-V toolchain installation
- Basic cross-compilation commands
- No-standard-library compilation
- Running on QEMU
- Debugging setup

## 34.9 Exercises

1. Install RISC-V toolchain on your system
2. Cross-compile a program for mini-riscv-os
3. Research differences between ABIs
4. Implement remote debugging workflow
5. Compare riscv64-unknown-elf-gcc and clang output
