# 38. 事件驅動與領域驅動設計

## 事件驅動架構

```
┌─────────────────────────────────────────────────────────┐
│                   事件驱动架构                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   传统方式（同步）                                       │
│   Producer ────→ Consumer                               │
│   必须等待响应                                          │
│                                                         │
│   事件驱动（异步）                                       │
│   Producer ──→ Event ──→ Broker ──→ Consumer          │
│   立即返回，之后处理                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助事件驅動設計

### 事件設計

```
你：
如何设计事件驱动系统？

AI：
## 事件设计

### 1. 事件结构
```javascript
// 事件格式
{
  "eventId": "uuid",
  "eventType": "order.created",
  "occurredAt": "2024-01-15T10:30:00Z",
  "aggregateId": "order-123",
  "aggregateType": "Order",
  "version": 1,
  "payload": {
    "orderId": "order-123",
    "userId": "user-456",
    "items": [...],
    "totalAmount": 100.00
  },
  "metadata": {
    "correlationId": "req-789",
    "causationId": "cmd-101"
  }
}
```

### 2. 事件类型
```
命令 (Command) - 指令性的操作
├─ CreateOrder
├─ CancelOrder
└─ UpdateUser

事件 (Event) - 已发生的事情
├─ OrderCreated
├─ OrderCancelled
└─ UserUpdated

查询 (Query) - 请求数据
└─ GetOrderStatus
```

### 3. CQRS 模式
```javascript
// 命令端 - 写
async function createOrder(orderData) {
  const orderId = generateId();
  
  // 保存到写库
  await db.orders.create({
    id: orderId,
    ...orderData,
    status: 'pending'
  });
  
  // 发布事件
  await eventBus.publish({
    type: 'OrderCreated',
    aggregateId: orderId,
    payload: orderData
  });
  
  return orderId;
}

// 查询端 - 读
async function getOrder(orderId) {
  // 从读库/缓存读取
  return await readDb.orders.findById(orderId);
}
```

## 領域驅動設計 (DDD)

```
你：
DDD 的核心概念是什么？

AI：
## DDD 核心概念

### 战略设计
```
限界上下文 (Bounded Context)
└─ 每个领域有明确的边界

├─ 电商上下文 ────────────→ 库存上下文
│  - 订单                 │  - 库存
│  - 购物车               │  - 仓库
│  - 支付                 │  - 配送
└─ 用户上下文
  - 用户
  - 认证
  - 权限
```

### 战术设计
```
聚合 (Aggregate)
└─ 相关对象的集合，共同维护一致性

├─ Order Aggregate
│   ├─ Order (根实体)
│   ├─ OrderItem (值对象)
│   └─ 业务规则：订单总额 = Σ(商品×数量)
│
├─ Product Aggregate
│   ├─ Product (根实体)
│   └─ ProductImage (实体)

值对象 (Value Object)
├─ Address { street, city, zip }
├─ Money { amount, currency }
└─ DateRange { start, end }

领域事件 (Domain Event)
├─ OrderPlaced
├─ PaymentReceived
└─ OrderShipped
```

### 领域服务 vs 应用服务
```javascript
// 领域服务 - 包含核心业务逻辑
class PricingService {
  calculateOrderTotal(items) {
    return items.reduce((total, item) => {
      return total + item.price * item.quantity;
    }, 0);
  }
}

// 应用服务 - 编排领域对象
class OrderApplicationService {
  constructor(orderRepo, pricingService, eventBus) {
    this.orderRepo = orderRepo;
    this.pricingService = pricingService;
    this.eventBus = eventBus;
  }
  
  async createOrder(command) {
    // 调用领域服务
    const total = this.pricingService.calculateOrderTotal(command.items);
    
    // 创建聚合
    const order = new Order({
      items: command.items,
      total: total
    });
    
    // 持久化
    await this.orderRepo.save(order);
    
    // 发布事件
    await this.eventBus.publish(order.events);
  }
}
```

## 事件溯源

```
你：
什么是事件溯源 (Event Sourcing)？

AI：
## 事件溯源

### 概念
```
传统存储：
├─ 当前状态：Order { status: 'shipped' }

事件溯源：
├─ 事件序列：
│   - OrderCreated: { items: [...] }
│   - PaymentReceived: { amount: 100 }
│   - OrderShipped: { trackingNo: 'SF123' }
│
└─ 通过重放事件得到当前状态
```

