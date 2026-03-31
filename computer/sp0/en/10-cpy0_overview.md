# 10. cpy0 Toolchain Overview——From Source to RISC-V Executable

## 10.1 What is cpy0?

cpy0 (pronounced "C-P-Y-Zero") is Professor Chen Zhong-Cheng's DIY compiler toolchain project, demonstrating how to build a complete compiler system from scratch.

Project location: [_code/cpy0/](../_code/cpy0/)

## 10.2 Toolchain Architecture

cpy0 contains multiple tools forming a complete compilation flow:

```
C language flow:
  C source (.c)
       ↓  [c0c / clang]
  LLVM IR (.ll)
       ↓  [ll0c]
  RISC-V assembly (.s)
       ↓  [rv0as]
  RISC-V object file (.o)
       ↓  [ld / rv0vm]
  Executable

Python language flow:
  Python source (.py)
       ↓  [py0c]
  qd0 bytecode (.qd)
       ↓  [qd0c]
  LLVM IR (.ll)
       ↓  [clang]
  Executable
       ↓  or [ll0c] → [rv0as] → [rv0vm]
  RISC-V executable
```

## 10.3 Tool Overview

| Tool | Function | Input | Output |
|------|----------|-------|--------|
| c0c | C compiler (DIY) | .c | .ll (LLVM IR) |
| ll0c | LLVM IR → RISC-V | .ll | .s (RISC-V assembly) |
| rv0as | RISC-V assembler | .s | .o (object file) |
| rv0vm | RISC-V VM | .o | execution result |
| py0c | Python compiler (DIY) | .py | .qd (bytecode) |
| qd0c | qd0 → LLVM IR | .qd | .ll |

## 10.4 Directory Structure

```
cpy0/
├── c0/           # C compiler related
│   ├── _doc/     # documentation
│   └── c0c/      # C compiler implementation
├── py0/          # Python compiler related
│   ├── _doc/     # documentation
│   ├── py0c/     # Python compiler implementation
│   └── py0i/     # Python interpreter (optional)
├── ll0/          # LLVM IR → RISC-V backend
│   ├── ll0c/     # backend implementation
│   └── ll0i/     # reverse tool (optional)
├── qd0/          # qd0 bytecode related
│   ├── _doc/     # documentation
│   └── qd0c/     # qd0 → LLVM IR converter
├── rv0/          # RISC-V VM
│   ├── rv0as     # RISC-V assembler
│   ├── rv0vm     # RISC-V VM
│   └── rv0objdump # disassembly tool
├── _data/        # test examples
│   ├── fact.c    # factorial (C)
│   └── test.py   # Python test
└── Makefile      # build script
```

## 10.5 Quick Start

### 10.5.1 Build Toolchain

```bash
cd _code/cpy0
make
```

This compiles all tools and runs tests.

### 10.5.2 Compile C Program to RISC-V

```bash
# Compile to LLVM IR using clang
clang --target=riscv64 -march=rv64g -mabi=lp64d -S fact.c -o fact.s

# Assemble using rv0as
./rv0/rv0as fact.s -o fact.o

# Execute using rv0vm
./rv0/rv0vm -e 0x6c fact.o
```

### 10.5.3 Compile Python Program

```bash
# Python → qd0 bytecode
./py0/py0c/py0c test.py -o test.qd

# qd0 → LLVM IR
./qd0/qd0c/qd0c test.qd -o test.ll

# LLVM IR → host executable
cc test.ll qd0/qd0c/qd0lib.c -o test.host -lm
./test.host
```

## 10.6 Complete Flow Diagram

```
                    ┌─────────────────────────────────────────┐
                    │              cpy0 Toolchain             │
                    └─────────────────────────────────────────┘

  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
  │   .c    │ ──▶ │ c0c or  │ ──▶ │  LLVM   │ ──▶ │   .ll   │
  │ (source)│     │ clang   │     │   IR    │     │         │
  └─────────┘     └─────────┘     └─────────┘     └─────────┘
                                                        
                         ┌───────────────────────────────────┐
                         │           C Language Branch       │
                         │  ll0c ──▶ .s ──▶ rv0as ──▶ .o   │
                         │                 ──▶ rv0vm  exec  │
                         └───────────────────────────────────┘

                         ┌───────────────────────────────────┐
                         │         Python Branch            │
                         │  py0c ──▶ .qd ──▶ qd0c ──▶ .ll  │
                         │       bytecode       LLVM IR     │
                         │  ──▶ clang ──▶ host executable    │
                         │  ──▶ ll0c ──▶ rv0vm exec        │
                         └───────────────────────────────────┘
```

## 10.7 Why Learn This Toolchain?

### 10.7.1 Understanding Compiler Fundamentals

cpy0 demonstrates a real usable compiler system:
- **Frontend**: lexical, syntax, semantic analysis
- **Middle**: intermediate representation (LLVM IR, qd0 bytecode)
- **Backend**: instruction selection, register allocation, code emission

### 10.7.2 Understanding Different Language Compilation

- C language: traditional compilation flow
- Python: needs to convert to bytecode first, then compile

### 10.7.3 Understanding RISC-V Architecture

Final goal is generating RISC-V machine code, requiring:
- Understanding RISC-V instruction format
- Understanding calling conventions
- Understanding memory layout

## 10.8 Test Examples

### 10.8.1 fact.c - Factorial

```c
// fact.c
long long fact(long long n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
}

long long main() {
    return fact(10);
}
```

### 10.8.2 test.py - Python Test

```python
# test.py
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))
```

## 10.9 Makefile Usage

```bash
# All tests
make test

# Only C programs
make test_c

# Only Python programs
make test_py

# Compile specific file
make fact
make test

# Clean generated files
make clean

# Run specific program
make run name=fact
```

## 10.10 Summary

In this chapter we learned:
- cpy0 toolchain overall architecture
- C and Python compilation flows
- Each tool's function and input/output
- How to build and use the toolchain
- Value of learning this toolchain

## 10.11 Exercises

1. Read the Makefile and understand each target
2. Try modifying a C program and recompile/execute
3. Try modifying a Python program and recompile/execute
4. Research differences between c0c and clang output
5. Trace a complete program's compilation process
