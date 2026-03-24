# 16. qd0c Converter——qd0 Bytecode to LLVM IR

## 16.1 Why Convert to LLVM IR?

LLVM IR is a powerful intermediate representation. Almost all modern languages can compile to it. Benefits of converting qd0 bytecode to LLVM IR:

- Can use LLVM's optimization passes
- Can compile to any architecture LLVM supports
- Can seamlessly integrate with C/C++ code

## 16.2 qd0c Converter Architecture

Location: [_code/cpy0/qd0/](../_code/cpy0/qd0/)

```
qd0 Bytecode (.qd)
       ↓
+-------------------+
|   qd0c            |
|   - Parse bytecode |
|   - Generate LLVM IR|
+-------------------+
       ↓
LLVM IR (.ll)
       ↓
+-------------------+
|   Clang/LLC       |
|   - Optimize       |
|   - Target code    |
+-------------------+
       ↓
RISC-V / x86 Executable
```

## 16.3 qd0c Design

### 16.3.1 Bytecode Parsing

```c
typedef struct {
    int type;
    union {
        int iconst;
        double fconst;
        char *sconst;
        char *name;
        int label;
    } val;
} Operand;

typedef struct {
    int opcode;
    Operand *args;
    int nargs;
} Instruction;

typedef struct {
    char *name;
    int nlocals;
    int nstack;
    Instruction *code;
    int ninst;
} Function;

typedef struct {
    Constant *constants;
    int nconsts;
    Function *functions;
    int nfuncs;
} Module;
```

### 16.3.2 Parsing Flow

```c
Module *parse_qd(const char *filename) {
    FILE *f = fopen(filename, "r");
    Module *m = new_module();
    
    char line[256];
    while (fgets(line, sizeof(line), f)) {
        if (line[0] == ';' || line[0] == '\n') continue;
        
        if (strcmp(line, "; Constants") == 0) {
            parse_constants(m);
        } else if (strcmp(line, "; Functions") == 0) {
            parse_functions(m);
        } else if (line[0] == ' ') {
            parse_instruction(m, line);
        }
    }
    
    fclose(f);
    return m;
}
```

## 16.4 LLVM IR Generation

### 16.4.1 Basic Framework

```c
void emit_llvm_header(Module *m, FILE *out) {
    fprintf(out, "; ModuleID = 'qd0_module'\n");
    fprintf(out, "source_filename = \"qd0_module\"\n");
    fprintf(out, "target datalayout = \"e-m:e-i64:64-f80:128-n8:16:32:64-S128\"\n");
    fprintf(out, "target triple = \"x86_64-unknown-linux-gnu\"\n\n");
}
```

### 16.4.2 Constants Pool Generation

```c
void emit_constants(Module *m, FILE *out) {
    for (int i = 0; i < m->nconsts; i++) {
        Constant *c = &m->constants[i];
        switch (c->type) {
            case CONST_INT:
                fprintf(out, "@const_int_%d = private constant i64 %d\n", i, c->val.iconst);
                break;
            case CONST_FLOAT:
                fprintf(out, "@const_float_%d = private constant double %f\n", i, c->val.fconst);
                break;
            case CONST_STRING:
                fprintf(out, "@const_str_%d = private constant [%ld x i8] c\"%s\\00\"\n",
                    i, strlen(c->val.sconst) + 1, c->val.sconst);
                break;
        }
    }
}
```

### 16.4.3 Function Translation

```c
void emit_function(Function *f, FILE *out) {
    // Function declaration
    fprintf(out, "define i64 @%s(", f->name);
    for (int i = 0; i < f->nargs; i++) {
        if (i > 0) fprintf(out, ", ");
        fprintf(out, "i64 %%arg_%d", i);
    }
    fprintf(out, ") {\n");
    
    // Allocate locals
    fprintf(out, "entry:\n");
    for (int i = 0; i < f->nlocals; i++) {
        fprintf(out, "  %%local_%d = alloca i64\n", i);
    }
    
    // Initialize parameters
    for (int i = 0; i < f->nargs; i++) {
        fprintf(out, "  store i64 %%arg_%d, i64* %%local_%d\n", i, i);
    }
    
    // Generate instructions
    for (int i = 0; i < f->ninst; i++) {
        emit_instruction(&f->code[i], out);
    }
    
    fprintf(out, "}\n\n");
}
```