### 实现
```javascript
class Order {
  constructor() {
    this.id = null;
    this.status = null;
    this.items = [];
    this.events = [];
  }
  
  // 从事件重建
  static fromEvents(events) {
    const order = new Order();
    events.forEach(event => order.apply(event));
    return order;
  }
  
  apply(event) {
    switch (event.type) {
      case 'OrderCreated':
        this.id = event.orderId;
        this.status = 'pending';
        this.items = event.items;
        break;
      case 'PaymentReceived':
        this.status = 'paid';
        break;
      case 'OrderShipped':
        this.status = 'shipped';
        this.trackingNo = event.trackingNo;
        break;
    }
  }
  
  // 业务方法
  ship(trackingNo) {
    if (this.status !== 'paid') {
      throw new Error('Cannot ship unpaid order');
    }
    
    this.applyEvent({ type: 'OrderShipped', trackingNo });
  }
  
  applyEvent(event) {
    this.apply(event);
    this.events.push(event);
  }
  
  getUncommittedEvents() {
    return [...this.events];
  }
}

// 使用
const events = await eventStore.getEvents('order-123');
const order = Order.fromEvents(events);

// 创建新订单
const order = new Order();
order.applyEvent({
  type: 'OrderCreated',
  orderId: 'order-123',
  items: [{ id: 'p1', quantity: 2 }]
});
order.applyEvent({
  type: 'PaymentReceived',
  amount: 100
});

// 保存事件
await eventStore.appendEvents('order-123', order.getUncommittedEvents());
```

### 优势
```
✓ 完整的历史记录
✓ 可以重放任意时间点的状态
✓ 易于审计
✓ 支持时间旅行调试
```

### 挑战
```
✗ 事件可能很多，需要快照优化
✗ 迁移历史事件困难
✗ 查询需要特殊处理
```
```

## Saga 模式

```
你：
微服务之间如何处理分布式事务？

AI：
## Saga 模式

### 解决的问题
```
传统事务无法跨服务：
用户服务 ──→ 订单服务 ──→ 支付服务
    ↓            ↓            ↓
  BEGIN      BEGIN        BEGIN
  UPDATE     INSERT       INSERT
  COMMIT     COMMIT       COMMIT
    ×         ×            ×
```

### Saga 编排
```javascript
// Saga 编排器
class OrderSaga {
  constructor(services) {
    this.userService = services.userService;
    this.orderService = services.orderService;
    this.inventoryService = services.inventoryService;
    this.paymentService = services.paymentService;
  }
  
  async execute(createOrderCommand) {
    try {
      // Step 1: 创建订单
      const order = await this.orderService.create({
        userId: createOrderCommand.userId,
        items: createOrderCommand.items
      });
      
      // Step 2: 预留库存
      await this.inventoryService.reserve({
        orderId: order.id,
        items: createOrderCommand.items
      });
      
      // Step 3: 处理支付
      await this.paymentService.charge({
        orderId: order.id,
        userId: createOrderCommand.userId,
        amount: order.total
      });
      
      // Step 4: 确认订单
      await this.orderService.confirm(order.id);
      
    } catch (error) {
      // 补偿操作
      await this.compensate(error, order);
    }
  }
  
  async compensate(error, order) {
    if (order.status === 'payment_completed') {
      // 退款
      await this.paymentService.refund({ orderId: order.id });
    }
    
    if (order.status === 'inventory_reserved') {
      // 释放库存
      await this.inventoryService.release({ orderId: order.id });
    }
    
    // 取消订单
    await this.orderService.cancel(order.id);
    
    // 记录失败原因
    await this.logCompensation(error, order);
  }
}
```

### Saga 与 CQRS
```javascript
// 完整的事件驱动 Saga
class OrderSaga {
  async handle(event) {
    switch (event.type) {
      case 'OrderCreationRequested':
        await this.startOrderCreation(event);
        break;
        
      case 'InventoryReserved':
        await this.processPayment(event);
        break;
        
      case 'PaymentSucceeded':
        await this.confirmOrder(event);
        break;
        
      case 'PaymentFailed':
        await this.cancelOrder(event);
        await this.releaseInventory(event);
        break;
    }
  }
}
```

## 實踐練習

```
1. 识别系统中的业务领域
2. 定义限界上下文
3. 设计领域事件
4. 实现 CQRS
5. 实现 Saga 编排
6. 添加事件溯源（可选）
7. 测试事件流程
```

**領域驅動設計幫助你用業務語言說話，而非技術術語。**
