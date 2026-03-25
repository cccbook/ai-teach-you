# 3. 解譯器

## 3.1 解譯器架構

### 3.1.1 解譯器的基本概念

解譯器（Interpreter）是一種直接執行高階語言程式的系統軟體。與編譯器不同，解譯器不需要預先將程式翻譯為機器碼，而是逐句讀取原始碼並立即執行。

**解譯器 vs 編譯器**

| 特性 | 解譯器 | 編譯器 |
|------|--------|--------|
| 執行方式 | 逐句直接執行 | 先翻譯後執行 |
| 輸出 | 執行結果 | 目的碼檔案 |
| 執行速度 | 較慢（重複翻譯） | 較快 |
| 跨平台性 | 較好 | 需重新編譯 |
| 互動性 | 較好 | 較差 |
| 錯誤報告 | 即時 | 需重新編譯 |

**解譯器的優勢**

1. **快速開發迭代**：不需要編譯-執行迴圈
2. **良好的錯誤報告**：可直接指出錯誤位置
3. **動態特性**：eval()、反射、動態型別
4. **平台無關性**：同一解譯器可在多平台執行

### 3.1.2 解譯器架構模型

現代解譯器的典型架構可分為幾個層次：

```
┌─────────────────────────────────────────────────────────────┐
│                    使用者程式                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    解譯器引擎                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   詞法分析  │→ │  語法分析   │→ │  AST 執行   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    執行環境                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ 符號表  │  │ 堆疊   │  │ 記憶體  │  │ 內建函數│     │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    作業系統 / 硬體                          │
└─────────────────────────────────────────────────────────────┘
```

### 3.1.3 直譯 vs 位元組碼直譯

**純直譯（Pure Interpretation）**

直接執行 AST 或原始的 Token 流：

```
原始碼 → 詞法分析 → 語法分析 → AST → 直譯執行
```

**位元組碼直譯（Bytecode Interpretation）**

先編譯為中間表示（位元組碼），再用 VM 解譯執行：

```
原始碼 → 詞法分析 → 語法分析 → AST → 位元組碼 → VM 直譯執行
```

**兩種方式的比較**

| 特性 | 純直譯 | 位元組碼直譯 |
|------|--------|--------------|
| 執行速度 | 最慢 | 較快 |
| 記憶體效率 | 需保留 AST | 位元組碼更緊湊 |
| 跨平台性 | 最佳 | 需 VM 實作 |
| 實作複雜度 | 簡單 | 中等 |
| JIT 相容性 | 困難 | 容易 |

### 3.1.4 環境與符號表

解譯器需要維護執行環境來追蹤變數、函數和作用域。

**符號表（Symbol Table）**

符號表是儲存所有識別字資訊的資料結構：

| 欄位 | 說明 |
|------|------|
| 名稱 | 識別字的名字 |
| 類型 | 變數型別、函數返回型別 |
| 作用域 | 定義所在的作用域 |
| 位置 | 記憶體位址或堆疊偏移 |
| 屬性 | 常數、參數、區域變數等 |

**作用域管理**

作用域（Scope）決定了識別字的可見性：

[_code/03/03_05_scope_management.c](_code/03/03_05_scope_management.c)

```c
#include <stdio.h>
#include <string.h>

typedef enum { GLOBAL, LOCAL, INNER } ScopeType;

typedef struct {
    char name[32];
    int value;
    ScopeType type;
} Variable;

void demonstrate_scope() {
    printf("=== Scope Management ===\n\n");
    
    printf("x = 10  (global scope)\n\n");
    printf("void outer() {\n");
    printf("    y = 20  (outer's scope)\n\n");
    printf("    void inner() {\n");
    printf("        z = 30  (inner's scope)\n");
    printf("        print(x, y, z)  // Visible: x, y, z\n");
    printf("    }\n");
    printf("}\n\n");
    
    printf("Variable lookup order (lexical scope):\n");
    printf("  1. Current scope\n");
    printf("  2. Parent scope\n");
    printf("  3. ... (continues until global scope)\n\n");
    
    printf("Scope Implementation Strategies:\n");
    printf("  1. Lexical Scope: Determined by source structure\n");
    printf("  2. Dynamic Scope: Determined by call stack\n");
    
    printf("\nC Scope Example:\n");
    int x = 10;
    printf("  Global x = %d\n", x);
    {
        int y = 20;
        printf("  Outer scope y = %d\n", y);
        {
            int z = 30;
            printf("  Inner scope z = %d\n", z);
        }
    }
}

int main() {
    demonstrate_scope();
    return 0;
}
```

