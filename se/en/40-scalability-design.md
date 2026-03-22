# 40. System Scalability Design

## Fundamental Principles of Scalability

```
┌─────────────────────────────────────────────────────────┐
│                   Scalability Principles                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Horizontal scaling over vertical scaling               │
│   └─ Add machines > Add single machine specs            │
│                                                         │
│   Stateless design                                       │
│   └─ Store sessions externally                          │
│                                                         │
│   Elastic scaling                                        │
│   └─ Automatically adjust resources based on load        │
│                                                         │
│   Redundancy design                                      │
│   └─ Multiple replicas for fault tolerance             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Scalability Design

### Stateless Design

```
You:
How do I design stateless applications?

AI:
## Stateless Design

### Stateful vs Stateless
```javascript
// ❌ Stateful - sessions stored in memory
const sessions = new Map();

app.post('/login', (req, res) => {
  const user = authenticate(req.body);
  sessions.set(req.sessionId, user);  // In-memory storage
  res.json({ token: req.sessionId });
});
```

```javascript
// ✅ Stateless - JWT Token
app.post('/login', (req, res) => {
  const user = authenticate(req.body);
  const token = jwt.sign({ userId: user.id }, SECRET);
  res.json({ token });
});

// JWT contains user info, no server-side storage needed
app.get('/profile', authenticateJWT, (req, res) => {
  // User info is in JWT
  res.json({ userId: req.user.userId });
});
```

### Distributed Sessions
```javascript
// Redis session storage
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
    maxAge: 1000 * 60 * 60 * 24  // 1 day
  }
}));
```

### Stateless Database Connections
```javascript
// ❌ Maintain connection at application layer
let dbConnection;

async function initDb() {
  dbConnection = await mysql.createConnection();
}
```

```javascript
// ✅ Use connection pool
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

// Connection pool manages connection lifecycle automatically
async function query(sql, params) {
  const [rows] = await pool.execute(sql, params);
  return rows;
}
```

## Load Balancing

```
You:
How do I implement load balancing?

AI:
## Load Balancing

### 1. DNS Load Balancing
```dns
# DNS A record round-robin
api.example.com.    300    A    10.0.0.1
api.example.com.    300    A    10.0.0.2
api.example.com.    300    A    10.0.0.3
```

### 2. Nginx Load Balancing
```nginx
upstream backend {
    least_conn;              # Least connections
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080 backup;  # Backup server
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
  # Default round-robin load balancing
```

### 4. Load Balancing Algorithms
```javascript
// Random
const server = servers[Math.floor(Math.random() * servers.length)];

// Round-robin
let currentIndex = 0;
const server = servers[currentIndex++ % servers.length];

// Least connections
const server = servers.reduce((min, s) => 
  s.connections < min.connections ? s : min
);

// Weighted round-robin
const totalWeight = servers.reduce((sum, s) => sum + s.weight, 0);
let random = Math.random() * totalWeight;
const server = servers.find(s => {
  random -= s.weight;
  return random <= 0;
});
```

## Auto-Scaling

```
You:
How do I implement auto-scaling?

AI:
## Auto-Scaling

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
          averageUtilization: 70  # Scale up at 70% CPU
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### Custom Metrics Scaling
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
          averageValue: "100"  # Scale at 100 requests per second
```

### Pre-scaling
```javascript
// Warm up before promotions
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

## Database Scaling

```
You:
How do I scale databases?

AI:
## Database Scaling Strategies

### 1. Read/Write Split
```yaml
# Writes: Primary database
# Reads: Replicas
# Sync: MySQL binlog / PostgreSQL WAL
```

```javascript
// Route read/write
function getDbConnection(isWrite) {
  if (isWrite) {
    return masterPool;
  }
  return Math.random() > 0.5 ? slavePool1 : slavePool2;
}

// Usage
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

### 2. Database Sharding
```javascript
// Hash sharding
function getShard(userId) {
  const shardCount = 4;
  const shardIndex = hash(userId) % shardCount;
  return `users_${shardIndex}`;
}

// Time-based sharding
function getMonthlyTable(prefix) {
  const now = new Date();
  const month = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}`;
  return `${prefix}_${month}`;
}
```

### 3. Sharding Middleware
```javascript
// Vitess / CockroachDB / TiDB
// Automatically handles sharding logic
```

### 4. Scaling Strategy Roadmap
```
Phase 1: Read/Write Split
├─ Simple
├─ Improves read performance
└─ Suitable for: Read-heavy workloads

Phase 2: Database per Service
├─ Split by functionality
└─ Suitable for: Microservices architecture

Phase 3: Data Sharding
├─ Hash/range sharding
├─ High complexity
└─ Suitable for: Massive data volumes

Phase 4: Distributed Database
├─ No sharding logic needed
└─ Suitable for: Ultra-large scale
```

## Fault Tolerance Design

```
You:
How do I design fault-tolerant systems?

AI:
## Fault Tolerance Design

### 1. Circuit Breaker
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

// Usage
const breaker = new CircuitBreaker();

app.get('/recommendations', async (req, res) => {
  try {
    const result = await breaker.execute(() => recommendService.get());
    res.json(result);
  } catch (error) {
    res.json(getFallbackRecommendations());  // Return degraded data
  }
});
```

### 2. Retry Mechanism
```javascript
async function retry(fn, maxAttempts = 3, delay = 1000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      
      console.log(`Attempt ${attempt} failed, retrying in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
      delay *= 2;  // Exponential backoff
    }
  }
}

// Usage
const result = await retry(
  () => externalApi.call(),
  3,
  1000
);
```

### 3. Timeout Control
```javascript
// Global timeout configuration
const DEFAULT_TIMEOUT = 5000;

async function withTimeout(promise, timeout = DEFAULT_TIMEOUT) {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), timeout)
    )
  ]);
}

// Usage
try {
  const result = await withTimeout(externalService.call(), 3000);
} catch (error) {
  if (error.message === 'Timeout') {
    // Handle timeout
  }
}
```

### 4. Rate Limiting
```javascript
// Sliding window rate limiter
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = new Map();
  }
  
  isAllowed(key) {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    // Clean up expired records
    const requests = (this.requests.get(key) || []).filter(t => t > windowStart);
    this.requests.set(key, requests);
    
    if (requests.length >= this.maxRequests) {
      return false;
    }
    
    requests.push(now);
    return true;
  }
}

const limiter = new RateLimiter(100, 60000);  // 100 per minute

app.use((req, res, next) => {
  if (!limiter.isAllowed(req.ip)) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  next();
});
```

### 5. Degradation Strategy
```javascript
async function getProductWithFallback(productId) {
  try {
    // Try to get real-time data
    const product = await productService.get(productId);
    return product;
  } catch (error) {
    // Return cached degraded data
    const cachedProduct = await redis.get(`product:${productId}:fallback`);
    if (cachedProduct) {
      return JSON.parse(cachedProduct);
    }
    
    // Return default degraded response
    return {
      id: productId,
      name: 'Default Product',
      price: 0,
      _fallback: true
    };
  }
}
```

## Hands-On Exercises

```
1. Evaluate current architecture scalability
2. Implement stateless design
3. Configure load balancing
4. Set up auto-scaling
5. Implement fault tolerance mechanisms
6. Conduct stress testing
7. Continuously monitor and optimize
```

**Good scalability design allows systems to handle future growth without major rewrites.**

(End of file - total 532 lines)
