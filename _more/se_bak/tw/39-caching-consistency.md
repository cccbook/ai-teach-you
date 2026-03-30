# 39. 快取策略與資料一致性

## 快取層級

```
┌─────────────────────────────────────────────────────────┐
│                   缓存层次结构                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   浏览器缓存                                            │
│   ├─ HTTP Cache (强缓存/协商缓存)                       │
│   └─ LocalStorage/SessionStorage                       │
│                                                         │
│   CDN 边缘缓存                                          │
│   ├─ 静态资源缓存                                       │
│   └─ API 响应缓存                                       │
│                                                         │
│   应用缓存                                              │
│   ├─ Redis/Memcached                                   │
│   └─ 本地内存缓存                                       │
│                                                         │
│   数据库缓存                                            │
│   ├─ 查询缓存                                           │
│   └─ Buffer Pool                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助快取設計

### HTTP 緩存

```
你：
HTTP 缓存如何配置？

AI：
## HTTP 缓存

### 1. 强缓存 (Cache-Control)
```javascript
// Express 设置强缓存
app.use('/static', express.static('public', {
  maxAge: '7d',           // 7 天内直接使用缓存
  etag: true,             // 生成 ETag
  lastModified: true       // 使用 Last-Modified
}));

// 禁止缓存
app.use((req, res, next) => {
  res.set('Cache-Control', 'no-store');
  next();
});
```

### 2. 协商缓存
```javascript
// 检查 If-None-Match
app.get('/api/data', (req, res) => {
  const data = getData();
  const etag = generateEtag(data);
  
  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end();  // Not Modified
  }
  
  res.set('ETag', etag);
  res.set('Cache-Control', 'private, max-age=0');
  res.json(data);
});
```

### 3. 不同资源的缓存策略
```javascript
// 静态资源 - 长期缓存
response.set('Cache-Control', 'public, max-age=31536000, immutable');

// API 响应 - 短期或不缓存
response.set('Cache-Control', 'private, no-store');

// 用户特定数据 - 不缓存
response.set('Cache-Control', 'private, no-cache, must-revalidate');
```

### 4. Cache-Control 指令
```
max-age=3600     - 缓存有效期 1 小时
s-maxage=7200    - 共享缓存有效期 2 小时
no-cache         - 每次都要验证
no-store         - 完全不缓存
public           - 可被任何缓存存储
private          - 只允许浏览器缓存
immutable        - 永不变化的资源
```

## Redis 快取模式

```
你：
Redis 缓存有哪些模式？

AI：
## Redis 缓存模式

### 1. Cache-Aside（旁路缓存）
```javascript
// 读
async function getUser(userId) {
  const cacheKey = `user:${userId}`;
  const cached = await redis.get(cacheKey);
  
  if (cached) {
    return JSON.parse(cached);
  }
  
  const user = await db.users.findById(userId);
  await redis.setex(cacheKey, 3600, JSON.stringify(user));
  
  return user;
}

// 写
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  await redis.del(`user:${userId}`);  // 删除缓存，不是更新
}
```

### 2. Read-Through
```javascript
// 缓存自动加载
const cache = new RedisCache({ redis });

async function getProduct(productId) {
  return await cache.getOrSet(
    `product:${productId}`,
    () => db.products.findById(productId),
    { ttl: 3600 }
  );
}
```

### 3. Write-Through
```javascript
// 同步更新缓存
async function saveUser(user) {
  await db.users.save(user);
  await redis.set(`user:${user.id}`, JSON.stringify(user));
}
```

### 4. Write-Behind
```javascript
// 异步写缓存
async function saveUser(user) {
  await db.users.save(user);
  
  // 异步更新缓存
  setImmediate(() => {
    redis.set(`user:${user.id}`, JSON.stringify(user));
  });
}
```

### 5. 缓存问题及解决

```javascript
// 缓存穿透
async function getUser(userId) {
  const cacheKey = `user:${userId}`;
  const cached = await redis.get(cacheKey);
  
  if (cached === 'NULL') {
    return null;  // 之前查不到的空值
  }
  
  if (!cached) {
    const user = await db.users.findById(userId);
    
    if (!user) {
      await redis.setex(cacheKey, 60, 'NULL');  // 短期缓存空值
    } else {
      await redis.setex(cacheKey, 3600, JSON.stringify(user));
    }
    
    return user;
  }
  
  return JSON.parse(cached);
}

// 缓存击穿
async function getProductWithLock(productId) {
  const cacheKey = `product:${productId}`;
  
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // 获取锁
  const lockKey = `lock:${cacheKey}`;
  const lock = await redis.set(lockKey, '1', 'NX', 'EX', 10);
  
  if (lock) {
    try {
      const product = await db.products.findById(productId);
      await redis.setex(cacheKey, 3600, JSON.stringify(product));
      return product;
    } finally {
      await redis.del(lockKey);
    }
  } else {
    // 等待后重试
    await new Promise(resolve => setTimeout(resolve, 100));
    return getProductWithLock(productId);
  }
}

