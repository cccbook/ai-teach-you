# 28. 效能優化與擴展

## 效能優化的核心思維

```
┌─────────────────────────────────────────────────────────┐
│                 性能优化思维                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   不要优化不必要的地方                                   │
│        ↓                                                │
│   先测量，再优化                                         │
│        ↓                                                │
│   找到瓶颈，针对性优化                                   │
│        ↓                                                │
│   权衡成本与收益                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 測量工具

```
你：
如何测量应用的性能瓶颈？

AI：
## 性能测量工具

### 前端性能
```
工具：
├─ Chrome DevTools Performance
├─ Lighthouse
├─ WebPageTest
└─ PageSpeed Insights

关键指标：
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Time to Interactive (TTI)
- Cumulative Layout Shift (CLS)
```

### 后端性能
```
工具：
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

### 测量示例
```sql
-- PostgreSQL 查询分析
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';

-- 输出
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

### 前端性能测量
```javascript
// 使用 Performance API
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    console.log(`${entry.name}: ${entry.duration}ms`);
  });
});

observer.observe({ entryTypes: ['measure', 'paint'] });

// LCP 测量
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP:', lastEntry.startTime);
}).observe({ entryTypes: ['largest-contentful-paint'] });
```
```

## 前端優化

```
你：
前端性能优化有哪些方法？

AI：
## 前端优化策略

### 1. 资源加载优化
```
减少请求：
├─ 代码分割 (Code Splitting)
├─ 懒加载 (Lazy Loading)
├─ 合并文件
└─ 资源内联 (小文件)

缓存优化：
├─ 强缓存 (Cache-Control)
├─ 协商缓存 (ETag/Last-Modified)
└─ CDN 缓存
```

### 2. 代码分割
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

### 3. 图片优化
```
格式选择：
├─ WebP (推荐)
├─ AVIF (更小)
├─ PNG (透明)
└─ JPEG (照片)

优化策略：
├─ 响应式图片 (srcset)
├─ 懒加载
├─ 压缩
└─ CDN 优化
```

```html
<!-- 响应式图片 -->
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

### 4. 渲染优化
```css
/* 避免重排重绘 */
.box {
  /* 改变 transform/opacity 不触发重排 */
  transform: translateX(100px); /* 推荐 */
  opacity: 0.5; /* 推荐 */
  
  /* 以下会触发重排，避免频繁修改 */
  /* width, height, margin, padding */
}

/* 内容变化使用 will-change */
.animated {
  will-change: transform;
  transform: translateZ(0); /* 强制 GPU 加速 */
}
```

```javascript
// React 优化
const MemoizedComponent = React.memo(({ data }) => {
  return <div>{data.map(item => <Item key={item.id} {...item} />)}</div>;
});

// Hooks 优化
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
const memoizedCallback = useCallback(() => doSomething(a, b), [a, b]);
```

### 5. 网络优化
```html
<!-- 预加载关键资源 -->
<link rel="preload" href="font.woff2" as="font" crossorigin>
<link rel="preconnect" href="https://api.example.com">

<!-- 预取将来可能需要的资源 -->
<link rel="prefetch" href="next-page.html">
```

## 後端優化

### 資料庫優化

```
你：
数据库性能优化有哪些方法？

AI：
## 数据库优化

### 1. 索引优化
```sql
-- 创建合适索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- 复合索引顺序：等值查询字段在前
CREATE INDEX idx_orders_status_user ON orders(status, user_id);
-- 适用于 WHERE status = 'pending' AND user_id = ?

-- 避免索引失效
-- ❌ LIKE '%xxx' 前缀通配符
-- ✅ LIKE 'xxx%' 后缀通配符
```

### 2. 查询优化
```sql
-- ❌ N+1 查询
SELECT * FROM orders;
-- 循环中：
SELECT * FROM users WHERE id = ?  -- N次

-- ✅ JOIN 查询
SELECT o.*, u.name 
FROM orders o
JOIN users u ON o.user_id = u.id;

-- ✅ 批量查询
-- ❌ 循环插入
-- ✅ 批量插入
INSERT INTO users (name, email) VALUES 
  ('A', 'a@test.com'),
  ('B', 'b@test.com');
```

### 3. 连接池优化
```javascript
// Node.js 示例
const pool = new Pool({
  max: 20,          // 最大连接数
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// 使用
const result = await pool.query('SELECT * FROM users');
// 不用手动释放，pool 会回收
```

### 4. 缓存策略
```javascript
// Redis 缓存
async function getUserWithCache(userId) {
  const cacheKey = `user:${userId}`;
  
  // 先查缓存
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // 缓存未命中，查数据库
  const user = await db.users.findById(userId);
  
  // 写入缓存
  await redis.setex(cacheKey, 3600, JSON.stringify(user));
  
  return user;
}
```