**作用域實現策略**

1. **詞法作用域（Lexical Scope）**：根據原始碼結構靜態決定
2. **動態作用域（Dynamic Scope）**：根據呼叫堆疊動態決定

### 3.1.5 解譯器實作

讓我們實作一個完整的解譯器：

[_code/03/03-1-interpreter.c](_code/03/03-1-interpreter.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKENS 100
#define MAX_VARS 100

typedef enum { 
    TOKEN_NUM, TOKEN_IDENT, TOKEN_PLUS, TOKEN_MINUS, 
    TOKEN_MULT, TOKEN_DIV, TOKEN_ASSIGN, TOKEN_LPAREN, 
    TOKEN_RPAREN, TOKEN_SEMI, TOKEN_PRINT, TOKEN_LET, TOKEN_EOF 
} TokenType;

typedef struct { TokenType type; int value; char name[32]; } Token;
typedef struct ASTNode { 
    char type; int value; char name[32];
    struct ASTNode *left, *right; 
} ASTNode;

Token tokens[MAX_TOKENS];
int token_pos = 0;
int var_count = 0;
int variables[MAX_VARS];

// ========== 詞法分析 ==========
void tokenize(const char* input) {
    int i = 0, t = 0;
    while (input[i]) {
        if (isspace(input[i])) { i++; continue; }
        if (isdigit(input[i])) {
            int v = 0;
            while (isdigit(input[i])) v = v * 10 + (input[i++] - '0');
            tokens[t++] = (Token){TOKEN_NUM, v, ""};
        } else if (isalpha(input[i]) || input[i] == '_') {
            char name[32] = {0}; int j = 0;
            while (isalnum(input[i]) || input[i] == '_') name[j++] = input[i++];
            if (strcmp(name, "print") == 0) tokens[t++] = (Token){TOKEN_PRINT, 0, ""};
            else if (strcmp(name, "let") == 0) tokens[t++] = (Token){TOKEN_LET, 0, ""};
            else { tokens[t++] = (Token){TOKEN_IDENT, 0, ""}; strcpy(tokens[t-1].name, name); }
        } else {
            switch(input[i++]) {
                case '+': tokens[t++] = (Token){TOKEN_PLUS, 0, ""}; break;
                case '-': tokens[t++] = (Token){TOKEN_MINUS, 0, ""}; break;
                case '*': tokens[t++] = (Token){TOKEN_MULT, 0, ""}; break;
                case '/': tokens[t++] = (Token){TOKEN_DIV, 0, ""}; break;
                case '=': tokens[t++] = (Token){TOKEN_ASSIGN, 0, ""}; break;
                case '(': tokens[t++] = (Token){TOKEN_LPAREN, 0, ""}; break;
                case ')': tokens[t++] = (Token){TOKEN_RPAREN, 0, ""}; break;
                case ';': tokens[t++] = (Token){TOKEN_SEMI, 0, ""}; break;
            }
        }
    }
    tokens[t] = (Token){TOKEN_EOF, 0, ""};
}

// ========== 語法分析 ==========
ASTNode* parse_expr();

ASTNode* make_num(int v) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = 'N'; n->value = v; n->left = n->right = NULL;
    return n;
}

ASTNode* parse_factor() {
    Token t = tokens[token_pos++];
    if (t.type == TOKEN_NUM) return make_num(t.value);
    if (t.type == TOKEN_LPAREN) {
        ASTNode* e = parse_expr();
        token_pos++; return e;
    }
    return NULL;
}

ASTNode* parse_term() {
    ASTNode* n = parse_factor();
    while (tokens[token_pos].type == TOKEN_MULT || tokens[token_pos].type == TOKEN_DIV) {
        char op = tokens[token_pos++].type == TOKEN_MULT ? '*' : '/';
        n = make_binop(op, n, parse_factor());
    }
    return n;
}

