# 28. Performance Optimization and Scaling

## Core Mindset for Performance Optimization

```
┌─────────────────────────────────────────────────────────┐
│               Performance Optimization Mindset             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Don't optimize what doesn't need optimizing            │
│        ↓                                                │
│   Measure first, then optimize                           │
│        ↓                                                │
│   Find bottlenecks, optimize targeted                    │
│        ↓                                                │
│   Balance cost vs. benefit                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Measurement Tools

```
You:
How to measure application performance bottlenecks?

AI:
## Performance Measurement Tools

### Frontend Performance
```
Tools:
├─ Chrome DevTools Performance
├─ Lighthouse
├─ WebPageTest
└─ PageSpeed Insights

Key metrics:
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Time to Interactive (TTI)
- Cumulative Layout Shift (CLS)
```

### Backend Performance
```
Tools:
├─ APM (Application Performance Monitoring)
│   ├─ Datadog APM
│   ├─ New Relic
│   └─ OpenTelemetry + Jaeger
│
├─ Profiling
│   ├─ Py-Spy (Python)
│   ├─ clinic.js (Node.js)
│   └─ async-profiler (Java)
│
└─ Database
    ├─ EXPLAIN ANALYZE
    └─ pg_stat_statements (PostgreSQL)
```

### Measurement Example
```sql
-- PostgreSQL query analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';

-- Output
Gather  (cost=1000.00..50000.00 rows=10000 width=500)
       (actual time=50.234..150.567 rows=5000 loops=1)
  Buffers: shared hit=1000 read=500
  ->  Hash Left Join  (cost=500.00..40000.00 rows=10000)
        (actual time=50.123..120.345 rows=5000)
        Hash Cond: (u.id = o.user_id)
        Buffers: shared hit=1000 read=500
        ->  Seq Scan on users  (cost=0.00..30000.00 rows=10000)
              Filter: (created_at > '2024-01-01')
              Rows Removed by Filter: 5000
        ->  Hash  (cost=300.00..300.00 rows=10000)
              ->  Seq Scan on orders
```

### Frontend Performance Measurement
```javascript
// Using Performance API
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    console.log(`${entry.name}: ${entry.duration}ms`);
  });
});

observer.observe({ entryTypes: ['measure', 'paint'] });

// LCP measurement
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP:', lastEntry.startTime);
}).observe({ entryTypes: ['largest-contentful-paint'] });
```

## Frontend Optimization

```
You:
What are the methods for frontend performance optimization?

AI:
## Frontend Optimization Strategies

### 1. Resource Loading Optimization
```
Reduce requests:
├─ Code splitting
├─ Lazy loading
├─ Merge files
└─ Inline small assets

Cache optimization:
├─ Aggressive caching (Cache-Control)
├─ Negotiated caching (ETag/Last-Modified)
└─ CDN caching
```

### 2. Code Splitting
```javascript
// React lazy loading
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### 3. Image Optimization
```
Format selection:
├─ WebP (recommended)
├─ AVIF (smaller)
├─ PNG (transparency)
└─ JPEG (photos)

Optimization strategies:
├─ Responsive images (srcset)
├─ Lazy loading
├─ Compression
└─ CDN optimization
```

```html
<!-- Responsive images -->
<img 
  src="image-400.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  loading="lazy"
  alt="..."
>
```

### 4. Rendering Optimization
```css
/* Avoid repaints and reflows */
.box {
  /* Changing transform/opacity doesn't trigger reflow */
  transform: translateX(100px); /* Recommended */
  opacity: 0.5; /* Recommended */
  
  /* The following trigger reflow, avoid frequent changes */
  /* width, height, margin, padding */
}

/* Use will-change for animated content */
.animated {
  will-change: transform;
  transform: translateZ(0); /* Force GPU acceleration */
}
```

```javascript
// React optimization
const MemoizedComponent = React.memo(({ data }) => {
  return <div>{data.map(item => <Item key={item.id} {...item} />)}</div>;
});

// Hooks optimization
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
const memoizedCallback = useCallback(() => doSomething(a, b), [a, b]);
```

### 5. Network Optimization
```html
<!-- Preload critical resources -->
<link rel="preload" href="font.woff2" as="font" crossorigin>
<link rel="preconnect" href="https://api.example.com">

<!-- Prefetch resources that may be needed later -->
<link rel="prefetch" href="next-page.html">
```

## Backend Optimization

### Database Optimization

```
You:
What are the methods for database performance optimization?

AI:
## Database Optimization

### 1. Index Optimization
```sql
-- Create appropriate indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Composite index order: equality fields first
CREATE INDEX idx_orders_status_user ON orders(status, user_id);
-- Suitable for WHERE status = 'pending' AND user_id = ?

-- Avoid index invalidation
-- ❌ LIKE '%xxx' prefix wildcard
-- ✅ LIKE 'xxx%' suffix wildcard
```

### 2. Query Optimization
```sql
-- ❌ N+1 queries
SELECT * FROM orders;
-- In loop:
SELECT * FROM users WHERE id = ?  -- N times

-- ✅ JOIN query
SELECT o.*, u.name 
FROM orders o
JOIN users u ON o.user_id = u.id;

-- ✅ Batch queries
-- ❌ Loop inserts
-- ✅ Batch insert
INSERT INTO users (name, email) VALUES 
  ('A', 'a@test.com'),
  ('B', 'b@test.com');
