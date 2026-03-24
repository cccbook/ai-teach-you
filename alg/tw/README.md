# 讓 AI 教你演算法

> 一本為人類程式設計師寫的演算法書籍

> 作者：陳鍾誠

---

## 書籍簡介

本書涵蓋兩大面向：**方法類**與**應用領域類**。方法類講解各種通用的演算法設計方法；應用領域類則展示演算法在特定領域的應用。每章都配有 Python 程式碼範例，幫助讀者深入理解各種演算法的原理與實現。

---

## 目錄

### 第一部分：方法類 (Method)

| 章節 | 主題 | 說明 |
|------|------|------|
| [Chapter 01](01-basics.md) | 查表法與基礎 | 查表法、列舉法、雜湊法、暴力法 |
| [Chapter 02](02-iteration.md) | 迭代法 | 迭代原理、收斂分析 |
| [Chapter 03](03-recursion.md) | 遞迴與函數式 | 遞迴法、函數式編程、Lambda Calculus |
| [Chapter 04](04-optimization.md) | 優化方法 | 評分法、改良法、爬山、模擬退火、梯度下降、貪婪 |
| [Chapter 05](05-search.md) | 搜尋法 | DFS，BFS、A*、最佳優先搜尋 |
| [Chapter 06](06-divide-conquer.md) | 分割擊破法 | 分治法、合併排序，快速排序、最近點對 |
| [Chapter 07](07-dp.md) | 動態規劃法 | DP 概述、費波那契、LCS、背包問題、區間 DP |
| [Chapter 08](08-random.md) | 隨機方法 | 隨機演算法、蒙地卡羅、遺傳演算法 |
| [Chapter 09](09-data.md) | 資料處理方法 | 前處理法、委託法、分層法、化約法 |
| [Chapter 10](10-approx.md) | 近似與模擬 | 逼近法、模擬法、轉換法 |

### 第二部分：應用領域類 (Domain)

| 章節 | 主題 | 說明 |
|------|------|------|
| [Chapter 11](11-text.md) | 文字與密碼學 | 文字處理、字串匹配、KMP、密碼學基礎 |
| [Chapter 12](12-audio.md) | 聲音處理 | 聲音訊號處理、FFT、音訊壓縮 |
| [Chapter 13](13-image.md) | 影像處理 | 影像基本操作、捲積、邊緣檢測、形態學 |
| [Chapter 14](14-graph.md) | 圖形理論 | 圖表示、遍歷，最短路徑，最小生成樹、網路流 |
| [Chapter 15](15-storage.md) | 儲存與資料庫 | 檔案組織，B+樹、索引結構、快取演算法 |
| [Chapter 16](16-quantum.md) | 量子計算 | 量子計算基礎、Grover、Shor 演算法 |
| [Chapter 17](17-ai.md) | 人工智慧 | 搜尋在 AI 中的應用、ML、DL 最佳化、強化學習 |

### 附錄

| 附錄 | 主題 |
|------|------|
| [Appendix A](appendix-a.md) | Python 實現經典演算法 |
| [Appendix B](appendix-b.md) | 演算法分析技巧 |
| [Appendix C](appendix-c.md) | 經典演算法題庫 |
| [Appendix D](appendix-d.md) | 參考資源 |

---

## 程式碼範例

所有程式碼範例放在 `_code/` 目錄下，按章節分類：

```
alg/_code/
├── 01/          # Chapter 1
├── 02/          # Chapter 2
...
└── 17/         # Chapter 17
```

---

## 索引

術語解釋放在 `index/` 目錄：

- [資料結構術語](index/data_structures.md)
- [排序演算法](index/sorting.md)
- [圖論術語](index/graph.md)
- [動態規劃術語](index/dp.md)

---

## 相關書籍

- [讓 AI 教你人工智慧](../ai/tw/README.md)
- [讓 AI 教你系統程式](../sp/tw/README.md)

---

*最後更新：2026-03-24*
