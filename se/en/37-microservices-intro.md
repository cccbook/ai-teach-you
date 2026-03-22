# 37. Introduction to Microservices Architecture

## Monolith vs Microservices

```
┌─────────────────────────────────────────────────────────┐
│                   Architecture Evolution                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Monolithic Application                                │
│   ┌─────────────────────────────┐                       │
│   │  Web │ API │ DB │ Queue │   │                       │
│   └─────────────────────────────┘                       │
│   Pros: Simple, easy deployment                         │
│   Cons: Hard to scale, fixed tech stack                 │
│                                                         │
│   Microservices Architecture                             │
│   ┌─────┐  ┌─────┐  ┌─────┐                            │
│   │User │  │Order│  │Product│                           │
│   │Service│ │Service│ │Service│                        │
│   └──┬──┘  └──┬──┘  └──┬──┘                          │
│      │         │         │                              │
│      └─────────┼─────────┘                              │
│                ↓                                         │
│           ┌─────────┐                                    │
│           │ Message │                                    │
│           │ Queue   │                                    │
│           └─────────┘                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Microservices Design

```
You:
When should I use microservices architecture?

AI:
## Microservices Suitability

### When to Use Microservices
```
✓ Large complex applications (100+ developers)
✓ Need to scale different modules independently
✓ Need to use different tech stacks
✓ Team already has DevOps capabilities
✓ Clear business domain boundaries
```

### When NOT to Use Microservices
```
✗ Small applications (team of 5 or less)
✗ Startups needing rapid iteration
✗ Team lacks operational experience
✗ Unclear business boundaries
```

### Decision Criteria
```
Ask yourself:
1. Do different modules have very different scaling needs?
2. Do different modules require different tech stacks?
3. Can the team develop and deploy independently?
4. Do you have sufficient DevOps capabilities?

If mostly "No" → Start with monolith
If mostly "Yes" → Consider microservices
```

## Service Decomposition

```
You:
How do I properly decompose microservices?

AI:
## Service Decomposition Strategies

### 1. Decompose by Business Capability
```
E-commerce system decomposition:
├─ User Service (registration, login, profile)
├─ Product Service (product info, categories, search)
├─ Order Service (order creation, management)
├─ Payment Service (payments, refunds)
├─ Inventory Service (stock management)
├─ Shipping Service (delivery tracking)
└─ Notification Service (email, SMS, push)
```

### 2. Decomposition Principles
```
High cohesion, low coupling:
├─ Each service is responsible for one business domain
├─ Services communicate via APIs
├─ Services can be deployed independently
├─ Avoid cross-service transactions
```

### 3. Avoid Over-decomposition
```
❌ Over-decomposition:
├─ User creation service
├─ User update service
├─ User delete service
├─ User query service

✅ Reasonable decomposition:
└─ User Service (unified user management)
```

### 4. Database Separation
```
Service A:
┌─────────────────┐
│    Service A     │
│                 │
│  ┌───────────┐ │
│  │ Database A│ │
│  └───────────┘ │
└─────────────────┘

Service B:
┌─────────────────┐
│    Service B     │
│                 │
│  ┌───────────┐ │
│  │ Database B│ │
│  └───────────┘ │
└─────────────────┘

⚠️ Avoid direct cross-database JOINs
```

### 5. Service Communication Patterns
```javascript
// Synchronous - REST
const response = await fetch('http://user-service/api/users/123')

// Synchronous - gRPC
const user = await userService.GetUser({ id: '123' })

// Asynchronous - Message Queue
await messageBroker.publish('user.created', { userId: '123' })
```
```

## API Gateway

```
You:
What is the purpose of an API Gateway?

AI:
## API Gateway

### Main Responsibilities
```
┌─────────────────────────────────────────────────────────┐
│                    API Gateway                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Route Forwarding                                      │
│   /api/users → user-service:8080                       │
│   /api/orders → order-service:8081                     │
│                                                         │
│   Authentication & Authorization                         │
│   └─ Verify tokens                                       │
│   └─ Permission checks                                   │
│                                                         │
│   Rate Limiting & Circuit Breaker                       │
│   └─ Prevent abuse                                       │
│   └─ Degrade when services unavailable                  │
│                                                         │
│   Request Aggregation                                   │
│   └─ Combine multiple backend calls                     │
│                                                         │
│   Protocol Translation                                  │
│   └─ HTTP → gRPC                                        │
│   └─ SOAP → REST                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Kong/Nginx Configuration
```yaml
# Kong example
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

### Node.js API Gateway Implementation
```javascript
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// JWT verification middleware
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

// Route forwarding
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

## Service Discovery

```
You:
How do microservices find each other?

AI:
## Service Discovery

### Service Registration
```javascript
// Register on service startup
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

// Deregister on service stop
process.on('SIGTERM', async () => {
  await consul.agent.service.deregister('user-service');
});
```

### Service Discovery
```javascript
// Client-side discovery
async function getServiceUrl(serviceName) {
  const { Services } = await consul.catalog.service.nodes(serviceName);
  if (!Services || Services.length === 0) {
    throw new Error(`Service ${serviceName} not found`);
  }
  const service = Services[0];
  return `http://${service.ServiceAddress}:${service.ServicePort}`;
}

// Usage
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
  type: ClusterIP  # Internal cluster access

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
  type: LoadBalancer  # External access
```

### Service Mesh (Istio)
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

## Distributed Tracing

```
You:
How do I trace requests across microservices?

AI:
## Distributed Tracing

### Concepts
```
Trace: Complete path of a request
├─ Span 1: API Gateway (0-100ms)
│   ├─ Span 2: User Service (10-60ms)
│   │   └─ Span 3: Database (20-40ms)
│   └─ Span 4: Order Service (20-80ms)
│       └─ Span 5: Payment Service (30-60ms)
```

### OpenTelemetry Implementation
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

// Create traces
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

### Jaeger Queries
```
Find slow requests:
├─ Service: order-service
├─ Operation: createOrder
└─ Condition: duration > 1s

View call chain:
├─ Gateway (50ms)
├─ User Service (30ms) - Database query (20ms)
└─ Order Service (40ms) - Inventory service (30ms)
```
```

## Hands-On Exercises

```
1. Evaluate if you need microservices
2. Design service boundaries
3. Create basic service skeletons
4. Configure API Gateway
5. Set up service discovery
6. Implement distributed tracing
7. Develop deployment strategy
```

**Microservices are a tool, not a goal. Don't do microservices for microservices' sake.**

(End of file - total 431 lines)
