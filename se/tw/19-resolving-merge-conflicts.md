# 19. 合併衝突的解決藝術

## 合併衝突的真相

合併衝突不是失敗，而是機會——它提醒你需要整合不同人的工作。

```
┌─────────────────────────────────────────────────────────┐
│                   合并冲突的本质                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   分支 A         分支 B                                  │
│     │               │                                    │
│     ▼               ▼                                    │
│   修改了 X        修改了 X                               │
│     │               │                                    │
│     └───────┬───────┘                                    │
│             ▼                                            │
│        Git 无法自动合并                                  │
│        需要你做决定                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 衝突的常見類型

### 1. 文字衝突
兩個人修改了同一行的代碼

### 2. 檔案衝突
一個分支刪除文件，另一個分支修改了它

### 3. 目錄/檔案名衝突
創建了同名的不同文件

## AI 輔助衝突解決

### 理解衝突標記

```
你：
请解释这个冲突标记：

<<<<<<< HEAD
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
=======
function calculateTotal(items) {
  return items.reduce((sum, item) => {
    return sum + item.price * item.quantity;
  }, 0);
}
>>>>>>> feature/discount

AI：
## 冲突分析

### HEAD（你的分支）
简单的价格求和
```javascript
return items.reduce((sum, item) => 
  sum + item.price, 0);
```

### feature/discount（其他分支）
考虑数量
```javascript
return items.reduce((sum, item) => {
  return sum + item.price * item.quantity;
}, 0);
```

### 可能的解决方案

**方案 1：采用 HEAD（忽略数量）**
```javascript
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**方案 2：采用 feature/discount（包含数量）**
```javascript
function calculateTotal(items) {
  return items.reduce((sum, item) => {
    return sum + item.price * item.quantity;
  }, 0);
}
```

**方案 3：合并两者（如果两个逻辑都需要）**
```javascript
function calculateTotal(items) {
  return items.reduce((sum, item) => {
    const qty = item.quantity || 1;
    return sum + item.price * qty;
  }, 0);
}
```

### 建议
需要根据业务逻辑选择：
- 如果购物车必须考虑数量 → 方案 2
- 如果显示商品总价不需要数量 → 方案 1
```

### 解決衝突的步驟

```
你：
请告诉我解决 Git 冲突的标准步骤。

AI：
## Git 冲突解决步骤

### 1. 开始解决前
```bash
# 确保工作区干净
git status

# 查看有哪些文件冲突
git diff --name-only --diff-filter=U
```

### 2. 拉取最新代码
```bash
# 方式一：Rebase 冲突
git fetch origin
git rebase origin/main

# 方式二：Merge 冲突
git fetch origin
git merge origin/main
```

### 3. 编辑冲突文件
删除冲突标记，保留想要的内容

### 4. 标记冲突已解决
```bash
git add <resolved-file>
# 或全部添加
git add .
```

### 5. 完成重定基准/合并
```bash
# Rebase 场景
git rebase --continue

# Merge 场景
git commit  # Git 会打开编辑器
```

### 6. 验证
```bash
git status
npm test
```
```

## 常見衝突場景與解決

### 場景 1：簡單的文字衝突

```
<<<<<<< HEAD
const API_URL = 'https://api.example.com';
=======
const API_URL = 'https://staging.example.com';
>>>>>>> feature/config

✅ 解决：根据环境选择
// 开发环境
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://api.example.com'
  : 'https://staging.example.com';
```

### 場景 2：兩個新功能衝突

```
<<<<<<< HEAD
// 添加日志记录
console.log('User logged in');
auth.login(user);
=======
// 添加性能追踪
const start = Date.now();
auth.login(user);
console.log(`Login took ${Date.now() - start}ms`);
>>>>>>> feature/logging

✅ 解决：保留两个功能
const start = Date.now();
console.log('User logged in');
auth.login(user);
console.log(`Login took ${Date.now() - start}ms`);
```

### 場景 3：一個刪除，一個修改

```
<<<<<<< HEAD
// 文件已被删除
=======
// 文件被修改
export const config = { debug: true };
>>>>>>> feature/config

✅ 解决：根据业务决定
// 如果确实不需要 → 采用 HEAD
// 如果需要 → 从其他分支恢复并修改
```

### 場景 4：依賴衝突

```
<<<<<<< HEAD
"dependencies": {
  "lodash": "^4.17.21"
}
=======
"dependencies": {
  "lodash": "^4.17.20"
}
>>>>>>> feature/update

✅ 解决：选择新版本
"dependencies": {
  "lodash": "^4.17.21"
}
```

