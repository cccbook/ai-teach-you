# 18. 程式碼審查流程

## Pull Request 的生命週期

```
┌─────────────────────────────────────────────────────────┐
│                   Pull Request 流程                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   创建分支 ──→ 开发 ──→ 提交 PR ──→ 审查 ──→ 合并      │
│       ↑                                    │            │
│       └────────────────────────────────────┘            │
│                   (可能需要修改)                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 撰寫好的 PR 描述

### PR 描述模板

讓 AI 幫你生成模板：

```
你：
请帮我生成一个 PR 描述模板

AI：
## PR 描述模板

```markdown
## 摘要
简要说明这个 PR 做了什么。

## 动机
为什么需要这个变更？
解决了什么问题？

## 变更内容
- [ ] 新增功能 X
- [ ] 修改功能 Y
- [ ] 修复 bug Z

## 技术细节
重要的实现细节，方便 reviewer 理解。

## 测试
- [ ] 单元测试
- [ ] 集成测试
- [ ] E2E 测试

## 截图/录屏
（如有 UI 变更）

## 相关 Issue
Closes #123
```

### 實際示例

```
## 摘要
实现用户头像上传功能，支持裁剪和压缩。

## 动机
用户反馈希望有自定义头像功能。
Issue: #234

## 变更内容
- 新增头像上传 API
- 新增图片裁剪组件
- 新增图片压缩工具
- 集成 AWS S3 存储

## 技术细节
- 使用 Sharp 进行图片处理
- 头像限制 200KB，尺寸 200x200
- 使用 Presigned URL 避免暴露凭证

## 测试
- [x] 单元测试（上传服务）
- [x] 集成测试（完整流程）
- [ ] E2E 测试（将在下个 PR 添加）
```

## 讓 AI 幫你撰寫 PR

```
你：
请帮我用英文写一个清晰的 PR 描述：

功能：实现了用户登录的「记住我」功能
实现：
- 添加 remember_token 字段到 users 表
- 登录时如果勾选「记住我」，生成 30 天有效期的 token
- 每次访问自动续期 token

AI：
## PR: Add "Remember Me" functionality

### Summary
Implemented persistent login with "Remember Me" option for enhanced user experience.

### Changes
- Added `remember_token` column to users table
- Generate 30-day token when "Remember Me" is checked
- Auto-extend token on each authenticated request
- Updated login/logout flows

### Technical Details
- Token stored as secure HTTP-only cookie
- Token rotation on each use (security best practice)
- Cleanup expired tokens on login

### Testing
- [x] Unit tests for token generation/validation
- [x] Integration test for login flow
- [x] Manual testing on staging

### Screenshots
[Login form with "Remember Me" checkbox]
```

## PR 審查清單

### 作為 Reviewer

```
┌─────────────────────────────────────────────────────────┐
│                  PR 审查清单                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  功能性                                                 │
│  □ 代码逻辑正确吗？                                     │
│  □ 所有边界情况处理了吗？                               │
│  □ 是否有安全风险？                                     │
│                                                         │
│  测试                                                   │
│  □ 有测试吗？                                          │
│  □ 测试覆盖足够吗？                                     │
│  □ 测试能通过吗？                                       │
│                                                         │
│  代码质量                                               │
│  □ 代码清晰易懂吗？                                     │
│  □ 变量/函数命名合适吗？                                │
│  □ 有重复代码吗？                                       │
│  □ 有注释吗？（该有的地方有，不该有的地方没有）          │
│                                                         │
│  集成                                                   │
│  □ 与现有代码风格一致吗？                               │
│  □ 不会破坏其他功能吗？                                 │
│  □ 文档更新了吗？                                       │
│                                                         │
│  性能                                                   │
│  □ 有性能问题吗？                                       │
│  □ 数据库查询优化了吗？                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 讓 AI 幫你做 Code Review

```
你：
请作为代码审查者，审查这个 PR：

变更内容：添加用户头像上传功能
代码：[代码]