## 16.5 Instruction Translation

### 16.5.1 LOAD_CONST

```c
void emit_LOAD_CONST(Operand *args, FILE *out) {
    int idx = args[0].val.iconst;
    fprintf(out, "  %%t%d = load i64, i64* @const_int_%d\n", temp_id++, idx);
}
```

### 16.5.2 LOAD_FAST

```c
void emit_LOAD_FAST(Operand *args, FILE *out) {
    int idx = args[0].val.iconst;
    fprintf(out, "  %%t%d = load i64, i64* %%local_%d\n", temp_id++, idx);
}
```

### 16.5.3 STORE_FAST

```c
void emit_STORE_FAST(Operand *args, FILE *out) {
    int idx = args[0].val.iconst;
    fprintf(out, "  store i64 %s, i64* %%local_%d\n", pop_temp(), idx);
}
```

### 16.5.4 BINARY_OP

```c
void emit_BINARY_OP(Operand *args, FILE *out) {
    char *b = pop_temp();
    char *a = pop_temp();
    char *result = alloc_temp();
    
    switch (args[0].val.iconst) {
        case '+':
            fprintf(out, "  %s = add i64 %s, %s\n", result, a, b);
            break;
        case '-':
            fprintf(out, "  %s = sub i64 %s, %s\n", result, a, b);
            break;
        case '*':
            fprintf(out, "  %s = mul i64 %s, %s\n", result, a, b);
            break;
        case '/':
            fprintf(out, "  %s = sdiv i64 %s, %s\n", result, a, b);
            break;
        // ...
    }
    push_temp(result);
}
```

### 16.5.5 COMPARE_OP

```c
void emit_COMPARE_OP(Operand *args, FILE *out) {
    char *b = pop_temp();
    char *a = pop_temp();
    char *result = alloc_temp();
    
    switch (args[0].val.iconst) {
        case '<':
            fprintf(out, "  %s = icmp slt i64 %s, %s\n", result, a, b);
            break;
        case LE:
            fprintf(out, "  %s = icmp sle i64 %s, %s\n", result, a, b);
            break;
        case '>':
            fprintf(out, "  %s = icmp sgt i64 %s, %s\n", result, a, b);
            break;
        case GE:
            fprintf(out, "  %s = icmp sge i64 %s, %s\n", result, a, b);
            break;
        case EQ:
            fprintf(out, "  %s = icmp eq i64 %s, %s\n", result, a, b);
            break;
        case NE:
            fprintf(out, "  %s = icmp ne i64 %s, %s\n", result, a, b);
            break;
    }
    push_temp(result);
}
```

### 16.5.6 JUMP Instructions

```c
void emit_POP_JUMP_IF_FALSE(Operand *args, FILE *out) {
    char *cond = pop_temp();
    fprintf(out, "  br i1 %s, label %%l%d, label %%l%d\n", 
        cond, current_label, args[0].val.label);
}

void emit_JUMP_ABSOLUTE(Operand *args, FILE *out) {
    fprintf(out, "  br label %%l%d\n", args[0].val.label);
}
```

### 16.5.7 CALL_FUNCTION

```c
void emit_CALL_FUNCTION(Operand *args, FILE *out) {
    int nargs = args[0].val.iconst;
    char *func_name = args[1].val.name;
    
    // Collect arguments (reverse order)
    char *args_list[10];
    for (int i = nargs - 1; i >= 0; i--) {
        args_list[i] = pop_temp();
    }
    
    // Generate call
    fprintf(out, "  %%t%d = call i64 @%s(", temp_id++, func_name);
    for (int i = 0; i < nargs; i++) {
        if (i > 0) fprintf(out, ", ");
        fprintf(out, "i64 %s", args_list[i]);
    }
    fprintf(out, ")\n");
    push_temp(alloc_temp());
}
```

