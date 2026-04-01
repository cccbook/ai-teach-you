# 符號表 (Symbol Table)

## 概述

符號表是編譯器中用於儲存識別字相關資訊的資料結構，是編譯器最重要的資料結構之一。

## 符號資訊

每個符號包含以下資訊：

| 欄位 | 說明 |
|-----|------|
| 名稱 | 識別字名稱 |
| 類型 | 資料類型（int, float, char 等） |
| 作用域 | 所屬作用域編號 |
| 位址 | 記憶體位址或偏移量 |
| 屬性 | 變數、函數、參數等 |

## 作用域管理

符號表通常使用巢狀結構管理作用域：

```
Scope 0 (全域)
├── x: int
└── foo: function

    Scope 1 (foo 內)
    ├── a: int (param)
    ├── b: int (param)
    └── y: int

        Scope 2 (if 內)
        └── z: int
```

## 資料結構

```c
typedef struct Symbol {
    char* name;
    Type* type;
    int scope;
    int offset;
    bool isFunction;
    bool isVariable;
    struct Symbol* next;
} Symbol;

typedef struct Scope {
    int level;
    Symbol* symbols;
    struct Scope* parent;
} Scope;
```

## 參考資源

- [第 4 章：語意分析](../04-semantic.md)
