# 教科書 Python 轉 C 程式碼擴展技能

## 概述

本技能描述如何將包含 Python 程式碼範例的教科書章節，轉換為可編譯、可測試的 C 程式碼檔案。

## 適用場景

- 將包含程式碼範例的 Markdown 教科書章節轉換為實際可運作的程式碼檔案
- 建立與教科書章節對應的 `_code/` 目錄結構
- 為每個章節建立編譯和測試腳本
- 撰寫測試報告

## 工作流程

### 步驟 1: 理解專案結構

```
project/
├── tw/                          # 繁體中文教科書目錄
│   ├── 01-chapter.md
│   ├── 02-chapter.md
│   └── ...
└── _code/                       # 程式碼目錄（與 tw/ 同層）
    ├── 01/                      # 與 01-chapter.md 對應
    │   ├── 01-1-example.c
    │   └── test.sh
    ├── 02/
    └── ...
```

### 步驟 2: 找出所有需要建立的檔案

使用 `grep` 找出 Markdown 中參考的程式碼檔案：

```bash
grep "_code/" tw/*.md
```

這會回傳所有類似 `[_code/02/02-1-regex.c](_code/02/02-1-regex.c)` 的引用。

### 步驟 3: 閱讀 Markdown 章節

對每個章節：

1. 找到所有 `[_code/xx/filename.c](_code/xx/filename.c)` 連結
2. 讀取該連結後面的 ```c ... ``` 程式碼區塊
3. 理解程式碼的用途和邏輯

### 步驟 4: 建立目錄結構

```bash
mkdir -p _code/{01,02,03,04,05,06,07,08,09,10,11,12,13,14}
```

### 步驟 5: 建立 C 程式碼檔案

建立與 Markdown 中相同的程式碼，但確保：

1. **完整可編譯**：移除任何標記式預留位置（如 `// ...`）
2. **添加 helper 函數**：填入未定義的輔助函數
3. **添加 main() 函數**：確保程式可獨立執行
4. **包含必要的 header**：`<stdio.h>`, `<stdlib.h>`, `<string.h>` 等

### 步驟 6: 建立測試腳本

為每個章節建立 `test.sh`：

```bash
#!/bin/bash
set -e

echo "Testing Chapter XX"
cd "$(dirname "$0")"

echo "Compiling..."
gcc -o file1 file1.c
gcc -o file2 file2.c

echo "Running tests..."
./file1
./file2

echo "All tests passed!"
```

## 常見模式與轉換技巧

### 1. 詞法分析器/Tokenizer

**Python 版本** (PLY):
```python
tokens = ['NUMBER', 'PLUS', 'MINUS']
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
```

**C 版本**:
```c
typedef enum { TOKEN_NUM, TOKEN_PLUS, TOKEN_MINUS, TOKEN_EOF } TokenType;

typedef struct {
    TokenType type;
    int value;
    char lexeme[64];
} Token;

Token tokens[100];
int token_count = 0;

TokenType get_token_type(const char* str) {
    if (strcmp(str, "+") == 0) return TOKEN_PLUS;
    // ...
}
```

### 2. AST 節點

**Python 版本**:
```python
class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.type = node_type
        self.value = value
        self.children = children or []
```

**C 版本**:
```c
typedef enum { NODE_NUM, NODE_BINOP, NODE_IDENT } NodeType;

typedef struct ASTNode {
    NodeType type;
    int value;  // for numbers
    char name[64];  // for identifiers
    struct ASTNode *left;
    struct ASTNode *right;
} ASTNode;

ASTNode* make_num(int v) {
    ASTNode* n = malloc(sizeof(ASTNode));
    n->type = NODE_NUM;
    n->value = v;
    n->left = n->right = NULL;
    return n;
}
```

### 3. 虛擬機 (VM)

**Python 版本**:
```python
def run_vm(bytecode):
    stack = []
    for op in bytecode:
        if op == 'ADD':
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
```

**C 版本**:
```c
#define MAX_STACK 256

typedef enum { OP_LOAD, OP_ADD, OP_HALT } OpCode;

int stack[MAX_STACK];
int sp = 0;

void push(int v) { stack[sp++] = v; }
int pop() { return stack[--sp]; }

void run(OpCode* bc) {
    for (int pc = 0; bc[pc] != OP_HALT; pc++) {
        switch (bc[pc]) {
            case OP_LOAD: push(bc[++pc]); break;
            case OP_ADD: {
                int b = pop(), a = pop();
                push(a + b);
                break;
            }
        }
    }
}
```

### 4. 排程器模擬

```c
typedef struct {
    int pid;
    char name[32];
    int burst_time;
    int priority;
} Process;

// FCFS queue
void fcfs_schedule(Process* procs, int n) {
    int time = 0;
    for (int i = 0; i < n; i++) {
        printf("Time %d: Running P%d\n", time, procs[i].pid);
        time += procs[i].burst_time;
    }
}
```

