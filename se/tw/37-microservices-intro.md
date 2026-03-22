# 37. 微服務架構入門

## 單體 vs 微服務

```
┌─────────────────────────────────────────────────────────┐
│                   架构演进                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   单体应用                                              │
│   ┌─────────────────────────────┐                       │
│   │  Web │ API │ DB │ 队列 │   │                       │
│   └─────────────────────────────┘                       │
│   优点：简单、部署容易                                  │
│   缺点：扩展困难、技术栈固定                            │
│                                                         │
│   微服务架构                                            │
│   ┌─────┐  ┌─────┐  ┌─────┐                           │
│   │用户 │  │订单 │  │商品 │                           │
│   │服务 │  │服务 │  │服务 │                           │
│   └──┬──┘  └──┬──┘  └──┬──┘                        │
│      │         │         │                             │
│      └─────────┼─────────┘                             │
│                ↓                                       │
│           ┌─────────┐                                  │
│           │  消息   │                                  │
│           │  队列   │                                  │
│           └─────────┘                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助微服務設計

```
你：
什么时候应该使用微服务架构？

AI：
## 微服务适用场景

### 应该使用微服务
```
✓ 大型复杂应用（100+ 开发者）
✓ 需要独立扩展不同模块
✓ 需要使用不同技术栈
✓ 团队已具备 DevOps 能力
✓ 业务领域边界清晰
```

### 不应该使用微服务
```
✗ 小型应用（5 人以下团队）
✗ 创业公司需要快速迭代
✗ 团队缺乏运维经验
✗ 业务边界不清晰
```

### 判断标准
```
问自己：
1. 不同模块的扩展需求是否差异很大？
2. 不同模块是否需要不同技术栈？
3. 团队是否能独立开发和部署？
4. 是否有足够的 DevOps 能力？

如果多数答案是「否」→ 先用单体
如果多数答案是「是」→ 考虑微服务
```

## 服務拆分

```
你：
如何合理拆分微服务？

AI：
## 服务拆分策略

### 1. 按业务能力拆分
```
电商系统拆分：
├─ 用户服务（注册、登录、用户信息）
├─ 商品服务（商品信息、分类、搜索）
├─ 订单服务（创建订单、订单管理）
├─ 支付服务（支付、退款）
├─ 库存服务（库存管理）
├─ 物流服务（配送追踪）
└─ 通知服务（邮件、短信、推送）
```

### 2. 拆分原则
```
高内聚、低耦合：
├─ 每个服务负责一个业务领域
├─ 服务之间通过 API 通信
├─ 服务可以独立部署
├─ 避免跨服务的事务
```

### 3. 避免过度拆分
```
❌ 过度拆分：
├─ 用户创建服务
├─ 用户更新服务
├─ 用户删除服务
├─ 用户查询服务

✅ 合理拆分：
└─ 用户服务（统一的用户管理）
```

### 4. 数据库分离
```
服务 A：
┌─────────────────┐
│    服务 A        │
│                 │
│  ┌───────────┐ │
│  │  数据库 A  │ │
│  └───────────┘ │
└─────────────────┘

服务 B：
┌─────────────────┐
│    服务 B        │
│                 │
│  ┌───────────┐ │
│  │  数据库 B  │ │
│  └───────────┘ │
└─────────────────┘

⚠️ 避免直接跨库 JOIN
```

### 5. 服务通信模式
```javascript
// 同步通信 - REST
const response = await fetch('http://user-service/api/users/123')

// 同步通信 - gRPC
const user = await userService.GetUser({ id: '123' })

// 异步通信 - 消息队列
await messageBroker.publish('user.created', { userId: '123' })
```
```

## API 網關

