# 17. Advanced Git Techniques and Branching Strategies

## Why Git Matters

Git is not just a code management tool, but the lifeblood of team collaboration. Mastering advanced Git techniques can significantly improve your development efficiency.

## AI-Assisted Git Operations

### Common Git Tasks

```
You:
Please help me understand this complex Git command:

git rebase -i HEAD~3

AI:
## Git Rebase Interactive Command Explained

### Command Structure
```
-i  : interactive mode
HEAD~3 : last 3 commits
```

### What appears in editor:
```
pick abc1234 Commit message 1
pick def5678 Commit message 2
pick ghi9012 Commit message 3

# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# d, drop = remove commit
```

### Use Cases
1. Clean up commit history
2. Modify commit messages
3. Merge multiple commits
4. Delete unnecessary commits
```

### Common Scenario Commands

```
You:
Please give me a complete Git workflow including:
1. Create feature branch
2. Commit code
3. Keep branch synced
4. Clean up commit history
5. Merge to main branch

AI:
## Complete Git Workflow

### 1. Create Feature Branch
```bash
# From latest main
git checkout main
git pull origin main
git checkout -b feature/user-auth

# Or more concisely
git switch main && git pull && git switch -c feature/user-auth
```

### 2. Develop and Commit
```bash
# Regular commit flow
git add .
git commit -m "feat: add user authentication"

# If you want to stage specific files
git add src/auth/login.ts
git add src/auth/auth.service.ts
git commit -m "feat: implement login logic"

# View commit history
git log --oneline -5
```

### 3. Keep Branch Synced
```bash
# Method 1: Merge (preserves history)
git checkout feature/user-auth
git fetch origin
git merge origin/main
# After resolving conflicts
git add .
git commit -m "merge: resolve conflicts with main"

# Method 2: Rebase (linear history)
git checkout feature/user-auth
git fetch origin
git rebase origin/main
# Resolve conflicts one by one
git add .
git rebase --continue
```

### 4. Clean Up Commit History (Optional)
```bash
# Merge last 3 commits
git rebase -i HEAD~3

# Squash multiple commits into one
pick abc1234 feat: add login
squash def5678 feat: add register
squash ghi9012 feat: add password reset

# Modify commit message
reword abc1234 feat: implement user authentication (login, register, reset)
```

### 5. Merge to Main Branch
```bash
# Switch to main
git checkout main

# Method 1: Merge (recommended for team collaboration)
git merge feature/user-auth

# Method 2: Squash and merge (for single feature)
git merge --squash feature/user-auth
git commit -m "feat: implement complete user authentication"

# Push
git push origin main
```

### 6. Cleanup (Optional)
```bash
# Delete merged branch
git branch -d feature/user-auth
git push origin --delete feature/user-auth
```

## Branching Strategies

### Common Branch Models

#### 1. Git Flow

```
┌─────────────────────────────────────────────────────────┐
│                     Git Flow                             │
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
│   (Created from develop, merged back to develop)          │
│                                                         │
└─────────────────────────────────────────────────────────┘

Best for: Enterprise projects with regular releases
Pros: Clear process, suitable for complex projects
Cons: Relatively complex
```

#### 2. GitHub Flow

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Flow                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   main ───────●───────────────────────●───────────→    │
│                ↑                     ↙                 │
│                │         PR + Review                   │
│                ↑                     ↑                 │
│   feature/    ●─────────●─────────●                     │
│                                                         │
│   Rules:                                                 │
│   1. main is always deployable                          │
│   2. All work done in branches                         │
│   3. Merge through PR                                  │
│   4. Deploy immediately after merge                    │
│                                                         │
└─────────────────────────────────────────────────────────┘

Best for: Internet projects with continuous deployment
Pros: Simple and agile
Cons: Not suitable for maintaining multiple versions
```

#### 3. Trunk-Based Development

```
┌─────────────────────────────────────────────────────────┐
│              Trunk-Based Development                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   main/trunk ──●──●──●──●──●──●──●──●──●──●──●──→    │
│                     ↑      ↑                            │
│                     │      │                            │
│                     │      └── Feature Flags            │
│                     │                                   │
│               Short-lived branches (1-2 days)          │
│                                                         │
└─────────────────────────────────────────────────────────┘

Best for: Fast-iterating teams
Pros: Less merge conflicts, faster integration
Cons: Requires feature flag support
```

### Have AI Help You Choose Branching Strategy

