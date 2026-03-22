# 30. NoSQL 與訊息佇列

## NoSQL 的適用場景

```
┌─────────────────────────────────────────────────────────┐
│                  NoSQL 使用场景                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   什么时候用 NoSQL：                                     │
│   ✓ 需要快速水平扩展                                    │
│   ✓ 数据模型灵活                                        │
│   ✓ 高写入吞吐量                                        │
│   ✓ 简单查询模式                                        │
│   ✓ 海量数据                                           │
│                                                         │
│   什么时候不用 NoSQL：                                   │
│   ✗ 需要复杂 JOIN                                      │
│   ✗ 强事务一致性要求                                    │
│   ✗ 结构化数据分析                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## NoSQL 資料庫類型

```
┌─────────────────────────────────────────────────────────┐
│                   NoSQL 分类                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   文档数据库          键值数据库                         │
│   ├─ MongoDB          ├─ Redis                         │
│   ├─ CouchDB          ├─ DynamoDB                      │
│   └─ Firestore        └─ Memcached                     │
│   场景：JSON 数据    场景：缓存、会话                     │
│                                                         │
│   列族数据库          图数据库                          │
│   ├─ Cassandra        ├─ Neo4j                         │
│   ├─ HBase            ├─ Amazon Neptune                │
│   └─ ScyllaDB         └─ Age                          │
│   场景：时序、大数据  场景：社交关系、推荐                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助 MongoDB

### 文檔設計

```
你：
请帮我设计 MongoDB schema 用于博客系统。

AI：
## MongoDB 博客设计

### 嵌入 vs 引用

```
嵌入（Embed）：数据总是一起访问
引用（Reference）：数据独立访问

博客场景：
- 文章和评论：嵌入（一起显示）
- 文章和作者：引用（作者页面独立）
```

### Schema 设计
```javascript
// 文章集合
db.articles.insertOne({
  _id: ObjectId(),
  title: "MongoDB 最佳实践",
  slug: "mongodb-best-practices",
  content: "...",
  excerpt: "这是摘要...",
  
  // 嵌入作者信息（常用字段）
  author: {
    _id: ObjectId(),
    name: "张三",
    avatar: "https://..."
  },
  
  // 嵌入标签（数量有限）
  tags: ["MongoDB", "数据库", "NoSQL"],
  
  // 嵌入分类
  category: {
    _id: ObjectId(),
    name: "数据库"
  },
  
  // 嵌入评论（适合评论量少的场景）
  comments: [
    {
      _id: ObjectId(),
      userId: ObjectId(),
      userName: "李四",
      content: "写得很好！",
      createdAt: ISODate("2024-01-15"),
      likes: 5
    }
  ],
  
  // 元数据
  viewCount: 1000,
  likeCount: 50,
  
  // 状态
  status: "published",  // draft, published, archived
  publishedAt: ISODate("2024-01-10"),
  
  // 时间戳
  createdAt: ISODate("2024-01-10"),
  updatedAt: ISODate("2024-01-15")
});
```

### 索引设计
```javascript
// 文章查询常用索引
db.articles.createIndex({ status: 1, publishedAt: -1 });
db.articles.createIndex({ "author._id": 1 });
db.articles.createIndex({ tags: 1 });
db.articles.createIndex({ slug: 1 }, { unique: true });
db.articles.createIndex({ title: "text", content: "text" });

// 文本搜索
db.articles.createIndex(
  { title: "text", content: "text", excerpt: "text" },
  { weights: { title: 10, excerpt: 5, content: 1 } }
);
```

### 查询示例
```javascript
// 1. 获取文章列表（分页）
db.articles.find(
  { status: "published" },
  { title: 1, excerpt: 1, author: 1, publishedAt: 1 }
)
.sort({ publishedAt: -1 })
.skip(0)
.limit(10);

// 2. 文本搜索
db.articles.find({
  $text: { $search: "MongoDB 索引" }
}, {
  score: { $meta: "textScore" }
}).sort({
  score: { $meta: "textScore" }
});