ASTNode* parse_expr() {
    ASTNode* n = parse_term();
    while (tokens[token_pos].type == TOKEN_PLUS || tokens[token_pos].type == TOKEN_MINUS) {
        char op = tokens[token_pos++].type == TOKEN_PLUS ? '+' : '-';
        n = make_binop(op, n, parse_term());
    }
    return n;
}

// ========== 執行 ==========
int eval_expr(ASTNode* n) {
    if (n->type == 'N') return n->value;
    int l = eval_expr(n->left), r = eval_expr(n->right);
    switch(n->type) { case '+': return l + r; case '-': return l - r; case '*': return l * r; case '/': return l / r; }
    return 0;
}

int main() {
    // 測試執行
    // run("let x = 10;"); run("let y = 20;"); run("print(x + y);");
    return 0;
}
```

## 3.2 Bytecode 與 VM

### 3.2.1 虛擬機的理論基礎

虛擬機（Virtual Machine, VM）是軟體模擬的計算機，提供指令集和執行環境。

**虛擬機的分類**

| 類型 | 特點 | 代表 |
|------|------|------|
| 系統虛擬機 | 模擬完整硬體，可執行 OS | VMware, VirtualBox, QEMU |
| 程式虛擬機 | 執行單一應用程式 | JVM, .NET CLR, Python VM |

本書主要討論**程式虛擬機**。

**虛擬機的優勢**

1. **跨平台性**：同一 VM 可在多種硬體上執行
2. **安全性**：隔離執行環境，防止惡意程式
3. **可攜性**：一次編譯，到處執行
4. **可驗證性**：位元組碼可在執行前驗證

### 3.2.2 基於堆疊的虛擬機（Stack-based VM）

堆疊式 VM 使用運算元堆疊（Operand Stack）進行運算，是最常見的 VM 設計。

**堆疊式 VM 的特性**

| 特性 | 說明 |
|------|------|
| 隱含運算元位置 | 運算元從堆疊彈出，結果推回堆疊 |
| 指令緊湊 | 指令無需指定暫存器或記憶體位置 |
| 簡單實作 | 堆疊操作易於理解和最佳化 |
| 執行速度 | 需頻繁記憶體訪問（堆疊存取） |

**JVM 是典型的堆疊式 VM**

[_code/03/03-2-stack-vm.c](_code/03/03-2-stack-vm.c)

```c
#include <stdio.h>

#define MAX_STACK 100
#define MAX_VARS 100

typedef enum { 
    OP_LOAD_CONST, OP_LOAD_VAR, OP_STORE_VAR, 
    OP_ADD, OP_SUB, OP_MUL, OP_DIV, 
    OP_PRINT, OP_HALT 
} OpCode;

int stack[MAX_STACK];
int sp = 0;
int variables[MAX_VARS];

void push(int v) { stack[sp++] = v; }
int pop() { return stack[--sp]; }

void run_vm(OpCode bytecode[], int data[], int pc) {
    while (1) {
        switch(bytecode[pc]) {
            case OP_LOAD_CONST: push(data[pc+1]); pc += 2; break;
            case OP_ADD: { int b=pop(), a=pop(); push(a+b); pc++; break; }
            case OP_PRINT: printf("%d\n", pop()); pc++; break;
            case OP_HALT: return;
        }
    }
}

int main() {
    OpCode code[] = {OP_LOAD_CONST, OP_ADD, OP_PRINT, OP_HALT};
    int data[] = {0, 10, 0, 20, 0};
    run_vm(code, data, 0);
    return 0;
}
```

### 3.2.3 基於暫存器的虛擬機（Register-based VM）

暫存器式 VM 使用虛擬暫存器集合儲存運算元。

**暫存器式 VM 的特性**

| 特性 | 說明 |
|------|------|
| 明確運算元位置 | 指令指定來源和目的暫存器 |
| 較少指令 | 減少指令數量 |
| 較快執行 | 減少堆疊存取次數 |
| 實作複雜 | 需管理暫存器分配 |

**Lua VM 是著名的暫存器式 VM**

Lua 5.0 從堆疊式改為暫存器式，效能提升顯著。

[_code/03/03_06_register_vs_stack.c](_code/03/03_06_register_vs_stack.c)

```c
#include <stdio.h>

