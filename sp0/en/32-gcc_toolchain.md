# 32. GCC Toolchain——From Source to Executable

## 32.1 GCC Toolchain Overview

GNU Compiler Collection (GCC) is the core compiler of the GNU project:

```
Source ──→ Preprocessor ──→ Compiler ──→ Assembler ──→ Linker ──→ Executable
  .c          .i           .s        .o        a.out
```

## 32.2 Compilation Process

### 32.2.1 Complete Compilation

```bash
gcc hello.c -o hello
```

### 32.2.2 Step-by-Step Execution

```bash
# Preprocess
gcc -E hello.c -o hello.i

# Compile (no assembly)
gcc -S hello.c -o hello.s

# Assemble (no linking)
gcc -c hello.c -o hello.o

# Link
gcc hello.o -o hello
```

## 32.3 Important GCC Options

### 32.3.1 Warning Options

```bash
gcc -Wall hello.c       # All warnings
gcc -Wextra hello.c     # Extra warnings
gcc -Werror hello.c     # Warnings as errors
gcc -pedantic hello.c   # ISO C warnings
```

### 32.3.2 Optimization Options

```bash
gcc -O0 hello.c         # No optimization
gcc -O1 hello.c         # Basic optimization
gcc -O2 hello.c         # Standard optimization
gcc -O3 hello.c         # Aggressive optimization
gcc -Os hello.c         # Size optimization
gcc -Ofast hello.c      # Fast optimization (includes floating-point)
```

### 32.3.3 Debug Options

```bash
gcc -g hello.c                      # Generate debug info
gcc -g3 hello.c                     # Include macro definitions
gcc -ggdb hello.c                    # GDB-specific format
```

## 32.4 Libraries

### 32.4.1 Static Linking

```bash
gcc -static hello.c -o hello_static
```

### 32.4.2 Dynamic Linking

```bash
gcc -shared foo.c -o libfoo.so
gcc -L. -lfoo main.c -o main
```

### 32.4.3 Search Paths

```bash
gcc -I./include hello.c     # Header search path
gcc -L./lib hello.c         # Library search path
```

## 32.5 Target Architecture

### 32.5.1 Specify Target

```bash
gcc -target riscv64-unknown-elf hello.c
```

### 32.5.2 Cross-Compilation

```bash
# Compile RISC-V on x86_64
riscv64-unknown-elf-gcc hello.c -o hello.rv
```

## 32.6 Static Analysis

### 32.6.1 Using Compiler

```bash
gcc -fsyntax-only hello.c        ; Syntax check only
gcc -fanalyzer hello.c           ; Static analysis
```

### 32.6.2 Other Tools

```bash
# Link-time optimization
gcc -flto hello.c -o hello

# Virtual function elimination threshold
gcc -fvirtual-function-elimination hello.c
```

## 32.7 Practical Tips

### 32.7.1 Conditional Compilation

```bash
# Define macro
gcc -DDEBUG=1 hello.c -o hello

# Undefine macro
gcc -UMY_MACRO hello.c -o hello
```

### 32.7.2 Version Information

```bash
__DATE__    ; Compilation date
__TIME__    ; Compilation time
__FILE__    ; Source file name
__LINE__    ; Line number
__VERSION__ ; GCC version
```

## 32.8 Summary

In this chapter we learned:
- Complete GCC toolchain flow
- Step-by-step compilation
- Important compilation options
- Library handling
- Cross-compilation
- Static analysis

## 32.9 Exercises

1. Use `-S` to view assembly differences between optimization levels
2. Implement a debug system using conditional compilation
3. Research `-flto` link-time optimization
4. Compare static and dynamic linking performance
5. Cross-compile the same program for different architectures
