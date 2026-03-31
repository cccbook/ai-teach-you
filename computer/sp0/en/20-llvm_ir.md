# 20. LLVM IR——Modern Compiler's Intermediate Representation

## 20.1 Introduction to LLVM IR

LLVM IR (Intermediate Representation) is the core of the LLVM compiler framework. It is:
- **Static Single Assignment (SSA)**: Each variable is assigned only once
- **Type-safe**: All values have explicit types
- **Readable**: Almost like assembly but more abstract

## 20.2 LLVM IR Basic Syntax

### 20.2.1 Module Structure

```llvm
; ModuleID = 'module_name'
source_filename = "filename.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Global variables
@global_var = global i32 42
@str = private constant [13 x i8] c"Hello World\00"

; Function definition
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

declare i32 @printf(i8*, ...)
```

## 20.3 Basic Types

| IR Type | C Equivalent | Size |
|---------|-------------|------|
| `i1` | `_Bool` | 1 bit |
| `i8` | `char` | 8 bits |
| `i16` | `short` | 16 bits |
| `i32` | `int` | 32 bits |
| `i64` | `long long` | 64 bits |
| `half` | `__fp16` | 16 bits |
| `float` | `float` | 32 bits |
| `double` | `double` | 64 bits |
| `void` | `void` | - |

## 20.4 Composite Types

```llvm
; Pointers
i32*                    ; int*
i8*                     ; char*

; Arrays
[10 x i32]              ; int[10]
[4 x i8]                ; char[4]

; Structs
%struct.Point = type { i64, i64 }  ; struct Point { long long x, y; }

; Vectors (SIMD)
<4 x float>             ; __m128
```

## 20.5 Global Symbols

```llvm
; Constants
@pi = constant double 3.141592653589793

; Global variables
@counter = global i32 0
@counter = uninitialized global i32 0

; Read-only global variables
@msg = constant [13 x i8] c"Hello World\00"
```

## 20.6 Instruction Classification

### 20.6.1 Binary Operations

```llvm
; Arithmetic
%add = add i32 %a, %b
%sub = sub i32 %a, %b
%mul = mul i32 %a, %b
%sdiv = sdiv i32 %a, %b      ; signed division
%udiv = udiv i32 %a, %b      ; unsigned division
%srem = srem i32 %a, %b      ; signed remainder
%urem = urem i32 %a, %b      ; unsigned remainder

; Bitwise
%and = and i32 %a, %b
%or  = or  i32 %a, %b
%xor = xor i32 %a, %b
%shl = shl i32 %a, %b
%lshr = lshr i32 %a, %b     ; logical right shift
%ashr = ashr i32 %a, %b     ; arithmetic right shift
```

### 20.6.2 Comparison Instructions

```llvm
; Set on Condition (result is i1: 1 or 0)

%eq  = icmp eq   i32 %a, %b    ; ==
%ne  = icmp ne   i32 %a, %b    ; !=
%slt = icmp slt  i32 %a, %b    ; <  (signed)
%ult = icmp ult  i32 %a, %b    ; <  (unsigned)
%sle = icmp sle  i32 %a, %b    ; <= (signed)
%ule = icmp ule  i32 %a, %b    ; <= (unsigned)
%sgt = icmp sgt  i32 %a, %b    ; >  (signed)
%ugt = icmp ugt  i32 %a, %b    ; >  (unsigned)
%sge = icmp sge  i32 %a, %b    ; >= (signed)
%uge = icmp uge  i32 %a, %b    ; >= (unsigned)

; Floating-point comparisons
%fcmp = fcmp oeq float %a, %b  ; ordered equal
%fcmp = fcmp one float %a, %b   ; ordered not equal
%fcmp = fcmp olt float %a, %b   ; ordered less than
```

### 20.6.3 Memory Instructions

```llvm
; Allocate local space (on stack)
%ptr = alloca i32              ; int* ptr = alloca(int);
%ptr = alloca i32, align 4     ; 4-byte aligned

; Load
%val = load i32, i32* %ptr     ; int val = *ptr;

; Store
store i32 %val, i32* %ptr      ; *ptr = val;

; Get element pointer
%elem = getelementptr i32, i32* %arr, i64 %idx
%val = load i32, i32* %elem
```

### 20.6.4 GetElementPtr (GEP)

GEP is the standard way to compute pointer offsets in LLVM:

```llvm
; Array element
%arr = alloca [10 x i32]
%idx = load i64, i64* %idx_ptr
%elem_ptr = getelementptr [10 x i32], [10 x i32]* %arr, i64 0, i64 %idx
%val = load i32, i32* %elem_ptr

; Struct member
%pt = alloca %struct.Point
%x_ptr = getelementptr %struct.Point, %struct.Point* %pt, i64 0, i32 0
store i64 10, i64* %x_ptr
```

### 20.6.5 Control Flow

```llvm
; Unconditional jump
br label %dest

; Conditional jump
%cmp = icmp eq i32 %a, %b
br i1 %cmp, label %then, label %else

; PHI node (SSA form)
%result = phi i32 [ %val1, %label1 ], [ %val2, %label2 ]
```

