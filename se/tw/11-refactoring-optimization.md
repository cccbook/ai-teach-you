# 11. 重構與優化既有程式碼

## 為什麼要重構

```
不重構的代碼 = 技術債務 = 未來的噩夢
適當重構 = 提升可維護性 = 未來的從容
```

AI 是重構的絕佳助手，但重構需要謹慎——改錯了可能引入新的 bug。

## 重構的基本原則

### 1. 小步前進

```
❌ 一次重構太多
┌─────────────────────────────────┐
│  重构前          重构后          │
│  1000 行   →    1000 行（新）   │
│                                 │
│  风险：bug 难定位                │
└─────────────────────────────────┘

✅ 分步重構
┌─────────────────────────────────┐
│  Step 1: 提取函数 A              │
│  Step 2: 提取函数 B              │
│  Step 3: 重命名变量              │
│  Step 4: 优化逻辑                │
│                                 │
│  每步都测试，风险可控            │
└─────────────────────────────────┘
```

### 2. 有測試保護

重構前必須有測試，或者重構後立即補充測試。

### 3. 保持功能不變

重構是「改變結構，不改變行為」。

## AI 輔助重構的常見場景

### 場景一：長函數拆分

```
你：
这段函数有 200 行，请帮我拆分成多个小函数：

[代码]

AI：
## 建议的重构方案

### 当前问题
- 函数过长（200 行）
- 职责不单一
- 难以测试

### 拆分方案

```javascript
// 主函数：协调逻辑
async function processOrder(orderId) {
  const order = await fetchOrder(orderId);
  const validation = validateOrder(order);
  if (!validation.success) {
    return handleValidationError(validation.errors);
  }
  
  const pricing = calculatePricing(order);
  const payment = await processPayment(pricing);
  const fulfillment = await fulfillOrder(payment);
  
  return fulfillment;
}

// 子函数 1：获取订单
async function fetchOrder(orderId) { ... }

// 子函数 2：验证订单
function validateOrder(order) { ... }

// 子函数 3：计算价格
function calculatePricing(order) { ... }

// 子函数 4：处理支付
async function processPayment(pricing) { ... }

// 子函数 5：履约订单
async function fulfillOrder(payment) { ... }

// 子函数 6：处理验证错误
function handleValidationError(errors) { ... }
```

### 場景二：消除重複代碼

```
你：
这段代码有多处重复的日志记录逻辑，请帮我提取公共逻辑：

[代码]

AI：
## 重复代码分析

发现 3 处重复的日志模式：

```javascript
// 重复模式 1：错误日志
console.error(`[ERROR] ${new Date().toISOString()} - ${message}`);

// 重复模式 2：带上下文的日志
console.log(`[INFO] ${new Date().toISOString()} - ${context}: ${message}`);
```

## 建议方案：使用 Logger 类

```javascript
class Logger {
  constructor(context) {
    this.context = context;
  }
  
  error(message, error = null) {
    console.error(`[ERROR] ${new Date().toISOString()} - ${this.context}: ${message}`, error);
  }
  
  info(message) {
    console.log(`[INFO] ${new Date().toISOString()} - ${this.context}: ${message}`);
  }
}

// 使用方式
const logger = new Logger('OrderService');
logger.info('Order created');
logger.error('Payment failed', error);
```
```

### 場景三：複雜條件簡化

```
你：
请帮我简化这个复杂的条件判断：

[代码]

AI：
## 简化方案

### 原始代码
```javascript
if (user && user.isActive && user.hasPermission && 
    (user.role === 'admin' || user.role === 'editor' || 
     user.permissions.includes('edit'))) {
  // 执行操作
}
```

### 简化后
```javascript
function canEdit(user) {
  if (!user?.isActive) return false;
  if (user.role === 'admin') return true;
  if (user.role === 'editor') return true;
  return user.permissions.includes('edit');
}

if (canEdit(user)) {
  // 执行操作
}
```

### 或者使用策略模式
```javascript
const permissions = {
  admin: () => true,
  editor: () => true,
  viewer: (user) => user.permissions.includes('edit')
};

const canEdit = (user) => {
  if (!user?.isActive) return false;
  return permissions[user.role]?.(user) ?? false;
};
```

### 場景四：回調地獄改 Promise/Async-Await

```
你：
请把这个回调地狱改成 async/await：

[代码]

AI：
## 重构方案

### 原始代码（回调地狱）
```javascript
getData(function(a) {
  getMoreData(a, function(b) {
    getMoreData(b, function(c) {
      getMoreData(c, function(d) {
        console.log(d);
      });
    });
  });
});
```

### 重构后（async/await）
```javascript
async function fetchAllData() {
  const a = await getData();
  const b = await getMoreData(a);
  const c = await getMoreData(b);
  const d = await getMoreData(c);
  console.log(d);
  return d;
}
```
```

## 重構工作流

```
┌─────────────────────────────────────────────────────┐
│               AI 辅助重构工作流                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. 理解当前代码                                     │
│     你：「这段代码在做什么？」                         │
│     AI → 你：代码目的和结构                          │
│                                                     │
│  2. 识别问题                                         │
│     你：「请列出这段代码的问题」                      │
│     AI → 你：具体问题和改进建议                      │
│                                                     │
│  3. 制定重构计划                                     │
│     你：「请帮我制定分步重构计划」                    │
│     AI → 你：步骤和优先级                           │
│                                                     │
│  4. 逐步重构                                         │
│     你：「请按第 1 步重构」                          │
│     AI → 你：重构后的代码                           │
│                                                     │
│  5. 验证和测试                                       │
│     你/你运行测试套件                               │
│                                                     │
│  6. 重复步骤 4-5，直到完成                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 重構的边界

### 應該重構

- [ ] 代码难以理解
- [ ] 有明显的重复代码
- [ ] 函数/类过长
- [ ] 修改一个功能需要改动多个地方
- [ ] 难以添加新功能
- [ ] 测试难以编写

### 不應該重構

- [ ] 代码已经稳定，几乎不需要改动
- [ ] 重写比重构更划算（ROI 问题）
- [ ] 没有测试保护
- [ ] 临时代码/即将废弃的代码
- [ ] 赶 deadline 的时候

## AI 重構的安全檢查

讓 AI 做重構後的安全檢查：

```
你：
请帮我检查这段重构后的代码：

重构前：
[原始代码]

重构后：
[新代码]

请确认：
1. 功能是否等价
2. 是否有新引入的问题
3. 边界情况是否处理一致
```

## 實踐練習

選擇一段「有味道」的代碼（你自己的或別人的），用以下流程重構：

```
1. 用 AI 分析代码问题
2. 制定重构计划
3. 让 AI 逐步重构
4. 逐段验证功能不变
5. 记录重构前后的差异
```

**重構是持續的過程，不是一次性事件。養成重構的習慣，讓代碼庫保持健康。**