```
你：
API 网关的作用是什么？

AI：
## API 网关

### 主要职责
```
┌─────────────────────────────────────────────────────────┐
│                    API Gateway                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   路由转发                                             │
│   /api/users → user-service:8080                       │
│   /api/orders → order-service:8081                    │
│                                                         │
│   认证授权                                             │
│   └─ 验证 Token                                        │
│   └─ 权限检查                                          │
│                                                         │
│   限流熔断                                             │
│   └─ 防止滥用                                          │
│   └─ 服务不可用时降级                                  │
│                                                         │
│   请求聚合                                             │
│   └─ 合并多个后端调用                                  │
│                                                         │
│   协议转换                                             │
│   └─ HTTP → gRPC                                      │
│   └─ SOAP → REST                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Kong/Nginx 配置
```yaml
# Kong 示例
services:
  - name: user-service
    url: http://user-service:8080
    routes:
      - name: user-route
        paths:
          - /api/users
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 100

  - name: order-service
    url: http://order-service:8081
    routes:
      - name: order-route
        paths:
          - /api/orders
```

### Node.js API 网关实现
```javascript
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// JWT 验证中间件
app.use('/api', async (req, res, next) => {
  const token = req.headers.authorization;
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  try {
    const user = await verifyToken(token);
    req.user = user;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
});

// 路由转发
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:8080',
  changeOrigin: true
}));

app.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:8081',
  changeOrigin: true
}));

app.listen(3000);
```
```

## 服務發現

```
你：
微服务如何相互发现？

AI：
## 服务发现

### 服务注册
```javascript
// 服务启动时注册
const consul = require('consul')();

async function registerService() {
  await consul.agent.service.register({
    name: 'user-service',
    address: 'user-service',
    port: 8080,
    check: {
      http: 'http://user-service:8080/health',
      interval: '10s'
    }
  });
}

// 服务停止时注销
process.on('SIGTERM', async () => {
  await consul.agent.service.deregister('user-service');
});
```

### 服务发现
```javascript
// 客户端发现
async function getServiceUrl(serviceName) {
  const { Services } = await consul.catalog.service.nodes(serviceName);
  if (!Services || Services.length === 0) {
    throw new Error(`Service ${serviceName} not found`);
  }
  const service = Services[0];
  return `http://${service.ServiceAddress}:${service.ServicePort}`;
}

// 使用
const userServiceUrl = await getServiceUrl('user-service');
```

### Kubernetes Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP  # 集群内部访问

---
apiVersion: v1
kind: Service
metadata:
  name: user-service-external
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 8080
  type: LoadBalancer  # 外部访问
```

### 服务网格 (Istio)
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
    - user-service
  http:
    - route:
        - destination:
            host: user-service
            subset: v1
          weight: 90
        - destination:
            host: user-service
            subset: v2
          weight: 10
```
```

## 分布式追蹤

```
你：
微服务如何追踪请求？

AI：
## 分布式追踪

### 概念
```
Trace: 请求的完整路径
├─ Span 1: API Gateway (0-100ms)
│   ├─ Span 2: User Service (10-60ms)
│   │   └─ Span 3: Database (20-40ms)
│   └─ Span 4: Order Service (20-80ms)
│       └─ Span 5: Payment Service (30-60ms)
```

### OpenTelemetry 实现
```javascript
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');

const sdk = new NodeSDK({
  serviceName: 'order-service',
  traceExporter: new JaegerExporter({
    endpoint: 'http://jaeger:14268/api/traces'
  })
});

sdk.start();

// 创建追踪
const tracer = trace.getTracer('order-service');

async function createOrder(orderData) {
  return tracer.startActiveSpan('createOrder', async (span) => {
    try {
      span.setAttribute('userId', orderData.userId);
      
      const user = await tracer.startActiveSpan('getUser', async (userSpan) => {
        const user = await userService.getUser(orderData.userId);
        userSpan.end();
        return user;
      });
      
      const order = await db.orders.create(orderData);
      span.end();
      return order;
    } catch (error) {
      span.recordException(error);
      span.end();
      throw error;
    }
  });
}
```

### Jaeger 查询
```
查找慢请求：
├─ 服务：order-service
├─ 操作：createOrder
└─ 条件：duration > 1s

查看调用链路：
├─ Gateway (50ms)
├─ User Service (30ms) - 数据库查询 (20ms)
└─ Order Service (40ms) - 库存服务 (30ms)
```
```

## 實踐練習

```
1. 评估是否需要微服务
2. 设计服务边界
3. 创建基础服务骨架
4. 配置 API 网关
5. 设置服务发现
6. 实现分布式追踪
7. 制定部署策略
```

**微服務是工具，不是目標。不要為了微服務而微服務。**