### 20.6.6 PHI Nodes

PHI nodes select values based on predecessor block:

```llvm
; C code:
; int foo(int x) {
;     if (x > 0) return x;
;     else return -x;
; }

define i32 @foo(i32 %x) {
entry:
    %cmp = icmp sgt i32 %x, 0
    br i1 %cmp, label %then, label %else

then:
    ret i32 %x

else:
    %neg = sub i32 0, %x
    ret i32 %neg
}

; No PHI because both branches return
```

Complex example (loop):
```llvm
loop:
    %i_old = phi i32 [ 0, %entry ], [ %i_new, %loop ]
    ; ... loop body ...
    %i_new = add i32 %i_old, 1
    %cmp = icmp slt i32 %i_new, %n
    br i1 %cmp, label %loop, label %exit
```

### 20.6.7 Function Calls

```llvm
; Direct call
%result = call i32 @add(i32 %a, i32 %b)

; Call via pointer
%fp = load i32 (i32, i32)*, i32 (i32, i32)** @func_ptr
%result = call i32 %fp(i32 %a, i32 %b)

; Declare external functions
declare i32 @printf(i8*, ...)
declare void @exit(i32)

; Variadic
declare i32 @scanf(i8*, ...)
```

### 20.6.8 Select

```llvm
%max = select i1 %cmp, i32 %a, i32 %b
; equivalent to: %max = %cmp ? %a : %b;
```

## 20.7 Complete Example

### 20.7.1 C Program

```c
#include <stdio.h>

long long sum_array(long long *arr, int n) {
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}

int main() {
    long long data[] = {1, 2, 3, 4, 5};
    printf("%lld\n", sum_array(data, 5));
    return 0;
}
```

### 20.7.2 Generated LLVM IR

```llvm
@.str = private constant [4 x i8] c"%lld\0A\00"

define i64 @sum_array(i64* %arr, i32 %n) {
entry:
    %sum = alloca i64, align 8
    %i = alloca i32, align 4
    store i64 0, i64* %sum, align 8
    store i32 0, i32* %i, align 4
    br label %for.cond

for.cond:
    %i_val = load i32, i32* %i
    %cmp = icmp slt i32 %i_val, %n
    br i1 %cmp, label %for.body, label %for.end

for.body:
    %sum_val = load i64, i64* %sum
    %i_val2 = load i32, i32* %i
    %idxprom = sext i32 %i_val2 to i64
    %arrayidx = getelementptr i64, i64* %arr, i64 %idxprom
    %val = load i64, i64* %arrayidx
    %add = add i64 %sum_val, %val
    store i64 %add, i64* %sum
    br label %for.inc

for.inc:
    %i_val3 = load i32, i32* %i
    %inc = add i32 %i_val3, 1
    store i32 %inc, i32* %i
    br label %for.cond

for.end:
    %result = load i64, i64* %sum
    ret i64 %result
}

define i32 @main() {
entry:
    %data = alloca [5 x i64], align 8
    %arraydecay = getelementptr [5 x i64], [5 x i64]* %data, i64 0, i64 0
    call void @llvm.memset.p0i8.i64(i8* align 8 %arraydecay, i8 0, i64 40, i1 false)
    %sum = call i64 @sum_array(i64* %arraydecay, i32 5)
    %call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i64 0, i64 0), i64 %sum)
    ret i32 0
}

declare i32 @printf(i8*, ...)
declare void @llvm.memset.p0i8.i64(i8*, i8, i64, i1)
```

## 20.8 Generate IR with Clang

```bash
# Generate readable IR
clang -S -emit-llvm -O0 foo.c -o foo.ll

# Generate bitcode
clang -c -emit-llvm foo.c -o foo.bc

# Specify target
clang -S -emit-llvm --target=riscv64 foo.c -o foo.ll

# Show optimized IR
clang -S -emit-llvm -O2 foo.c -o foo_O2.ll
```

## 20.9 Optimize with opt

```bash
# Basic optimization
opt -O2 foo.ll -S -o foo_opt.ll

# View passes
opt --help | grep -i pass

# Specific optimizations
opt -mem2reg foo.ll -S -o foo_reg2mem.ll  ; register promotion
opt -gvn foo.ll -S -o foo_gvn.ll          ; global value numbering
opt -dce foo.ll -S -o foo_dce.ll          ; dead code elimination
```

## 20.10 Execute IR with lli

```bash
# Execute IR directly
lli foo.ll

# Or execute bitcode
lli foo.bc
```

## 20.11 Summary

In this chapter we learned:
- LLVM IR basic syntax
- Type system (basic and composite)
- Binary operations and comparison instructions
- Memory instructions (alloca, load, store, gep)
- Control flow instructions
- PHI nodes and SSA form
- Function calls
- Using Clang and opt tools

## 20.12 Exercises

1. Use `clang -S -emit-llvm` to generate IR for a program with structs
2. Research how PHI nodes implement SSA form
3. Experiment with different optimization passes using `opt`
4. Implement a simple LLVM IR to x86 compiler
5. Research various uses of the `getelementptr` instruction
