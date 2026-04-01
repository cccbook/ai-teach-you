# 目錄

## 第一部分：編譯器基礎

* [1. 編譯器簡介](01-intro.md) - 編譯器的歷史、架構與工作流程，LLVM 概述
* [2. 詞法分析](02-lexer.md) - Token 化與正規表達式
* [3. 語法分析](03-parser.md) - 語法分析器與遞迴下降
* [4. 語意分析](04-semantic.md) - 符號表與類型檢查

## 第二部分：LLVM IR 中間碼

* [5. LLVM IR 語法](05-ir.md) - LLVM IR 語法入門與 .ll 檔案格式
* [6. 中間碼生成](06-ir-gen.md) - 從 AST 生成 LLVM IR
* [7. 程式碼優化](07-optimization.md) - LLVM Pass 優化，常數折疊、死程式碼消除

## 第三部分：目標碼與執行環境

* [8. 目標碼生成](08-codegen.md) - 從 LLVM IR 生成目標碼
* [9. 執行時期環境](09-runtime.md) - 堆疊框架與函數呼叫
* [10. 記憶體管理](10-memory.md) - malloc 與記憶體配置

## 第四部分：進階主題

* [11. 連結器與載入器](11-linker.md) - 符號解析與重定位
* [12. JIT 編譯與虛擬機](12-jit.md) - LLVM JIT 編譯技術
* [13. 迴圈優化與向量化](13-loop-vectorize.md) - 迴圈優化、SIMD 向量化
* [14. LLVM Pass 開發](14-pass.md) - 自訂編譯器優化 Pass
* [15. 現代編譯器架構](15-modern.md) - LLVM 與 GCC 內部結構

## 附錄

* [專有名詞索引](./index/README.md)
