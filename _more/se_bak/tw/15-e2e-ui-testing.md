# 15. 端到端測試與 UI 測試

## 什麼是端到端測試

```
┌─────────────────────────────────────────────────────┐
│                   端到端测试                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   用户操作 ──→ 前端 ──→ API ──→ 后端 ──→ 数据库    │
│                                                     │
│   验证：整个流程是否正常工作                          │
│                                                     │
└─────────────────────────────────────────────────────┘

单元测试：测试单个函数
集成测试：测试组件协作
E2E 测试：测试整个系统（模拟真实用户）
```

## E2E 測試工具

| 工具 | 适用场景 | 特点 |
|------|----------|------|
| Playwright | Web 应用 | 微软出品，支持多浏览器 |
| Cypress | Web 应用 | 开发者体验好，生态丰富 |
| Selenium | 旧版 Web | 支持多语言，浏览器兼容广 |
| Puppeteer | Node.js | Google 出品，轻量 |
| Detox | 移动应用 | React Native 专用 |
| Appium | 移动应用 | 通用移动测试 |

## Playwright 快速入門

### 基本結構

```
你：
请用 Playwright 写一个登录流程的 E2E 测试。

AI：
## Playwright E2E 测试

```javascript
const { test, expect } = require('@playwright/test');

test.describe('登录流程', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });
  
  test('成功登录', async ({ page }) => {
    // 填写表单
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    
    // 提交
    await page.click('[data-testid="login-button"]');
    
    // 验证跳转
    await expect(page).toHaveURL('/dashboard');
    
    // 验证用户信息
    await expect(page.locator('[data-testid="user-name"]'))
      .toContainText('Test User');
  });
  
  test('登录失败显示错误', async ({ page }) => {
    await page.fill('[data-testid="email-input"]', 'wrong@example.com');
    await page.fill('[data-testid="password-input"]', 'wrongpass');
    
    await page.click('[data-testid="login-button"]');
    
    await expect(page.locator('[data-testid="error-message"]'))
      .toContainText('Invalid credentials');
  });
});
```
```

### 常用選擇器

```
┌─────────────────────────────────────────────────────┐
│                  选择器优先级                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. data-testid (最推荐)                           │
│     page.locator('[data-testid="submit"]')         │
│                                                     │
│  2. 角色选择器                                      │
│     page.getByRole('button', { name: 'Submit' })  │
│                                                     │
│  3. 文本选择器                                      │
│     page.getByText('Hello World')                  │
│                                                     │
│  4. CSS 选择器                                      │
│     page.locator('.class-name')                    │
│                                                     │
│  5. XPath (最后手段)                                │
│     page.locator('//button[@type="submit"]')     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 等待策略

```
你：
请解释 Playwright 中的等待策略。

AI：
## Playwright 等待策略

### 1. 断言等待（推荐）
```javascript
await expect(page.locator('.status')).toHaveText('Ready');
// Playwright 会自动等待条件满足
```

### 2. 网络等待
```javascript
await page.waitForResponse('**/api/data');
```

### 3. 导航等待
```javascript
await page.waitForURL('**/dashboard');
```

### 4. 函数等待
```javascript
await page.waitForFunction(() => {
  return window.someValue === 'ready';
});
```

### 不要这样做 ❌
```javascript
// 硬编码等待 - 不推荐
await page.waitForTimeout(2000); // 浪费时间且不稳定
```

