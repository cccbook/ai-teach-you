# 計算機結構——使用 Verilog 實作設計

## 書籍概述

本書以 Verilog 硬體描述語言實作各種計算機結構元件，從基礎的數位邏輯電路開始，逐步建構完整的處理器系統。理論與實作並重，每個單元都配有可執行的 Verilog 程式碼範例。

## 目錄結構

### 第一部分：數位邏輯基礎

| 章節 | 說明 |
|------|------|
| [01-數位邏輯基礎](./01-digital-logic-basics.md) | 布林代數、邏輯閘、真值表 |
| [02-組合邏輯電路](./02-combinational-logic.md) | 多工器、解多工器、編碼器、解碼器 |
| [03-序向邏輯電路](./03-sequential-logic.md) | 正反器、暫存器、計數器 |

### 第二部分：Verilog 語言基礎

| 章節 | 說明 |
|------|------|
| [04-Verilog 語法入門](./04-verilog-basics.md) | 模組、資料類型、運算子 |
| [05-Verilog 模組設計](./05-verilog-module-design.md) | 結構化設計、階層式設計 |

### 第三部分：計算機結構核心元件

| 章節 | 說明 |
|------|------|
| [06-算術邏輯單元](./06-arithmetic-logic-unit.md) | ALU 加減乘除、邏輯運算 |
| [07-暫存器與暫存器檔案](./07-registers-register-file.md) | 暫存器堆疊、讀寫控制 |
| [08-記憶體設計](./08-memory.md) | ROM、RAM、指令記憶體、資料記憶體 |

### 第四部分：處理器設計

| 章節 | 說明 |
|------|------|
| [09-控制單元](./09-control-unit.md) | 微程式控制、指令解碼 |
| [10-指令集架構](./10-instruction-set.md) | 指令格式、定址模式 |
| [11-單週期處理器](./11-single-cycle-processor.md) | MIPS 指令集實作 |
| [12-多週期處理器](./12-multi-cycle-processor.md) | 狀態機設計 |
| [13-管線化處理器](./13-pipelined-processor.md) | 五級管線、資料 hazard |

### 第五部分：記憶體與效能

| 章節 | 說明 |
|------|------|
| [14-快取記憶體](./14-cache-memory.md) | 直接映射、關聯映射 |
| [15-虛擬記憶體](./15-virtual-memory.md) | 分頁、TLB |
| [16-效能分析與優化](./16-performance-optimization.md) | Amdahl 定律、管線優化 |

### 第六部分：進階主題

| 章節 | 說明 |
|------|------|
| [17-輸入輸出系統](./17-io-system.md) | 中斷、DMA |
| [18-平行處理](./18-parallel-processing.md) | 多核心、向量處理器 |
| [19-現代處理器技術](./19-modern-processor-techniques.md) | 超純量、預測執行 |

---

## 程式碼範例清單

請參考 [_code/code_list.md](../_code/code_list.md)

## 執行環境

- Icarus Verilog (iverilog)
- Verilog 標準：IEEE 1364-2005

## 專有名詞索引

請參考 [index/README.md](./index/README.md)

## 附錄

- [附錄 A：Verilog 快速參考](./appendix/appendix-a-verilog-quick-ref.md)
- [附錄 B：MIPS 指令集](./appendix/appendix-b-mips-instruction-set.md)
- [附錄 C：實驗環境建置](./appendix/appendix-c-environment-setup.md)
