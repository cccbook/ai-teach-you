# 17. Git 進階技巧與分支策略

## Git 為什麼重要

Git 不只是代碼管理工具，更是團隊協作的命脈。掌握 Git 的高級技巧，能大幅提升你的開發效率。

## AI 輔助 Git 操作

### 常見 Git 任務

```
你：
请帮我理解这个复杂的 Git 命令：

git rebase -i HEAD~3

AI：
## Git Rebase 交互式命令解释

### 命令结构
```
-i  : interactive（交互模式）
HEAD~3 : 最近的 3 次提交
```

### 执行后会出现编辑器，内容类似：
```
pick abc1234 提交消息1
pick def5678 提交消息2
pick ghi9012 提交消息3

# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# d, drop = remove commit
```

### 使用场景
1. 整理提交历史
2. 修改提交消息
3. 合并多个提交
4. 删除不需要的提交
```

### 常用場景命令

```
你：
请给我一个完整的 Git 工作流程，包括：
1. 创建功能分支
2. 提交代码
3. 保持分支同步
4. 整理提交历史
5. 合并到主分支

AI：
## Git 完整工作流程

### 1. 创建功能分支
```bash
# 从最新的 main 创建
git checkout main
git pull origin main
git checkout -b feature/user-auth

# 或者用更简洁的方式
git switch main && git pull && git switch -c feature/user-auth
```

### 2. 开发并提交
```bash
# 常规提交流程
git add .
git commit -m "feat: add user authentication"

# 如果想暂存特定文件
git add src/auth/login.ts
git add src/auth/auth.service.ts
git commit -m "feat: implement login logic"

# 查看提交历史
git log --oneline -5
```

### 3. 保持分支同步
```bash
# 方式一：Merge（保留历史）
git checkout feature/user-auth
git fetch origin
git merge origin/main
# 解决冲突后
git add .
git commit -m "merge: resolve conflicts with main"

# 方式二：Rebase（线性历史）
git checkout feature/user-auth
git fetch origin
git rebase origin/main
# 逐个解决冲突
git add .
git rebase --continue
```

### 4. 整理提交历史（可选）
```bash
# 合并最近的 3 个提交
git rebase -i HEAD~3

# 将多个提交 squash 成一个
pick abc1234 feat: add login
squash def5678 feat: add register
squash ghi9012 feat: add password reset

# 修改提交消息
reword abc1234 feat: implement user authentication (login, register, reset)
```

### 5. 合并到主分支
```bash
# 切换到 main
git checkout main

# 方式一：Merge（团队协作推荐）
git merge feature/user-auth

# 方式二：Squash and merge（单一功能）
git merge --squash feature/user-auth
git commit -m "feat: implement complete user authentication"

# 推送
git push origin main
```

### 6. 清理（可选）
```bash
# 删除已合并的分支
git branch -d feature/user-auth
git push origin --delete feature/user-auth
```
```

## 分支策略

### 常見分支模型

#### 1. Git Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Git Flow                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   main ──────●──────────────●──────────────────●──→   │
│                 ↘            ↙↘                         │
│   release/    ●──●──●    ●──●──●──●                     │
│   1.0        ↙            ↙↘                           │
│   hotfix/    ●────────●                                │
│   1.0.1                                                     │
│                                                         │
│                    ↘                                     │
│   develop ───●──●──●──●──●──●──●──●──●──●──●──●──→    │
│                    ↘         ↘         ↘                │
│   feature/        ●─────────────●─────────●             │
│   login           ↑                                        │
│   (从 develop 创建，合并回 develop)                        │
│                                                         │
└─────────────────────────────────────────────────────────┘

适用场景：定期发布的企业项目
优点：流程清晰，适合复杂项目
缺点：相对复杂
```

#### 2. GitHub Flow

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Flow                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   main ───────●───────────────────────●───────────→    │
│                ↑                     ↙                 │
│                │         PR + Review                   │
│                ↑                     ↑                 │
│   feature/    ●─────────●─────────●                     │
│                                                         │
│   规则：                                                 │
│   1. main 始终可部署                                    │
│   2. 所有工作在分支完成                                  │
│   3. 通过 PR 合并                                      │
│   4. 合并后立即部署                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘

适用场景：持续部署的互联网项目
优点：简单敏捷
缺点：不适合多版本维护
```

#### 3. Trunk-Based Development

```
┌─────────────────────────────────────────────────────────┐
│              Trunk-Based Development                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   main/trunk ──●──●──●──●──●──●──●──●──●──●──●──→    │
│                     ↑      ↑                            │
│                     │      │                            │
│                     │      └── 功能开关 (Feature Flag)  │
│                     │                                   │
│               短期分支 (1-2 天)                          │
│                                                         │
└─────────────────────────────────────────────────────────┘

适用场景：快速迭代的团队
优点：合并冲突少，快速集成
缺点：需要功能开关支持
```

