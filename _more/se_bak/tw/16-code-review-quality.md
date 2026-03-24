# 16. 程式碼審查與品質把關

## 程式碼審查的價值

```
┌─────────────────────────────────────────────────────┐
│              代码审查 (Code Review)                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│   捕获 Bug      知识共享      代码质量      团队一致  │
│      ↓              ↓             ↓            ↓    │
│   ────────────────────────────────────────────────  │
│                                                     │
│   代码审查不只是找 Bug，还包括：                      │
│   • 逻辑正确性                                       │
│   • 安全性                                           │
│   • 性能                                             │
│   • 可维护性                                         │
│   • 代码风格一致性                                   │
│   • 测试覆盖                                         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## AI 輔助程式碼審查

### 常規審查清單

讓 AI 幫你創建審查清單：

```
你：
请为 [你的技术栈] 项目创建代码审查清单

AI：
## 代码审查清单

### 通用检查
□ 代码逻辑是否正确？
□ 边界情况是否处理？
□ 是否有明显的错误？
□ 代码是否清晰易懂？

### 功能检查
□ 功能是否符合需求？
□ 测试覆盖是否足够？
□ 错误处理是否完善？

### 性能检查
□ 是否有性能问题？
□ 数据库查询是否优化？
□ 是否有 N+1 查询问题？

### 安全检查
□ 是否有注入风险？
□ 敏感数据是否加密？
□ 权限控制是否正确？
□ 依赖是否安全？

### 代码风格
□ 是否符合项目规范？
□ 命名是否清晰？
□ 注释是否必要？
□ 是否重复造轮子？
```

### AI 審查示例

```
你：
请审查这段代码：

```javascript
async function createUser(req, res) {
  const { name, email, password } = req.body;
  
  // 简单验证
  if (!name || !email || !password) {
    return res.status(400).send('Missing fields');
  }
  
  // 创建用户
  const user = await User.create({ name, email, password });
  
  res.json(user);
}
```

AI：
## 代码审查

### 🔴 问题

**1. 密码明文存储 (严重安全漏洞)**
密码直接存入数据库，没有加密。
```javascript
// 应该
const hashedPassword = await bcrypt.hash(password, 10);
const user = await User.create({ name, email, password: hashedPassword });
```

**2. 邮箱格式未验证**
```javascript
// 建议
if (!isValidEmail(email)) {
  return res.status(400).json({ error: 'Invalid email format' });
}
```

**3. 邮箱重复未检查**
用户表中 email 应唯一。

### 🟡 改进建议

**4. 密码强度检查**
```javascript
if (password.length < 8) {
  return res.status(400).json({ error: 'Password too weak' });
}
```

**5. 错误处理改进**
```javascript
// 当前：所有错误都返回 500
// 建议：区分不同错误类型
try {
  const existingUser = await User.findOne({ email });
  if (existingUser) {
    return res.status(409).json({ error: 'Email already exists' });
  }
} catch (dbError) {
  // 记录数据库错误
  logger.error(dbError);
  return res.status(500).json({ error: 'Database error' });
}
```

### 🟢 做得好的地方

- 使用 async/await ✅
- 参数解构 ✅
- 返回适当的 HTTP 状态码 ✅
```

## 審查不同類型的代碼

### 1. API 代碼審查

```
你：
请审查这个 Express API：

```javascript
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);
});
```

AI：
## API 代码审查

### 🔴 严重问题

**1. 缺少权限检查**
任何人都可以查看任何用户信息。
```javascript
// 应该验证当前用户是否有权限
async function getUser(req, res) {
  const currentUser = await authMiddleware(req);
  const requestedId = req.params.id;
  
  if (currentUser.id !== requestedId && !currentUser.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  const user = await User.findById(requestedId);
  res.json(user);
}
```

**2. 未检查用户是否存在**
当用户不存在时，`findById` 返回 `null`，`res.json(null)` 不是好的处理方式。

**3. 缺少错误处理**
数据库错误会导致未捕获的 Promise rejection。

### 🟡 建议

**4. 字段选择**
```javascript
// 不要返回敏感字段
const user = await User.findById(id).select('-password -token');
```

