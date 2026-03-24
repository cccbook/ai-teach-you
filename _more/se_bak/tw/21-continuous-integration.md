# 21. 持續整合的實踐

## CI/CD 是什麼

```
┌─────────────────────────────────────────────────────────┐
│                     CI/CD 概念                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   CI = Continuous Integration（持續整合）               │
│   每次代码变更自动构建、测试                             │
│                                                         │
│   CD = Continuous Delivery（持續交付）                  │
│   代码随时可部署到生产环境                               │
│                                                         │
│   CD = Continuous Deployment（持續部署）                │
│   代码自动部署到生产环境                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## CI 的核心價值

```
┌─────────────────────────────────────────────────────────┐
│                   CI 的价值                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   快速发现 Bug                                          │
│   ↓                                                     │
│   每次提交都跑测试，bug 藏不住                           │
│                                                         │
│   减少集成风险                                          │
│   ↓                                                     │
│   小步快跑，大幅降低集成难度                             │
│                                                         │
│   提高代码质量                                          │
│   ↓                                                     │
│   代码必须通过检查才能合并                               │
│                                                         │
│   增强信心                                              │
│   ↓                                                     │
│   随时可以部署上线                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助 CI 配置

### 基礎 CI 配置

```
你：
请帮我配置 GitHub Actions，实现：
1. PR 创建时运行测试
2. 测试通过才能合并
3. 自动运行 lint

AI：
## GitHub Actions 配置

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ESLint
        run: npm run lint

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run Tests
        run: npm test -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
```

### 分支保護規則

```
你：
请告诉我如何配置分支保护规则，要求：
1. PR 必须通过 CI 才能合并
2. 需要至少 1 人 review
3. 禁止强制推送

AI：
## GitHub 分支保护配置

### 路径：Settings → Branches → Add rule

### 规则配置：

**Branch name pattern:** `main`

☑ Protect matching branches
☑ Require a pull request before merging
  └─ Required approving reviewers: 1
☑ Require status checks to pass before merging
  └─ Select: `lint`, `test`, `build`
☑ Require linear history
☑ Do not allow bypassing the above settings

### 解释
1. 必须通过 PR 合并
2. 至少 1 人 review
3. 必须通过 lint、test、build
4. 禁止 force push
5. 强制线性历史（禁止 merge commit）
```

## 常見 CI 檢查

### 1. Lint

```
# ESLint 检查
npm run lint

# 类型检查
npm run typecheck

# 格式检查
npm run format:check
```

### 2. 測試

```
# 单元测试
npm test

# 集成测试
npm run test:integration

# E2E 测试
npm run test:e2e

# 测试覆盖率
npm test -- --coverage
```

### 3. 安全檢查

```
你：
请帮我配置 npm 安全检查。

AI：
## 安全检查配置

```yaml
# 在 CI 中添加
- name: Security audit
  run: npm audit --audit-level=high
```

### 常用安全工具

| 工具 | 用途 |
|------|------|
| npm audit | npm 依赖安全 |
| Snyk | 深度依赖分析 |
| SonarQube | 代码质量/安全 |
| Trivy | 容器镜像扫描 |
```

### 4. 构建

```
# 构建应用
npm run build

# 生成制品
npm run package
```

## 高級 CI 配置

### 矩陣構建

```
你：
请帮我配置多版本测试的 CI。

AI：
## 矩阵构建配置

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
        # 也可以加操作系统
        # os: [ubuntu-latest, windows-latest]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
```
```

### 快取優化

```
你：
请帮我配置依赖缓存。

AI：
## 依赖缓存配置

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # 自动缓存 node_modules

# 或者手动配置更细粒度的缓存
- name: Cache node_modules
  uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

### 並行作業

```
你：
如何加快 CI 速度？

AI：
## 加快 CI 的策略

### 1. 依赖缓存
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.npm
      .next/cache
```

### 2. 只测试变更的文件
```yaml
- name: Find changed files
  id: changed
  uses: tj-actions/changed-files@v34
  
- name: Run tests on changed files
  if: steps.changed.outputs.any_changed == 'true'
  run: |
    npm test -- ${{ steps.changed.outputs.all_changed_files }}
```

### 3. 并行执行独立任务
```yaml
jobs:
  lint:
    ...
  test-unit:
    ...
  test-integration:
    ...
  # 这些任务可以并行
```

### 4. 跳过不必要的运行
```yaml
# 在 commit message 中添加 [skip ci] 跳过 CI
git commit -m "[skip ci] update readme"
```
```

## 測試資料庫配置

```
你：
CI 中如何配置测试数据库？

AI：
## CI 测试数据库配置

### 方式一：GitHub 托管的数据库
```yaml
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432

steps:
  - name: Run tests
    env:
      DATABASE_URL: postgres://test:test@localhost:5432/test
    run: npm test
```

### 方式二：内存数据库
```yaml
# 对于 SQLite
- name: Setup SQLite
  run: |
    apt-get update
    apt-get install -y sqlite3

# 对于 MongoDB
- name: Setup MongoDB Memory Server
  run: npm install mongodb-memory-server
```

### 方式三：Docker 服务
```yaml
services:
  mysql:
    image: mysql:8
    env:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: test
    ports:
      - 3306:3306
    options: >-
      --health-cmd="mysqladmin ping"
      --health-interval=10s
      --health-timeout=5s
      --health-retries=5
```
```

## AI 輔助 Debug CI

```
你：
CI 失败了，请帮我分析：

```
Error: Cannot find module 'express'
Require stack:
  /home/user/project/src/app.js
```

AI：
## 错误分析

### 问题
找不到 'express' 模块

### 可能原因
1. `node_modules` 没有安装
2. `npm ci` 失败
3. 依赖版本冲突

### 排查步骤

1. 检查是否有 `npm ci` 步骤
```yaml
- name: Install dependencies
  run: npm ci  # 不要用 npm install
```

2. 检查是否有缓存问题
```yaml
- name: Clear cache
  run: rm -rf node_modules package-lock.json
```

3. 检查 package.json 是否包含 express
```json
{
  "dependencies": {
    "express": "^4.18.0"
  }
}
```

### 建议修复
```yaml
- name: Install dependencies
  run: npm ci
  
- name: Verify modules
  run: ls node_modules | grep express
```

### 常见原因
- 使用了 `npm install` 而不是 `npm ci`
- `npm install` 缓存不一致
- package-lock.json 和 package.json 不同步
```

## CI 最佳實踐

```
□ PR 创建时自动运行 CI
□ CI 失败阻止合并
□ CI 运行时间 < 10 分钟
□ 有测试覆盖率报告
□ 有构建产物
□ 使用缓存加速
□ 失败时提供清晰错误信息
□ 定期清理旧的构建记录
```

## 實踐練習

```
1. 为你的项目配置基础 CI
2. 添加测试覆盖率
3. 配置分支保护规则
4. 优化 CI 速度
5. 设置 CI 失败通知
```

**CI 是質量防線，也是團隊紀律。一個好的 CI 流程，讓你能放心大膽地重構。**
