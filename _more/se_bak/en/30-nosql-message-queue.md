# 30. NoSQL and Message Queues

## When to Use NoSQL

```
┌─────────────────────────────────────────────────────────┐
│                  NoSQL Use Cases                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   When to use NoSQL:                                    │
│   ✓ Need fast horizontal scaling                        │
│   ✓ Flexible data model                                │
│   ✓ High write throughput                               │
│   ✓ Simple query patterns                              │
│   ✓ Massive data                                       │
│                                                         │
│   When NOT to use NoSQL:                                │
│   ✗ Need complex JOINs                                 │
│   ✗ Strong transactional consistency needs             │
│   ✗ Structured data analysis                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## NoSQL Database Types

```
┌─────────────────────────────────────────────────────────┐
│                   NoSQL Categories                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Document DB           Key-Value DB                    │
│   ├─ MongoDB           ├─ Redis                        │
│   ├─ CouchDB           ├─ DynamoDB                    │
│   └─ Firestore         └─ Memcached                   │
│   For: JSON data       For: Cache, sessions            │
│                                                         │
│   Column Family         Graph DB                        │
│   ├─ Cassandra         ├─ Neo4j                        │
│   ├─ HBase             ├─ Amazon Neptune              │
│   └─ ScyllaDB          └─ Age                         │
│   For: Time-series, big data  For: Social, recommendations│
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted MongoDB

### Document Design

```
You:
Please help me design MongoDB schema for a blog system.

AI:
## MongoDB Blog Design

### Embed vs Reference

```
Embed: Data always accessed together
Reference: Data accessed independently

Blog scenario:
- Posts and comments: Embed (shown together)
- Posts and authors: Reference (author page is separate)
```

### Schema Design
```javascript
// Posts collection
db.articles.insertOne({
  _id: ObjectId(),
  title: "MongoDB Best Practices",
  slug: "mongodb-best-practices",
  content: "...",
  excerpt: "This is a summary...",
  
  // Embed author info (frequently used fields)
  author: {
    _id: ObjectId(),
    name: "John",
    avatar: "https://..."
  },
  
  // Embed tags (limited quantity)
  tags: ["MongoDB", "Database", "NoSQL"],
  
  // Embed category
  category: {
    _id: ObjectId(),
    name: "Database"
  },
  
  // Embed comments (good for small comment volume)
  comments: [
    {
      _id: ObjectId(),
      userId: ObjectId(),
      userName: "Jane",
      content: "Great post!",
      createdAt: ISODate("2024-01-15"),
      likes: 5
    }
  ],
  
  // Metadata
  viewCount: 1000,
  likeCount: 50,
  
  // Status
  status: "published",  // draft, published, archived
  publishedAt: ISODate("2024-01-10"),
  
  // Timestamps
  createdAt: ISODate("2024-01-10"),
  updatedAt: ISODate("2024-01-15")
});
```

### Index Design
```javascript
// Common query indexes
db.articles.createIndex({ status: 1, publishedAt: -1 });
db.articles.createIndex({ "author._id": 1 });
db.articles.createIndex({ tags: 1 });
db.articles.createIndex({ slug: 1 }, { unique: true });
db.articles.createIndex({ title: "text", content: "text" });

// Text search
db.articles.createIndex(
  { title: "text", content: "text", excerpt: "text" },
  { weights: { title: 10, excerpt: 5, content: 1 } }
);
```

### Query Examples
```javascript
// 1. Get article list (paginated)
db.articles.find(
  { status: "published" },
  { title: 1, excerpt: 1, author: 1, publishedAt: 1 }
)
.sort({ publishedAt: -1 })
.skip(0)
.limit(10);

// 2. Text search
db.articles.find({
  $text: { $search: "MongoDB index" }
}, {
  score: { $meta: "textScore" }
}).sort({
  score: { $meta: "textScore" }
});

