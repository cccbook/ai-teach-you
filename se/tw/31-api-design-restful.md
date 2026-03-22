# 31. API 設計與 RESTful 原則

## RESTful 基礎

```
┌─────────────────────────────────────────────────────────┐
│                    REST 原则                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Resource-based（资源导向）                             │
│   └─ 用名词表示资源：/users, /orders, /products          │
│                                                         │
│   Stateless（无状态）                                   │
│   └─ 每个请求包含所有必要信息                           │
│                                                         │
│   Cacheable（可缓存）                                    │
│   └─ 合理使用缓存提升性能                               │
│                                                         │
│   Client-Server（客户端-服务端分离）                     │
│   └─ 客户端不关心服务端实现                             │
│                                                         │
│   Uniform Interface（统一接口）                         │
│   └─ 标准 HTTP 方法和状态码                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## HTTP 方法

```
┌─────────────────────────────────────────────────────────┐
│                   HTTP 方法对照                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   GET    /users        获取用户列表                      │
│   GET    /users/:id    获取单个用户                     │
│   POST   /users        创建用户                         │
│   PUT    /users/:id    完整更新用户                     │
│   PATCH  /users/:id    部分更新用户                     │
│   DELETE /users/:id    删除用户                         │
│                                                         │
│   GET    /users/:id/orders    获取用户的订单             │
│   POST   /users/:id/orders   创建用户的订单             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助 API 設計

### API 設計示例

```
你：
请帮我设计一个任务管理系统的 RESTful API。

AI：
## 任务管理系统 API

### 资源设计

```
用户 (Users)
├─ POST /users          注册
├─ GET /users/:id       获取用户信息
└─ PUT /users/:id       更新用户

项目 (Projects)
├─ GET /projects        列表
├─ POST /projects       创建
├─ GET /projects/:id    详情
├─ PUT /projects/:id    更新
└─ DELETE /projects/:id 删除

任务 (Tasks)
├─ GET /projects/:projectId/tasks    列表
├─ POST /projects/:projectId/tasks   创建
├─ GET /tasks/:id                     详情
├─ PUT /tasks/:id                     更新
└─ DELETE /tasks/:id                  删除
```

### API 详细设计

#### 用户相关
```yaml
# POST /users - 注册
Request:
  body:
    email: "user@example.com"
    password: "SecurePass123"
    name: "张三"

Response 201:
  body:
    id: "uuid"
    email: "user@example.com"
    name: "张三"
    createdAt: "2024-01-15T10:00:00Z"

# GET /users/:id
Response 200:
  body:
    id: "uuid"
    email: "user@example.com"
    name: "张三"
    avatar: "https://..."
    createdAt: "2024-01-15T10:00:00Z"
```

#### 项目相关
```yaml
# GET /projects
Query:
  page: 1
  limit: 20
  status: active
  sort: createdAt

Response 200:
  body:
    data:
      - id: "uuid"
        name: "项目A"
        description: "..."
        status: "active"
        memberCount: 5
    meta:
      total: 100
      page: 1
      limit: 20

# POST /projects
Request:
  body:
    name: "新项目"
    description: "项目描述"
    memberIds: ["uuid1", "uuid2"]

Response 201:
  body:
    id: "uuid"
    name: "新项目"
    ...
```

#### 任务相关
```yaml
# GET /projects/:projectId/tasks
Query:
  status: pending,in_progress
  assignee: userId
  priority: high
  dueDate: from:2024-01-01,to:2024-12-31

Response 200:
  body:
    data:
      - id: "uuid"
        title: "完成任务"
        status: "pending"
        priority: "high"
        dueDate: "2024-02-01"
        assignee:
          id: "uuid"
          name: "张三"
    meta:
      total: 50

# PATCH /tasks/:id - 更新任务
Request:
  body:
    status: "completed"
    completedAt: "2024-01-20T15:30:00Z"

Response 200:
  body:
    id: "uuid"
    title: "完成任务"
    status: "completed"
    completedAt: "2024-01-20T15:30:00Z"
    updatedAt: "2024-01-20T15:30:00Z"
```

### 错误响应
```yaml
Error 400:
  body:
    error:
      code: "VALIDATION_ERROR"
      message: "请求参数验证失败"
      details:
        - field: "email"
          message: "邮箱格式不正确"

Error 401:
  body:
    error:
      code: "UNAUTHORIZED"
      message: "请先登录"

Error 404:
  body:
    error:
      code: "NOT_FOUND"
      message: "任务不存在"

Error 500:
  body:
    error:
      code: "INTERNAL_ERROR"
      message: "服务器内部错误"
```
```

### 實作

```javascript
// Express 实现示例
const express = require('express');
const app = express();

// 项目列表
app.get('/projects', async (req, res) => {
  const { page = 1, limit = 20, status, sort = 'createdAt' } = req.query;
  
  const projects = await projectService.list({
    page: parseInt(page),
    limit: parseInt(limit),
    status,
    sort
  });
  
  res.json({
    data: projects.data,
    meta: {
      total: projects.total,
      page: parseInt(page),
      limit: parseInt(limit)
    }
  });
});

// 创建项目
app.post('/projects', async (req, res, next) => {
  try {
    const { name, description, memberIds } = req.body;
    
    // 验证
    if (!name || name.length < 2) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: '项目名称至少2个字符',
          details: [{ field: 'name' }]
        }
      });
    }
    
    const project = await projectService.create({
      name,
      description,
      memberIds
    });
    
    res.status(201).json(project);
  } catch (error) {
    next(error);
  }
});
```