### 5. 分页优化
```sql
-- ❌ OFFSET 分页（大数据量慢）
SELECT * FROM orders ORDER BY id LIMIT 1000000, 20;

-- ✅ 游标分页（推荐）
-- 上一页最后一条: id = 1000
SELECT * FROM orders 
WHERE id > 1000 
ORDER BY id 
LIMIT 20;
```

## 快取策略

```
你：
缓存策略有哪些？如何选择？

AI：
## 缓存策略

### 缓存模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| Cache-Aside | 应用自己管理缓存 | 通用 |
| Read-Through | 缓存自动加载 | 读多写少 |
| Write-Through | 写入时同步更新缓存 | 数据一致性要求高 |
| Write-Behind | 异步写入缓存 | 写入性能重要 |

### Cache-Aside 模式
```
读取：
应用 → 缓存 → (命中) → 返回
         ↓ (未命中)
       数据库 → 写入缓存 → 返回

写入：
应用 → 数据库 → 删除缓存（不是更新）
```

### 缓存失效策略
```javascript
// 1. TTL (Time To Live)
await redis.setex(key, 3600, value);  // 1小时后过期

// 2. LRU (Least Recently Used)
// Redis 默认策略

// 3. 主动失效
await redis.del(key);  // 删除缓存
```

### 缓存问题

| 问题 | 描述 | 解决方案 |
|------|------|----------|
| 缓存穿透 | 查询不存在的数据 | 布隆过滤器/空值缓存 |
| 缓存击穿 | 热点 key 过期 | 互斥锁/永不过期 |
| 缓存雪崩 | 大量 key 同时过期 | 过期时间随机化 |

```javascript
// 缓存穿透：空值缓存
const value = await cache.get(key);
if (value === null) {
  const dbValue = await db.get(key);
  if (!dbValue) {
    await cache.setex(key, 60, 'NULL');  // 短期缓存空值
  } else {
    await cache.setex(key, 3600, dbValue);
  }
}

// 缓存击穿：互斥锁
const lock = await redis.set(key, '1', 'NX', 'EX', 10);
if (lock) {
  const value = await db.get(key);
  await cache.set(key, value);
  await redis.del(key + '_lock');
}
```
```

## 擴展策略

```
你：
系统如何扩展？

AI：
## 扩展策略

### 垂直扩展 (Scale Up)
```
增加单机资源：
├─ CPU
├─ 内存
├─ 磁盘
└─ 网络带宽

优点：简单
缺点：有上限
```

### 水平扩展 (Scale Out)
```
增加机器数量：

单实例           →    多实例
   ↓                        ↓
┌─────────┐          ┌─────┬─────┬─────┐
│  Server │          │ S1  │ S2  │ S3  │
└─────────┘          └─────┴─────┴─────┘
                           ↓
                      负载均衡器
```

### 扩展维度

| 维度 | 方法 | 工具 |
|------|------|------|
| Web 层 | 水平扩展 | 负载均衡器 |
| 应用层 | 无状态设计 | K8s HPA |
| 数据库层 | 读写分离/分库分表 | ProxySQL/Citus |
| 缓存层 | Redis Cluster | 一致性哈希 |
| 存储层 | 对象存储/CDN | S3/OSS |

### 无状态设计
```javascript
// ❌ 有状态：session 存在内存
const session = {};
session[userId] = { ... };

// ✅ 无状态：session 存在外部存储
const session = await redis.get(`session:${sessionId}`);
```

### 数据库扩展路线
```
Step 1: 读写分离
┌──────────┐     ┌──────────┐
│ 主库(写) │ ←── │ 从库(读) │
└──────────┘     └──────────┘

Step 2: 分库
按业务拆分：用户库、订单库、商品库

Step 3: 分表
水平分表：user_0, user_1, user_2...

Step 4: 分片
分布式数据库：Citus, TiDB, CockroachDB
```

## 負載測試

```
你：
如何进行负载测试？

AI：
## 负载测试

### 工具选择
```
├─ k6 (推荐) - 脚本友好
├─ Artillery - Node.js
├─ JMeter - Java，功能全
├─ Locust - Python，分布式
└─ wrk - 简单快速
```

### k6 示例
```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // 预热
    { duration: '5m', target: 100 },   // 稳定
    { duration: '2m', target: 200 },   // 压力测试
    { duration: '5m', target: 200 },   // 高负载
    { duration: '2m', target: 0 },     // 下降
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% 请求 < 500ms
    http_req_failed: ['rate<0.01'],    // 错误率 < 1%
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

### 运行
```bash
# 本地运行
k6 run load-test.js

# 云端分布式运行
k6 run cloud -o cloud load-test.js
```

### 分析结果
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
```

## 實踐練習

```
1. 设置性能监控
2. 运行基准测试
3. 识别性能瓶颈
4. 实施优化
5. 再次测试验证
6. 文档化性能目标
7. 定期回归测试
```

**效能優化是持續的過程。測量、優化、再測量。**