// 3. Aggregation
db.articles.aggregate([
  { $match: { status: "published" } },
  { $unwind: "$tags" },
  { $group: { _id: "$tags", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
]);

// 4. Update comment (atomic operation)
db.articles.updateOne(
  { _id: articleId, "comments._id": commentId },
  { $inc: { "comments.$.likes": 1 } }
);
```

## AI-Assisted Redis

### Redis Data Structures

```
You:
What data structures does Redis have? How to choose?

AI:
## Redis Data Structures

| Structure | Commands | Use Cases |
|-----------|---------|----------|
| String | SET/GET | Cache, counters, simple values |
| Hash | HSET/HGET | Objects, config |
| List | LPUSH/RPOP | Queues, timelines |
| Set | SADD/SMEMBERS | Tags, friends |
| Sorted Set | ZADD/ZRANGE | Leaderboards, priority queues |
| Bitmap | SETBIT | User check-ins, Bloom filters |
| HyperLogLog | PFADD | Count unique users |
| Stream | XADD/XREAD | Message queues, event streams |

### String
```javascript
// Cache page
await redis.setex('page:1', 3600, htmlContent);
const content = await redis.get('page:1');

// Counter
await redis.incr('view_count:article:123');
const count = await redis.get('view_count:article:123');

// Distributed lock
await redis.set('lock:order:123', clientId, 'NX', 'EX', 30);
```

### Hash
```javascript
// User object
await redis.hset('user:1001', {
  name: 'John',
  email: 'john@example.com',
  age: 25
});

const user = await redis.hgetall('user:1001');
await redis.hincrby('user:1001', 'age', 1);
```

### List
```javascript
// Message queue
await redis.lpush('queue:tasks', JSON.stringify({ task: 'send_email' }));
const task = await redis.rpop('queue:tasks');

// Latest messages feed
await redis.lpush('user:1001:feed', JSON.stringify({ content: 'Hello' }));
const feed = await redis.lrange('user:1001:feed', 0, 9);
```

### Sorted Set
```javascript
// Leaderboard
await redis.zadd('leaderboard', 1000, 'user:1001');
await redis.zadd('leaderboard', 2000, 'user:1002');
await redis.zadd('leaderboard', 1500, 'user:1003');

// Get Top 10
const top10 = await redis.zrevrange('leaderboard', 0, 9, 'WITHSCORES');

// Get user rank
const rank = await redis.zrevrank('leaderboard', 'user:1001');
```

### Bitmap
```javascript
// User check-in
const date = new Date().toISOString().slice(0, 10); // 2024-01-15
await redis.setbit(`sign:${userId}:${date.slice(0, 7)}`, parseInt(date.slice(-2)) - 1, 1);

// Check check-in
const signed = await redis.getbit(`sign:${userId}:2024-01`, 14);
```

## Message Queues

### Why Message Queues

```
┌─────────────────────────────────────────────────────────┐
│                   Value of Message Queues                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Decoupling                    Peak Shaving             │
│   ┌─────┐    ┌─────┐           ┌─────────────────┐     │
│   │Service│───→│Queue │───→┌─────┐│ Input: 10000/sec │     │
│   └─────┘    └─────┘   │Service││ Output: 100/sec  │     │
│                        │Service││ Queue absorbs peak│     │
│   Async                  └─────┘└─────────────────┘     │
│   ┌─────┐                      │                        │
│   │Sync │───→ Takes 1 sec     │                        │
│   └─────┘                      │                        │
│   ┌─────┐    ┌─────┐         │                        │
│   │Publish│───→│Queue │───→ Async processing            │
│   └─────┘    └─────┘         │                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### AI-Assisted Message Queue Design

```
You:
Please help me design a message queue system for order processing.

AI:
## Order Processing Message Queue

### Architecture Design
```
User places order ──→ Order service ──→ Create order ──→ Send message
                                        │
                                        ↓
                               ┌────────────────┐
                               │ Order Queue    │
                               └────────────────┘
                                        │
               ┌────────────────────────┼────────────────────────┐
               ↓                        ↓                        ↓
     ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
     │ Payment service │    │ Inventory service│    │ Shipping service│
     │                 │    │                 │    │                 │
     │ - Deduct payment│    │ - Deduct stock │    │ - Create delivery│
     │ - Send notify   │    │ - Check stock  │    │ - Send notify   │
     └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### RabbitMQ Configuration
```javascript
// Connection
const amqp = require('amqplib');
const conn = await amqp.connect('amqp://localhost');

// Create channel
const channel = await conn.createChannel();

// Exchange
await channel.assertExchange('order.events', 'topic', {
  durable: true
});

// Queues
await channel.assertQueue('order.payment', { durable: true });
await channel.assertQueue('order.inventory', { durable: true });
await channel.assertQueue('order.notification', { durable: true });

// Bindings
channel.bindQueue('order.payment', 'order.events', 'order.created');
channel.bindQueue('order.inventory', 'order.events', 'order.created');
channel.bindQueue('order.notification', 'order.events', 'order.*');

// Consumer
channel.consume('order.payment', async (msg) => {
  const order = JSON.parse(msg.content);
  try {
    await processPayment(order);
    channel.ack(msg);
  } catch (error) {
    // Dead letter queue or retry
    channel.nack(msg, false, true);
  }
});
```

### Publish Message
```javascript
async function createOrder(orderData) {
  // Create order
  const order = await db.orders.create(orderData);
  
  // Publish event
  channel.publish(
    'order.events',
    'order.created',
    Buffer.from(JSON.stringify({
      orderId: order.id,
      userId: order.userId,
      items: order.items,
      totalAmount: order.totalAmount,
      timestamp: Date.now()
    })),
    { persistent: true }
  );
  
  return order;
}
```

### Kafka Configuration (for high throughput)
```javascript
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'order-service',
  brokers: ['localhost:9092']
});

const producer = kafka.producer();
await producer.connect();

const consumer = kafka.consumer({ groupId: 'order-processor' });
await consumer.connect();
await consumer.subscribe({ topic: 'order-events', fromBeginning: false });

await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    const order = JSON.parse(message.value.toString());
    await processOrder(order);
  }
});

// Produce message
await producer.send({
  topic: 'order-events',
  messages: [
    { key: order.userId.toString(), value: JSON.stringify(order) }
  ]
});
```

### Message Queue Comparison

```
You:
How to choose between RabbitMQ vs Kafka vs Redis Streams?

AI:
## Message Queue Comparison

| Feature | RabbitMQ | Kafka | Redis Streams |
|---------|----------|-------|---------------|
| Throughput | Medium | Very High | Medium |
| Latency | Low | Medium | Very Low |
| Message persistence | Supported | Supported | Supported |
| Message ordering | By queue | By partition | By consumer group |
| Message acknowledgment | Supported | Supported | Supported |
| Dead letter queue | Native | Needs config | Manual |
| Operational complexity | Medium | High | Low |
| Best for | Task queues | Log/stream processing | Lightweight queues |

### Selection Guide
```
High throughput + log analysis → Kafka
Complex routing + task queues → RabbitMQ
Lightweight + low latency → Redis Streams
Small team + quick implementation → Redis Streams
Microservices + enterprise → RabbitMQ
Big data + real-time analytics → Kafka
```

## Practice Exercises

```
1. Evaluate if your system needs NoSQL
2. Choose appropriate NoSQL database
3. Design data model
4. Configure Redis (if needed)
5. Design message queue architecture
6. Implement producer/consumer
7. Set up monitoring and alerts
```

**NoSQL and message queues are important components of modern architecture. Correct selection and design greatly enhance system flexibility and performance.**