## 16.6 Complete Example

### Input: test.qd

```qd
; Constants
0
1
10
"fib"
"%d\n"

function fib:
    LOAD_FAST 0
    LOAD_CONST 0
    COMPARE_OP <=
    POP_JUMP_IF_FALSE L1
    LOAD_FAST 0
    RETURN_VALUE
L1:
    LOAD_FAST 0
    LOAD_CONST 0
    BINARY_OP -
    CALL_FUNCTION fib, 1
    LOAD_FAST 0
    LOAD_CONST 0
    BINARY_OP -
    CALL_FUNCTION fib, 1
    BINARY_OP +
    RETURN_VALUE
```

### Output: test.ll

```llvm
; ModuleID = 'qd0_module'
source_filename = "qd0_module"

define i64 @fib(i64 %arg_0) {
entry:
  %local_0 = alloca i64
  store i64 %arg_0, i64* %local_0
  
  %t0 = load i64, i64* %local_0
  %t1 = load i64, i64* @const_int_0
  %t2 = icmp sle i64 %t0, %t1
  br i1 %t2, label %L0, label %L1

L0:
  %t3 = load i64, i64* %local_0
  ret i64 %t3

L1:
  %t4 = load i64, i64* %local_0
  %t5 = load i64, i64* @const_int_0
  %t6 = sub i64 %t4, %t5
  %t7 = call i64 @fib(i64 %t6)
  %t8 = load i64, i64* %local_0
  %t9 = load i64, i64* @const_int_0
  %t10 = sub i64 %t8, %t9
  %t11 = call i64 @fib(i64 %t10)
  %t12 = add i64 %t7, %t11
  ret i64 %t12
}

define i64 @main() {
entry:
  %t0 = load i64, i64* @const_int_2
  %t1 = call i64 @fib(i64 %t0)
  ; printf call...
  ret i64 0
}
```

## 16.7 Using qd0c

```bash
# Basic usage
./qd0/qd0c/qd0c test.qd -o test.ll

# Compile to host executable
cc test.ll qd0/qd0c/qd0lib.c -o test.host -lm
./test.host

# Compile to RISC-V
llc -march=riscv64 test.ll -o test.s
./rv0/rv0as test.s -o test.o
./rv0/rv0vm test.o
```

## 16.8 qd0lib.c - C Library

qd0 needs C library support (like printf):

```c
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

// printf("%d\n", value)
int64_t qd0_print_int(int64_t x) {
    printf("%" PRId64 "\n", x);
    return x;
}

// printf("%f\n", value)
double qd0_print_float(double x) {
    printf("%f\n", x);
    return x;
}

// dynamic memory allocation
void *qd0_alloc(int64_t size) {
    return malloc((size_t)size);
}

// exit
void qd0_exit(int64_t code) {
    exit((int)code);
}
```

## 16.9 Complete Flow Diagram

```
Python (.py)
     ↓ [py0c]
qd0 (.qd)
     ↓ [qd0c]
LLVM IR (.ll)
     ↓ [Clang/LLC]
     ├──→ Host executable (x86)
     └──→ RISC-V (.s → .o)
              ↓ [rv0vm]
          RISC-V execution
```

## 16.10 Summary

In this chapter we learned:
- qd0c converter architecture design
- qd0 bytecode parsing
- Each qd0 instruction to LLVM IR translation
- qd0lib.c library
- Complete flow
- Compiling to different targets

## 16.11 Exercises

1. Add floating point operation support to qd0c
2. Research how to optimize generated LLVM IR
3. Add string built-in support to qd0c
4. Compare qd0c and LuaJIT IR generation
5. Implement a simple JIT compiler
