# Git

## 概述

Git 是一個分散式版本控制系統，用於追蹤程式碼變更、協調多人協作。是現代軟體開發的必備工具。

## 基本概念

### 工作區域

```
┌─────────────────┐
│   Working Dir   │  工作目錄
├─────────────────┤
│     Staging     │  暫存區
├─────────────────┤
│    Repository   │  本地倉庫
└─────────────────┘
```

### 三棵樹

| 區域 | 說明 |
|------|------|
| Working Directory | 工作目錄，實際檔案 |
| Staging Area | 暫存區，準備提交的變更 |
| Repository | 倉庫，提交的歷史記錄 |

## 基本命令

### 初始化與克隆

```bash
# 初始化新倉庫
git init

# 克隆遠端倉庫
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git my-folder
```

### 基本操作

```bash
# 查看狀態
git status

# 新增檔案到暫存區
git add filename.txt        # 單一檔案
git add .                   # 所有變更
git add *.js                # 符合模式的檔案

# 提交
git commit -m "提交訊息"
git commit -am "快速提交（僅追蹤中的檔案）"

# 查看歷史
git log
git log --oneline           # 簡潔格式
git log --graph             # 圖形化
```

### 分支操作

```bash
# 查看分支
git branch                   # 本地分支
git branch -r               # 遠端分支
git branch -a               # 所有分支

# 建立分支
git branch feature/new-feature

# 切換分支
git checkout feature-branch
git switch feature-branch    # 新語法

# 建立並切換
git checkout -b new-branch
git switch -c new-branch    # 新語法

# 刪除分支
git branch -d branch-name
git branch -D branch-name   # 強制刪除
```

### 遠端操作

```bash
# 查看遠端
git remote -v

# 新增遠端
git remote add origin https://github.com/user/repo.git

# 推送
git push origin main
git push -u origin feature   # 設定上游分支

# 拉取
git pull origin main

# 獲取（不下載）
git fetch origin
```

### 合併與變更

```bash
# 合併分支
git checkout main
git merge feature-branch

# 變更基底
git rebase main

# 取消變更
git checkout -- filename     # 恢復檔案
git restore filename        # 新語法
git reset HEAD filename     # 取消暫存
```

## 進階命令

### 貯藏（Stash）

```bash
# 貯藏變更
git stash
git stash save "工作描述"

# 查看貯藏
git stash list

# 恢復貯藏
git stash apply             # 保留貯藏
git stash pop               # 恢復並刪除

# 刪除貯藏
git stash drop
```

### 標籤

```bash
# 建立標籤
git tag v1.0.0
git tag -a v1.0.0 -m "版本 1.0.0"

# 推送標籤
git push origin v1.0.0
git push origin --tags
```

### 檢視差異

```bash
git diff                    # 未暫存的變更
git diff --staged           # 暫存區的變更
git diff branch1..branch2    # 分支間差異
```

## 團隊協作流程

### Git Flow

```
main ──────●─────●─────●─────●─── (production)
           │             │
develop ───●─────●─────●─────●───
           │     │     │
      feature   │  release
        ●─●─●  │   ●─●
              hotfix
                ●─●
```

### GitHub Flow

```bash
# 1. 從 main 建立功能分支
git checkout -b feature/new-feature

# 2. 開發並提交
git add .
git commit -m "Add new feature"

# 3. 推送並建立 Pull Request
git push -u origin feature/new-feature

# 4. Code Review 後合併到 main
```

## 常用別名

```bash
# ~/.gitconfig
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

## 參考資源

- [Git 官方網站](https://git-scm.com/)
- [Git 中文文件](https://git-scm.com/book/zh-tw/v2)
- [GitHub](https://github.com/)
