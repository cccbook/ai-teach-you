# 39. Caching Strategies and Data Consistency

## Cache Levels

```
┌─────────────────────────────────────────────────────────┐
│                   Cache Hierarchy                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Browser Cache                                          │
│   ├─ HTTP Cache (strong cache/negotiated cache)         │
│   └─ LocalStorage/SessionStorage                       │
│                                                         │
│   CDN Edge Cache                                         │
│   ├─ Static resource caching                           │
│   └─ API response caching                               │
│                                                         │
│   Application Cache                                       │
│   ├─ Redis/Memcached                                   │
│   └─ Local in-memory cache                             │
│                                                         │
│   Database Cache                                         │
│   ├─ Query cache                                        │
│   └─ Buffer Pool                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Cache Design

### HTTP Caching

```
You:
How do I configure HTTP caching?

AI:
## HTTP Caching

### 1. Strong Cache (Cache-Control)
```javascript
// Express set strong cache
app.use('/static', express.static('public', {
  maxAge: '7d',           // Use cache directly within 7 days
  etag: true,             // Generate ETag
  lastModified: true       // Use Last-Modified
}));

// Disable caching
app.use((req, res, next) => {
  res.set('Cache-Control', 'no-store');
  next();
});
```

### 2. Negotiated Cache
```javascript
// Check If-None-Match
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

### 3. Caching Strategies for Different Resources
```javascript
// Static assets - long-term cache
response.set('Cache-Control', 'public, max-age=31536000, immutable');

// API responses - short-term or no cache
response.set('Cache-Control', 'private, no-store');

// User-specific data - no cache
response.set('Cache-Control', 'private, no-cache, must-revalidate');
```

### 4. Cache-Control Directives
```
max-age=3600     - Cache valid for 1 hour
s-maxage=7200    - Shared cache valid for 2 hours
no-cache         - Always validate
no-store         - Never cache at all
public           - Can be stored by any cache
private          - Only browser caching allowed
immutable        - Resources that never change
```

## Redis Caching Patterns

```
You:
What are the Redis caching patterns?

AI:
## Redis Caching Patterns

### 1. Cache-Aside (Lazy Loading)
```javascript
// Read
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

// Write
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  await redis.del(`user:${userId}`);  // Delete cache, don't update
}
```

### 2. Read-Through
```javascript
// Cache auto-loading
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
// Synchronously update cache
async function saveUser(user) {
  await db.users.save(user);
  await redis.set(`user:${user.id}`, JSON.stringify(user));
}
```

### 4. Write-Behind
```javascript
// Asynchronously write to cache
async function saveUser(user) {
  await db.users.save(user);
  
  // Asynchronously update cache
  setImmediate(() => {
    redis.set(`user:${user.id}`, JSON.stringify(user));
  });
}
```

### 5. Cache Problems and Solutions

```javascript
// Cache penetration
async function getUser(userId) {
  const cacheKey = `user:${userId}`;
  const cached = await redis.get(cacheKey);
  
  if (cached === 'NULL') {
    return null;  // Previously unfound null value
  }
  
  if (!cached) {
    const user = await db.users.findById(userId);
    
    if (!user) {
      await redis.setex(cacheKey, 60, 'NULL');  // Short-term cache for null
    } else {
      await redis.setex(cacheKey, 3600, JSON.stringify(user));
    }
    
    return user;
  }
  
  return JSON.parse(cached);
}

// Cache busting
async function getProductWithLock(productId) {
  const cacheKey = `product:${productId}`;
  
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Acquire lock
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
    // Wait and retry
    await new Promise(resolve => setTimeout(resolve, 100));
    return getProductWithLock(productId);
  }
}

// Cache avalanche
// Solution 1: Randomize expiration time
const ttl = 3600 + Math.random() * 600;  // 1 hour to 1 hour 10 minutes

// Solution 2: Never expire + async update
async function getProduct(productId) {
  let product = await redis.get(`product:${productId}`);
  
  if (!product) {
    product = await db.products.findById(productId);
    await redis.set(`product:${productId}`, JSON.stringify(product));
  }
  
  return product;
}
```

## Data Consistency

```
You:
How do I ensure consistency between cache and database?

AI:
## Cache Consistency Strategies

### 1. Cache-Aside (Most Common)
```
Read:
App → Cache → Hit → Return
        ↓ Miss
    Database → Write to Cache → Return

Write:
App → Database → Delete Cache
```

### 2. Delete vs Update
```javascript
// ❌ Update cache
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  await redis.set(`user:${userId}`, JSON.stringify(newData));  // Problem
}

// ✅ Delete cache
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  await redis.del(`user:${userId}`);  // Correct
}

// Why?
// In concurrent scenarios:
// Thread A: WriteDB(A data) → UpdateCache(A data)
// Thread B: WriteDB(B data) → UpdateCache(B data) → Error! Cache becomes A data
```

### 3. Dual Write (Not Recommended)
```javascript
// Write to both cache and database simultaneously
async function updateUser(userId, data) {
  await Promise.all([
    db.users.update(userId, data),
    redis.set(`user:${userId}`, JSON.stringify(data))
  ]);
}

// Problems:
// - Only one of the two writes might succeed
// - Database and cache may be inconsistent
```

### 4. Eventual Consistency vs Strong Consistency
```javascript
// Eventual consistency (acceptable delay)
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  await redis.del(`user:${userId}`);  // Cache will eventually be updated
}

// Strong consistency (needs synchronization)
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

### 5. Delayed Double Delete
```javascript
async function updateUser(userId, data) {
  // 1. Delete cache first
  await redis.del(`user:${userId}`);
  
  // 2. Update database
  await db.users.update(userId, data);
  
  // 3. Delete again after a delay
  setTimeout(async () => {
    await redis.del(`user:${userId}`);
  }, 500);
}
```

## Multi-Level Caching

```
You:
How do I design multi-level caching?

AI:
## Multi-Level Cache Architecture

### Architecture
```
Request → L1 (Local Cache) → L2 (Redis) → Database
           ↓ Hit               ↓ Hit
          Return              Return
```

### Implementation
```javascript
class MultiLevelCache {
  constructor() {
    this.localCache = new Map();  // L1: Local memory
    this.redis = new Redis();    // L2: Redis
  }
  
  async get(key) {
    // L1 query
    const l1Value = this.localCache.get(key);
    if (l1Value && !this.isExpired(l1Value)) {
      return l1Value.data;
    }
    
    // L2 query
    const l2Value = await this.redis.get(key);
    if (l2Value) {
      const data = JSON.parse(l2Value);
      // Backfill L1
      this.localCache.set(key, {
        data,
        expireAt: Date.now() + 60000  // 1 minute
      });
      return data;
    }
    
    return null;
  }
  
  async set(key, value, ttl = 3600) {
    // Write to both L1 and L2 simultaneously
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

### Cache Warming
```javascript
async function warmUpCache() {
  // Preload hot data
  const hotProducts = await db.products.findHot({ limit: 100 });
  
  for (const product of hotProducts) {
    await cache.set(`product:${product.id}`, product, 3600);
  }
  
  // Scheduled warming
  cron.schedule('0 * * * *', warmUpCache);  // Every hour
}
```

## Hands-On Exercises

```
1. Analyze data access patterns
2. Choose caching strategy
3. Implement cache layer
4. Handle cache problems
5. Set expiration times
6. Monitor cache hit rate
7. Regularly optimize
```

**Cache is a silver bullet, but not a万能药 (panacea). Proper use of caching can greatly improve performance, but misuse leads to data inconsistency.**

(End of file - total 417 lines)
