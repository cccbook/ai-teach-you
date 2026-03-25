# 4. 編譯器

## 4.1 編譯器架構

### 4.1.1 編譯器的基本概念

編譯器（Compiler）是將高階語言寫成的原始碼翻譯為機器語言或低階語言的系統軟體。

**編譯器的核心任務**

1. **忠實性**：產生的目標程式必須與原始碼語意一致
2. **效率**：目標程式的執行效率應盡可能高
3. **可讀性**：編譯過程中的錯誤訊息應清晰準確

**翻譯 vs 解釋**

```
編譯：原始碼 ──→ 目的碼 ──→ 執行
        [編譯器]     [CPU]

解釋：原始碼 ──→ 直譯執行
        [解譯器]
```

### 4.1.2 編譯器的組織結構

現代編譯器通常採用前端-後端分離的架構：

```
┌─────────────────────────────────────────────────────────────────┐
│                          原始碼                                   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        編譯器前端                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  詞法分析   │→ │  語法分析   │→ │  語意分析   │            │
│  │   (Lexer)   │  │  (Parser)   │  │  (Analyze)  │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                │                │                      │
│         ▼                ▼                ▼                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    中間表示 (IR)                          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        編譯器後端                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   最佳化    │→ │  目的碼     │→ │   連結      │            │
│  │ (Optimize)  │  │  (Codegen) │  │  (Link)    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        目的碼 / 執行檔                            │
└─────────────────────────────────────────────────────────────────┘
```

**前端的職責**

- 語言相關：只與特定語言相關
- 產生 IR：將原始碼轉換為與語言無關的中間表示

**後端的職責**

- 硬體相關：只與特定目標架構相關
- 處理 IR：最佳化並產生目標碼

### 4.1.3 編譯器前端的理論

**詞法分析器（Scanner）**

詞法分析器負責將字元流轉換為 Token 序列：

```
"int x = 42;"
          │
          ▼ [詞法分析]
          │
[(INT, "int"), (IDENT, "x"), (ASSIGN, "="), (NUM, 42), (SEMI, ";")]
```

**語法分析器（Parser）**

語法分析器將 Token 序列組織為語法樹：

```
                        宣告
                       /    \
                   類型      賦值
                   "int"   /    \
                         識別字  常數
                          "x"   42
```

**語意分析器**

語意分析負責：
- 類型檢查
- 作用域解析
- 常數折疊
- 雜湊檢查

### 4.1.4 符號表管理

符號表是編譯器維護的核心資料結構，用於儲存識別字的資訊。

**符號表的內容**

| 屬性 | 說明 |
|------|------|
| 名稱 | 識別字的名字 |
| 類型 | int, float, array, function 等 |
| 作用域 | 定義所在的作用域 |
| 記憶體位置 | 堆疊偏移或全域位址 |
| 參數列表 | 函數參數（針對函數） |
| 其他屬性 | const、static 等修飾符 |

**作用域與符號表**

