# LLVM IR

## 概述

LLVM IR（Intermediate Representation）是 LLVM 編譯器架構的中間表示形式。

## 三種形式

1. 記憶體中的資料結構
2. 位元碼（.bc 檔案）
3. 可讀文字格式（.ll 檔案）

## 基本類型

| IR 類型 | C 對應 |
|--------|--------|
| i1 | bool |
| i8 | char |
| i32 | int |
| i64 | long |
| float | float |
| double | double |

## 範例

```llvm
define i32 @add(i32 %a, i32 %b) {
  %result = add i32 %a, %b
  ret i32 %result
}
```

## 參考資源

- LLVM Language Reference: https://llvm.org/docs/LangRef.html
