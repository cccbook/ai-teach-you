# 13. AI 輔助的測試策略

## 測試是軟體品質的基石

沒有測試的代碼就像沒有安全網的高空走鋼絲——也許能走過去，但一旦失足，就是災難。

## AI 對測試的影響

### 傳統測試的痛點
- 寫測試耗時費力
- 容易遺漏邊界情況
- 測試維護成本高

### AI 帶來的改變
- 快速生成測試用例
- 識別潛在的邊界情況
- 幫助理解測試失敗原因

**但 AI 不能取代你對業務邏輯的理解。**

## 測試金字塔

```
           ▲
          /E\        E = End-to-End (少量)
         /2E \
        /─────\
       / I    \      I = Integration (适量)
      /───I────\
     / I    I   \
    /─────────────\
   /   Unit Tests   \    U = Unit Tests (大量)
  /───────────────────\
 /______________________\
```

## AI 生成單元測試

### 基本模式

```
你：
请为这个函数生成单元测试：

```javascript
function add(a, b) {
  return a + b;
}
```

AI：
## 单元测试

```javascript
// 基本功能测试
test('add(1, 2) returns 3', () => {
  expect(add(1, 2)).toBe(3);
});

// 边界测试
test('add(0, 0) returns 0', () => {
  expect(add(0, 0)).toBe(0);
});

test('add(-1, 1) returns 0', () => {
  expect(add(-1, 1)).toBe(0);
});

// 类型测试
test('add("1", "2") returns "12" (string concatenation)', () => {
  expect(add("1", "2")).toBe("12");
});
```

## 提示：AI 可能遗漏的业务逻辑测试

你必须补充：
```javascript
test('金额计算时保留两位小数', () => {
  expect(add(0.1, 0.2)).toBeCloseTo(0.3);
});
```
```

### 測試邊界情況

讓 AI 幫你想邊界情況：

```
你：
请为这个函数列出所有可能的边界情况：

```javascript
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

AI：
## 边界情况

| 情况 | 期望结果 | 原因 |
|------|---------|------|
| "test@example.com" | true | 标准邮箱 |
| "" | false | 空字符串 |
| "test@" | false | 缺少域名 |
| "@example.com" | false | 缺少用户名 |
| "test@example" | false | 缺少 TLD |
| "test@.com" | false | 域名格式错误 |
| "test @example.com" | false | 包含空格 |
| "test@example..com" | false | 双点 |
| "test+tag@example.com" | true | 加号别名 |
| "a@b.co" | true | 最短有效格式 |
| 12345 | false | 非字符串 |
| null | false | null 值 |
| undefined | false | undefined 值 |
```

## AI 生成整合測試

### API 整合測試

```
你：
请为这个 REST API 生成集成测试：

POST /api/users
{
  "name": "string",
  "email": "string"
}

需要测试：
1. 成功创建用户
2. 邮箱格式错误
3. 邮箱已存在
4. 缺少必填字段

AI：
## 集成测试

```javascript
const request = require('supertest');
const app = require('../app');
const db = require('../db');

describe('POST /api/users', () => {
  beforeEach(async () => {
    await db.users.deleteMany({});
  });

  test('成功创建用户', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: '张三', email: 'zhang@example.com' });
    
    expect(res.status).toBe(201);
    expect(res.body).toMatchObject({
      name: '张三',
      email: 'zhang@example.com'
    });
    expect(res.body.id).toBeDefined();
  });

  test('邮箱格式错误 - 400', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: '张三', email: 'invalid-email' });
    
    expect(res.status).toBe(400);
    expect(res.body.error).toContain('email');
  });

  test('邮箱已存在 - 409', async () => {
    await db.users.create({
      name: '已有用户',
      email: 'existing@example.com'
    });
    
    const res = await request(app)
      .post('/api/users')
      .send({ name: '新用户', email: 'existing@example.com' });
    
    expect(res.status).toBe(409);
  });

  test('缺少必填字段 - 400', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: '张三' }); // 缺少 email
    
    expect(res.status).toBe(400);
    expect(res.body.error).toContain('email');
  });
});
```
```

## AI 生成端到端測試

### 使用 Playwright/Cypress

```
你：
请用 Playwright 写一个 E2E 测试：
1. 打开登录页面
2. 输入邮箱和密码
3. 点击登录
4. 验证跳转到了首页