[_code/04/04_01_symbol_table.c](_code/04/04_01_symbol_table.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SCOPES 100
#define MAX_SYMBOLS 1000

typedef struct {
    char name[64];
    char type[32];
    char kind[32];
    int address;
} Symbol;

typedef struct {
    Symbol symbols[MAX_SYMBOLS];
    int count;
} Scope;

typedef struct {
    Scope scopes[MAX_SCOPES];
    int scope_count;
} SymbolTable;

void enter_scope(SymbolTable *st) {
    if (st->scope_count < MAX_SCOPES) {
        st->scopes[st->scope_count].count = 0;
        st->scope_count++;
    }
}

void exit_scope(SymbolTable *st) {
    if (st->scope_count > 0) {
        st->scope_count--;
    }
}

void define_symbol(SymbolTable *st, const char *name, const char *type, const char *kind, int address) {
    if (st->scope_count == 0) return;
    Scope *current = &st->scopes[st->scope_count - 1];
    if (current->count < MAX_SYMBOLS) {
        Symbol *sym = &current->symbols[current->count++];
        strncpy(sym->name, name, 63);
        strncpy(sym->type, type, 31);
        strncpy(sym->kind, kind, 31);
        sym->address = address;
    }
}

Symbol* lookup_symbol(SymbolTable *st, const char *name) {
    for (int i = st->scope_count - 1; i >= 0; i--) {
        Scope *scope = &st->scopes[i];
        for (int j = 0; j < scope->count; j++) {
            if (strcmp(scope->symbols[j].name, name) == 0) {
                return &scope->symbols[j];
            }
        }
    }
    return NULL;
}

int main() {
    SymbolTable st;
    st.scope_count = 0;
    enter_scope(&st);
    
    define_symbol(&st, "x", "int", "variable", 0);
    define_symbol(&st, "main", "function", "function", 0);
    
    enter_scope(&st);
    define_symbol(&st, "x", "int", "parameter", 8);
    define_symbol(&st, "y", "double", "variable", 16);
    
    Symbol *sym = lookup_symbol(&st, "x");
    if (sym) printf("lookup('x'): type=%s, kind=%s, address=%d\n", sym->type, sym->kind, sym->address);
    
    sym = lookup_symbol(&st, "y");
    if (sym) printf("lookup('y'): type=%s, kind=%s, address=%d\n", sym->type, sym->kind, sym->address);
    
    sym = lookup_symbol(&st, "main");
    if (sym) printf("lookup('main'): type=%s, kind=%s, address=%d\n", sym->type, sym->kind, sym->address);
    
    exit_scope(&st);
    sym = lookup_symbol(&st, "x");
    if (sym) printf("After exit_scope, lookup('x'): type=%s, kind=%s, address=%d\n", sym->type, sym->kind, sym->address);
    
    return 0;
}
```

### 4.1.5 完整編譯器實作

讓我們實作一個簡化的編譯器，展示完整流程：

[_code/04/04_02_compiler.c](_code/04/04_02_compiler.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKENS 1000
#define MAX_IR 100

typedef enum {TOKEN_NUMBER, TOKEN_IDENT, TOKEN_KEYWORD, TOKEN_LPAREN, TOKEN_RPAREN, 
              TOKEN_LBRACE, TOKEN_RBRACE, TOKEN_SEMI, TOKEN_PLUS, TOKEN_MINUS, 
              TOKEN_MULT, TOKEN_ASSIGN, TOKEN_LT, TOKEN_GT, TOKEN_EOF} TokenType;

typedef struct {
    TokenType type;
    char value[64];
} Token;

typedef struct ASTNode {
    char type[32];
    char op[8];
    int value;
    char name[64];
    struct ASTNode *left;
    struct ASTNode *right;
} ASTNode;

typedef struct {
    Token tokens[MAX_TOKENS];
    int count;
    int pos;
    char ir[MAX_IR][128];
    int ir_count;
} Compiler;

void lex(Compiler *c, const char *source) {
    c->count = 0;
    int i = 0;
    while (source[i] != '\0') {
        if (isspace(source[i])) { i++; continue; }
        if (isdigit(source[i])) {
            int j = i;
            while (isdigit(source[j])) j++;
            c->tokens[c->count].type = TOKEN_NUMBER;
            int len = j - i;
            if (len > 63) len = 63;
            strncpy(c->tokens[c->count].value, source + i, len);
            c->tokens[c->count].value[len] = '\0';
            i = j;
            c->count++;
            continue;
        }
        if (isalpha(source[i]) || source[i] == '_') {
            int j = i;
            while (isalnum(source[j]) || source[j] == '_') j++;
            char word[64];
            int len = j - i;
            if (len > 63) len = 63;
            strncpy(word, source + i, len);
            word[len] = '\0';
            if (strcmp(word, "int") == 0 || strcmp(word, "return") == 0 || 
                strcmp(word, "print") == 0) {
                c->tokens[c->count].type = TOKEN_KEYWORD;
            } else {
                c->tokens[c->count].type = TOKEN_IDENT;
            }
            strcpy(c->tokens[c->count].value, word);
            i = j;
            c->count++;
            continue;
        }
        switch (source[i]) {
            case '+': c->tokens[c->count].type = TOKEN_PLUS; strcpy(c->tokens[c->count].value, "+"); break;
            case '-': c->tokens[c->count].type = TOKEN_MINUS; strcpy(c->tokens[c->count].value, "-"); break;
            case '*': c->tokens[c->count].type = TOKEN_MULT; strcpy(c->tokens[c->count].value, "*"); break;
            default: i++; continue;
        }
        i++;
        c->count++;
    }
    c->tokens[c->count].type = TOKEN_EOF;
    c->count++;
}

Token *peek(Compiler *c) {
    if (c->pos < c->count) return &c->tokens[c->pos];
    return NULL;
}

void consume(Compiler *c) {
    if (c->pos < c->count) c->pos++;
}

ASTNode *primary(Compiler *c) {
    Token *t = peek(c);
    ASTNode *node = malloc(sizeof(ASTNode));
    if (!node) return NULL;
    memset(node, 0, sizeof(ASTNode));
    
    if (t->type == TOKEN_NUMBER) {
        strcpy(node->type, "number");
        node->value = atoi(t->value);
        consume(c);
    } else if (t->type == TOKEN_IDENT) {
        strcpy(node->type, "identifier");
        strcpy(node->name, t->value);
        consume(c);
    }
    return node;
}

ASTNode *multiplicative(Compiler *c) {
    ASTNode *result = primary(c);
    while (peek(c) && peek(c)->type == TOKEN_MULT) {
        consume(c);
        ASTNode *right = primary(c);
        ASTNode *op = malloc(sizeof(ASTNode));
        memset(op, 0, sizeof(ASTNode));
        strcpy(op->type, "binary");
        strcpy(op->op, "*");
        op->left = result;
        op->right = right;
        result = op;
    }
    return result;
}

ASTNode *additive(Compiler *c) {
    ASTNode *result = multiplicative(c);
    while (peek(c) && (peek(c)->type == TOKEN_PLUS || peek(c)->type == TOKEN_MINUS)) {
        Token *op_tok = consume(c);
        ASTNode *right = multiplicative(c);
        ASTNode *op = malloc(sizeof(ASTNode));
        memset(op, 0, sizeof(ASTNode));
        strcpy(op->type, "binary");
        strcpy(op->op, op_tok->value);
        op->left = result;
        op->right = right;
        result = op;
    }
    return result;
}

void generate_ir_expr(Compiler *c, ASTNode *node, char *out) {
    if (!node) return;
    if (strcmp(node->type, "number") == 0) {
        sprintf(out, "%d", node->value);
    } else if (strcmp(node->type, "identifier") == 0) {
        strcpy(out, node->name);
    } else if (strcmp(node->type, "binary") == 0) {
        char left[64], right[64];
        generate_ir_expr(c, node->left, left);
        generate_ir_expr(c, node->right, right);
        sprintf(out, "(%s %s %s)", left, node->op, right);
    }
}

void generate_asm(Compiler *c) {
    printf("\n=== x86 Assembly ===\n");
    printf("    .global main\n");
    printf("main:\n");
    for (int i = 0; i < c->ir_count; i++) {
        char *line = c->ir[i];
        if (strstr(line, "return")) {
            int val = 0;
            char *p = strchr(line, ' ');
            if (p) {
                while (*p == ' ') p++;
                if (isdigit(*p)) val = atoi(p);
            }
            printf("    movl $%d, %%eax\n", val);
            printf("    ret\n");
        } else if (strstr(line, "print")) {
            char *p = strchr(line, ' ');
            while (p && *p == ' ') p++;
            if (isdigit(*p)) {
                printf("    movl $%d, %%edi\n", atoi(p));
            }
            printf("    call print_int\n");
        }
    }
}

int main() {
    Compiler c;
    memset(&c, 0, sizeof(Compiler));
    
    const char *source = "10 + 20";
    printf("=== Source Code ===\n%s\n", source);
    
    lex(&c, source);
    printf("\n=== Tokens ===\n");
    for (int i = 0; i < c.count; i++) {
        printf("(%d, \"%s\") ", c.tokens[i].type, c.tokens[i].value);
    }
    printf("\n");
    
    c.pos = 0;
    ASTNode *ast = additive(&c);
    
    printf("\n=== AST ===\n");
    printf("expr: ");
    char buf[128];
    generate_ir_expr(&c, ast, buf);
    printf("%s\n", buf);
    
    c.ir_count = 0;
    sprintf(c.ir[c.ir_count++], "  return %s", buf);
    sprintf(c.ir[c.ir_count++], "  print %s", buf);
    
    printf("\n=== IR ===\n");
    for (int i = 0; i < c.ir_count; i++) {
        printf("%s\n", c.ir[i]);
    }
    
    generate_asm(&c);
    
    return 0;
}
```

## 4.2 語意分析與符號表

### 4.2.1 語意分析的職責

語意分析位於語法分析之後，負責檢查程式在語法正確之外是否具有語意有效性。

**語意分析的任務**

| 任務 | 說明 | 範例 |
|------|------|------|
| 類型檢查 | 確保運算類型相容 | `int x = "hello";` |
| 作用域解析 | 識別字使用前已宣告 | `y = 5;`（y 未宣告）|
| 唯一性檢查 | 同作用域無重複宣告 | `int x, x;` |
| 常數折疊 | 編譯期計算常數表達式 | `int x = 2 * 3;` → `int x = 6;` |
| 雜湊檢查 | 呼叫者與定義匹配 | `foo(a, b)` 但 `foo(x)` |

### 4.2.2 類型系統理論

**靜態 vs 動態類型**

| 特性 | 靜態類型 | 動態類型 |
|------|----------|----------|
| 類型檢查時機 | 編譯時 | 執行時 |
| 執行速度 | 較快 | 較慢 |
| 錯誤時機 | 早期 | 晚期 |
| 範例 | C, C++, Java | Python, JavaScript |

**強類型 vs 弱類型**

| 特性 | 強類型 | 弱類型 |
|------|--------|--------|
| 隱式轉換 | 禁止或嚴格限制 | 允許較多 |
| 類型安全 | 較高 | 較低 |
| 範例 | Java, Haskell | C, JavaScript |

### 4.2.3 符號表的實現

符號表需要支援：
- 插入（Insert）
- 查詢（Lookup）
- 作用域管理

[_code/04/04_01_symbol_table.c](_code/04/04_01_symbol_table.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SCOPES 100
#define MAX_SYMBOLS 1000

typedef struct {
    char name[64];
    char type[32];
    char kind[32];
    int address;
} Symbol;

typedef struct {
    Symbol symbols[MAX_SYMBOLS];
    int count;
} Scope;

typedef struct {
    Scope scopes[MAX_SCOPES];
    int scope_count;
} SymbolTable;

void enter_scope(SymbolTable *st) {
    if (st->scope_count < MAX_SCOPES) {
        st->scopes[st->scope_count].count = 0;
        st->scope_count++;
    }
}

void exit_scope(SymbolTable *st) {
    if (st->scope_count > 0) {
        st->scope_count--;
    }
}

void define_symbol(SymbolTable *st, const char *name, const char *type, const char *kind, int address) {
    if (st->scope_count == 0) return;
    Scope *current = &st->scopes[st->scope_count - 1];
    if (current->count < MAX_SYMBOLS) {
        Symbol *sym = &current->symbols[current->count++];
        strncpy(sym->name, name, 63);
        strncpy(sym->type, type, 31);
        strncpy(sym->kind, kind, 31);
        sym->address = address;
    }
}

Symbol* lookup_symbol(SymbolTable *st, const char *name) {
    for (int i = st->scope_count - 1; i >= 0; i--) {
        Scope *scope = &st->scopes[i];
        for (int j = 0; j < scope->count; j++) {
            if (strcmp(scope->symbols[j].name, name) == 0) {
                return &scope->symbols[j];
            }
        }
    }
    return NULL;
}

int main() {
    SymbolTable st;
    st.scope_count = 0;
    enter_scope(&st);

    define_symbol(&st, "x", "int", "variable", 0);
    define_symbol(&st, "main", "function", "function", 0);

    enter_scope(&st);
    define_symbol(&st, "x", "int", "parameter", 8);
    define_symbol(&st, "y", "double", "variable", 16);

    printf("lookup('x'): %p\n", (void*)lookup_symbol(&st, "x"));
    printf("lookup('y'): %p\n", (void*)lookup_symbol(&st, "y"));
    printf("lookup('main'): %p\n", (void*)lookup_symbol(&st, "main"));

    exit_scope(&st);
    printf("After exit_scope, lookup('x'): %p\n", (void*)lookup_symbol(&st, "x"));

    return 0;
}
```

## 4.3 中間碼生成

### 4.3.1 中間表示（IR）的類型

IR 是編譯器內部的程式表示，介於原始碼和目的碼之間。

**IR 的特性**

1. **與語言無關**：適用於多種原始語言
2. **與硬體無關**：適用於多種目標架構
3. **易於最佳化**：便於進行各種轉換

**常見的 IR 形式**

| 形式 | 說明 | 範例 |
|------|------|------|
| 三地址碼（TAC） | 每條指令最多三個運算元 | `t1 = a + b` |
| 靜態單一形式（SSA） | 每個變數只被賦值一次 | `t1 = a + b` |
| 控制流程圖（CFG） | 基本區塊 + 跳轉邊 | 圖結構 |

### 4.3.2 三地址碼（TAC）

三地址碼是最廣泛使用的 IR 形式。

**TAC 的特點**

- 每條指令最多包含：一個運算和三個運算元
- 形式：`x = y op z` 或 `x = op y`
- 臨時變數用於儲存中間結果

**TAC 範例**

原始碼：
```c
a = b + c * d;
```

TAC：
```
t1 = c * d
a = b + t1
```

### 4.3.3 控制流程圖（CFG）

CFG 將程式劃分為基本區塊，並記錄跳轉關係。

**基本區塊（Basic Block）**

基本區塊是滿足以下條件的最大連續指令序列：
1. 指令按序執行，無跳轉進入（除入口外）
2. 無跳轉離開（除末尾外）

**CFG 的構建**

```
入口 → B1 → B2 → B3 → 出口
            ↓
            B4 → B5
```

## 4.4 目的碼生成

### 4.4.1 目的碼生成的考量

目的碼生成將 IR 轉換為特定硬體的機器碼或組合語言。

**生成的考量因素**

| 因素 | 說明 |
|------|------|
| 指令選擇 | 選擇合適的目標指令 |
| 暫存器配置 | 有效利用有限暫存器 |
| 指令排程 | 最小化延遲 |
| 呼叫約定 | 遵守 ABI 規範 |

### 4.4.2 x86-64 呼叫約定

x86-64 System V ABI 的呼叫約定：

**參數傳遞順序**

```
%rdi, %rsi, %rdx, %rcx, %r8, %r9
```

**返回值**

```
整數/指標：%rax
浮點數：%xmm0
```

**被呼叫者保存**

```
%rbx, %rbp, %r12, %r13, %r14, %r15
```

### 4.4.3 目的碼範例

組合語言範例：
```asm
    .global _main
_main:
    # 參數傳遞
    movq $10, %rdi      # 第一個參數
    call _factorial
    
    # 列印結果
    movq %rax, %rsi
    leaq format(%rip), %rdi
    movq $0, %rax
    syscall
    
    ret

factorial:
    cmpq $1, %rdi
    jle .Lbase
    
    pushq %rbp
    movq %rsp, %rbp
    
    decq %rdi
    call factorial
    
    popq %rbp
    ret

.Lbase:
    movq $1, %rax
    ret

format:
    .asciz "%d\n"
```

## 4.5 連結器與載入器

### 4.5.1 連結器的角色

連結器（Linker）將多個目的檔合併為單一執行檔。

**連結的類型**

| 類型 | 說明 |
|------|------|
| 靜態連結 | 編譯時完成所有符號解析 |
| 動態連結 | 執行時動態載入共享庫 |

**連結的步驟**

1. **符號解析**：將符號引用與定義匹配
2. **重定位**：調整位址參照
3. **段合併**：合併相同類型的段

### 4.5.2 連結器實作概念

[_code/04/04_03_linker.c](_code/04/04_03_linker.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_OBJECTS 100
#define MAX_SYMBOLS 1000

typedef struct {
    char name[64];
    int address;
} Symbol;

typedef struct {
    char name[64];
    Symbol symbols[MAX_SYMBOLS];
    int sym_count;
    char references[MAX_SYMBOLS][64];
    int ref_count;
} ObjectFile;

typedef struct {
    ObjectFile objects[MAX_OBJECTS];
    int obj_count;
    Symbol symbols[MAX_SYMBOLS];
    int sym_count;
} Linker;

void add_object(Linker *l, const char *name, Symbol *syms, int sym_count) {
    if (l->obj_count >= MAX_OBJECTS) return;
    ObjectFile *obj = &l->objects[l->obj_count++];
    strncpy(obj->name, name, 63);
    obj->sym_count = sym_count;
    for (int i = 0; i < sym_count; i++) {
        obj->symbols[i] = syms[i];
        l->symbols[l->sym_count++] = syms[i];
    }
}

int resolve_references(Linker *l) {
    for (int i = 0; i < l->obj_count; i++) {
        ObjectFile *obj = &l->objects[i];
        for (int j = 0; j < obj->ref_count; j++) {
            int found = 0;
            for (int k = 0; k < l->sym_count; k++) {
                if (strcmp(obj->references[j], l->symbols[k].name) == 0) {
                    found = 1;
                    break;
                }
            }
            if (!found) {
                printf("Error: Undefined symbol: %s\n", obj->references[j]);
                return -1;
            }
        }
    }
    return 0;
}

void *link(Linker *l) {
    if (resolve_references(l) != 0) return NULL;
    void *exec = malloc(1024);
    printf("Executable linked successfully\n");
    return exec;
}

int main() {
    Linker l;
    memset(&l, 0, sizeof(Linker));
    
    Symbol obj1_syms[] = {{"main", 0x1000}, {"foo", 0x2000}};
    add_object(&l, "a.o", obj1_syms, 2);
    
    void *exec = link(&l);
    if (exec) {
        printf("Link complete. Executable at %p\n", exec);
        free(exec);
    }
    
    return 0;
}
```

### 4.5.3 載入器

[_code/04/04_04_loader.c](_code/04/04_04_loader.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    void *exec_data;
    size_t exec_size;
    void *entry_point;
    void *text_section;
    void *data_section;
    void *bss_section;
} Program;

typedef struct {
    Program *program;
    void *memory;
    size_t mem_size;
} Loader;

int load(Loader *l, Program *p) {
    printf("=== Loader Steps ===\n");
    
    printf("1. Reading executable header\n");
    printf("   Entry point: %p\n", p->entry_point);
    
    printf("2. Mapping sections to memory\n");
    printf("   .text: %p\n", p->text_section);
    printf("   .data: %p\n", p->data_section);
    printf("   .bss: %p\n", p->bss_section);
    
    printf("3. Setting program counter\n");
    printf("   PC set to: %p\n", p->entry_point);
    
    printf("4. Jumping to entry point\n");
    
    l->program = p;
    l->memory = malloc(1024 * 1024);
    l->mem_size = 1024 * 1024;
    
    printf("Program loaded successfully\n");
    return 0;
}

int main() {
    Loader l;
    memset(&l, 0, sizeof(Loader));
    
    Program prog = {
        .entry_point = (void *)0x401000,
        .text_section = (void *)0x401000,
        .data_section = (void *)0x404000,
        .bss_section = (void *)0x405000
    };
    
    load(&l, &prog);
    
    free(l.memory);
    return 0;
}
```