## 版本控制

```
你：
API 如何做版本控制？

AI：
## API 版本控制

### 方式一：URL 路径（推荐）
```
GET /api/v1/users
GET /api/v2/users
```
简单直观，但破坏缓存

### 方式二：Header
```
GET /api/users
API-Version: 2024-01-01
```
不破坏 URL，但使用不便

### 方式三：Query 参数
```
GET /api/users?version=2
```
不推荐，污染 URL

### 实践建议
```javascript
// 使用路径版本
app.use('/api/v1', require('./routes/v1'));
app.use('/api/v2', require('./routes/v2'));

// 迁移策略
// v1 标记废弃
app.get('/api/v1/users', (req, res) => {
  res.set('Deprecation', 'true');
  res.set('Sunset', 'Sat, 31 Dec 2024 23:59:59 GMT');
  // 实际处理
});

// 同时保留新旧版本
app.get('/api/v2/users', async (req, res) => {
  const users = await getUsers();
  // 新的响应格式
  res.json({ data: users });
});
```
```

## 分頁

```
你：
API 分页如何设计？

AI：
## API 分页设计

### Offset 分页
```yaml
GET /users?page=2&limit=20

Response:
  data: [...]
  meta:
    page: 2
    limit: 20
    total: 1000
    totalPages: 50
```
简单但深分页效率低

### Cursor 分页（游标分页）
```yaml
GET /users?cursor=abc123&limit=20

Response:
  data: [...]
  meta:
    nextCursor: "def456"
    hasMore: true
```
适合大数据量，性能稳定

### Keyset 分页
```yaml
GET /users?since=2024-01-01&limit=20

Response:
  data: [...]
  pagination:
    nextSince: "2024-01-02"
```

### 实现示例
```javascript
// Cursor 分页
app.get('/posts', async (req, res) => {
  const { cursor, limit = 20 } = req.query;
  
  let query = db.posts.where('status', 'published');
  
  if (cursor) {
    const decoded = JSON.parse(atob(cursor));
    query = query.where('createdAt', '<', decoded.createdAt);
  }
  
  const posts = await query
    .orderBy('createdAt', 'desc')
    .limit(parseInt(limit) + 1);
  
  const hasMore = posts.length > parseInt(limit);
  const data = hasMore ? posts.slice(0, -1) : posts;
  
  const nextCursor = hasMore 
    ? btoa(JSON.stringify({ createdAt: data[data.length-1].createdAt }))
    : null;
  
  res.json({
    data,
    meta: {
      nextCursor,
      hasMore
    }
  });
});
```
```

## 認證與授權

```
你：
API 认证如何设计？

AI：
## API 认证

### 常见方式

| 方式 | 适用场景 | 安全性 |
|------|----------|--------|
| API Key | 服务间调用 | 中 |
| Basic Auth | 简单场景 | 低 |
| JWT | Web/Mobile API | 高 |
| OAuth 2.0 | 第三方登录 | 高 |

### JWT 实现
```javascript
// 登录获取 Token
app.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;
  
  const user = await authService.verify(email, password);
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  const token = jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );
  
  res.json({ token });
});

// 认证中间件
const authenticate = async (req, res, next) => {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' });
  }
  
  const token = authHeader.split(' ')[1];
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// 使用
app.get('/profile', authenticate, async (req, res) => {
  const user = await userService.getById(req.user.userId);
  res.json(user);
});
```

### 权限控制
```javascript
// RBAC 中间件
const authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
};

// 使用
app.delete('/users/:id', 
  authenticate,
  authorize('admin'),
  async (req, res) => {
    await userService.delete(req.params.id);
    res.status(204).send();
  }
);
```

## API 文件

```
你：
如何生成 API 文档？

AI：
## API 文档

### OpenAPI/Swagger 规范
```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: Task Management API
  version: 1.0.0

paths:
  /projects:
    get:
      summary: 获取项目列表
      tags: [Projects]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectList'
```

### 使用 Swagger UI
```javascript
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./openapi.json');

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
```

### 文档注释
```javascript
/**
 * @route POST /api/projects
 * @desc 创建新项目
 * @access Private
 * @param {string} name - 项目名称 (必填)
 * @param {string} description - 项目描述
 * @returns {Object} 创建的项目
 */
app.post('/api/projects', authenticate, async (req, res) => {
  // ...
});
```
```

## 實踐練習

```
1. 设计你的应用 API
2. 定义资源结构
3. 选择版本策略
4. 实现认证
5. 编写 OpenAPI 文档
6. 测试 API
```

**好的 API 設計是開發者體驗的基礎。投資時間在 API 設計上，回報是長期的可維護性和易用性。**