void print_stack_based_vm() {
    printf("=== Stack-based VM ===\n\n");
    
    printf("Computing 1 + 2:\n");
    printf("Stack Operations:\n");
    printf("  iconst 1    // Push 1 onto stack -> Stack: [1]\n");
    printf("  iconst 2    // Push 2 onto stack -> Stack: [1, 2]\n");
    printf("  iadd        // Pop 2, Pop 1, Push 3 -> Stack: [3]\n");
    printf("  print       // Print 3\n\n");
    
    printf("Stack bytecode:\n  [iconst 1, iconst 2, iadd, print, halt]\n\n");
}

void print_register_based_vm() {
    printf("=== Register-based VM ===\n\n");
    
    printf("Computing 1 + 2:\n");
    printf("Register Operations:\n");
    printf("  LOADK R0, 1    // R0 = 1\n");
    printf("  LOADK R1, 2    // R1 = 2\n");
    printf("  ADD R2, R0, R1 // R2 = R0 + R1\n");
    printf("  PRINT R2       // Print R2\n\n");
    
    printf("Register bytecode:\n  [LOADK 0 1, LOADK 1 2, ADD 2 0 1, PRINT 2, HALT]\n\n");
}

int main() {
    printf("=== Stack vs Register-based VM ===\n\n");
    print_stack_based_vm();
    print_register_based_vm();
    return 0;
}
```

### 3.2.4 位元組碼設計原則

設計位元組碼指令集時需考慮：

**指令格式**

| 格式 | 位元組數 | 說明 |
|------|----------|------|
| 零位址 | 1 | 所有運算元隱含（如堆疊 VM） |
| 一位址 | 2 | 一個運算元 |
| 二位址 | 3 | 兩個運算元 |
| 三位址 | 4+ | 三個運算元 |

**指令分類**

| 類別 | 指令範例 |
|------|----------|
| 載入/儲存 | LOAD, STORE, PUSH, POP |
| 算術運算 | ADD, SUB, MUL, DIV |
| 邏輯運算 | AND, OR, NOT, XOR |
| 比較跳轉 | CMP, JMP, JE, JNE |
| 函數呼叫 | CALL, RET, ENTER, LEAVE |
| 物件操作 | NEW, GETFIELD, PUTFIELD |

## 3.3 垃圾回收（Garbage Collection）

### 3.3.1 記憶體管理的基本概念

手動記憶體管理容易出錯，現代程式語言傾向使用自動記憶體管理。

**手動管理的問題**

1. **遺漏釋放**：忘記釋放記憶體 → 記憶體洩漏
2. **重複釋放**：釋放已釋放的記憶體 → 懸垂指標
3. **使用未釋放記憶體**：使用已釋放的記憶體 → 未定義行為

**自動記憶體管理的目標**

1. **自動化**：程式設計師無需關心記憶體釋放
2. **安全性**：杜絕懸垂指標和記憶體洩漏
3. **效率**：最小化 GC 帶來的性能影響

### 3.3.2 引用計數（Reference Counting）

引用計數是最直接的 GC 方法。

**基本原理**

每個物件維護一個引用計數器：
- 建立物件時，計數 = 1
- 有新參照時，計數 +1
- 參照失效時，計數 -1
- 計數 = 0 時，回收記憶體

[_code/03/03-3-gc.c](_code/03/03-3-gc.c)

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Object {
    int ref_count;
    int marked;
    int value;
} Object;

Object* allocate() {
    Object* obj = (Object*)malloc(sizeof(Object));
    obj->ref_count = 1;
    obj->marked = 0;
    return obj;
}

void reference(Object* obj) {
    if (obj) obj->ref_count++;
}

void dereference(Object** obj_ptr) {
    Object* obj = *obj_ptr;
    if (!obj) return;
    obj->ref_count--;
    if (obj->ref_count == 0) {
        printf("回收記憶體\n");
        free(obj);
    }
    *obj_ptr = NULL;
}

// 標記-清除 GC
void mark(Object* obj) {
    if (!obj || obj->marked) return;
    obj->marked = 1;
}

void sweep(Object** heap, int count) {
    int freed = 0;
    for (int i = 0; i < count; i++) {
        if (heap[i] && !heap[i]->marked) {
            printf("GC 回收物件\n");
            free(heap[i]);
            heap[i] = NULL;
            freed++;
        }
    }
    printf("GC 完成，回收 %d 個物件\n", freed);
}
```