// 3. 聚合统计
db.articles.aggregate([
  { $match: { status: "published" } },
  { $unwind: "$tags" },
  { $group: { _id: "$tags", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
]);

// 4. 更新评论（原子操作）
db.articles.updateOne(
  { _id: articleId, "comments._id": commentId },
  { $inc: { "comments.$.likes": 1 } }
);
```

## AI 輔助 Redis

### Redis 資料結構

```
你：
Redis 有哪些数据结构？如何选择？

AI：
## Redis 数据结构

| 结构 | 命令 | 适用场景 |
|------|------|----------|
| String | SET/GET | 缓存、计数器、简单值 |
| Hash | HSET/HGET | 对象、配置 |
| List | LPUSH/RPOP | 队列、时间线 |
| Set | SADD/SMEMBERS | 标签、好友关系 |
| Sorted Set | ZADD/ZRANGE | 排行榜、优先级队列 |
| Bitmap | SETBIT | 用户签到、布隆过滤器 |
| HyperLogLog | PFADD | 统计独立用户数 |
| Stream | XADD/XREAD | 消息队列、事件流 |

### String
```javascript
// 缓存页面
await redis.setex('page:1', 3600, htmlContent);
const content = await redis.get('page:1');

// 计数器
await redis.incr('view_count:article:123');
const count = await redis.get('view_count:article:123');

// 分布式锁
await redis.set('lock:order:123', clientId, 'NX', 'EX', 30);
```

### Hash
```javascript
// 用户对象
await redis.hset('user:1001', {
  name: '张三',
  email: 'zhang@example.com',
  age: 25
});

const user = await redis.hgetall('user:1001');
await redis.hincrby('user:1001', 'age', 1);
```

### List
```javascript
// 消息队列
await redis.lpush('queue:tasks', JSON.stringify({ task: 'send_email' }));
const task = await redis.rpop('queue:tasks');

// 最新消息列表
await redis.lpush('user:1001:feed', JSON.stringify({ content: 'Hello' }));
const feed = await redis.lrange('user:1001:feed', 0, 9);
```

### Sorted Set
```javascript
// 排行榜
await redis.zadd('leaderboard', 1000, 'user:1001');
await redis.zadd('leaderboard', 2000, 'user:1002');
await redis.zadd('leaderboard', 1500, 'user:1003');

// 获取 Top 10
const top10 = await redis.zrevrange('leaderboard', 0, 9, 'WITHSCORES');

// 获取用户排名
const rank = await redis.zrevrank('leaderboard', 'user:1001');
```

### Bitmap
```javascript
// 用户签到
const date = new Date().toISOString().slice(0, 10); // 2024-01-15
await redis.setbit(`sign:${userId}:${date.slice(0, 7)}`, parseInt(date.slice(-2)) - 1, 1);

// 检查签到
const signed = await redis.getbit(`sign:${userId}:2024-01`, 14);
```
```

## 訊息佇列

### 為什麼需要訊息佇列

```
┌─────────────────────────────────────────────────────────┐
│                   消息队列 的价值                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   解耦                          削峰填谷                  │
│   ┌─────┐    ┌─────┐           ┌─────────────────┐     │
│   │服务A│───→│队列 │───→┌─────┐│ 输入：10000/秒  │     │
│   └─────┘    └─────┘   │服务B││ 输出：100/秒    │     │
│                        │服务C││ 队列：吸收峰值    │     │
│   异步                  └─────┘└─────────────────┘     │
│   ┌─────┐                      │                        │
│   │同步 │───→ 耗时 1 秒         │                        │
│   └─────┘                      │                        │
│   ┌─────┐    ┌─────┐           │                        │
│   │發布 │───→│隊列 │───→ 異步處理                       │
│   └─────┘    └─────┘           │                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### AI 輔助訊息佇列設計

```
你：
请帮我设计一个订单处理的消息队列系统。

AI：
## 订单处理消息队列

### 架构设计
```
用户下单 ──→ 订单服务 ──→ 创建订单 ──→ 发送消息
                                       │
                                       ↓
                              ┌────────────────┐
                              │   订单消息队列  │
                              └────────────────┘
                                       │
              ┌────────────────────────┼────────────────────────┐
              ↓                        ↓                        ↓
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   支付服务       │    │   库存服务       │    │   物流服务       │
    │                 │    │                 │    │                 │
    │ - 扣款           │    │ - 扣减库存       │    │ - 创建配送       │
    │ - 发送通知       │    │ - 检查库存       │    │ - 发送通知       │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### RabbitMQ 配置
```javascript
// 连接
const amqp = require('amqplib');
const conn = await amqp.connect('amqp://localhost');

// 创建通道
const channel = await conn.createChannel();

// 交换机
await channel.assertExchange('order.events', 'topic', {
  durable: true
});

// 队列
await channel.assertQueue('order.payment', { durable: true });
await channel.assertQueue('order.inventory', { durable: true });
await channel.assertQueue('order.notification', { durable: true });

// 绑定
channel.bindQueue('order.payment', 'order.events', 'order.created');
channel.bindQueue('order.inventory', 'order.events', 'order.created');
channel.bindQueue('order.notification', 'order.events', 'order.*');

// 消费者
channel.consume('order.payment', async (msg) => {
  const order = JSON.parse(msg.content);
  try {
    await processPayment(order);
    channel.ack(msg);
  } catch (error) {
    // 死信队列或重试
    channel.nack(msg, false, true);
  }
});
```

### 发布消息
```javascript
async function createOrder(orderData) {
  // 创建订单
  const order = await db.orders.create(orderData);
  
  // 发布事件
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

### Kafka 配置（适合高吞吐）
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

// 生产消息
await producer.send({
  topic: 'order-events',
  messages: [
    { key: order.userId.toString(), value: JSON.stringify(order) }
  ]
});
```
```

### 訊息佇列對比

```
你：
RabbitMQ vs Kafka vs Redis Streams 怎么选？

AI：
## 消息队列对比

| 特性 | RabbitMQ | Kafka | Redis Streams |
|------|----------|-------|--------------|
| 吞吐量 | 中等 | 极高 | 中等 |
| 延迟 | 低 | 中等 | 极低 |
| 消息持久化 | 支持 | 支持 | 支持 |
| 消息顺序 | 按队列 | 分区有序 | 按消费者组 |
| 消息确认 | 支持 | 支持 | 支持 |
| 死信队列 | 原生支持 | 需要配置 | 需要手动 |
| 运维复杂度 | 中 | 高 | 低 |
| 适用场景 | 任务队列 | 日志/流处理 | 轻量队列 |

### 选择建议
```
高吞吐量 + 日志分析 → Kafka
复杂路由 + 任务队列 → RabbitMQ
轻量 + 低延迟 → Redis Streams
团队小 + 快速实现 → Redis Streams
微服务 + 企业级 → RabbitMQ
大数据 + 实时分析 → Kafka
```
```

## 實踐練習

```
1. 评估你的系统是否需要 NoSQL
2. 选择合适的 NoSQL 数据库
3. 设计数据模型
4. 配置 Redis（如果需要）
5. 设计消息队列架构
6. 实现消息生产者/消费者
7. 设置监控和告警
```

**NoSQL 和訊息佇列是現代架構的重要組成。正確選擇和設計，能大大提升系統的彈性和效能。**
