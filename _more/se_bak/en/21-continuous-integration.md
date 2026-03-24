# 21. Continuous Integration Practices

## What is CI/CD

```
┌─────────────────────────────────────────────────────────┐
│                     CI/CD Concepts                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   CI = Continuous Integration                           │
│   Automatic build and test on every code change         │
│                                                         │
│   CD = Continuous Delivery                              │
│   Code always ready to deploy to production             │
│                                                         │
│   CD = Continuous Deployment                            │
│   Code automatically deployed to production             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Core Value of CI

```
┌─────────────────────────────────────────────────────────┐
│                     Value of CI                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Fast Bug Detection                                    │
│   ↓                                                     │
│   Tests run on every commit, bugs can't hide            │
│                                                         │
│   Reduced Integration Risk                              │
│   ↓                                                     │
│   Small frequent merges greatly reduce integration pain  │
│                                                         │
│   Improved Code Quality                                 │
│   ↓                                                     │
│   Code must pass checks before merging                   │
│                                                         │
│   Increased Confidence                                   │
│   ↓                                                     │
│   Ready to deploy anytime                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted CI Configuration

### Basic CI Configuration

```
You:
Please help me configure GitHub Actions with:
1. Run tests on PR creation
2. Tests must pass before merging
3. Automatically run lint

AI:
## GitHub Actions Configuration

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

### Branch Protection Rules

```
You:
Please tell me how to configure branch protection rules:
1. PR must pass CI before merging
2. At least 1 person needs to review
3. Disable force push

AI:
## GitHub Branch Protection Configuration

### Path: Settings → Branches → Add rule

### Rule Configuration:

**Branch name pattern:** `main`

☑ Protect matching branches
☑ Require a pull request before merging
   └─ Required approving reviewers: 1
☑ Require status checks to pass before merging
   └─ Select: `lint`, `test`, `build`
☑ Require linear history
☑ Do not allow bypassing the above settings

### Explanation
1. Must merge through PR
2. At least 1 reviewer
3. Must pass lint, test, build
4. No force push
5. Enforce linear history (no merge commits)
```

## Common CI Checks

### 1. Lint

```
# ESLint check
npm run lint

# Type check
npm run typecheck

# Format check
npm run format:check
```

### 2. Tests

```
# Unit tests
npm test

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# Test coverage
npm test -- --coverage
```

### 3. Security Checks

```
You:
Please help me configure npm security checks.

AI:
## Security Check Configuration

```yaml
# In CI, add
- name: Security audit
  run: npm audit --audit-level=high
```

### Common Security Tools

| Tool | Purpose |
|------|---------|
| npm audit | npm dependency security |
| Snyk | Deep dependency analysis |
| SonarQube | Code quality/security |
| Trivy | Container image scanning |
```

### 4. Build

```
# Build application
npm run build

# Generate artifacts
npm run package
```

## Advanced CI Configuration

### Matrix Build

```
You:
Please help me configure CI for multi-version testing.

AI:
## Matrix Build Configuration

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
        # Can also add OS
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

### Cache Optimization

```
You:
Please help me configure dependency caching.

AI:
## Dependency Cache Configuration

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # Auto-cache node_modules

# Or manually configure more granular cache
- name: Cache node_modules
  uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

### Parallel Jobs

```
You:
How to speed up CI?

AI:
## Strategies to Speed Up CI

### 1. Dependency caching
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.npm
      .next/cache
```

### 2. Only test changed files
```yaml
- name: Find changed files
  id: changed
  uses: tj-actions/changed-files@v34
  
- name: Run tests on changed files
  if: steps.changed.outputs.any_changed == 'true'
  run: |
    npm test -- ${{ steps.changed.outputs.all_changed_files }}
```

### 3. Run independent tasks in parallel
```yaml
jobs:
  lint:
    ...
  test-unit:
    ...
  test-integration:
    ...
  # These can run in parallel
```

### 4. Skip unnecessary runs
```yaml
# Add [skip ci] in commit message to skip CI
git commit -m "[skip ci] update readme"
```
```

## Test Database Configuration

```
You:
How to configure test database in CI?

AI:
## CI Test Database Configuration

### Method 1: GitHub-hosted database
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

### Method 2: In-memory database
```yaml
# For SQLite
- name: Setup SQLite
  run: |
    apt-get update
    apt-get install -y sqlite3

# For MongoDB
- name: Setup MongoDB Memory Server
  run: npm install mongodb-memory-server
```

### Method 3: Docker services
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

## AI-Assisted CI Debugging

```
You:
CI failed, please help me analyze:

```
Error: Cannot find module 'express'
Require stack:
  /home/user/project/src/app.js
```

AI:
## Error Analysis

### Problem
Cannot find 'express' module

### Possible Causes
1. `node_modules` not installed
2. `npm ci` failed
3. Dependency version conflict

### Troubleshooting Steps

1. Check if `npm ci` step exists
```yaml
- name: Install dependencies
  run: npm ci  # Don't use npm install
```

2. Check for cache issues
```yaml
- name: Clear cache
  run: rm -rf node_modules package-lock.json
```

3. Check if package.json includes express
```json
{
  "dependencies": {
    "express": "^4.18.0"
  }
}
```

### Suggested Fix
```yaml
- name: Install dependencies
  run: npm ci
  
- name: Verify modules
  run: ls node_modules | grep express
```

### Common Causes
- Used `npm install` instead of `npm ci`
- `npm install` cache inconsistency
- package-lock.json and package.json out of sync
```

## CI Best Practices

```
□ CI runs automatically on PR creation
□ CI failure blocks merging
□ CI run time < 10 minutes
□ Has test coverage report
□ Has build artifacts
□ Uses caching for speed
□ Provides clear error messages on failure
□ Regularly cleans old build records
```

## Practice Exercises

```
1. Configure basic CI for your project
2. Add test coverage
3. Configure branch protection rules
4. Optimize CI speed
5. Set up CI failure notifications
```

**CI is a quality firewall and team discipline. A good CI process lets you confidently refactor.**