```
You:
Our team has 5 people, building a SaaS product, weekly releases,
need to maintain 2 versions.
Please recommend a suitable Git workflow.

AI:
## Recommended: Modified Git Flow

### Branch Structure
```
main        - Production code (always deployable)
develop     - Main development branch
release/*   - Release preparation branches
hotfix/*    - Emergency fix branches
feature/*  - Feature development branches
```

### Workflow
1. Create `feature/*` from `develop`
2. PR to `develop` when complete
3. Create `release/x.x` when preparing for release
4. Merge `release/*` to both `main` and `develop`
5. Emergency fixes from `main` create `hotfix/*`

### Your Version Maintenance
- v1.x in main history tags
- v2.x in main latest code
- Hot fixes need cherry-pick or separate fixes
```

## Advanced Git Techniques

### 1. Finding Problems

```
You:
Which commit introduced this bug?

AI:
## Finding the Commit That Introduced a Problem

### Method 1: Git bisect (Binary search)
```bash
# Start bisect
git bisect start

# Mark known bad version
git bisect bad HEAD

# Mark known good version
git bisect good v1.0.0

# Git will automatically checkout middle version, test it
# If this version has the problem
git bisect bad
# If normal
git bisect good

# Repeat until finding the first bad commit
# Git will output something like:
# 123abc is the first bad commit
```

### Method 2: Git blame
```bash
# View single line's commit history
git blame src/utils/helper.ts

# View specific lines
git blame -L 10,20 src/utils/helper.ts
```

### Method 3: Git log
```bash
# View all commits for a file
git log --follow -p src/auth/login.ts

# Search commits by keyword
git log --grep="login" --oneline

# View files modified today
git log --since="24 hours ago" --oneline
```

### 2. Recovering from Mistakes

```
You:
I accidentally reset to a previous commit. How to recover?

AI:
## Recovering State Before Reset

### Method 1: Using reflog
```bash
# View all HEAD movement records
git reflog

# Output similar to:
# a1b2c3d HEAD@{0}: reset: moving to HEAD~3
# e4f5g6h HEAD@{1}: commit: add new feature
# i7j8k9l HEAD@{2}: commit: fix bug
# m1n2o3p HEAD@{3}: commit: initial

# Recover to state before reset
git checkout e4f5g6h
# Or create new branch
git checkout -b recovery-branch e4f5g6h
```

### Method 2: Using ORIG_HEAD
```bash
# reset saves original position in ORIG_HEAD
git reset --hard ORIG_HEAD
```

### Other Common Recovery Scenarios
```bash
# Recover deleted branch
git checkout -b recovered-branch <sha>

# Recover deleted file
git checkout HEAD -- deleted-file.txt

# Recover stashed content
git stash pop

# Recover file from commit
git reset --soft HEAD~1
```

### 3. Amending Commits

```
You:
I just committed but forgot to add a file.

AI:
## Fixing Forgotten Files

### Method 1: Using --amend
```bash
# Add forgotten file
git add forgotten-file.ts

# Amend last commit
git commit --amend --no-edit

# Note: This changes commit hash, not recommended for shared branches
```

### Method 2: Create supplementary commit (Recommended)
```bash
# Create a new commit
git add forgotten-file.ts
git commit -m "chore: add missing file from previous commit"
```

### Modify Commit Message
```bash
git commit --amend -m "New commit message"
```

## AI-Assisted Conflict Resolution

```
You:
Please help me resolve this merge conflict:

AI:
## Conflict Analysis

### Conflicting File
`src/user/user.service.ts`

### Conflicting Content
```javascript
<<<<<<< HEAD (current branch)
const user = await db.users.findOne({ 
  email: userData.email 
});
=======
const user = await db.users.findOne({ 
  _id: userData.id 
});
>>>>>>> feature/new-auth

### Analysis
- HEAD wants to query by email
- feature branch wants to query by ID

### Suggested Resolution
If both are needed:
```javascript
const user = await db.users.findOne({ 
  $or: [
    { _id: userData.id },
    { email: userData.email }
  ]
});
```

If only one is needed, choose based on business logic.
```

## Practice Exercises

```
1. Use AI to analyze your project's Git history
2. Evaluate current branching strategy
3. Try using Git bisect to find an old bug
4. Practice different scenarios of rebase and merge
5. Create your Git cheat sheet
```

**Git is a tool, not a goal. Choose a flow that works for your team, rather than blindly following rules.**
