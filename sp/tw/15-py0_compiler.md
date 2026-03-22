# 15. py0 編譯器——Python 到 qd0 位元組碼

## 15.1 為什麼要自製 Python 編譯器？

Python 是動態語言，通常透過直譯器執行。但 Python 程式碼也可以編譯成位元組碼以提高效能。

```
Python (.py)  →  位元組碼 (.pyc)  →  直譯器執行
                  或
                編譯到 IR  →  機器碼
```

## 15.2 py0 編譯器架構

py0 將 Python 子集編譯到 qd0（自訂虛擬機）位元組碼。

位置：[_code/cpy0/py0/](../_code/cpy0/py0/)

## 15.3 支援的 Python 語法

py0 支援 Python 的子集：
- 基本資料類型：int, float, str, bool
- 變數宣告和賦值
- 算術和比較運算子
- if/else 條件
- while 迴圈
- 函式定義和呼叫
- print 函式
- 基本內建函式

**不支援**：類別、例外、import、列表推導等

## 15.4 qd0 位元組碼

qd0 是一個簡單的堆疊式虛擬機位元組碼。

### 15.4.1 指令集

| 指令 | 說明 | 堆疊變化 |
|------|------|----------|
| LOAD_CONST | 載入常量 | → value |
| LOAD_FAST | 載入本地變數 | → value |
| STORE_FAST | 儲存本地變數 | value → |
| LOAD_GLOBAL | 載入全域變數 | → value |
| BINARY_OP | 二元運算 | a, b → result |
| COMPARE_OP | 比較運算 | a, b → result |
| POP_JUMP_IF_FALSE | 條件跳躍 | value → |
| JUMP_ABSOLUTE | 無條件跳躍 | |
| CALL_FUNCTION | 函式呼叫 | args → result |
| RETURN_VALUE | 返回值 | value → |
| MAKE_FUNCTION | 建立函式 | code → func |
| PRINT | 列印 | value → |

### 15.4.2 位元組碼格式

```
+------------------+
| Header           |  Magic + 版本
+------------------+
| Constants Pool   |  常量表
+------------------+
| Names Pool       |  名稱表
+------------------+
| Functions Pool   |  函式表
+------------------+
| Code Object      |
|  - instructions  |
|  - locals        |
|  - stack size    |
+------------------+
```

## 15.5 py0 編譯器實作

### 15.5.1 詞彙分析器

```c
// token 類型
enum {
    tok_int = 256, tok_float, tok_string, tok_ident,
    tok_def, tok_if, tok_else, tok_while, tok_return,
    tok_and, tok_or, tok_not,
    // ...
};

// 詞彙分析
void next_token() {
    skip_whitespace();
    if (isdigit(c)) return scan_number();
    if (isalpha(c) || c == '_') return scan_ident();
    // ...
}
```

### 15.5.2 語法分析器

使用遞迴下降解析器：

```c
// 解析程式
AST *parse_program() {
    AST *ast = new_node(AST_PROGRAM);
    while (tok != tok_eof) {
        if (tok == tok_def) {
            add_child(ast, parse_function());
        } else {
            add_child(ast, parse_statement());
        }
    }
    return ast;
}

// 解析函式定義
AST *parse_function() {
    expect(tok_def);
    char *name = ident;
    expect(tok_ident);
    expect('(');
    // 解析參數...
    expect(')');
    expect(':');
    AST *body = parse_block();
    return new_function_node(name, params, body);
}

// 解析表達式
AST *parse_expr(int precedence) {
    AST *left = parse_atom();
    while (is_binary_op(tok) && precedence_of(tok) >= precedence) {
        OpType op = tok;
        next_token();
        AST *right = parse_expr(precedence_of(op) + 1);
        left = new_binary_node(op, left, right);
    }
    return left;
}
```

### 15.5.3 程式碼生成器

將 AST 翻譯成 qd0 位元組碼：