## 使用工具解決衝突

### 命令行工具

```
# 配置合并工具
git config merge.tool vimdiff

# 使用合并工具
git mergetool
```

### VS Code 衝突編輯器

VS Code 有內建的衝突編輯器：
- 點擊「Accept Current Change」
- 點擊「Accept Incoming Change」
- 點擊「Accept Both Changes」
- 手動編輯

### AI 輔助解決複雜衝突

```
你：
这个冲突比较复杂，请帮我分析：

<<<<<<< HEAD
class UserService {
  async createUser(data) {
    const user = await this.db.users.create(data);
    await this.sendWelcomeEmail(user);
    return user;
  }
  
  async getUser(id) {
    return this.db.users.findById(id);
  }
}
=======
class UserService {
  async createUser(data) {
    const user = await this.db.users.create({
      ...data,
      createdAt: new Date()
    });
    return user;
  }
  
  async deleteUser(id) {
    await this.db.users.delete(id);
    await this.sendDeletionNotice(id);
  }
}
>>>>>>> feature/user-crud

AI：
## 冲突分析

### 冲突点
两个分支都修改了 `createUser` 方法

### HEAD 的改动
- 添加了 `sendWelcomeEmail` 邮件通知

### feature 的改动
- 添加了 `createdAt` 时间戳
- 移除了邮件通知

### 解决方案

**推荐：合并两者**
```javascript
class UserService {
  async createUser(data) {
    const user = await this.db.users.create({
      ...data,
      createdAt: new Date()
    });
    await this.sendWelcomeEmail(user);
    return user;
  }
  
  async getUser(id) {
    return this.db.users.findById(id);
  }
  
  async deleteUser(id) {
    await this.db.users.delete(id);
    await this.sendDeletionNotice(id);
  }
}
```

**理由**
- 保留了 `createdAt` 字段（有用）
- 保留了邮件通知（用户反馈）
- 添加了新方法 `deleteUser`（功能增强）
```

## 預防衝突的策略

### 1. 頻繁同步

```
# 每天开始工作前
git fetch origin
git rebase origin/main

# 或使用 pull with rebase
git pull --rebase origin main
```

### 2. 小而頻繁的提交

```
❌ 不好：一个月的工作一次性提交
✅ 好：每天提交，频繁合并
```

### 3. 良好代碼組織

```
❌ 不好：多人修改同一个文件同一区域
✅ 好：模块化，减少文件冲突

// 拆分服务
user.service.ts
order.service.ts
product.service.ts
```

### 4. 使用 Feature Branch

```
避免直接在 main 开发
每个功能/修复使用独立分支
```

### 5. 溝通

```
重大重构前通知团队
约定修改范围
错开修改同一文件
```

## 衝突解決後的驗證

```
你：
冲突解决后应该验证什么？

AI：
## 冲突解决后的检查清单

### 1. 功能验证
- 运行测试：`npm test`
- 手动测试关键流程
- 检查是否有回归问题

### 2. 代码检查
```bash
# 检查冲突标记是否全部清除
git diff --check

# 查看合并后的差异
git diff main...HEAD
```

### 3. 构建验证
```bash
npm run build
```

### 4. 特殊检查
- 如果修改了 API：测试 API 端点
- 如果修改了数据库：检查迁移
- 如果修改了配置：验证配置加载
```

## 實踐練習

```
1. 创建一个测试仓库
2. 创建两个分支，分别修改同一文件
3. 尝试合并，观察冲突
4. 练习解决各种类型的冲突
5. 练习使用 Git mergetool
6. 练习使用 VS Code 冲突编辑器
```

## 衝突解決的心態

```
┌─────────────────────────────────────────────────────────┐
│                 解决冲突的正确心态                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 不要恐慌                                            │
│     冲突是正常的，Git 会帮你标记问题                      │
│                                                         │
│  2. 理解优先                                            │
│     先理解两边改了什么，再决定保留什么                    │
│                                                         │
│  3. 不要随意删除代码                                    │
│     如果不确定，可以问团队成员                           │
│                                                         │
│  4. 保持代码质量                                        │
│     合并后的代码应该比合并前更好                         │
│                                                         │
│  5. 测试为王                                            │
│     解决冲突后一定要测试                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**衝突解決是每個工程師必須掌握的核心技能。練習得越多，處理起來就越從容。**