### 5. 記憶體管理

```c
// Page table entry
typedef struct {
    int frame;
    int valid;
    int dirty;
} PTE;

// Virtual address translation
unsigned long translate(unsigned long vaddr, PageTable* pt) {
    unsigned vpn = vaddr >> PAGE_BITS;
    unsigned offset = vaddr & ((1 << PAGE_BITS) - 1);
    if (!pt->entries[vpn].valid) return -1; // page fault
    return (pt->entries[vpn].frame << PAGE_BITS) | offset;
}
```

## 常見問題與解決

### 1. 隱式函數宣告

C99 不允許隱式函數宣告。確保在使用前宣告所有函數：

```c
// 宣告順序
ASTNode* parse_expr();
ASTNode* parse_term();

ASTNode* parse_expr() { /* ... */ }
ASTNode* parse_term() { /* ... */ }
```

### 2. 大型結構體堆疊溢出

對於大型陣列，使用堆積分配：

```c
// 錯誤 - 可能堆疊溢出
PageTable pt;  // NUM_PAGES = 1M entries

// 正確
PageTable* pt = malloc(sizeof(PageTable));
```

### 3. 缺少 helper 函數

Markdown 中的程式碼可能缺少輔助函數。必要時添加：

```c
// Markdown 中可能只有：
ASTNode* make_num(int v);

// 需要添加完整實作：
ASTNode* make_num(int v) {
    ASTNode* n = malloc(sizeof(ASTNode));
    n->type = NODE_NUM;
    n->value = v;
    n->left = n->right = NULL;
    return n;
}
```

### 4. 網路程式需要客戶端/伺服器配對

TCP/UDP 程式碼只能編譯，無法獨立測試。在 test.sh 中標註：

```bash
echo "Note: Network programs compile but require"
echo "runtime testing with actual client/server connections."
```

### 5. 指標運算

確保所有指標運算正確：

```c
// 正確
int phys = (frame << PAGE_BITS) | offset;

// 錯誤
int phys = frame * PAGE_SIZE + offset;  // 運算子優先順序可能出問題
```

## 測試腳本範本

```bash
#!/bin/bash
set -e

echo "==================================="
echo "Testing Chapter XX - Title"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o file1 file1.c
gcc -o file2 file2.c -lm  # -lm for math library

echo ""
echo "Running tests..."
echo ""

echo "--- Test: file1.c ---"
./file1
echo "Expected: ..."

echo ""
echo "--- Test: file2.c ---"
./file2
echo "Expected: ..."

echo ""
echo "==================================="
echo "All Chapter XX tests passed!"
echo "==================================="
```

## 檔案命名慣例

| Markdown 參考 | 檔案系統中的實際檔案 |
|---------------|---------------------|
| `_code/02/02-1-regex.c` | `_code/02/02-1-regex.c` |
| `_code/04/04_01_symbol_table.c` | `_code/04/04_01_symbol_table.c` |
| `_code/05/05_01_tac_generator.c` | `_code/05/05_01_tac_generator.c` |

注意：有些章節使用 `-` 分隔符，有些使用 `_`（如 `04_01`）。保持與 Markdown 引用完全一致。

## 測試報告範本

```markdown
# Test Report - Chapter XX

## Summary

All C files for this chapter compile successfully and produce expected outputs.

## Test Results

| File | Status | Output |
|------|--------|---------|
| file1.c | PASS | expected output |
| file2.c | PASS | expected output |

## Running Tests

```bash
cd _code/XX && ./test.sh
```
```

## 驗證清單

建立完所有檔案後，確認：

- [ ] 所有 Markdown 中引用的檔案都已建立
- [ ] 所有 C 檔案可使用 `gcc` 編譯
- [ ] 每個章節有 `test.sh` 腳本
- [ ] 所有測試腳本執行成功
- [ ] 建立了 `test_report.md` 總結報告

## 編譯命令參考

```bash
# 基本 C 程式
gcc -o output input.c

# 使用數學函式庫
gcc -o output input.c -lm

# 使用正則表達式
gcc -o output input.c -lm

# 網路程式（無需額外參數）
gcc -o output input.c
```

## 注意事項

1. **不要假設庫的存在**：除非專案已確認使用某庫，否則使用標準 C
2. **處理邊界情況**：確保指標運算、陣列存取不會超出範圍
3. **記憶體管理**：使用 `malloc`/`free`，避免記憶體洩漏
4. **可讀性**：程式碼應能獨立理解，不依賴 Markdown 上下文

## 總結

完成一個章節的 C 程式碼轉換通常需要：
- 讀取 Markdown 章節 (5-10 分鐘)
- 建立對應 C 檔案 (15-30 分鐘，取決於程式碼複雜度)
- 修復編譯錯誤 (5-15 分鐘)
- 建立測試腳本 (10 分鐘)
- 執行測試驗證 (5 分鐘)