```c
void gen_code(AST *node) {
    switch (node->type) {
        case AST_INT:
            emit(LOAD_CONST);
            emit_const_index(node->value);
            break;
            
        case AST_IDENT:
            emit(LOAD_FAST);
            emit_var_index(node->name);
            break;
            
        case AST_ASSIGN:
            gen_code(node->right);
            emit(STORE_FAST);
            emit_var_index(node->left->name);
            break;
            
        case AST_BINOP:
            gen_code(node->left);
            emit(PSH);
            gen_code(node->right);
            emit(BINARY_OP);
            emit_op_code(node->op);
            break;
            
        case AST_IF:
            gen_code(node->cond);
            emit(POP_JUMP_IF_FALSE);
            int else_patch = emit_placeholder();
            gen_code(node->then);
            if (node->else_part) {
                emit(JUMP_ABSOLUTE);
                int end_patch = emit_placeholder();
                patch(else_patch);
                gen_code(node->else_part);
                patch(end_patch);
            } else {
                patch(else_patch);
            }
            break;
            
        case AST_WHILE:
            int loop_start = get_code_pos();
            gen_code(node->cond);
            emit(POP_JUMP_IF_FALSE);
            int exit_patch = emit_placeholder();
            gen_code(node->body);
            emit(JUMP_ABSOLUTE);
            emit_jump_target(loop_start);
            patch(exit_patch);
            break;
            
        case AST_CALL:
            for (int i = 0; i < node->args->count; i++) {
                gen_code(node->args->items[i]);
            }
            emit(CALL_FUNCTION);
            emit_int(node->args->count);
            break;
    }
}
```

## 15.6 完整範例

### 輸入：test.py

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))
```

### 輸出：test.qd

```qd
; Constants
0
1
10
"fib"
"%d\n"

; Functions
function fib:
    instructions:
        LOAD_FAST 0           ; n
        LOAD_CONST 0         ; 0
        COMPARE_OP <=        ; n <= 1
        POP_JUMP_IF_FALSE L1 ; if not (n <= 1) goto L1
        LOAD_FAST 0           ; return n
        RETURN_VALUE
    L1:
        LOAD_FAST 0           ; n
        LOAD_CONST 0         ; 1
        BINARY_OP -          ; n - 1
        CALL_FUNCTION fib, 1  ; fib(n-1)
        LOAD_FAST 0           ; n
        LOAD_CONST 0         ; 1
        BINARY_OP -          ; n - 1
        CALL_FUNCTION fib, 1  ; fib(n-2)
        BINARY_OP +          ; fib(n-1) + fib(n-2)
        RETURN_VALUE

; Main
LOAD_CONST 2         ; 10
CALL_FUNCTION fib, 1 ; fib(10)
PRINT               ; print result
```

## 15.7 使用 py0

```bash
# 基本用法
./py0/py0c/py0c test.py -o test.qd

# 或使用 Makefile
make test_py
```

## 15.8 py0c 架構圖

```
+-------------------+
|   Python 原始碼    |
+-------------------+
         ↓
+-------------------+
|   詞彙分析器       |
|   (scanner)       |
+-------------------+
         ↓
+-------------------+
|   Token 流        |
+-------------------+
         ↓
+-------------------+
|   語法分析器       |
|   (parser)        |
+-------------------+
         ↓
+-------------------+
|   AST             |
+-------------------+
         ↓
+-------------------+
|   程式碼生成器     |
|   (codegen)       |
+-------------------+
         ↓
+-------------------+
|   qd0 位元組碼     |
+-------------------+
```

## 15.9 與標準 Python 直譯器比較

| 特性 | py0 | CPython |
|------|-----|---------|
| 語法覆蓋 | 子集 | 完整 |
| 速度 | 快（編譯後） | 慢（直譯） |
| 位元組碼 | qd0 | bytecode |
| VM | qd0 | CPython VM |
| 除錯 | 基本 | 完整 |
| 標準庫 | 無 | 完整 |

## 15.10 小結

本章節我們學習了：
- Python 編譯器的基本概念
- py0 編譯器的架構設計
- qd0 位元組碼格式
- 詞彙分析和語法分析
- AST 到位元組碼的轉換
- 完整範例
- py0 與 CPython 的比較

## 15.11 習題

1. 為 py0 添加 `for` 迴圈支援
2. 為 py0 添加 `+` 字串串聯支援
3. 研究如何添加簡單的類別支援
4. 比較 py0 和 MicroPython 的設計差異
5. 實現一個簡單的 qd0 直譯器
