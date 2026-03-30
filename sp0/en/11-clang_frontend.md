# 11. Clang Frontend——C Language to LLVM IR

## 11.1 Clang Introduction

Clang is part of the LLVM project, a C/C++/Objective-C compiler frontend. Known for speed and clear error messages.

```bash
# Basic usage
clang hello.c -o hello

# Generate LLVM IR
clang -S -emit-llvm hello.c -o hello.ll

# Generate Bitcode
clang -c -emit-llvm hello.c -o hello.bc
```

## 11.2 LLVM IR Introduction

LLVM IR (Intermediate Representation) is LLVM's intermediate representation language:
- Static Single Assignment (SSA) form
- Infinite virtual registers
- Type-safe
- Highly readable

## 11.3 Simple Program IR

Source:
```c
long long fact(long long n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
}
```

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

## 11.4 IR Basic Structure

### 11.4.1 Module

```llvm
; Module start
source_filename = "test.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "riscv64-unknown-linux-gnu"

; Definitions
@global_var = global i32 42
@str = private constant [13 x i8] c"Hello World\00"

; Function definition
define i64 @fact(i64 %n) { ... }
```

### 11.4.2 Type System

| IR Type | C Equivalent | Description |
|---------|--------------|-------------|
| `i8` | `char` | 8-bit integer |
| `i16` | `short` | 16-bit integer |
| `i32` | `int` | 32-bit integer |
| `i64` | `long long` | 64-bit integer |
| `float` | `float` | single precision |
| `double` | `double` | double precision |
| `i8*` | `char*` | pointer |
| `[N x i8]` | `char[N]` | array |

### 11.4.3 Function Types

```llvm
@func = declare i32 @external_func(i32 %a, i64 %b)
define i64 @fact(i64 %n) { ... }
define void @void_func() { ... }
```

## 11.5 Using Clang to Generate IR

### 11.5.1 Basic Commands

```bash
# Generate readable IR (-S)
clang -S -emit-llvm fact.c -o fact.ll

# Generate Bitcode (-c)
clang -c -emit-llvm fact.c -o fact.bc

# Show pre-optimization IR
clang -S -emit-llvm -O0 fact.c -o fact_O0.ll

# Show post-optimization IR
clang -S -emit-llvm -O2 fact.c -o fact_O2.ll
```

### 11.5.2 Specify Target Architecture

```bash
# RISC-V 64-bit
clang -S -emit-llvm \
    --target=riscv64 \
    -march=rv64g \
    -mabi=lp64d \
    fact.c -o fact.ll
```

### 11.5.3 View Generated IR

```bash
cat fact.ll
```

## 11.6 IR Instruction Details

### 11.6.1 Arithmetic Instructions

```llvm
%add = add i64 %a, %b      ; addition
%sub = sub i64 %a, %b      ; subtraction
%mul = mul i64 %a, %b      ; multiplication
%sdiv = sdiv i64 %a, %b    ; signed division
%udiv = udiv i64 %a, %b    ; unsigned division
%srem = srem i64 %a, %b    ; signed remainder
%urem = urem i64 %a, %b    ; unsigned remainder
```

### 11.6.2 Bitwise Instructions

```llvm
%and = and i64 %a, %b       ; bitwise AND
%or = or i64 %a, %b        ; bitwise OR
%xor = xor i64 %a, %b      ; bitwise XOR
%shl = shl i64 %a, %b      ; left shift
%lshr = lshr i64 %a, %b    ; logical right shift
%ashr = ashr i64 %a, %b    ; arithmetic right shift
```

### 11.6.3 Comparison Instructions

```llvm
%cmp = icmp eq i64 %a, %b     ; ==
%cmp = icmp ne i64 %a, %b     ; !=
%cmp = icmp slt i64 %a, %b    ; < (signed)
%cmp = icmp ult i64 %a, %b    ; < (unsigned)
%cmp = icmp sgt i64 %a, %b    ; > (signed)
%cmp = icmp sge i64 %a, %b    ; >= (signed)
```

### 11.6.4 Memory Instructions

```llvm
%val = load i64, i64* %ptr        ; load
store i64 %val, i64* %ptr         ; store
%addr = alloca i64                ; allocate local space
%addr = getelementptr i64, i64* %arr, i64 %idx  ; get element address
```

### 11.6.5 Control Flow

```llvm
br label %dest              ; unconditional jump
br i1 %cond, label %if, label %else  ; conditional jump

%sel = select i1 %cond, i64 %a, i64 %b  ; conditional select

switch i64 %val, label %default [
    i64 0, label %case0
    i64 1, label %case1
]
```

## 11.7 Complete Example Analysis

Source:
```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 10;
    int y = 20;
    int z = add(x, y);
    printf("%d + %d = %d\n", x, y, z);
    return 0;
}
```

Generated IR:
```llvm
@.str = private constant [21 x i8] c"%d + %d = %d\0A\00"

define i32 @add(i32 %a, i32 %b) {
entry:
    %add = add i32 %a, %b
    ret i32 %add
}

define i32 @main() {
entry:
    %x = alloca i32
    %y = alloca i32
    %z = alloca i32
    store i32 10, i32* %x
    store i32 20, i32* %y
    %x_val = load i32, i32* %x
    %y_val = load i32, i32* %y
    %call = call i32 @add(i32 %x_val, i32 %y_val)
    store i32 %call, i32* %z
    %x_val2 = load i32, i32* %x
    %y_val2 = load i32, i32* %y
    %z_val = load i32, i32* %z
    %call2 = call i32 (i8*, ...) @printf(i8* getelementptr...)
    ret i32 0
}

declare i32 @printf(i8*, ...)
```

## 11.8 Other Clang Features

### 11.8.1 Static Analysis

```bash
# Static analysis
clang --analyze hello.c

# Use scan-build
scan-build clang hello.c -o hello
```

### 11.8.2 Syntax Check Only

```bash
# Only syntax and semantic check
clang -fsyntax-only hello.c

# Show errors and warnings
clang -Wall -Wextra -pedantic hello.c
```

### 11.8.3 Dependency Tracking

```bash
# Generate dependencies
clang -MM hello.c

# Generate system framework dependencies
clang -MMD -MF hello.d -c hello.c
```

## 11.9 Using llvm-dis to View Bitcode

```bash
# Bitcode → IR
llvm-dis fact.bc -o fact_from_bc.ll

# Formatted output
llvm-dis fact.bc -o - | clang-format
```

## 11.10 Summary

In this chapter we learned:
- Clang compiler frontend basics
- LLVM IR type system
- IR basic structure and instructions
- Using Clang to generate and view IR
- IR to C source correspondence

## 11.11 Exercises

1. Generate IR for `fact.c` in cpy0 with `clang -S -emit-llvm`
2. Compare IR generated with `-O0`, `-O1`, `-O2`, `-O3`
3. Generate RISC-V target IR for cpy0's C programs
4. Research `getelementptr` instruction usage
5. Write a simple LLVM IR program and execute with `lli`
