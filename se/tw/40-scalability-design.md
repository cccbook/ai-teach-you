# 40. 系統擴展性設計

## 擴展性的基本原則

```
┌─────────────────────────────────────────────────────────┐
│                   扩展性原则                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   水平扩展优于垂直扩展                                   │
│   └─ 增加机器 > 增加单机配置                            │
│                                                         │
│   无状态设计                                             │
│   └─ 会话存储在外部                                     │
│                                                         │
│   弹性伸缩                                              │
│   └─ 根据负载自动增减资源                               │
│                                                         │
│   冗余设计                                              │
│   └─ 多副本容错                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助擴展性設計

### 無狀態設計

```
你：
如何设计无状态应用？

AI：
## 无状态设计

### 有状态 vs 无状态
```javascript
// ❌ 有状态 - 会话存储在内存
const sessions = new Map();

app.post('/login', (req, res) => {
  const user = authenticate(req.body);
  sessions.set(req.sessionId, user);  // 内存存储
  res.json({ token: req.sessionId });
});
```

```javascript
// ✅ 无状态 - JWT Token
app.post('/login', (req, res) => {
  const user = authenticate(req.body);
  const token = jwt.sign({ userId: user.id }, SECRET);
  res.json({ token });
});

// JWT 自包含用户信息，无需服务端存储
app.get('/profile', authenticateJWT, (req, res) => {
  // 用户信息在 JWT 中
  res.json({ userId: req.user.userId });
});
```

### 分布式会话
```javascript
// Redis 存储会话
const session = require('express-session');
const RedisStore = require('connect-redis');

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: 'keyboard cat',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,
    httpOnly: true,
    maxAge: 1000 * 60 * 60 * 24  // 1 天
  }
}));
```

### 无状态数据库连接
```javascript
// ❌ 在应用层保持连接
let dbConnection;

async function initDb() {
  dbConnection = await mysql.createConnection();
}
```

```javascript
// ✅ 使用连接池
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  database: 'test',
  waitForConnections: true,
  connectionLimit: 10,
  maxIdle: 10,
  idleTimeout: 60000,
  queueLimit: 0
});

// 连接池自动管理连接生命周期
async function query(sql, params) {
  const [rows] = await pool.execute(sql, params);
  return rows;
}
```

## 負載均衡

```
你：
如何实现负载均衡？

AI：
## 负载均衡

### 1. DNS 负载均衡
```dns
# DNS A 记录轮询
api.example.com.    300    A    10.0.0.1
api.example.com.    300    A    10.0.0.2
api.example.com.    300    A    10.0.0.3
```

### 2. Nginx 负载均衡
```nginx
upstream backend {
    least_conn;              # 最少连接
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080 backup;  # 备用服务器
}

server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Kubernetes Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
  # 默认轮询负载均衡
```

### 4. 负载均衡算法
```javascript
// 随机
const server = servers[Math.floor(Math.random() * servers.length)];

// 轮询
let currentIndex = 0;
const server = servers[currentIndex++ % servers.length];

// 最少连接
const server = servers.reduce((min, s) => 
  s.connections < min.connections ? s : min
);

// 加权轮询
const totalWeight = servers.reduce((sum, s) => sum + s.weight, 0);
let random = Math.random() * totalWeight;
const server = servers.find(s => {
  random -= s.weight;
  return random <= 0;
});
```

## 自動擴展

```
你：
如何实现自动扩展？

AI：
## 自动扩展

### Kubernetes HPA
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70  # CPU 70% 时扩容
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### 自定义指标扩缩容
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Pods
      pods:
        metric:
          name: requests_per_second
        target:
          type: AverageValue
          averageValue: "100"  # 每秒 100 请求时扩容
```

### 预扩展
```javascript
// 促销前预热
async function preScale(event) {
  if (event.type === 'PROMOTION_STARTING') {
    await k8sApi.scaleDeployment({
      name: 'myapp',
      namespace: 'default',
      body: { spec: { replicas: 20 } }
    });
  }
}
```

## 資料庫擴展

```
你：
数据库如何扩展？

AI：
## 数据库扩展策略

### 1. 读写分离
```yaml
# 写入：主库
# 读取：从库
# 同步：MySQL binlog / PostgreSQL WAL
```