### 最佳实践 ✅
```javascript
// 使用断言等待
await expect(page.locator('.modal')).toBeVisible();

// 等待特定元素
await page.waitForSelector('.loaded', { state: 'visible' });
```
```

## 常見 E2E 測試場景

### 1. 表單填寫與提交

```
test('完整的表单提交流程', async ({ page }) => {
  await page.goto('/register');
  
  // 填写表单
  await page.fill('#name', '张三');
  await page.fill('#email', 'zhang@example.com');
  await page.fill('#password', 'SecurePass123');
  await page.fill('#confirmPassword', 'SecurePass123');
  
  // 上传文件
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.click('#avatar-upload');
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles('./test-assets/avatar.jpg');
  
  // 勾选协议
  await page.check('#terms-agreement');
  
  // 提交
  await page.click('button[type="submit"]');
  
  // 验证结果
  await expect(page).toHaveURL('/profile');
  await expect(page.locator('.welcome-message'))
    .toContainText('欢迎，张三');
});
```

### 2. 購物車流程

```
test('完整的购物流程', async ({ page }) => {
  // 1. 浏览商品
  await page.goto('/products');
  await page.click('[data-product-id="prod-001"]');
  
  // 2. 加入购物车
  await page.click('[data-testid="add-to-cart"]');
  await expect(page.locator('.cart-badge')).toContainText('1');
  
  // 3. 查看购物车
  await page.click('[data-testid="cart-icon"]');
  await expect(page.locator('.cart-item')).toHaveCount(1);
  
  // 4. 修改数量
  await page.fill('[data-testid="quantity-input"]', '3');
  await page.click('[data-testid="update-quantity"]');
  
  // 5. 结账
  await page.click('[data-testid="checkout-button"]');
  await expect(page).toHaveURL('/checkout');
  
  // 6. 填写信息并下单
  await page.fill('#address', '北京市朝阳区xxx');
  await page.click('[data-testid="place-order"]');
  
  // 7. 验证订单确认
  await expect(page.locator('.order-success')).toBeVisible();
  await expect(page.locator('.order-number')).toBeVisible();
});
```

### 3. 認證流程

```
test('完整的注册-登录-登出流程', async ({ page }) => {
  const testEmail = `test${Date.now()}@example.com`;
  
  // 注册
  await page.goto('/register');
  await page.fill('#email', testEmail);
  await page.fill('#password', 'SecurePass123');
  await page.click('#register-button');
  
  // 验证邮箱（如果有邮件验证）
  // ...
  
  // 登出
  await page.click('[data-testid="user-menu"]');
  await page.click('text=登出');
  
  // 尝试访问需要登录的页面
  await page.goto('/dashboard');
  await expect(page).toHaveURL('/login');
  
  // 用新账号登录
  await page.fill('#email', testEmail);
  await page.fill('#password', 'SecurePass123');
  await page.click('#login-button');
  
  // 验证登录成功
  await expect(page).toHaveURL('/dashboard');
});
```

## UI 測試的常見問題

### 1. 測試不穩定 (Flaky Tests)

```
你：
测试经常超时失败，但手动测试没问题，怎么解决？

AI：
## 解决 Flaky Tests

### 1. 添加适当的等待
❌ 错误：
await page.click('#submit');
await page.fill('#result', 'xxx'); // 可能还没出现

✅ 正确：
await page.click('#submit');
await expect(page.locator('#result')).toBeVisible();
await page.fill('#result', 'xxx');

### 2. 使用网络条件控制
```javascript
await page.route('**/api/**', async (route) => {
  // 模拟慢网络
  await route.fulfill({
    status: 200,
    body: '...',
    headers: { 'x-delay': '1000' }
  });
});
```

### 3. 确保测试隔离
```javascript
test.beforeEach(async ({ page }) => {
  // 每个测试都清理状态
  await page.evaluate(() => localStorage.clear());
  await page.reload();
});
```
```

### 2. 選擇器脆弱

```
你：
选择器经常因为 UI 改版而失败，怎么办？

AI：
## 稳定的测试 ID

### 1. 使用 data-testid
```html
<button data-testid="submit-button">提交</button>
```

### 2. 使用语义化选择器
```javascript
// 避免
page.locator('.btn.primary.submit.xl');

// 优先
page.getByRole('button', { name: '提交' });
page.getByLabel('用户名');
page.getByPlaceholder('请输入邮箱');
```

### 3. 使用测试组件库
大多数 UI 库支持测试 ID：
- Material-UI: `data-testid` prop
- Ant Design: `data-testid` 或 `id`
- React: 原生支持
```
```

## 測試輔助工具

### Page Object 模式

```
你：
请用 Page Object 模式重构这个测试：

```javascript
test('登录', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'pass');
  await page.click('.login-btn');
  await expect(page).toHaveURL('/dashboard');
});
```

AI：
## Page Object 模式

### 1. 创建 Page Object
```javascript
// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
  }
  
  async goto() {
    await this.page.goto('/login');
  }
  
  async login(email, password) {
    await this.page.fill('#email', email);
    await this.page.fill('#password', password);
    await this.page.click('.login-btn');
  }
}

module.exports = LoginPage;
```

### 2. 使用 Page Object
```javascript
const LoginPage = require('./pages/LoginPage');

test('登录', async ({ page }) => {
  const loginPage = new LoginPage(page);
  
  await loginPage.goto();
  await loginPage.login('test@example.com', 'pass');
  
  await expect(page).toHaveURL('/dashboard');
});
```

### 3. 好处
- UI 变只需要改 Page Object
- 测试代码更清晰
- 可复用页面操作
```

## 實踐練習

```
1. 安装 Playwright 或 Cypress
2. 配置测试环境
3. 编写一个关键用户流程的 E2E 测试
4. 设置 CI 集成
5. 报告和分析测试结果
```

## E2E 測試最佳實踐

```
□ 每个 E2E 测试验证一个关键流程
□ 使用 data-testid 或语义化选择器
□ 避免硬编码等待
□ 确保测试环境与生产一致
□ 失败时提供有意义的错误信息
□ 定期清理测试数据
□ 在 CI 中运行 E2E 测试
□ 监控 flaky 测试
```

**E2E 測試是代價最高的測試，但也是最接近真實用戶的測試。只對關鍵路徑做 E2E 測試。**
