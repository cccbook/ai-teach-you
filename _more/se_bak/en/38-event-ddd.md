# 38. Event-Driven and Domain-Driven Design

## Event-Driven Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Event-Driven Architecture                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Traditional (Synchronous)                              │
│   Producer ────→ Consumer                                │
│   Must wait for response                                │
│                                                         │
│   Event-Driven (Asynchronous)                            │
│   Producer ──→ Event ──→ Broker ──→ Consumer            │
│   Return immediately, process later                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Event-Driven Design

### Event Design

```
You:
How do I design an event-driven system?

AI:
## Event Design

### 1. Event Structure
```javascript
// Event format
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

### 2. Event Types
```
Command - Directive operations
├─ CreateOrder
├─ CancelOrder
└─ UpdateUser

Event - Things that have happened
├─ OrderCreated
├─ OrderCancelled
└─ UserUpdated

Query - Request data
└─ GetOrderStatus
```

### 3. CQRS Pattern
```javascript
// Command side - Write
async function createOrder(orderData) {
  const orderId = generateId();
  
  // Save to write database
  await db.orders.create({
    id: orderId,
    ...orderData,
    status: 'pending'
  });
  
  // Publish event
  await eventBus.publish({
    type: 'OrderCreated',
    aggregateId: orderId,
    payload: orderData
  });
  
  return orderId;
}

// Query side - Read
async function getOrder(orderId) {
  // Read from read database/cache
  return await readDb.orders.findById(orderId);
}
```

## Domain-Driven Design (DDD)

```
You:
What are the core concepts of DDD?

AI:
## DDD Core Concepts

### Strategic Design
```
Bounded Context
└─ Each domain has clear boundaries

├─ E-commerce Context ────────────→ Inventory Context
│  - Orders                      │  - Inventory
│  - Shopping Cart               │  - Warehouses
│  - Payments                    │  - Shipping
└─ User Context
  - Users
  - Authentication
  - Permissions
```

### Tactical Design
```
Aggregate
└─ Collection of related objects maintaining consistency together

├─ Order Aggregate
│   ├─ Order (root entity)
│   ├─ OrderItem (value object)
│   └─ Business rule: Order total = Σ(item price × quantity)
│
├─ Product Aggregate
│   ├─ Product (root entity)
│   └─ ProductImage (entity)

Value Object
├─ Address { street, city, zip }
├─ Money { amount, currency }
└─ DateRange { start, end }

Domain Event
├─ OrderPlaced
├─ PaymentReceived
└─ OrderShipped
```

### Domain Service vs Application Service
```javascript
// Domain service - contains core business logic
class PricingService {
  calculateOrderTotal(items) {
    return items.reduce((total, item) => {
      return total + item.price * item.quantity;
    }, 0);
  }
}

// Application service - orchestrates domain objects
class OrderApplicationService {
  constructor(orderRepo, pricingService, eventBus) {
    this.orderRepo = orderRepo;
    this.pricingService = pricingService;
    this.eventBus = eventBus;
  }
  
  async createOrder(command) {
    // Call domain service
    const total = this.pricingService.calculateOrderTotal(command.items);
    
    // Create aggregate
    const order = new Order({
      items: command.items,
      total: total
    });
    
    // Persist
    await this.orderRepo.save(order);
    
    // Publish events
    await this.eventBus.publish(order.events);
  }
}
```

## Event Sourcing

```
You:
What is Event Sourcing?

AI:
## Event Sourcing

### Concept
```
Traditional storage:
├─ Current state: Order { status: 'shipped' }

Event Sourcing:
├─ Event sequence:
│   - OrderCreated: { items: [...] }
│   - PaymentReceived: { amount: 100 }
│   - OrderShipped: { trackingNo: 'SF123' }
│
└─ Derive current state by replaying events
```

### Implementation
```javascript
class Order {
  constructor() {
    this.id = null;
    this.status = null;
    this.items = [];
    this.events = [];
  }
  
  // Rebuild from events
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
  
  // Business method
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

// Usage
const events = await eventStore.getEvents('order-123');
const order = Order.fromEvents(events);

// Create new order
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

// Save events
await eventStore.appendEvents('order-123', order.getUncommittedEvents());
```

### Advantages
```
✓ Complete audit trail
✓ Can replay state at any point in time
✓ Easy to audit
✓ Supports time-travel debugging
```

### Challenges
```
✗ Events can be numerous, need snapshot optimization
✗ Migrating historical events is difficult
✗ Queries require special handling
```
```

## Saga Pattern

```
You:
How do microservices handle distributed transactions?

AI:
## Saga Pattern

### Problem Solved
```
Traditional transactions cannot span services:
User Service ──→ Order Service ──→ Payment Service
    ↓            ↓            ↓
  BEGIN       BEGIN        BEGIN
  UPDATE      INSERT       INSERT
  COMMIT      COMMIT       COMMIT
    ×          ×           ×
```

### Saga Orchestration
```javascript
// Saga orchestrator
class OrderSaga {
  constructor(services) {
    this.userService = services.userService;
    this.orderService = services.orderService;
    this.inventoryService = services.inventoryService;
    this.paymentService = services.paymentService;
  }
  
  async execute(createOrderCommand) {
    try {
      // Step 1: Create order
      const order = await this.orderService.create({
        userId: createOrderCommand.userId,
        items: createOrderCommand.items
      });
      
      // Step 2: Reserve inventory
      await this.inventoryService.reserve({
        orderId: order.id,
        items: createOrderCommand.items
      });
      
      // Step 3: Process payment
      await this.paymentService.charge({
        orderId: order.id,
        userId: createOrderCommand.userId,
        amount: order.total
      });
      
      // Step 4: Confirm order
      await this.orderService.confirm(order.id);
      
    } catch (error) {
      // Compensation actions
      await this.compensate(error, order);
    }
  }
  
  async compensate(error, order) {
    if (order.status === 'payment_completed') {
      // Refund
      await this.paymentService.refund({ orderId: order.id });
    }
    
    if (order.status === 'inventory_reserved') {
      // Release inventory
      await this.inventoryService.release({ orderId: order.id });
    }
    
    // Cancel order
    await this.orderService.cancel(order.id);
    
    // Log failure reason
    await this.logCompensation(error, order);
  }
}
```

### Saga with CQRS
```javascript
// Complete event-driven Saga
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

## Hands-On Exercises

```
1. Identify business domains in your system
2. Define bounded contexts
3. Design domain events
4. Implement CQRS
5. Implement Saga orchestration
6. Add event sourcing (optional)
7. Test event flows
```

**Domain-Driven Design helps you speak in business language, not technical jargon.**

(End of file - total 420 lines)
