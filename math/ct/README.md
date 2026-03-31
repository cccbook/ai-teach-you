# 計算理論：從希爾伯特到最新發展

> 從希爾伯特、哥德爾、丘奇、圖靈、喬姆斯基，到 NP-Complete，再到最新計算理論的發展

這是一本關於計算理論的深度教材，強調理論與實作的結合。

---

## 目錄

### 第一部分：基礎與歷史

| 章節 | 主題 | 說明 |
|------|------|------|
| [01-導論](01-introduction.md) | 計算理論導論 | 三大領域、簡史、第一個計算模型 |
| [02-希爾伯特](02-hilbert-entscheidungsproblem.md) | 希爾伯特與判定問題 | 23問題、Entscheidungsproblem、形式系統 |
| [03-哥德爾](03-godel-incompleteness.md) | 哥德爾不完備定理 | 哥德爾編號、自引用、兩大不完備定理 |

### 第二部分：λ演算

| 章節 | 主題 | 說明 |
|------|------|------|
| [04-λ演算理論](04-church-lambda-calculus.md) | 丘奇的λ演算 | 語法、Church編碼、SKI組合子 |
| [05-λ演算實作](05-lambda-implementation.md) | λ演算Python實作 | 完整解譯器、詞法分析、歸約引擎 |

### 第三部分：圖靈機

| 章節 | 主題 | 說明 |
|------|------|------|
| [06-圖靈機理論](06-turing-machine-theory.md) | 圖靈機理論 | 直覺、形式定義、停機問題 |
| [07-圖靈機實作](07-turing-machine-implementation.md) | 圖靈機Python實作 | 多帶、NTM、通用圖靈機、視覺化 |

### 第四部分：丘奇-圖靈論題與語言

| 章節 | 主題 | 說明 |
|------|------|------|
| [08-丘奇-圖靈論題](08-church-turing-thesis.md) | 丘奇-圖靈論題 | 兩種模型的等價性、其他計算模型 |
| [09-喬姆斯基層級](09-chomsky-hierarchy.md) | 喬姆斯基層級 | 正規、上下文無關、上下文敏感語言 |
| [10-自動機實作](10-automata-implementation.md) | 自動機Python實作 | DFA、NFA、正則引擎、PDA |

### 第五部分：複雜度理論

| 章節 | 主題 | 說明 |
|------|------|------|
| [11-NP-完全理論](11-np-completeness.md) | NP-完全理論 | P vs NP、Cook-Levin定理、經典NP-完全問題 |

### 第六部分：現代發展

| 章節 | 主題 | 說明 |
|------|------|------|
| [12-現代發展](12-modern-developments.md) | 現代計算理論 | 量子計算、PCP定理、新興範式 |

---

## 程式碼目錄

```
_code/
├── 01/          # 第1章 狀態機、計算理論基礎
├── 02/          # 第2章 丢番圖方程
├── 03/          # 第3章 哥德爾編號、自引用
├── 04/          # 第4章 Church編碼、組合子
├── 05/          # 第5章 λ演算解譯器
│   └── lambda_interpreter/
├── 06/          # 第6章 圖靈機設計
├── 07/          # 第7章 圖靈機模擬器
├── 08/          # 第8章 相關演示
├── 09/          # 第9章 泵引理
├── 10/          # 第10章 自動機實現
├── 11/          # 第11章 NP-完全問題
└── 12/          # 第12章 量子計算基礎
```

---

## 快速開始

### 運行λ演算解譯器

```bash
cd _code/05
python -m lambda_interpreter.interpreter
```

### 運行圖靈機模擬器

```bash
cd _code/07
python 07-1-basic-turing-machine.py
```

### 運行自動機演示

```bash
cd _code/10
python 10-1-dfa.py
```

---

## 專有名詞索引

- [λ演算](index/lambda-calculus.md) - 函數式計算的理論基礎
- [圖靈機](index/turing-machine.md) - 計算的機械模型
- [丘奇-圖靈論題](index/church-turing.md) - 可計算性的核心假設
- [哥德爾不完備](index/godel.md) - 形式系統的極限
- [NP-完全](index/np-complete.md) - 複雜度理論的核心概念
- [喬姆斯基層級](index/chomsky.md) - 形式語言的分類

---

## 參考資源

### 經典論文

- Turing, A.M. (1936). *On Computable Numbers*
- Church, A. (1936). *An Unsolvable Problem of Elementary Number Theory*
- Gödel, K. (1931). *On Formally Undecidable Propositions*
- Cook, S. (1971). *The Complexity of Theorem Proving Procedures*

### 推薦書籍

- Hopcroft, J.E., Motwani, R., Ullman, J.D. - *Introduction to Automata Theory*
- Sipser, M. - *Introduction to the Theory of Computation*
- Arora, S., Barak, B. - *Computational Complexity: A Modern Approach*

---

*最後更新：2026-03-31*