// 缓存雪崩
// 方案 1: 过期时间随机化
const ttl = 3600 + Math.random() * 600;  // 1小时~1小时10分

// 方案 2: 永不过期 + 异步更新
async function getProduct(productId) {
  let product = await redis.get(`product:${productId}`);
  
  if (!product) {
    product = await db.products.findById(productId);
    await redis.set(`product:${productId}`, JSON.stringify(product));
  }
  
  return product;
}
```

## 資料一致性

```
你：
缓存和数据库如何保证一致性？

AI：
## 缓存一致性策略

### 1. Cache-Aside（最常用）
```
读取：
应用 → 缓存 → 命中 → 返回
         ↓ 未命中
       数据库 → 写入缓存 → 返回

写入：
应用 → 数据库 → 删除缓存
```

### 2. 删除 vs 更新
```javascript
// ❌ 更新缓存
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  await redis.set(`user:${userId}`, JSON.stringify(newData));  // 问题
}

// ✅ 删除缓存
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  await redis.del(`user:${userId}`);  // 正确
}

// 为什么？
// 并发情况下：
// 线程A: 写DB(A数据) → 更新缓存(A数据)
// 线程B: 写DB(B数据) → 更新缓存(B数据) → 错误！缓存变成A数据
```

### 3. 双写模式（不推荐）
```javascript
// 同时写缓存和数据库
async function updateUser(userId, data) {
  await Promise.all([
    db.users.update(userId, data),
    redis.set(`user:${userId}`, JSON.stringify(data))
  ]);
}

// 问题：
// - 两个写操作可能只有一个成功
// - 数据库和缓存可能不一致
```

### 4. 最终一致性 vs 强一致性
```javascript
// 最终一致性（可接受延迟）
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  await redis.del(`user:${userId}`);  // 缓存最终会更新
}

// 强一致性（需要同步）
async function updateUser(userId, data) {
  const lock = await acquireLock(`user:${userId}`);
  try {
    await db.users.update(userId, data);
    const user = await db.users.findById(userId);
    await redis.set(`user:${userId}`, JSON.stringify(user));
  } finally {
    releaseLock(lock);
  }
}
```

### 5. 延迟双删
```javascript
async function updateUser(userId, data) {
  // 1. 先删除缓存
  await redis.del(`user:${userId}`);
  
  // 2. 更新数据库
  await db.users.update(userId, data);
  
  // 3. 延迟一段时间后再删除
  setTimeout(async () => {
    await redis.del(`user:${userId}`);
  }, 500);
}
```

## 多級緩存

```
你：
如何设计多级缓存？

AI：
## 多级缓存架构

### 架构
```
请求 → L1 (本地缓存) → L2 (Redis) → 数据库
         ↓命中           ↓命中
        返回             返回
```

### 实现
```javascript
class MultiLevelCache {
  constructor() {
    this.localCache = new Map();  // L1: 本地内存
    this.redis = new Redis();    // L2: Redis
  }
  
  async get(key) {
    // L1 查询
    const l1Value = this.localCache.get(key);
    if (l1Value && !this.isExpired(l1Value)) {
      return l1Value.data;
    }
    
    // L2 查询
    const l2Value = await this.redis.get(key);
    if (l2Value) {
      const data = JSON.parse(l2Value);
      // 回填 L1
      this.localCache.set(key, {
        data,
        expireAt: Date.now() + 60000  // 1 分钟
      });
      return data;
    }
    
    return null;
  }
  
  async set(key, value, ttl = 3600) {
    // 同时写入 L1 和 L2
    this.localCache.set(key, {
      data: value,
      expireAt: Date.now() + 60000
    });
    
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }
  
  async delete(key) {
    this.localCache.delete(key);
    await this.redis.del(key);
  }
}
```

### 缓存预热
```javascript
async function warmUpCache() {
  // 预加载热点数据
  const hotProducts = await db.products.findHot({ limit: 100 });
  
  for (const product of hotProducts) {
    await cache.set(`product:${product.id}`, product, 3600);
  }
  
  // 定时预热
  cron.schedule('0 * * * *', warmUpCache);  // 每小时
}
```

## 實踐練習

```
1. 分析数据访问模式
2. 选择缓存策略
3. 实现缓存层
4. 处理缓存问题
5. 设置过期时间
6. 监控缓存命中率
7. 定期优化
```

**緩存是銀彈，但不是萬能的。正確使用緩存可以大幅提升性能，但錯誤使用會導致數據不一致。**
