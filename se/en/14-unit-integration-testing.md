# 14. Unit Tests and Integration Tests

## Two Layers of Testing Protection

```
┌─────────────────────────────────────────┐
│                                         │
│   Unit Tests       Integration Tests    │
│                                         │
│   Fast execution   Slower execution     │
│   Isolated         Component collab     │
│   Detailed cover   Path coverage        │
│                                         │
└─────────────────────────────────────────┘
```

## Unit Testing

### Unit Test Principles (FIRST)

```
F - Fast
  Tests should complete in milliseconds

I - Independent
  Each test should not depend on other tests

R - Repeatable
  Results should be consistent regardless of when run

S - Self-validating
  Tests should automatically determine pass/fail

T - Timely
  Tests should be written immediately after code
```

### Good Unit Test Examples

```
You:
Please write unit tests for this shopping cart class:

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

AI:
## Unit Tests

```javascript
describe('ShoppingCart', () => {
  let cart;
  let mockProduct;
  
  beforeEach(() => {
    cart = new ShoppingCart();
    mockProduct = { id: 'p1', name: 'Product A', price: 100 };
  });
  
  describe('addItem', () => {
    test('Adding new product', () => {
      cart.addItem(mockProduct);
      expect(cart.items).toHaveLength(1);
      expect(cart.items[0].quantity).toBe(1);
    });
    
    test('Adding existing product increases quantity', () => {
      cart.addItem(mockProduct);
      cart.addItem(mockProduct);
      expect(cart.items).toHaveLength(1);
      expect(cart.items[0].quantity).toBe(2);
    });
    
    test('Custom quantity', () => {
      cart.addItem(mockProduct, 5);
      expect(cart.items[0].quantity).toBe(5);
    });
  });
  
  describe('removeItem', () => {
    test('Remove existing product', () => {
      cart.addItem(mockProduct);
      cart.removeItem('p1');
      expect(cart.items).toHaveLength(0);
    });
    
    test('Removing non-existent product does not throw', () => {
      expect(() => cart.removeItem('non-existent')).not.toThrow();
    });
  });
  
  describe('getTotal', () => {
    test('Empty cart total', () => {
      expect(cart.getTotal()).toBe(0);
    });
    
    test('Single product total', () => {
      cart.addItem(mockProduct, 2);
      expect(cart.getTotal()).toBe(200);
    });
    
    test('Multiple products total', () => {
      cart.addItem(mockProduct, 2);
      cart.addItem({ id: 'p2', price: 50 }, 3);
      expect(cart.getTotal()).toBe(350);
    });
  });
  
  describe('getItemCount', () => {
    test('Empty cart count', () => {
      expect(cart.getItemCount()).toBe(0);
    });
    
    test('Total product count', () => {
      cart.addItem(mockProduct, 3);
      cart.addItem({ id: 'p2', price: 50 }, 2);
      expect(cart.getItemCount()).toBe(5);
    });
  });
});
```
```

### Mocks and Stubs

AI helps you understand when to use mocks:

```
You:
What's the difference between mock and stub in unit testing?

AI:
## Mock vs Stub

### Stub
Pre-configured fake data, used to bypass dependencies
```javascript
const stubDb = {
  findUser: () => ({ id: 1, name: 'Test' })
};
```

### Mock
Verifies interaction behavior, records call counts, parameters, etc.
```javascript
const mockMailer = {
  send: jest.fn()
};

userService.sendWelcomeEmail('test@example.com');
expect(mockMailer.send).toHaveBeenCalledWith(
  'test@example.com',
  expect.stringContaining('Welcome')
);
```

### Use Cases
- Stub: When you need data but don't want to actually query the database
- Mock: When you need to verify interactions between objects
```

## Integration Testing

### Scope of Integration Tests

```
┌─────────────────────────────────────┐
│        Integration Test Scope       │
├─────────────────────────────────────┤
│                                     │
│   Module A ──→ Module B ──→ Module C│
│      ↑                    ↑         │
│      └────────────────────┘         │
│              ↓                      │
│         Database                    │
│                                     │
└─────────────────────────────────────┘

Integration tests: Test multiple modules working together
Unit tests: Test single module (mock external dependencies)
```