### 讓 AI 幫你選擇分支策略

```
你：
我们团队 5 人，做 SaaS 产品，每周发布一次，
需要维护 2 个版本。
请推荐合适的 Git 流程。

AI：
## 推荐：改良版 Git Flow

### 分支结构
```
main        - 生产环境代码（永远可部署）
develop     - 开发主分支
release/*   - 发布准备分支
hotfix/*    - 紧急修复分支
feature/*  - 功能开发分支
```

### 工作流程
1. 从 `develop` 创建 `feature/*`
2. 开发完成后 PR 到 `develop`
3. 准备发布时创建 `release/x.x`
4. `release/*` 合并到 `main` 和 `develop`
5. 紧急修复从 `main` 创建 `hotfix/*`

### 你们的版本维护
- v1.x 在 main 的历史 tag
- v2.x 在 main 的最新代码
- 热修复需要 cherry-pick 或分别修复
```

## 進階 Git 技巧

### 1. 查找問題

```
你：
这段代码是哪个提交引入的？

AI：
## 查找引入问题的提交

### 方法一：Git bisect（二分查找）
```bash
# 开始二分查找
git bisect start

# 标记已知的问题版本
git bisect bad HEAD

# 标记正常的版本
git bisect good v1.0.0

# Git 会自动 checkout 中间版本，测试
# 如果这个版本有问题
git bisect bad
# 如果正常
git bisect good

# 重复直到找到第一个问题提交
# Git 会输出类似：
# 123abc is the first bad commit
```

### 方法二：Git blame
```bash
# 查看单行的提交历史
git blame src/utils/helper.ts

# 查看特定行的修改
git blame -L 10,20 src/utils/helper.ts
```

### 方法三：Git log
```bash
# 查看某个文件的所有提交
git log --follow -p src/auth/login.ts

# 按关键词搜索提交
git log --grep="login" --oneline

# 查看今天修改的文件
git log --since="24 hours ago" --oneline
```
```

### 2. 恢復誤操作

```
你：
我不小心 reset 到了之前的提交，怎么恢复？

AI：
## 恢复 reset 前的状态

### 方法一：使用 reflog
```bash
# 查看所有 HEAD 移动记录
git reflog

# 输出类似：
# a1b2c3d HEAD@{0}: reset: moving to HEAD~3
# e4f5g6h HEAD@{1}: commit: add new feature
# i7j8k9l HEAD@{2}: commit: fix bug
# m1n2o3p HEAD@{3}: commit: initial

# 恢复到 reset 前的位置
git checkout e4f5g6h
# 或者创建新分支
git checkout -b recovery-branch e4f5g6h
```

### 方法二：使用 ORIG_HEAD
```bash
# reset 会在 ORIG_HEAD 保存原始位置
git reset --hard ORIG_HEAD
```

### 其他常见恢复场景
```bash
# 恢复误删的分支
git checkout -b recovered-branch <sha>

# 恢复误删的文件
git checkout HEAD -- deleted-file.txt

# 恢复误 stash 的内容
git stash pop

# 恢复误 commit 的文件
git reset --soft HEAD~1
```
```

### 3. 補救提交

```
你：
我刚 commit 了，但是忘记添加文件了。

AI：
## 补救忘记的文件

### 方法一：使用 --amend
```bash
# 添加忘记的文件
git add forgotten-file.ts

# 修改最后一次提交
git commit --amend --no-edit

# 注意：这会修改 commit hash，不是推荐的生产做法
```

### 方法二：创建补充提交（推荐）
```bash
# 创建一个新提交
git add forgotten-file.ts
git commit -m "chore: add missing file from previous commit"
```

### 修改提交消息
```bash
git commit --amend -m "新的提交消息"
```
```

## AI 輔助衝突解決

```
你：
请帮我解决这个合并冲突：

AI：
## 冲突分析

### 冲突文件
`src/user/user.service.ts`

### 冲突内容
```javascript
<<<<<<< HEAD (当前分支)
const user = await db.users.findOne({ 
  email: userData.email 
});
=======
const user = await db.users.findOne({ 
  _id: userData.id 
});
>>>>>>> feature/new-auth

### 分析
- HEAD 想要按邮箱查询
- feature 分支想要按 ID 查询

### 建议解决方案
如果两者都需要：
```javascript
const user = await db.users.findOne({ 
  $or: [
    { _id: userData.id },
    { email: userData.email }
  ]
});
```

如果只需要一个，根据业务逻辑选择。
```

## 實踐練習

```
1. 用 AI 分析你项目的 Git 历史
2. 评估当前的分支策略
3. 尝试用 Git bisect 找一个老 bug
4. 练习 rebase 和 merge 的不同场景
5. 创建你的 Git 速查表
```

**Git 是工具，不是目的。選擇讓團隊舒適的流程，而不是盲目遵循規則。**
