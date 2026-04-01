# 詞法分析 (Lexical Analysis)

## 概述

詞法分析是編譯器的第一個階段，負責將原始程式的字元序列轉換為 Token 序列。

## 工作流程

```
原始程式碼:  int x = 10;
                │
                ▼
         ┌────────────┐
         │  詞法分析   │
         └────────────┘
                │
                ▼
Tokens: [INT] [IDENT x] [ASSIGN] [NUMBER 10] [SEMICOLON]
```

## Token 類型

| 類型 | 範例 |
|-----|------|
| 關鍵字 | int, return, if, else |
| 識別字 | x, y, main, add |
| 運算子 | +, -, *, /, =, <, > |
| 常數 | 10, 3.14, "hello" |
| 分隔符 | ( ) { } ; , |

## 實作方法

- 有限狀態機（Finite State Machine）
- 正規表達式（Regular Expression）
- Lex/Flex 工具

## 參考資源

- [第 2 章：詞法分析](../02-lexer.md)
