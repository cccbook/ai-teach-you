# 4. 語意分析

## 4.1 什麼是語意分析

語意分析（Semantic Analysis）是編譯器的第三個階段，負責檢查程式碼的語義正確性，包括：
- 類型檢查
- 作用域分析
- 符號表管理
- 常數折疊

語意分析在語法分析的基礎上進行，利用 AST 和符號表來進行更深層次的分析。

## 4.2 符號表

符號表（Symbol Table）是編譯器中最重要的資料結構之一，用於儲存識別字的相關資訊：

[程式檔案：04-1-symbol-table.h](../_code/04/04-1-symbol-table.h)
```c
typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_DOUBLE,
    TYPE_CHAR,
    TYPE_VOID,
    TYPE_POINTER,
    TYPE_ARRAY,
    TYPE_FUNCTION
} TypeKind;

typedef struct Symbol {
    char* name;
    Type* type;
    int scope;
    int offset;
    bool isFunction;
    bool isVariable;
    bool isParam;
    struct Symbol* next;
} Symbol;

typedef struct Scope {
    int level;
    Symbol* symbols;
    struct Scope* parent;
} Scope;
```

## 4.3 符號表實作

以下是符號表的完整實作：

[程式檔案：04-1-symbol-table.c](../_code/04/04-1-symbol-table.c)
```c
SymbolTable* createSymbolTable() {
    SymbolTable* table = (SymbolTable*)malloc(sizeof(SymbolTable));
    table->current = (Scope*)malloc(sizeof(Scope));
    table->current->level = 0;
    table->current->symbols = NULL;
    table->current->parent = NULL;
    table->nextOffset = 0;
    return table;
}

void enterScope(SymbolTable* table) {
    Scope* newScope = (Scope*)malloc(sizeof(Scope));
    newScope->level = table->current->level + 1;
    newScope->symbols = NULL;
    newScope->parent = table->current;
    table->current = newScope;
}

void exitScope(SymbolTable* table) {
    if (table->current->parent) {
        Scope* oldScope = table->current;
        table->current = table->current->parent;
        free(oldScope);
    }
}

Symbol* lookup(SymbolTable* table, char* name) {
    Scope* scope = table->current;
    while (scope) {
        Symbol* sym = scope->symbols;
        while (sym) {
            if (strcmp(sym->name, name) == 0) {
                return sym;
            }
            sym = sym->next;
        }
        scope = scope->parent;
    }
    return NULL;
}
```

## 4.4 類型檢查

類型檢查確保運算元的類型相容：

```c
int a = 10;
float b = 3.14;
int c = a + b;  // 錯誤：不能將 float 加到 int
```

類型檢查規則：
- 加法、減法、乘法、除法：兩個運算元必須類型相同
- 比較運算子：兩個運算元必須類型相容
- 賦值運算：右值必須可以轉換為左值的類型
- 函數呼叫：參數類型必須與函數簽名匹配

## 4.5 作用域管理

作用域（Scope）決定了識別字的可訪問範圍：

```
int x = 10;           // 全域作用域

void foo() {
    int x = 20;       // foo 的本地作用域
    if (x > 5) {
        int y = x;    // if 區塊的作用域
    }
}
```

作用域規則：
- 內層作用域可以訪問外層作用域的識別字
- 外層作用域不能訪問內層作用域的識別字
- 相同作用域中不能有重複的識別字

## 4.6 使用 clang 查看語意分析

```bash
# 查看語意分析錯誤
clang -Wall -Wextra -fsyntax-only example.c

# 查看類型資訊
clang -Xclang -ast-dump example.c
```

## 4.7 本章小結

本章介紹了語意分析的核心概念：
- 符號表管理識別字的資訊
- 作用域管理識別字的可訪問範圍
- 類型檢查確保語義正確性
- 語意分析連接了前端和後端

## 練習題

1. 實作陣列類型和指標類型的符號表記錄。
2. 為語意分析器加入類型推斷功能。
3. 實作函數重載的語意檢查。
4. 為結構體和聯合體添加符號表支援。
