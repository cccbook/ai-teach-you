# Git Worktree 協作設定

> 來源：第 12 章「系統架構設計」

---

## 為什麼使用 Git Worktree？

### 傳統方式問題

- 切換分支需要等待
- 無法同時開發多個功能

### Worktree 優勢

- 同時多分支工作
- 不影響主分支
- 適合 AI 協作

---

## 基本指令

```bash
# 建立 worktree
git worktree add ../feature-branch main

# 列出 worktree
git worktree list

# 刪除 worktree
git worktree remove ../feature-branch
```

---

## AI 協作範例

```bash
# 1. 建立開發分支
git worktree add -b ai-feature ../ai-feature

# 2. AI 在 worktree 中開發
cd ../ai-feature
# 使用 AI 生成程式碼

# 3. 主分支繼續開發
cd main
# 其他人繼續工作
```
