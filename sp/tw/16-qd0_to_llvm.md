# 16. qd0c 轉換器——qd0 位元組碼到 LLVM IR

## 16.1 為什麼要轉換到 LLVM IR？

LLVM IR 是一個強大的中介表示，幾乎所有現代語言都可以編譯到它。將 qd0 位元組碼轉換到 LLVM IR 的好處：

- 可以使用 LLVM 的優化 passes
- 可以編譯到任何 LLVM 支援的目標架構
- 可以與 C/C++ 代碼無縫整合

## 16.2 qd0c 轉換器架構

位置：[_code/cpy0/qd0/](../_code/cpy0/qd0/)

```
qd0 位元組碼 (.qd)
       ↓
+-------------------+
|   qd0c            |
|   - 解析位元組碼   |
|   - 生成 LLVM IR  |
+-------------------+
       ↓
LLVM IR (.ll)
       ↓
+-------------------+
|   Clang/LLC       |
|   - 優化           |
|   - 目標碼生成     |
+-------------------+
       ↓
RISC-V / x86 執行檔
```

## 16.3 qd0c 的設計

### 16.3.1 位元組碼解析

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

### 16.3.2 解析流程

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

## 16.4 LLVM IR 生成

### 16.4.1 基本框架

```c
void emit_llvm_header(Module *m, FILE *out) {
    fprintf(out, "; ModuleID = 'qd0_module'\n");
    fprintf(out, "source_filename = \"qd0_module\"\n");
    fprintf(out, "target datalayout = \"e-m:e-i64:64-f80:128-n8:16:32:64-S128\"\n");
    fprintf(out, "target triple = \"x86_64-unknown-linux-gnu\"\n\n");
}
```

### 16.4.2 常量池生成

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

### 16.4.3 函式翻譯

```c
void emit_function(Function *f, FILE *out) {
    // 函式宣告
    fprintf(out, "define i64 @%s(", f->name);
    for (int i = 0; i < f->nargs; i++) {
        if (i > 0) fprintf(out, ", ");
        fprintf(out, "i64 %%arg_%d", i);
    }
    fprintf(out, ") {\n");
    
    // 分配本地變數
    fprintf(out, "entry:\n");
    for (int i = 0; i < f->nlocals; i++) {
        fprintf(out, "  %%local_%d = alloca i64\n", i);
    }
    
    // 初始化參數
    for (int i = 0; i < f->nargs; i++) {
        fprintf(out, "  store i64 %%arg_%d, i64* %%local_%d\n", i, i);
    }
    
    // 生成指令
    for (int i = 0; i < f->ninst; i++) {
        emit_instruction(&f->code[i], out);
    }
    
    fprintf(out, "}\n\n");
}
```

## 16.5 指令翻譯

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

### 16.5.6 JUMP 指令

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
    
    // 收集參數（倒序）
    char *args_list[10];
    for (int i = nargs - 1; i >= 0; i--) {
        args_list[i] = pop_temp();
    }
    
    // 生成 call
    fprintf(out, "  %%t%d = call i64 @%s(", temp_id++, func_name);
    for (int i = 0; i < nargs; i++) {
        if (i > 0) fprintf(out, ", ");
        fprintf(out, "i64 %s", args_list[i]);
    }
    fprintf(out, ")\n");
    push_temp(alloc_temp());
}
```

## 16.6 完整範例

### 輸入：test.qd

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

### 輸出：test.ll

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

## 16.7 使用 qd0c

```bash
# 基本用法
./qd0/qd0c/qd0c test.qd -o test.ll

# 編譯到主機執行
cc test.ll qd0/qd0c/qd0lib.c -o test.host -lm
./test.host

# 編譯到 RISC-V
llc -march=riscv64 test.ll -o test.s
./rv0/rv0as test.s -o test.o
./rv0/rv0vm test.o
```

## 16.8 qd0lib.c - C 函式庫

qd0 需要一些 C 函式的支援（如 printf）：

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

// 動態記憶體分配
void *qd0_alloc(int64_t size) {
    return malloc((size_t)size);
}

// exit
void qd0_exit(int64_t code) {
    exit((int)code);
}
```

## 16.9 完整流程圖

```
Python (.py)
     ↓ [py0c]
qd0 (.qd)
     ↓ [qd0c]
LLVM IR (.ll)
     ↓ [Clang/LLC]
     ├──→ 主機執行檔 (x86)
     └──→ RISC-V (.s → .o)
              ↓ [rv0vm]
          RISC-V 執行
```

## 16.10 小結

本章節我們學習了：
- qd0c 轉換器的架構設計
- qd0 位元組碼解析
- 各 qd0 指令到 LLVM IR 的翻譯
- qd0lib.c 函式庫
- 完整流程
- 編譯到不同目標

## 16.11 習題

1. 為 qd0c 添加對浮點運算的支援
2. 研究如何優化生成的 LLVM IR
3. 為 qd0c 添加對字串內建的支援
4. 比較 qd0c 和 LuaJIT 的 IR 生成
5. 實現一個簡單的 JIT 編譯器