请重点关注：
1. 安全性
2. 性能
3. 错误处理

AI：
## PR Review

### 整体评价
功能完整，实现合理。建议修改以下问题后合并。

---

### 🔴 必须修复 (Blocking)

**1. 缺少文件类型验证 (安全)**
```javascript
// 当前：接受任何文件
const upload = await s3.upload(params).promise();

// 建议：验证文件类型
const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
if (!allowedTypes.includes(file.mimetype)) {
  throw new Error('Invalid file type');
}
```

**2. 缺少文件大小限制 (DoS 风险)**
```javascript
// 建议：限制文件大小
const MAX_SIZE = 5 * 1024 * 1024; // 5MB
if (file.size > MAX_SIZE) {
  throw new Error('File too large');
}
```

---

### 🟡 建议修复 (Non-blocking)

**3. 缺少错误处理**
```javascript
// 当前：直接上传
const upload = await s3.upload(params).promise();

// 建议：添加错误处理
try {
  const upload = await s3.upload(params).promise();
} catch (error) {
  logger.error('S3 upload failed', error);
  throw new Error('Failed to upload image');
}
```

**4. S3 路径可预测**
当前路径：`avatars/{userId}.jpg`
建议：添加随机前缀防止路径猜测

---

### 🟢 做得好的地方

- 使用了 async/await ✅
- 参数验证清晰 ✅
- 代码结构良好 ✅

---

### 总结
修复安全相关问题后可以合并。
建议：添加单元测试覆盖边界情况。
```

## 提供有效的回饋

### 反饋的藝術

```
❌ 不好的反馈：
「这段代码不好」

✅ 好的反馈：
「这个实现可能导致 N+1 查询问题。建议使用 eager loading：
```javascript
const users = await User.findAll({
  include: [{ model: Post }]  // 一次查询
});
```」

理由：
1. 指出具体问题
2. 解释原因
3. 提供解决方案
4. 给出代码示例
```

### 反饋模板

```
## 代码审查反馈

### 🔴 问题：[标题]
**位置：** `src/path/file.ts:45`

**问题：** [描述]

**建议：** [解决方案]

---

### 🟡 建议：[标题]
**位置：** 同上

**建议：** [改进建议]
（如有时间）

---

### ✅ 做得好的
- [列举做得好的地方]
```

### 回覆反饋

作為 PR 作者，如何回覆 reviewer 的反饋：

```
你：
请帮我写一个回复给 reviewer：

reviewer 指出：缺少文件类型验证

AI：
## 回复模板

### 回复示例 1 - 接受反馈
```
[@reviewer] 说得对，这是个安全漏洞。
已添加文件类型验证：
commit abc123

请重新 review。
```

### 回复示例 2 - 解释决策
```
[@reviewer] 关于这个建议：

我的考虑是这样的：[你的理由]

如果你觉得仍然需要修改，请告诉我，我们可以讨论。
```

### 回复示例 3 - 提出问题
```
[@reviewer] 好问题！

我目前的理解是：[你的理解]

但是可能我没有考虑到 [reviewer 提出的点]。

你认为应该怎么处理？
```
```

## PR 自動化

### CI/CD 配置

讓 AI 幫你配置 PR 自動化：

```
你：
请帮我配置 GitHub Actions，要求：
1. PR 创建时运行测试
2. 测试通过才能合并
3. 自动运行 lint

AI：
## GitHub Actions 配置

```yaml
# .github/workflows/pr-check.yml
name: PR Check

on:
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run Lint
        run: npm run lint

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run Tests
        run: npm test

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
```

## 實踐練習

```
1. 创建一个完整的 PR，包含详细的描述
2. 用 AI 帮你审查自己的 PR
3. 练习写不同类型的反馈
4. 配置一个 PR 模板
5. 设置 CI 自动检查
```

**好的 PR 不僅是為了通過審查，更是為了知識傳遞和代碼品質的把關。**