### Database Integration Tests

```
You:
Please write an integration test using a real database:

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

AI:
## Database Integration Test

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
  test('Successfully create user', async () => {
    const user = await createUser('John', 'john@example.com');
    
    expect(user.name).toBe('John');
    expect(user.email).toBe('john@example.com');
    expect(user.id).toBeDefined();
  });
  
  test('Duplicate email throws error', async () => {
    await createUser('John', 'john@example.com');
    
    await expect(
      createUser('Jane', 'john@example.com')
    ).rejects.toThrow('Email already exists');
  });
  
  test('User is correctly saved to database', async () => {
    await createUser('John', 'john@example.com');
    
    const saved = await mongoose.connection
      .collection('users')
      .findOne({ email: 'john@example.com' });
    
    expect(saved.name).toBe('John');
  });
});
```
```

### API Integration Tests

```
You:
Please write integration tests for this Express API:

app.post('/api/orders', async (req, res) => {
  const { userId, items } = req.body;
  
  // Verify user exists
  const user = await db.users.findById(userId);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  // Create order
  const order = await db.orders.create({
    userId,
    items,
    total: items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    status: 'pending'
  });
  
  res.json(order);
});

AI:
## API Integration Tests

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
  test('Successfully create order', async () => {
    // First create user
    const user = await mongoose.connection
      .collection('users')
      .insertOne({ name: 'John', email: 'john@example.com' });
    
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
  
  test('User not found returns 404', async () => {
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
  
  test('Missing required fields returns 400', async () => {
    const res = await request(app)
      .post('/api/orders')
      .send({});
    
    expect(res.status).toBe(400);
  });
});
```
```

## Test Data Setup

### Test Fixtures

```
You:
Please refactor this test's data setup using the fixture pattern:

```javascript
beforeEach(async () => {
  await db.users.deleteMany({});
  await db.users.insertOne({ name: 'John', email: 'john@example.com', role: 'admin' });
  await db.users.insertOne({ name: 'Jane', email: 'jane@example.com', role: 'user' });
  await db.products.insertOne({ name: 'Product A', price: 100 });
  await db.products.insertOne({ name: 'Product B', price: 200 });
});
```

AI:
## Fixture Pattern

```javascript
const testData = {
  users: [
    { _id: 'user1', name: 'John', email: 'john@example.com', role: 'admin' },
    { _id: 'user2', name: 'Jane', email: 'jane@example.com', role: 'user' }
  ],
  products: [
    { _id: 'product1', name: 'Product A', price: 100 },
    { _id: 'product2', name: 'Product B', price: 200 }
  ]
};

async function loadFixtures() {
  await db.users.deleteMany({});
  await db.products.deleteMany({});
  await db.users.insertMany(testData.users);
  await db.products.insertMany(testData.products);
}

beforeEach(loadFixtures);

// Or use object-factory pattern
function createUser(overrides = {}) {
  return {
    name: 'Test User',
    email: 'test@example.com',
    role: 'user',
    ...overrides
  };
}

test('Admin can delete user', async () => {
  const admin = createUser({ role: 'admin' });
  await db.users.insertOne(admin);
  
  const res = await request(app)
    .delete(`/api/users/${admin._id}`)
    .set('Authorization', `Bearer ${admin.token}`);
  
  expect(res.status).toBe(204);
});
```
```

## Test Coverage

```
You:
Please explain the meaning of test coverage metrics and how to interpret them:

AI:
## Test Coverage Metrics

### Statement Coverage
- How many statements were executed
- Target: > 80%

### Branch Coverage
- Each conditional branch executed at least once
- Target: > 75%

### Function Coverage
- Each function called at least once
- Target: 100%

### Line Coverage
- How many lines of code were executed
- Target: > 80%

### Important Notes
⚠️ High coverage ≠ High quality tests
⚠️ 100% coverage may hide logic errors
⚠️ Focus on critical path coverage
```

## Practice Exercises

```
1. Select a business module
2. Write unit tests covering core logic
3. Write integration tests covering API endpoints
4. Generate coverage report
5. Identify uncovered edge cases
6. Add tests until satisfied
```

**Good test standards: Fast, Reliable, Maintainable, Finds Bugs.**