```

### 3. Connection Pool Optimization
```javascript
// Node.js example
const pool = new Pool({
  max: 20,          // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Usage
const result = await pool.query('SELECT * FROM users');
// No need to manually release, pool recycles
```

### 4. Cache Strategy
```javascript
// Redis cache
async function getUserWithCache(userId) {
  const cacheKey = `user:${userId}`;
  
  // Check cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // Cache miss, query database
  const user = await db.users.findById(userId);
  
  // Write to cache
  await redis.setex(cacheKey, 3600, JSON.stringify(user));
  
  return user;
}
```

### 5. Pagination Optimization
```sql
-- ❌ OFFSET pagination (slow with large data)
SELECT * FROM orders ORDER BY id LIMIT 1000000, 20;

-- ✅ Cursor pagination (recommended)
-- Last item from previous page: id = 1000
SELECT * FROM orders 
WHERE id > 1000 
ORDER BY id 
LIMIT 20;
```

## Caching Strategies

```
You:
What are caching strategies? How to choose?

AI:
## Caching Strategies

### Caching Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| Cache-Aside | App manages cache | General |
| Read-Through | Cache auto-loads | Read-heavy, write-light |
| Write-Through | Sync update on write | High consistency needs |
| Write-Behind | Async write to cache | Write performance |

### Cache-Aside Pattern
```
Read:
App → Cache → (hit) → Return
         ↓ (miss)
       Database → Write to cache → Return

Write:
App → Database → Delete cache (not update)
```

### Cache Invalidation Strategies
```javascript
// 1. TTL (Time To Live)
await redis.setex(key, 3600, value);  // Expires in 1 hour

// 2. LRU (Least Recently Used)
// Redis default policy

// 3. Active invalidation
await redis.del(key);  // Delete cache
```

### Cache Problems

| Problem | Description | Solution |
|---------|-------------|----------|
| Cache penetration | Query non-existent data | Bloom filter/null value cache |
| Cache breakdown | Hot key expires | Mutex/never expire |
| Cache avalanche | Mass key expiration | Randomize expiration times |

```javascript
// Cache penetration: null value caching
const value = await cache.get(key);
if (value === null) {
  const dbValue = await db.get(key);
  if (!dbValue) {
    await cache.setex(key, 60, 'NULL');  // Short-term null cache
  } else {
    await cache.setex(key, 3600, dbValue);
  }
}

// Cache breakdown: mutex
const lock = await redis.set(key, '1', 'NX', 'EX', 10);
if (lock) {
  const value = await db.get(key);
  await cache.set(key, value);
  await redis.del(key + '_lock');
}
```

## Scaling Strategies

```
You:
How to scale a system?

AI:
## Scaling Strategies

### Vertical Scaling (Scale Up)
```
Increase single machine resources:
├─ CPU
├─ Memory
├─ Disk
└─ Network bandwidth

Pros: Simple
Cons: Has limits
```

### Horizontal Scaling (Scale Out)
```
Increase machine count:

Single instance           →    Multiple instances
   ↓                              ↓
┌─────────┐              ┌─────┬─────┬─────┐
│  Server │              │ S1  │ S2  │ S3  │
└─────────┘              └─────┴─────┴─────┘
                               ↓
                          Load balancer
```

### Scaling Dimensions

| Dimension | Method | Tools |
|-----------|--------|-------|
| Web layer | Horizontal scaling | Load balancer |
| App layer | Stateless design | K8s HPA |
| Database layer | Read replicas/sharding | ProxySQL/Citus |
| Cache layer | Redis Cluster | Consistent hashing |
| Storage layer | Object storage/CDN | S3/OSS |

### Stateless Design
```javascript
// ❌ Stateful: session in memory
const session = {};
session[userId] = { ... };

// ✅ Stateless: session in external storage
const session = await redis.get(`session:${sessionId}`);
```

### Database Scaling Roadmap
```
Step 1: Read replicas
┌──────────┐     ┌──────────┐
│ Primary  │ ←── │ Replica  │
│ (write)  │     │ (read)   │
└──────────┘     └──────────┘

Step 2: Database sharding
Sharded by business: users, orders, products

Step 3: Table sharding
Horizontal sharding: user_0, user_1, user_2...

Step 4: Distributed database
Citus, TiDB, CockroachDB
```

## Load Testing

```
You:
How to perform load testing?

AI:
## Load Testing

### Tool Selection
```
├─ k6 (recommended) - Script-friendly
├─ Artillery - Node.js
├─ JMeter - Java, full-featured
├─ Locust - Python, distributed
└─ wrk - Simple and fast
```

### k6 Example
```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Warmup
    { duration: '5m', target: 100 },   // Stable
    { duration: '2m', target: 200 },   // Stress test
    { duration: '5m', target: 200 },   // High load
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% requests < 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

### Run
```bash
# Local run
k6 run load-test.js

# Cloud distributed run
k6 run cloud -o cloud load-test.js
```

### Analyze Results
```
     ✓ status is 200
     ✓ response time < 500ms

   ████████████████████████████████████████ 100%

  http_req_duration...
    avg: 150ms
    min: 50ms
    med: 120ms
    max: 450ms
    p95: 280ms
    p99: 380ms
```

## Practice Exercises

```
1. Set up performance monitoring
2. Run baseline tests
3. Identify performance bottlenecks
4. Implement optimizations
5. Test again to verify
6. Document performance targets
7. Regular regression tests
```

**Performance optimization is an ongoing process. Measure, optimize, measure again.**
