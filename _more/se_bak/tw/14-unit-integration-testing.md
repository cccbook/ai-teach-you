# 14. 單元測試與整合測試

## 測試的兩層護盾

```
┌─────────────────────────────────────────┐
│                                         │
│   单元测试          整合测试            │
│   (Unit Tests)     (Integration Tests) │
│                                         │
│   快速执行          较慢执行            │
│   隔离测试          组件协作            │
│   细节覆盖          路径覆盖            │
│                                         │
└─────────────────────────────────────────┘
```

## 單元測試

### 單元測試的原則 (FIRST)

```
F - Fast（快速）
  测试应该在毫秒级完成

I - Independent（独立）
  每个测试不应该依赖其他测试

R - Repeatable（可重复）
  无论何时运行，结果应该一致

S - Self-validating（自验证）
  测试应该能自动判断通过/失败

T - Timely（及时）
  应该在代码写完后立即写测试
```

### 好的單元測試示例

```
你：
请为这个购物车类写单元测试：

```javascript
class ShoppingCart {
  constructor() {
    this.items = [];
  }
  
  addItem(product, quantity = 1) {
    const existing = this.items.find(i => i.product.id === product.id);
    if (existing) {
      existing.quantity += quantity;
    } else {
      this.items.push({ product, quantity });
    }
  }
  
  removeItem(productId) {
    this.items = this.items.filter(i => i.product.id !== productId);
  }
  
  getTotal() {
    return this.items.reduce((sum, item) => 
      sum + item.product.price * item.quantity, 0
    );
  }
  
  getItemCount() {
    return this.items.reduce((sum, item) => sum + item.quantity, 0);
  }
}
```

AI：
## 单元测试

```javascript
describe('ShoppingCart', () => {
  let cart;
  let mockProduct;
  
  beforeEach(() => {
    cart = new ShoppingCart();
    mockProduct = { id: 'p1', name: '产品A', price: 100 };
  });
  
  describe('addItem', () => {
    test('添加新商品', () => {
      cart.addItem(mockProduct);
      expect(cart.items).toHaveLength(1);
      expect(cart.items[0].quantity).toBe(1);
    });
    
    test('添加已有商品增加数量', () => {
      cart.addItem(mockProduct);
      cart.addItem(mockProduct);
      expect(cart.items).toHaveLength(1);
      expect(cart.items[0].quantity).toBe(2);
    });
    
    test('自定义数量', () => {
      cart.addItem(mockProduct, 5);
      expect(cart.items[0].quantity).toBe(5);
    });
  });
  
  describe('removeItem', () => {
    test('删除存在的商品', () => {
      cart.addItem(mockProduct);
      cart.removeItem('p1');
      expect(cart.items).toHaveLength(0);
    });
    
    test('删除不存在的商品不报错', () => {
      expect(() => cart.removeItem('non-existent')).not.toThrow();
    });
  });
  
  describe('getTotal', () => {
    test('空购物车总价', () => {
      expect(cart.getTotal()).toBe(0);
    });
    
    test('单个商品总价', () => {
      cart.addItem(mockProduct, 2);
      expect(cart.getTotal()).toBe(200);
    });
    
    test('多个商品总价', () => {
      cart.addItem(mockProduct, 2);
      cart.addItem({ id: 'p2', price: 50 }, 3);
      expect(cart.getTotal()).toBe(350);
    });
  });
  
  describe('getItemCount', () => {
    test('空购物车数量', () => {
      expect(cart.getItemCount()).toBe(0);
    });
    
    test('商品总数量', () => {
      cart.addItem(mockProduct, 3);
      cart.addItem({ id: 'p2', price: 50 }, 2);
      expect(cart.getItemCount()).toBe(5);
    });
  });
});
```
```

### Mock 和 Stub

AI 幫你理解什麼時候用 Mock：

```
你：
单元测试中 mock 和 stub 的区别是什么？

AI：
## Mock vs Stub

### Stub（桩）
预先设置好的假数据，用于绕过依赖
```javascript
const stubDb = {
  findUser: () => ({ id: 1, name: 'Test' })
};
```

### Mock（模拟对象）
验证交互行为，记录调用次数、参数等
```javascript
const mockMailer = {
  send: jest.fn()
};

userService.sendWelcomeEmail('test@example.com');
expect(mockMailer.send).toHaveBeenCalledWith(
  'test@example.com',
  expect.stringContaining('欢迎')
);
```

### 使用场景
- Stub：当你需要数据，但不想真的查数据库
- Mock：当你需要验证对象之间的交互
```

## 整合測試

### 整合測試的範圍

```
┌─────────────────────────────────────┐
│           整合测试范围                │
├─────────────────────────────────────┤
│                                     │
│   模块A ──→ 模块B ──→ 模块C         │
│      ↑                    ↑         │
│      └────────────────────┘         │
│              ↓                     │
│         数据库                      │
│                                     │
└─────────────────────────────────────┘

整合测试：测试多个模块协作
单元测试：测试单个模块（mock 外部依赖）
```

### 數據庫整合測試

```
你：
请写一个使用真实数据库的集成测试：

```javascript
// app.js
const db = require('./db');
const userService = require('./userService');

async function createUser(name, email) {
  const existing = await db.users.findOne({ email });
  if (existing) {
    throw new Error('Email already exists');
  }
  return userService.createUser({ name, email });
}
```

AI：
## 数据库集成测试

```javascript
const { MongoMemoryServer } = require('mongodb-memory-server');
const mongoose = require('mongoose');
const app = require('./app');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  const uri = mongoServer.getUri();
  await mongoose.connect(uri);
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