AI：
## E2E 测试

```javascript
const { test, expect } = require('@playwright/test');

test('用户登录流程', async ({ page }) => {
  // 1. 打开登录页面
  await page.goto('/login');
  
  // 2. 输入邮箱和密码
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  
  // 3. 点击登录
  await page.click('button[type="submit"]');
  
  // 4. 验证跳转到首页
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('欢迎');
});
```

## AI 輔助測試驅動開發 (TDD)

### TDD 循環

```
┌─────────────────────────────────────┐
│         Red - Green - Refactor       │
├─────────────────────────────────────┤
│                                     │
│   1. Red：写一个失败的测试           │
│      你/AI 写测试 → 运行 → 失败     │
│              ↓                      │
│   2. Green：写最少的代码让它通过      │
│      AI 生成实现 → 运行 → 通过       │
│              ↓                      │
│   3. Refactor：重构改进              │
│      改善代码 → 测试仍通过          │
│              ↓                      │
│         回到步骤 1                   │
│                                     │
└─────────────────────────────────────┘
```

### AI 輔助 TDD 示例

```
你（第一轮 Red）：
请帮我写一个测试，验证字符串反转函数：
- 输入 "hello"，输出 "olleh"
- 输入 ""，输出 ""
- 输入 "a"，输出 "a"

AI：
```javascript
test('字符串反转', () => {
  expect(reverseString('hello')).toBe('olleh');
  expect(reverseString('')).toBe('');
  expect(reverseString('a')).toBe('a');
});
```

你：运行测试 → 失败 ✓

你（第二轮 Green）：
请实现这个反转函数，让测试通过。

AI：
```javascript
function reverseString(str) {
  return str.split('').reverse().join('');
}
```

你：运行测试 → 通过 ✓

你（第三轮 Refactor）：
现在代码已经通过，可以继续下一个功能。
```

## AI 識別測試盲點

```
你：
请审查我的测试，找出可能的盲点：

[测试代码]
[被测试的代码]

AI：
## 测试覆盖分析

### 已覆盖
✓ 正常路径
✓ 空输入

### 可能遗漏
⚠️ 超长字符串
⚠️ Unicode 字符
⚠️ 特殊字符
⚠️ 并发调用
⚠️ 异常抛出

### 建议补充
```javascript
test('处理超长字符串', () => {
  const long = 'a'.repeat(1000000);
  expect(reverseString(long)).toBe('a'.repeat(1000000));
});

test('处理 Unicode', () => {
  expect(reverseString('你好')).toBe('好你');
});
```
```

## 測試維護

### AI 幫你更新測試

```
你：
我修改了函数签名，请帮我更新测试：

旧签名：calculateTax(price, rate)
新签名：calculateTax(price, rate, options)

新 options 参数：
{
  includeShipping: boolean, // 默认 false
  discount: number // 默认 0
}

AI：
## 更新后的测试

```javascript
describe('calculateTax', () => {
  test('基本计算', () => {
    expect(calculateTax(100, 0.1)).toBe(10);
  });
  
  test('包含运费', () => {
    expect(calculateTax(100, 0.1, { includeShipping: true, shipping: 20 }))
      .toBe(12);
  });
  
  test('应用折扣', () => {
    expect(calculateTax(100, 0.1, { discount: 10 }))
      .toBe(9);
  });
  
  test('默认参数', () => {
    expect(calculateTax(100, 0.1, {}))
      .toBe(10); // 默认行为不变
  });
});
```
```

## 測試策略檢查清單

```
□ 每个函数/方法都有单元测试
□ 公共 API 有集成测试
□ 关键业务流程有 E2E 测试
□ 边界情况被覆盖
□ 错误处理被测试
□ 测试独立，不相互依赖
□ 测试名称描述清晰
□ 测试结果被持续监控
```

## 實踐練習

```
1. 选择一个没有测试的模块
2. 让 AI 为它生成测试
3. 运行测试，确保通过
4. 审查 AI 的测试，找出遗漏
5. 补充遗漏的测试
6. 将测试集成到 CI/CD 流程
```

**記住：AI 能幫你寫測試，但不能幫你決定測試什麼。你的業務理解才是測試價值的關鍵。**