**5. 响应缓存**
考虑对公开数据添加缓存。

### ✅ 正确做法
```javascript
app.get('/api/users/:id', 
  authenticate,
  checkPermission,
  async (req, res) => {
    try {
      const user = await User.findById(req.params.id)
        .select('-password -token');
      
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      
      res.json(user);
    } catch (error) {
      logger.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
);
```
```

### 2. 前端代碼審查

```
你：
请审查这个 React 组件：

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => setUser(data));
  }, []);
  
  return <div>{user.name}</div>;
}
```

AI：
## React 代码审查

### 🔴 严重问题

**1. 依赖数组为空**
`userId` 变化时不会重新获取数据。
```javascript
useEffect(() => {
  fetch(`/api/users/${userId}`)
    .then(res => res.json())
    .then(data => setUser(data));
}, [userId]); // 添加 userId
```

**2. 缺少加载状态**
用户为 null 时直接访问 `.name` 会报错。
```jsx
if (!user) return <Loading />;
```

**3. 缺少错误处理**
网络错误时没有处理。

**4. 缺少 Key（在父组件）**
如果这是列表项，需要提供 key。

### 🟡 建议

**5. 使用 useCallback/useMemo 优化**

**6. 考虑数据获取库**
```jsx
function UserProfile({ userId }) {
  const { data: user, loading, error } = useSWR(
    `/api/users/${userId}`,
    fetcher
  );
  
  if (loading) return <Loading />;
  if (error) return <Error error={error} />;
  if (!user) return null;
  
  return <div>{user.name}</div>;
}
```

### ✅ 改进后的代码
```jsx
function UserProfile({ userId }) {
  const { data: user, loading, error } = useSWR(
    userId ? `/api/users/${userId}` : null,
    fetcher
  );
  
  if (loading) return <LoadingSkeleton />;
  if (error) return <ErrorPage message={error.message} />;
  
  return <div>{user.name}</div>;
}
```
```

## AI 審查的最佳實踐

### 1. 分解審查

```
❌ 一次審查太多代碼
✅ 分批審查，每次關注一個方面
```

### 2. 明確審查目標

```
你：
请审查这段代码的安全性，不要关注其他方面。

你：
请审查这段代码的性能问题。
```

### 3. 迭代式審查

```
第一轮：整体逻辑
第二轮：安全检查
第三轮：性能优化
第四轮：代码风格
```

## 建立團隊審查標準

### 審查等級

```
P0 - 必须修复（阻塞）
├─ 安全漏洞
├─ 数据丢失风险
└─ 明显的 Bug

P1 - 强烈建议修复
├─ 性能问题
├─ 边界情况遗漏
└─ 测试不足

P2 - 建议改进（可选）
├─ 代码风格
├─ 注释改进
└─ 小优化
```

### 讓 AI 幫你生成團隊審查指南

```
你：
请帮我生成一个代码审查指南模板，
包含：审查标准、审查流程、反馈模板

AI：
## 代码审查指南

### 审查标准

**必须通过**
- [ ] 功能正确
- [ ] 通过所有测试
- [ ] 无安全漏洞
- [ ] 错误处理完善

**强烈建议**
- [ ] 测试覆盖
- [ ] 性能达标
- [ ] 文档完整

**建议改进**
- [ ] 代码风格
- [ ] 注释清晰

### 审查流程

1. 作者提交 PR
2. 自动检查（CI）通过
3. 至少 1 人 Review
4. 所有 P0 问题解决
5. 合并

### 反馈模板

```
## 代码审查反馈

### 🔴 P0 - 必须修复
[具体问题和修改建议]

### 🟡 P1 - 建议修复
[建议]

### 🟢 P2 - 可选改进
[可选建议]

### ✅ 做得好的地方
[肯定的点]
```
```

## 實踐練習

```
1. 找一个最近的代码变更
2. 用 AI 审查（分多轮）
3. 整理发现的问题
4. 评估问题的严重程度
5. 修复问题
6. 对比修复前后的差异
```

**好的代碼審查不在於找出最多的問題，而在於找出重要的問題並推動改進。**