```javascript
// 路由读写
function getDbConnection(isWrite) {
  if (isWrite) {
    return masterPool;
  }
  return Math.random() > 0.5 ? slavePool1 : slavePool2;
}

// 使用
async function createUser(data) {
  return getDbConnection(true).query(
    'INSERT INTO users VALUES (?, ?)',
    [data.id, data.name]
  );
}

async function getUser(id) {
  return getDbConnection(false).query(
    'SELECT * FROM users WHERE id = ?',
    [id]
  );
}
```

### 2. 分库分表
```javascript
// 哈希分片
function getShard(userId) {
  const shardCount = 4;
  const shardIndex = hash(userId) % shardCount;
  return `users_${shardIndex}`;
}

// 按时间分表
function getMonthlyTable(prefix) {
  const now = new Date();
  const month = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}`;
  return `${prefix}_${month}`;
}
```

### 3. 分片中间件
```javascript
// Vitess / CockroachDB / TiDB
// 自动处理分片逻辑
```

### 4. 扩展策略路线图
```
阶段 1: 读写分离
├─ 简单
├─ 提升读性能
└─ 适用：读多写少

阶段 2: 按业务分库
├─ 按功能拆分
└─ 适用：微服务架构

阶段 3: 按数据分片
├─ 哈希/范围分片
├─ 复杂度高
└─ 适用：数据量巨大

阶段 4: 分布式数据库
├─ 无需分片逻辑
└─ 适用：超大规模
```

## 容錯設計

```
你：
如何设计容错系统？

AI：
## 容错设计

### 1. 熔断器
```javascript
class CircuitBreaker {
  constructor() {
    this.state = 'CLOSED';
    this.failureCount = 0;
    this.failureThreshold = 5;
    this.resetTimeout = 60000;
  }
  
  async execute(fn) {
    if (this.state === 'OPEN') {
      throw new Error('Circuit is open');
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }
  
  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      setTimeout(() => {
        this.state = 'HALF_OPEN';
      }, this.resetTimeout);
    }
  }
}

// 使用
const breaker = new CircuitBreaker();

app.get('/recommendations', async (req, res) => {
  try {
    const result = await breaker.execute(() => recommendService.get());
    res.json(result);
  } catch (error) {
    res.json(getFallbackRecommendations());  // 返回降级数据
  }
});
```

### 2. 重试机制
```javascript
async function retry(fn, maxAttempts = 3, delay = 1000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      
      console.log(`Attempt ${attempt} failed, retrying in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
      delay *= 2;  // 指数退避
    }
  }
}

// 使用
const result = await retry(
  () => externalApi.call(),
  3,
  1000
);
```

### 3. 超时控制
```javascript
// 全局超时配置
const DEFAULT_TIMEOUT = 5000;

async function withTimeout(promise, timeout = DEFAULT_TIMEOUT) {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), timeout)
    )
  ]);
}

// 使用
try {
  const result = await withTimeout(externalService.call(), 3000);
} catch (error) {
  if (error.message === 'Timeout') {
    // 处理超时
  }
}
```

### 4. 限流
```javascript
// 滑动窗口限流
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = new Map();
  }
  
  isAllowed(key) {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    // 清理过期记录
    const requests = (this.requests.get(key) || []).filter(t => t > windowStart);
    this.requests.set(key, requests);
    
    if (requests.length >= this.maxRequests) {
      return false;
    }
    
    requests.push(now);
    return true;
  }
}

const limiter = new RateLimiter(100, 60000);  // 1 分钟 100 次

app.use((req, res, next) => {
  if (!limiter.isAllowed(req.ip)) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  next();
});
```

### 5. 降级策略
```javascript
async function getProductWithFallback(productId) {
  try {
    // 尝试获取实时数据
    const product = await productService.get(productId);
    return product;
  } catch (error) {
    // 返回缓存的降级数据
    const cachedProduct = await redis.get(`product:${productId}:fallback`);
    if (cachedProduct) {
      return JSON.parse(cachedProduct);
    }
    
    // 返回默认降级响应
    return {
      id: productId,
      name: '默认商品',
      price: 0,
      _fallback: true
    };
  }
}
```

## 實踐練習

```
1. 评估当前架构的扩展性
2. 实现无状态设计
3. 配置负载均衡
4. 设置自动扩展
5. 实施容错机制
6. 进行压力测试
7. 持续监控和优化
```

**好的擴展性設計讓系統可以應對未來的增长，而不需要大規模重寫。**
