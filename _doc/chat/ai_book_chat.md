# AI 書籍寫作對話紀錄

## 時間範圍
2026-03-24

## 參與者
- User: 陳鍾誠 (作者)
- AI: OpenCode + Big Pickle 模型

---

## 對話摘要

### 1. 系統程式書籍回顧
- User 詢問「到目前為止我們做了什麼？」
- AI 回顧了已完成的工作：14章書籍寫完、程式碼目錄建立、2個程式碼檔案測試
- 待完成：提取程式碼、測試、加入連結

### 2. 繼續執行
- User 說「yes」繼續
- AI 修復了 01-1-hello.c（LSP 錯誤：Python 註解改為 C 註解）
- 測試並通過

### 3. 程式碼提取任務
- AI 使用 Task Agent 逐步提取各章節的程式碼
- 成功完成 Chapters 1-14 的程式碼提取
- 測試各章 Python/C 檔案

### 4. 連結格式修正
- User 指出連結格式錯誤：`sp/_code/01/...` 應改為相對路徑 `../_code/01/...`
- AI 修正了 Chapter 1 的所有連結

### 5. 連結位置修正
- User 指出連結應放在程式碼**前面**而非後面
- 格式範例：
  ```markdown
  [程式檔案：01-2-x86-assembly.s](../_code/01/01-2-x86-assembly.s)
  ```assembly
  ...
  ```
- AI 重新寫入 Chapter 1-2，並使用 Task Agent 完成 Chapters 3-14

### 6. 專有名詞索引
- User 要求建立專有名詞索引放在 `tw/index/README.md`
- 每個專有名詞要有簡要說明，點進去有詳細說明
- AI 建立了 index 目錄和多個術語檔案（lisp.md, c.md, compiler.md, python.md 等）

### 7. 程式類書籍寫作 Skill
- User 要求將這次寫程式類書籍的 skill 寫入 `/Users/Shared/ccc/mybook/ai-teach-you/_doc/skill/write_code_book_skill.md`
- 要求是通用程式類書籍，不是只有這本書
- AI 建立了完整的 skill 文件

### 8. Skill 改用繁體中文
- User 要求用繁體中文撰寫，並加註
- AI 完全重寫 skill，新增開頭註解 `> **注意**：本文件使用繁體中文撰寫。`

### 9. AI 書籍規劃
- User 要求閱讀 AI 書籍的 README 並寫出詳細 TOC
- AI 閱讀了 `/Users/Shared/ccc/mybook/ai-teach-you/ai/tw/README.md`
- 建立了 17 章 + 4 附錄的詳細 TOC

### 10. TOC 修正
- User 修正：
  - 加入第 16.6 實作：建構 AI 助手，參考 mini-openclaw.py
  - 第 17 章改為「強化學習」
  - 第 18 章改為「世界模型」
- AI 修正了 TOC.md

### 11. 生成式 AI 章節
- User 要求加入第 15 章「生成式 AI」
- 放置在「視覺聽覺模型」之後
- AI 修正並重新編號（14-19 章）

### 12. 強化學習範例規劃
- User 詢問強化學習要幾個實作範例
- AI 建議：Q-Learning 走迷宮 → DQN → Policy Gradient → AlphaGo 井字棋
- User 同意

### 13. 範例清單 code_list.md
- User 要求先規劃所有範例放在 `ai/_code/code_list.md`
- AI 建立了完整的程式碼範例清單（19章 + 附錄，共 106 個範例）

### 14. 爬山演算法加入
- User 要求在傳統 AI 技術中最開始加入爬山演算法
  - f(x) = (x-1)² 找最低點
  - 爬山演算法解決 TSP
- 同時更新 TOC.md
- AI 完成修正

### 15. 第 1 章範例新增
- User 詢問第 1 章（AI 歷史）可以加什麼範例
- AI 建議：ELIZA、規則式系統、傳統 ML 比較
- User 選擇：
  1. ELIZA（最具影響力）
  2. Prolog 家族關係
  3. Lisp 符號處理
  4. 簡化版 MYCIN

### 16. 第 3 章範例新增
- User 询问第 3 章要加什麼範例
- AI 建議：micrograd、microgpt、經典深度學習模型
- User 選擇：
  1. micrograd
  2. microgpt
  並指定順序：
  - f(x) = (x-1)² + (y-2)² + (z-3)² 找最低點
  - linear regression
  - CNN 解 MNIST
  - 最後才是 gpt

### 17. 確認與開始寫書
- User 確認以上規劃
- 要求：
  1. 先寫完範例程式，確認可執行
  2. 再開始寫書
  3. 一次寫完 19 章
  4. 不需要再討論
- 同時要求更新這次學到的 skill 到 `write_code_book_skill.md`

### 18. 第 3 章 TOC 修正
- User 給定新的第 3 章大綱：
  - 3.1 現代 AI 技術源自神經網路
  - 3.2 梯度下降算法
  - 3.3 反傳遞算法
  - 3.4 Hinton 等人 1986 在語音辨識上的成功
  - 3.5-3.9 其餘主題
- 那些範例只是在文章中的程式實作重現（意即不需独立章节）

---

## 學到的關鍵技能

1. **code_list.md 優先規劃**
   - 在開始寫書之前，先建立完整的程式碼範例清單
   - 確認每章都有足夠的實作範例
   - 方便追蹤進度

2. **相對路徑連結**
   - 書籍在 `tw/` 目錄
   - 程式碼在 `../_code/XX/` 目錄
   - 使用相對路徑確保連結正確

3. **連結放置位置**
   - 連結應放在程式碼**前面**而非後面
   - 格式：`[程式檔案：filename.ext](../_code/XX/filename.ext)`

4. **分階段工作**
   - 第一階段：建立 code_list.md 規劃所有範例
   - 第二階段：撰寫並測試所有程式碼
   - 第三階段：撰寫書籍本文
   - 第四階段：加入程式碼連結

5. **使用 Task Agent 加速**
   - 大量程式碼檔案可使用 Task Agent 並行處理
   - 確保每個檔案可執行並產出 demo output

6. **測試策略**
   - 可測試語言：Python, C, Shell
   - 跳過無法測試的語言（Haskell, Prolog, 等）
   - 跳過不完整的程式碼片段