**引用計數的優缺點**

| 優點 | 缺點 |
|------|------|
| 簡單直觀 | 無法處理循環引用 |
| 記憶體即時釋放 | 計數更新開銷大 |
| 增量式、無停顿 | 無法處理分散式場景 |

Python 使用引用計數作為主要記憶體管理，但需配合標記-清除處理循環引用。

### 3.3.3 標記-清除（Mark and Sweep）

標記-清除是一種追蹤式（Tracing）GC 方法。

**演算法步驟**

```
Phase 1: 標記（Mark）
  - 從根集合開始，標記所有可達物件
  
Phase 2: 清除（Sweep）
  - 遍歷整個堆，回收未標記的物件
```

**根集合（Root Set）**

根集合包括：
- 全域變數
- 呼叫堆疊上的參照
- 暫存器內容

[_code/03/03_07_mark_sweep_gc.c](_code/03/03_07_mark_sweep_gc.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_HEAP 100

typedef struct {
    int id;
    int size;
    int marked;
    void* data;
} Object;

Object* heap[MAX_HEAP];
int heap_count = 0;

Object* allocate(int size) {
    Object* obj = (Object*)malloc(sizeof(Object));
    obj->id = heap_count++;
    obj->marked = 0;
    obj->data = malloc(size);
    printf("  Allocated object %d\n", obj->id);
    return obj;
}

void mark(Object* obj) {
    if (!obj || obj->marked) return;
    obj->marked = 1;
    printf("  Marked object %d\n", obj->id);
}

void sweep() {
    int freed = 0;
    for (int i = 0; i < heap_count; i++) {
        if (!heap[i]->marked) {
            printf("  Freeing object %d\n", heap[i]->id);
            free(heap[i]->data);
            free(heap[i]);
            freed++;
        }
    }
    printf("  Freed %d objects\n", freed);
}

int main() {
    printf("=== Mark-Sweep GC ===\n\n");
    
    Object* obj1 = allocate(100);
    Object* obj2 = allocate(200);
    Object* obj3 = allocate(300);
    
    printf("\nMark phase (from roots):\n");
    mark(obj1);
    mark(obj3);
    
    printf("\nSweep phase:\n");
    sweep();
    
    printf("\nAlgorithm:\n");
    printf("  1. Mark: Mark all reachable objects from roots\n");
    printf("  2. Sweep: Free all unmarked objects\n");
    
    return 0;
}
```

**標記-清除的問題**

| 問題 | 說明 |
|------|------|
| 記憶體碎片化 | 回收後產生不連續空間 |
| STW 暫停 | GC 期間需停止程式執行 |
| 標記耗時 | 需遍歷所有可達物件 |

### 3.3.4 複製（Copying）GC

複製式 GC 將堆記憶體分為兩半，只使用一半。

**原理**

```
┌─────────────────┬─────────────────┐
│    From Space   │    To Space     │
│   (使用中)      │   (空閒)        │
└─────────────────┴─────────────────┘

GC 時：
1. 將 From Space 的存活物件複製到 To Space
2. 交換 From/To Space
```

[_code/03/03_08_copy_gc.c](_code/03/03_08_copy_gc.c)

```c
#include <stdio.h>
#include <stdlib.h>

#define SPACE_SIZE 50

typedef struct {
    int id;
    int alive;
    int forwarded_to;
} Object;

typedef struct {
    Object* objects[SPACE_SIZE];
    int count;
} Space;

Space from_space = {.count = 0};
Space to_space = {.count = 0};
Space* current;

Object* allocate(int size) {
    Object* obj = (Object*)malloc(sizeof(Object));
    obj->id = current->count++;
    obj->alive = 1;
    obj->forwarded_to = -1;
    current->objects[obj->id] = obj;
    printf("  Allocated object %d\n", obj->id);
    return obj;
}

Object* forward(Object* obj) {
    if (!obj || obj->forwarded_to >= 0) {
        return obj;
    }
    Object* new_obj = allocate(0);
    obj->forwarded_to = new_obj->id;
    printf("  Forwarded object %d -> %d\n", obj->id, new_obj->id);
    return new_obj;
}

void collect(Object* roots[], int n) {
    printf("\n=== Copy GC Collection ===\n");
    printf("Swapping spaces...\n\n");
    
    Space* temp = current;
    current = &to_space;
    to_space = *temp;
    current->count = 0;
    
    printf("Copying live objects:\n");
    for (int i = 0; i < n; i++) {
        roots[i] = forward(roots[i]);
    }
    printf("\n  Surviving: %d objects\n", current->count);
}

int main() {
    printf("=== Copy Garbage Collection ===\n\n");
    
    current = &from_space;
    Object* obj1 = allocate(100);
    Object* obj2 = allocate(200);
    Object* obj3 = allocate(300);
    
    Object* roots[] = {obj1, obj3};
    collect(roots, 2);
    
    printf("\nProperties:\n");
    printf("  + No memory fragmentation\n");
    printf("  + Mark + copy in one pass\n");
    printf("  - Uses only half of memory\n");
    
    return 0;
}
```

**複製 GC 的優缺點**

| 優點 | 缺點 |
|------|------|
| 無記憶體碎片 | 只使用一半堆空間 |
| 標記+複製一次完成 | 存活率高時效率低 |
| 無需清除階段 | 需複製所有存活物件 |

### 3.3.5 標記-壓縮（Mark-Compact）

標記-壓縮結合標記-清除和複製的優點。

**三階段演算法**

```
Phase 1: 標記（Mark）
  - 同標記-清除，找出所有存活物件

Phase 2: 計算新位置（Compute Locations）
  - 計算物件壓縮後的新位置

Phase 3: 壓縮（Compact）
  - 將所有存活物件移動到連續區域
```

**優點**

- 消除記憶體碎片
- 完整使用堆空間

**缺點**

- 需要多次堆遍歷
- 壓縮階段耗時

### 3.3.6 分代回收（Generational GC）

分代假設：
- 大多數物件很快就會變成垃圾（早夭）
- 少數物件會存活很久

**分代架構**

```
┌─────────────────────────────────────────────┐
│                  堆記憶體                    │
├──────────────┬──────────────────────────────┤
│   年輕代      │        老年代               │
│  ┌────────┐  │                            │
│  │ Eden   │  │    ┌──────┐ ┌──────┐     │
│  │        │  │    │From  │ │ To   │     │
│  ├────────┤  │    │Survivor│ │Survivor│   │
│  │S0│S1 │  │    └──────┘ └──────┘     │
│  │  │   │  │                            │
│  └────────┘  │                            │
└──────────────┴──────────────────────────────┘
```

**Minor GC vs Major GC**

| GC 類型 | 觸發條件 | 頻率 | 暫停時間 |
|---------|----------|------|----------|
| Minor GC | Eden 滿 | 頻繁 | 短 |
| Major GC | 老年代滿 | 較少 | 長 |

JVM、.NET GC 都是分代回收的典型實作。

### 3.3.7 各語言的 GC 策略

| 語言 | GC 策略 |
|------|---------|
| Python | 引用計數 + 標記-清除（處理循環） |
| Java | 分代 + 標記-清除/複製 |
| C# | 分代 + 標記-壓縮 |
| Go | 並髮標記-清除 |
| JavaScript | 分代 + 增量GC |
| Ruby | 標記-清除 |

## 3.4 例子：Python、JavaScript、Lua、LISP

### 3.4.1 Python 位元組碼

Python 程式會被編譯為 `.pyc` 位元組碼，由 CPython VM 執行。

```python
import dis

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# 查看 Python 的位元組碼
dis.dis(factorial)
```

輸出：
```
  2           0 LOAD_FAST                0 (n)
               2 LOAD_CONST               1 (1)
               4 COMPARE_OP               0 (<=)
               6 POP_JUMP_IF_FALSE       12

  3           8 LOAD_CONST               1 (1)
              10 RETURN_VALUE

  4          12 LOAD_FAST                0 (n)
              14 LOAD_GLOBAL              0 (factorial)
              16 LOAD_FAST                0 (n)
              18 LOAD_CONST               1 (1)
              20 BINARY_SUBTRACT
              22 CALL_FUNCTION            1
              24 BINARY_MULTIPLY
              26 RETURN_VALUE
```

**Python VM 特性**

- 基於堆疊
- 大約 100 個位元組碼指令
- 使用 pyc 檔案快取編譯結果

### 3.4.2 Lua VM

Lua 使用基於暫存器的 VM，5.0 版本從堆疊式改為暫存器式。

```lua
-- Lua 範例
function fib(n)
    if n <= 1 then return n end
    return fib(n - 1) + fib(n - 2)
end

print(fib(10))  -- 輸出 55
```

**Lua 5.3+ 位元組碼結構**

- 40 個 opcode
- 基於暫存器（最多 255 個）
- 緊湊的位元組碼格式

### 3.4.3 JavaScript V8 引擎

V8 是 Chrome 和 Node.js 使用的 JavaScript 引擎，採用 JIT 編譯架構。

**V8 架構**

```
原始碼
   │
   ▼
┌─────────────────────────────────────────────┐
│              Ignition（直譯器）              │
│  - 產生位元組碼                             │
│  - 收集執行資訊                             │
│  - 熱點偵測                                │
└─────────────────────────────────────────────┘
   │
   ▼（熱點程式碼）
┌─────────────────────────────────────────────┐
│         TurboFan（最佳化編譯器）             │
│  - JIT 編譯熱點程式碼                      │
│  - 型別特化                                │
│  - 機器碼生成                              │
└─────────────────────────────────────────────┘
   │
   ▼（效能退化）
┌─────────────────────────────────────────────┐
│         Deoptimization（去最佳化）          │
│  - 假設失敗時回退到 Ignition              │
└─────────────────────────────────────────────┘
```

### 3.4.4 LISP 評価器

LISP 以其簡單而優雅的 eval/apply 循環著稱。

**LISP 評価器原理**

```
eval(expr, env)
  │
  ├─ 數值/字串 → 直接返回
  │
  ├─ 符號 → 在 env 中查找
  │
  └─ 表達式 → 分類處理
      │
      ├─ quote → 返回原始形式
      ├─ if → 條件評価
      ├─ define → 定義變數
      ├─ lambda → 創建函數
      └─ 函數呼叫 → apply(func, args)
                         │
                         ├─ 內建函數 → 直接執行
                         └─ 使用者函數 → 求值函數體
```

[_code/03/03-4-lisp.c](_code/03/03-4-lisp.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { TYPE_NUM, TYPE_SYM, TYPE_CONS, TYPE_FUNC } ValueType;

typedef struct Value {
    ValueType type;
    int num;
    char sym[32];
    struct Value *car, *cdr;
    struct Value *params, *body;
} Value;

Value* make_num(int n) { 
    Value* v = malloc(sizeof(Value));
    v->type = TYPE_NUM; v->num = n; 
    return v; 
}

Value* make_sym(const char* s) { 
    Value* v = malloc(sizeof(Value));
    v->type = TYPE_SYM; strcpy(v->sym, s); 
    return v; 
}

Value* make_cons(Value* car, Value* cdr) { 
    Value* v = malloc(sizeof(Value));
    v->type = TYPE_CONS; v->car = car; v->cdr = cdr; 
    return v; 
}

Value* eval_expr(Value* expr);

int main() {
    // (+ 2 3)  => (cons '+' (cons 2 (cons 3 nil)))
    Value* expr = make_cons(make_sym("+"), 
        make_cons(make_num(2), make_cons(make_num(3), NULL)));
    printf("Result: %d\n", eval_expr(expr)->num);
    return 0;
}
```

這個 LISP 直譯器展示了函數式語言的核心概念：程式即資料、遞迴、高階函數。
