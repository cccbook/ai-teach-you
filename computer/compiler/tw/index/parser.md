# 語法分析 (Syntax Analysis / Parsing)

## 概述

語法分析是編譯器的第二個階段，負責檢查 Token 序列是否符合語法規則，並將其轉換為抽象語法樹（AST）。

## 工作流程

```
Token 序列: [INT] [IDENT] [LPAREN] ...
                │
                ▼
         ┌────────────┐
         │  語法分析   │
         └────────────┘
                │
                ▼
    抽象語法樹 (AST)
```

## 語法分析方法

### 1. 遞迴下降分析（Recursive Descent）

每個文法規則對應一個函數，適合 LL(1) 文法。

### 2. LR 分析

由下而上分析，適合大多數程式語言。

### 3. LALR 分析

LR 的簡化版本，效率和實用性兼具。

## 上下文無關文法範例

```
expression → term (('+' | '-') term)*
term       → factor (('*' | '/') factor)*
factor     → NUMBER | IDENT | '(' expression ')'
```

## 參考資源

- [第 3 章：語法分析](../03-parser.md)
