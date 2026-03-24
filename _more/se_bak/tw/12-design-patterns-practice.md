# 12. 設計模式的實際應用

## 為什麼要學習設計模式

設計模式是前人解決常見問題的智慧結晶。了解設計模式可以：
- 提高代碼的組織性
- 促進團隊溝通（有共同詞彙）
- 讓代碼更容易擴展和維護

## AI 與設計模式

AI 熟練掌握設計模式，能幫你：
1. 識別現有代碼使用的模式
2. 建議適合的設計模式
3. 生成符合模式的代碼

## 常見設計模式及應用場景

### 創建型模式

#### 1. 單例模式 (Singleton)

**場景**：全局只需一個實例

```
❌ 不用模式：
// 可能创建多个实例
const db1 = new Database();
const db2 = new Database();

✅ 使用單例：
class Database {
  static #instance = null;
  
  static getInstance() {
    if (!Database.#instance) {
      Database.#instance = new Database();
    }
    return Database.#instance;
  }
}

const db1 = Database.getInstance();
const db2 = Database.getInstance();
console.log(db1 === db2); // true
```

讓 AI 幫你實現：

```
你：
请用 [你的编程语言] 实现单例模式，
要求线程安全。

AI：
[生成线程安全的单例实现]
```

#### 2. 工廠模式 (Factory)

**場景**：創建對象需要複雜邏輯，或有多種對象類型

```
你：
我需要一个支付工厂，能根据支付方式创建对应的支付处理器。
支持：支付宝、微信支付、信用卡。

AI：
## 工厂模式实现

```javascript
class PaymentFactory {
  static createPayment(method) {
    switch (method) {
      case 'alipay':
        return new AlipayProcessor();
      case 'wechat':
        return new WechatPayProcessor();
      case 'credit_card':
        return new CreditCardProcessor();
      default:
        throw new Error(`Unknown payment method: ${method}`);
    }
  }
}

// 使用
const payment = PaymentFactory.createPayment('alipay');
payment.process(amount);
```
```

### 結構型模式

#### 3. 裝飾器模式 (Decorator)

**場景**：動態添加功能，不改變原有類

```
你：
请用装饰器模式实现日志记录功能，
要求：
1. 能够给任何函数添加日志
2. 不改变原函数代码

AI：
## 装饰器模式实现

```javascript
function withLogger(fn) {
  return function(...args) {
    console.log(`[LOG] Calling ${fn.name} with args:`, args);
    const start = Date.now();
    const result = fn.apply(this, args);
    console.log(`[LOG] ${fn.name} returned in ${Date.now() - start}ms`);
    return result;
  };
}

// 使用
const fetchUserWithLog = withLogger(fetchUser);
const result = fetchUserWithLog(userId);
```

或者用 TypeScript 装饰器：

```typescript
function log(target: any, name: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value;
  descriptor.value = function(...args: any[]) {
    console.log(`Calling ${name}`);
    return original.apply(this, args);
  };
  return descriptor;
}

class UserService {
  @log
  fetchUser(id: string) {
    // ...
  }
}
```

#### 4. 適配器模式 (Adapter)

**場景**：整合不同接口的類

```
你：
我有一个旧的支付 API（PayAPI）和新的支付服务（NewPayment），
接口不同。请用适配器模式统一。

旧接口：pay(amount, cardNumber)
新接口：pay({ amount, card: { number, cvv } })

AI：
## 适配器实现

```javascript
class PaymentAdapter {
  constructor() {
    this.newPayment = new NewPayment();
  }
  
  pay(amount, cardNumber) {
    // 适配旧接口到新接口
    return this.newPayment.pay({
      amount,
      card: {
        number: cardNumber,
        cvv: '' // 需要额外获取
      }
    });
  }
}

// 使用时统一使用适配器
const payment = new PaymentAdapter();
payment.pay(100, '1234567890'); // 兼容旧代码
```
```

### 行為型模式

#### 5. 觀察者模式 (Observer)

**場景**：一對多依賴，當狀態變化時通知所有觀察者

```
你：
请用观察者模式实现用户注册后的通知系统：
1. 发送欢迎邮件
2. 创建用户档案
3. 发送通知给管理员

AI：
## 观察者模式实现

```javascript
class EventEmitter {
  constructor() {
    this.listeners = {};
  }
  
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
    return () => this.off(event, callback);
  }
  
  emit(event, data) {
    (this.listeners[event] || []).forEach(cb => cb(data));
  }
  
  off(event, callback) {
    this.listeners[event] = this.listeners[event]
      .filter(cb => cb !== callback);
  }
}

// 使用
const events = new EventEmitter();

events.on('user:registered', async (user) => {
  await sendWelcomeEmail(user);
});

events.on('user:registered', async (user) => {
  await createUserProfile(user);
});

events.on('user:registered', async (user) => {
  await notifyAdmin(user);
});

// 用户注册时触发所有观察者
async function registerUser(data) {
  const user = await db.create(data);
  events.emit('user:registered', user);
  return user;
}
```

#### 6. 策略模式 (Strategy)

**場景**：有多種演算法，运行时可以切换

```
你：
请用策略模式实现折扣计算：
- 普通用户：无折扣
- 银卡会员：9折
- 金卡会员：8折
- 节日活动：随机立减 10-50 元

AI：
## 策略模式实现

```javascript
class DiscountStrategy {
  apply(user, amount) {
    return amount;
  }
}

class SilverDiscount extends DiscountStrategy {
  apply(user, amount) {
    return amount * 0.9;
  }
}

class GoldDiscount extends DiscountStrategy {
  apply(user, amount) {
    return amount * 0.8;
  }
}

class FestivalDiscount extends DiscountStrategy {
  apply(user, amount) {
    const discount = Math.random() * 40 + 10;
    return Math.max(amount - discount, 0);
  }
}

class DiscountContext {
  constructor(strategy) {
    this.strategy = strategy;
  }
  
  setStrategy(strategy) {
    this.strategy = strategy;
  }
  
  calculate(user, amount) {
    return this.strategy.apply(user, amount);
  }
}

// 使用
const context = new DiscountContext(new SilverDiscount());
const price = context.calculate(user, 100); // 90

context.setStrategy(new FestivalDiscount());
const price2 = context.calculate(user, 100); // 50-90 之间
```

## 讓 AI 幫你識別模式

```
你：
请识别这段代码使用了哪些设计模式，
并解释为什么使用这些模式：

[代码]
```

## 設計模式的陷阱

### 過度工程

```
❌ 不好：
为了展示自己「会设计模式」，在简单场景下硬套模式。

✅ 好：
只在确实需要时才使用设计模式。
简单代码 > 复杂的设计模式。
```

### 教條主義

設計模式是指導方針，不是強制規則。
理解模式的意圖，靈活運用。

## 常見模式選擇指南

```
场景 → 推荐模式

对象创建复杂 → 工厂模式
需要唯一实例 → 单例模式
需要给对象添加功能 → 装饰器模式
接口不兼容 → 适配器模式
一对多通知 → 观察者模式
需要切换算法 → 策略模式
处理请求链 → 责任链模式
状态机 → 状态模式
```

## 實踐練習

```
1. 选择一个你熟悉的项目
2. 让 AI 帮你识别可以应用设计模式的场景
3. 选择合适的设计模式
4. 让 AI 生成实现代码
5. 评估是否真的改善了代码
```

**設計模式是工具，不是目的。讓代碼更清晰、更易維護才是目的。**
