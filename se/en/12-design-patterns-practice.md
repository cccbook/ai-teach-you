# 12. Design Patterns in Practice

## Why Learn Design Patterns

Design patterns are the accumulated wisdom of predecessors solving common problems. Understanding design patterns can:
- Improve code organization
- Facilitate team communication (shared vocabulary)
- Make code easier to extend and maintain

## AI and Design Patterns

AI is proficient in design patterns and can help you:
1. Identify patterns used in existing code
2. Recommend suitable design patterns
3. Generate code that follows patterns

## Common Design Patterns and Use Cases

### Creational Patterns

#### 1. Singleton Pattern

**Use case**: Only one instance needed globally

```
❌ Without pattern:
// May create multiple instances
const db1 = new Database();
const db2 = new Database();

✅ Using Singleton:
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

Have AI help you implement it:

```
You:
Please implement the Singleton pattern in [your programming language],
with thread safety.

AI:
[Generates thread-safe singleton implementation]
```

#### 2. Factory Pattern

**Use case**: Complex creation logic or multiple object types

```
You:
I need a payment factory that creates payment processors based on payment method.
Support: Alipay, WeChat Pay, Credit Card.

AI:
## Factory Pattern Implementation

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

// Usage
const payment = PaymentFactory.createPayment('alipay');
payment.process(amount);
```
```

### Structural Patterns

#### 3. Decorator Pattern

**Use case**: Dynamically add functionality without changing the original class

```
You:
Please implement logging functionality using the decorator pattern:
1. Can add logging to any function
2. Don't modify the original function code

AI:
## Decorator Pattern Implementation

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

// Usage
const fetchUserWithLog = withLogger(fetchUser);
const result = fetchUserWithLog(userId);
```

Or using TypeScript decorators:

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

#### 4. Adapter Pattern

**Use case**: Integrate classes with different interfaces

```
You:
I have an old payment API (PayAPI) and a new payment service (NewPayment),
with different interfaces. Please unify them using the adapter pattern.

Old interface: pay(amount, cardNumber)
New interface: pay({ amount, card: { number, cvv } })

AI:
## Adapter Implementation

```javascript
class PaymentAdapter {
  constructor() {
    this.newPayment = new NewPayment();
  }
  
  pay(amount, cardNumber) {
    // Adapt old interface to new interface
    return this.newPayment.pay({
      amount,
      card: {
        number: cardNumber,
        cvv: '' // Need to get separately
      }
    });
  }
}

// Use the adapter for unified interface
const payment = new PaymentAdapter();
payment.pay(100, '1234567890'); // Compatible with old code
```
```

### Behavioral Patterns

#### 5. Observer Pattern

**Use case**: One-to-many dependency, notify all observers when state changes

```
You:
Please implement a notification system after user registration using the observer pattern:
1. Send welcome email
2. Create user profile
3. Notify admin

AI:
## Observer Pattern Implementation

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

// Usage
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

// Trigger all observers when user registers
async function registerUser(data) {
  const user = await db.create(data);
  events.emit('user:registered', user);
  return user;
}
```

#### 6. Strategy Pattern

**Use case**: Multiple algorithms that can be switched at runtime

```
You:
Please implement discount calculation using the strategy pattern:
- Regular users: no discount
- Silver members: 10% off
- Gold members: 20% off
- Festival promotion: random discount of 10-50 yuan

AI:
## Strategy Pattern Implementation

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

// Usage
const context = new DiscountContext(new SilverDiscount());
const price = context.calculate(user, 100); // 90

context.setStrategy(new FestivalDiscount());
const price2 = context.calculate(user, 100); // 50-90
```

## Use AI to Identify Patterns

```
You:
Please identify which design patterns are used in this code,
and explain why these patterns were chosen:

[code]
```

## Design Pattern Pitfalls

### Over-Engineering

```
❌ Bad:
Using patterns to show off "knowledge" by forcing patterns into simple scenarios.

✅ Good:
Only use patterns when truly needed.
Simple code > complex design patterns.
```

### Dogmatism

Design patterns are guidelines, not mandatory rules.
Understand the intent behind patterns and apply them flexibly.

## Common Pattern Selection Guide

```
Scenario → Recommended Pattern

Complex object creation → Factory Pattern
Need unique instance → Singleton Pattern
Need to add functionality to objects → Decorator Pattern
Incompatible interfaces → Adapter Pattern
One-to-many notifications → Observer Pattern
Need to switch algorithms → Strategy Pattern
Handle request chain → Chain of Responsibility Pattern
State machine → State Pattern
```

## Practice Exercises

```
1. Choose a project you're familiar with
2. Have AI identify scenarios where design patterns could be applied
3. Select appropriate design patterns
4. Have AI generate implementation code
5. Evaluate if it actually improved the code
```

**Design patterns are tools, not goals. The goal is clearer, more maintainable code.**