beforeEach(async () => {
  await mongoose.connection.dropDatabase();
});

describe('createUser', () => {
  test('成功创建用户', async () => {
    const user = await createUser('张三', 'zhang@example.com');
    
    expect(user.name).toBe('张三');
    expect(user.email).toBe('zhang@example.com');
    expect(user.id).toBeDefined();
  });
  
  test('重复邮箱报错', async () => {
    await createUser('张三', 'zhang@example.com');
    
    await expect(
      createUser('李四', 'zhang@example.com')
    ).rejects.toThrow('Email already exists');
  });
  
  test('用户被正确保存到数据库', async () => {
    await createUser('张三', 'zhang@example.com');
    
    const saved = await mongoose.connection
      .collection('users')
      .findOne({ email: 'zhang@example.com' });
    
    expect(saved.name).toBe('张三');
  });
});
```
```

### API 整合測試

```
你：
请为这个 Express API 写集成测试：

app.post('/api/orders', async (req, res) => {
  const { userId, items } = req.body;
  
  // 验证用户存在
  const user = await db.users.findById(userId);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  // 创建订单
  const order = await db.orders.create({
    userId,
    items,
    total: items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    status: 'pending'
  });
  
  res.json(order);
});

AI：
## API 集成测试

```javascript
const request = require('supertest');
const { MongoMemoryServer } = require('mongodb-memory-server');
const mongoose = require('mongoose');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  await mongoose.connect(mongoServer.getUri());
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

beforeEach(async () => {
  await mongoose.connection.dropDatabase();
});

describe('POST /api/orders', () => {
  test('成功创建订单', async () => {
    // 先创建用户
    const user = await mongoose.connection
      .collection('users')
      .insertOne({ name: '张三', email: 'zhang@example.com' });
    
    const res = await request(app)
      .post('/api/orders')
      .send({
        userId: user.insertedId.toString(),
        items: [{ id: 'p1', price: 100, quantity: 2 }]
      });
    
    expect(res.status).toBe(200);
    expect(res.body.total).toBe(200);
    expect(res.body.status).toBe('pending');
  });
  
  test('用户不存在返回 404', async () => {
    const fakeId = new mongoose.Types.ObjectId();
    
    const res = await request(app)
      .post('/api/orders')
      .send({
        userId: fakeId.toString(),
        items: [{ id: 'p1', price: 100, quantity: 1 }]
      });
    
    expect(res.status).toBe(404);
    expect(res.body.error).toBe('User not found');
  });
  
  test('缺少必填字段返回 400', async () => {
    const res = await request(app)
      .post('/api/orders')
      .send({});
    
    expect(res.status).toBe(400);
  });
});
```
```

## 測試數據的設置

### Test Fixtures

```
你：
请用 fixture 模式重构这个测试的数据设置：

```javascript
beforeEach(async () => {
  await db.users.deleteMany({});
  await db.users.insertOne({ name: '张三', email: 'zhang@example.com', role: 'admin' });
  await db.users.insertOne({ name: '李四', email: 'li@example.com', role: 'user' });
  await db.products.insertOne({ name: '产品A', price: 100 });
  await db.products.insertOne({ name: '产品B', price: 200 });
});
```

AI：
## Fixture 模式

```javascript
const testData = {
  users: [
    { _id: 'user1', name: '张三', email: 'zhang@example.com', role: 'admin' },
    { _id: 'user2', name: '李四', email: 'li@example.com', role: 'user' }
  ],
  products: [
    { _id: 'product1', name: '产品A', price: 100 },
    { _id: 'product2', name: '产品B', price: 200 }
  ]
};

async function loadFixtures() {
  await db.users.deleteMany({});
  await db.products.deleteMany({});
  await db.users.insertMany(testData.users);
  await db.products.insertMany(testData.products);
}

beforeEach(loadFixtures);

// 或者使用 object-factory 模式
function createUser(overrides = {}) {
  return {
    name: '测试用户',
    email: 'test@example.com',
    role: 'user',
    ...overrides
  };
}

test('管理员可以删除用户', async () => {
  const admin = createUser({ role: 'admin' });
  await db.users.insertOne(admin);
  
  const res = await request(app)
    .delete(`/api/users/${admin._id}`)
    .set('Authorization', `Bearer ${admin.token}`);
  
  expect(res.status).toBe(204);
});
```
```

## 測試覆蓋率

```
你：
请解释测试覆盖率指标的含义，以及如何解读：

AI：
## 测试覆盖率指标

### 语句覆盖率 (Statement Coverage)
- 执行了多少语句
- 目标：> 80%

### 分支覆盖率 (Branch Coverage)
- 每个条件分支至少执行一次
- 目标：> 75%

### 函数覆盖率 (Function Coverage)
- 每个函数至少调用一次
- 目标：100%

### 行覆盖率 (Line Coverage)
- 多少行代码被执行
- 目标：> 80%

### 注意事项
⚠️ 高覆盖率 ≠ 高质量测试
⚠️ 100% 覆盖率可能隐藏逻辑错误
⚠️ 关注关键路径的覆盖
```

## 實踐練習

```
1. 选择一个业务模块
2. 写单元测试覆盖核心逻辑
3. 写集成测试覆盖 API 端点
4. 生成覆盖率报告
5. 找出未覆盖的边界情况
6. 补充测试直到满意
```

**好測試的標準：快速、可靠、易維護、能發現問題。**
