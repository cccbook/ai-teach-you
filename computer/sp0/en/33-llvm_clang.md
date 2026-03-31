# 33. LLVM/Clang——Modular Compiler Framework

## 33.1 LLVM Project

LLVM is not just a compiler, but a **modular compiler framework**:

```
         ┌─────────────────────────┐
         │     Application            │
         └───────────┬─────────────┘
                     │
         ┌───────────▼───────────────┐
         │        Clang              │ ← C/C++/Objective-C frontend
         │     (Parsing, Semantic)  │
         └───────────┬───────────────┘
                     │
         ┌───────────▼───────────────┐
         │      LLVM Core            │ ← Intermediate Representation (IR)
         │  (Optimization, CodeGen)  │
         └───────────┬───────────────┘
                     │
         ┌───────────┼───────────────┐
         │           │               │
    ┌────▼────┐ ┌───▼───┐    ┌─────▼─────┐
    │  x86    │ │ ARM   │    │  RISC-V  │
    │ backend │ │ backend│    │  backend  │
    └─────────┘ └───────┘    └───────────┘
```

## 33.2 Clang Features

### 33.2.1 Fast Compilation

```bash
clang -O2 hello.c -o hello
```

### 33.2.2 Clear Error Messages

```c
// error.c
int main() {
    int* p = 0;
    return *p;  // Null pointer dereference
}
```

```bash
clang error.c -o error
# Output:
# error.c:3:12: warning: null pointer returned from function returning non-null 'int' [-Wreturn-stack-address]
#     return *p;
#            ^
# error.c:3:12: error: indirection requires pointer operand ('int' invalid)
```

## 33.3 LLVM IR

### 33.3.1 Generate IR

```bash
clang -S -emit-llvm hello.c -o hello.ll
```

### 33.3.2 View IR

```llvm
; hello.ll
@.str = private constant [12 x i8] c"Hello World\00"

define i32 @main() {
entry:
    %call = call i32 @puts(i8* getelementptr inbounds ([12 x i8], [12 x i8]* @.str, i64 0, i64 0))
    ret i32 0
}

declare i32 @puts(i8*)
```

## 33.4 Toolchain

### 33.4.1 opt - Optimization

```bash
opt -S -O2 hello.ll -o hello_opt.ll
```

### 33.4.2 llc - Compile to Assembly

```bash
llc hello.ll -o hello.s
llc -march=riscv64 hello.ll -o hello_rv.s
```

### 33.4.3 lli - Interpret Execution

```bash
lli hello.ll
```

### 33.4.4 llvm-dis - Disassemble

```bash
llvm-dis hello.bc -o hello.ll
```

## 33.5 Static Analysis

### 33.5.1 scan-build

```bash
scan-build clang hello.c -o hello
```

### 33.5.2 clang --analyze

```bash
clang --analyze hello.c
```

## 33.6 AST Viewing

```bash
# Show abstract syntax tree
clang -Xclang -ast-dump hello.c

# Show semantic diff view
clang -Xclang -ast-view hello.c
```

## 33.7 Summary

In this chapter we learned:
- LLVM project architecture
- Clang features
- LLVM IR usage
- opt, llc, lli tools
- Static analysis tools

## 33.8 Exercises

1. Use `clang -ast-dump` to view AST
2. Compare GCC and Clang error messages
3. Experiment with different optimization passes using `opt`
4. Research LLVM pass manager
5. Implement a simple LLVM pass
