# 27. Monitoring, Logging, and Alerting

## Three Pillars of Observability

```
┌─────────────────────────────────────────────────────────┐
│                   Observability                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐                                       │
│   │   Metrics   │  Aggregated numeric data              │
│   │   指标      │  CPU, requests, latency percentiles   │
│   └─────────────┘                                       │
│                                                         │
│   ┌─────────────┐                                       │
│   │    Logs     │  Event records                        │
│   │    日志      │  Error stacks, access logs           │
│   └─────────────┘                                       │
│                                                         │
│   ┌─────────────┐                                       │
│   │   Traces    │  Complete path of requests           │
│   │   链路追踪   │  Distributed calls, service deps     │
│   └─────────────┘                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Metrics Monitoring

### Core Metrics

```
You:
What are the KPI metrics for web applications?

AI:
## Web Application Core Metrics

### Golden Signals

| Metric | Description | Target |
|--------|-------------|--------|
| Latency | Request response time | P99 < 500ms |
| Traffic | QPS, concurrent connections | Depends on business |
| Errors | 5xx ratio | < 0.1% |
| Saturation | CPU/Memory usage | < 80% |

### Application Layer Metrics
```
- Request rate (requests/sec)
- Error rate (errors/sec)
- Latency distribution (P50, P95, P99)
- Concurrent connections
- Queue length
```

### Database Metrics
```
- Query latency
- Connection pool utilization
- Slow query count
- Deadlock count
- Replication lag (primary/replica)
```

### Business Metrics
```
- Active users
- Order conversion rate
- API call success rate
- Task completion rate
```

### Alert Rules Example
```yaml
# Prometheus alert rules
groups:
- name: web-app
  rules:
  - alert: HighErrorRate
    expr: sum(rate(http_requests_total{status=~"5.."}[5m])) 
          / sum(rate(http_requests_total[5m])) > 0.01
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate"
      description: "Error rate is above 1%"

  - alert: HighLatency
    expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High latency"
```

## Log Management

### Log Levels

```
You:
How should log levels be designed?

AI:
## Log Level Design

### Standard Levels
```
DEBUG   - Detailed development info, off in production
INFO    - Normal operation info
WARN    - Warning, might be a problem
ERROR   - Error, needs attention
FATAL   - Fatal error, system unavailable
```

### Usage Guide
```javascript
// DEBUG - Detailed debug info
logger.debug(`Processing item ${i} of ${total}`);

// INFO - Important operations
logger.info(`User ${userId} logged in`);
logger.info(`Order ${orderId} created`);

// WARN - Situations to note
logger.warn(`Rate limit approaching for user ${userId}`);
logger.warn(`Config using default value for ${key}`);

// ERROR - Errors but recoverable
logger.error(`Failed to send email to ${email}`, { error });

// FATAL - System-level errors
logger.fatal(`Database connection lost: ${error.message}`);
```

### Production Environment Recommendations
```
Log level = WARN  # Or ERROR
        ↓
Only log important issues
        ↓
Save storage costs
        ↓
Improve readability
```

### Structured Logging

```
You:
Please help me implement structured logging.

AI:
## Structured Logging

### Node.js Example
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'user-service' },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    })
  ]
});

// Usage
logger.info('User created', {
  userId: '123',
  email: 'test@example.com',
  action: 'register'
});

// Output
{
  "level": "info",
  "message": "User created",
  "userId": "123",
  "email": "test@example.com",
  "action": "register",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "user-service"
}
```

### Python Example
```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

log = structlog.get_logger()

log.info("user_created", 
    user_id="123", 
    email="test@example.com"
)
```

### Log Aggregation Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Log Collection Flow                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Application logs                                      │
│      ↓                                                  │
│   Container/VM                                          │
│      ↓                                                  │
│   Log collector (Fluentd/Filebeat)                      │
│      ↓                                                  │
│   Log storage (Elasticsearch/Loki)                       │
│      ↓                                                  │
│   Visualization (Kibana/Grafana)                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Distributed Tracing

```
You:
Please explain the concept of distributed tracing.

AI:
## Distributed Tracing

### Why Needed
```
In microservices architecture, one request may call 10+ services
    ↓
Hard to locate which service is slow
    ↓
Need distributed tracing
```

### Core Concepts
```
Span - One operation (a function/a call)
  ├─ name: "handle-request"
  ├─ start_time: 10:00:00
  ├─ end_time: 10:00:01
  └─ tags: { service: "api", method: "GET" }

Trace - Complete request path
  └─ Spans: [span1, span2, span3, ...]
```

### OpenTelemetry Example
```javascript
const { trace } = require('@opentelemetry/api');

// Create tracer
const tracer = trace.getTracer('my-app');

// Usage
async function handleRequest(req) {
  return tracer.startActiveSpan('handle-request', async (span) => {
    try {
      span.setAttribute('http.method', req.method);
      
      const user = await tracer.startActiveSpan('get-user', async (userSpan) => {
        const user = await db.users.findById(req.userId);
        userSpan.end();
        return user;
      });
      
      const result = await processUser(user);
      span.setAttribute('result', 'success');
      return result;
    } catch (error) {
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

### Distributed Trace Example
```
Trace: abc123

├─ Span: api-gateway (0ms - 150ms)
│   └─ Span: auth-service (10ms - 30ms)
│   └─ Span: user-service (20ms - 50ms)
│       └─ Span: database query (25ms - 35ms)
│   └─ Span: order-service (40ms - 120ms)
│       └─ Span: payment-service (50ms - 100ms)
│           └─ Span: payment-api (60ms - 90ms)
│       └─ Span: inventory-service (80ms - 110ms)
│   └─ Span: response-format (140ms - 150ms)

Finding: payment-service is the bottleneck (70ms)
```

## Alert Design

### Alert Severity Levels

```
You:
How to design effective alert rules?

AI:
## Alert Design Principles

### Alert Levels

| Level | Name | Response Time | Meaning |
|-------|------|---------------|---------|
| P1 | Critical | 5 minutes | Service unavailable |
| P2 | Major | 15 minutes | Core functionality impaired |
| P3 | Warning | 1 hour | Needs attention |
| P4 | Info | Work hours | Can be handled later |

### Design Principles

**1. Alert Fatigue**
```
❌ Too many alerts → Ignored
✅ Precise alerts → Timely response
```

**2. Alerts must be actionable**
```
❌ "Service CPU > 50%"
✅ "Service CPU > 90% for 5 minutes"

❌ "Error occurred"
✅ "5xx error rate > 1% for 5 minutes"
```

**3. Include context**
```yaml
annotations:
  summary: "Service responding slowly"
  description: |
    {{ $labels.service }} P99 latency too high
    
    Current value: {{ $value }}ms
    Threshold: 1000ms
    Duration: {{ $duration }}
    
    View details: [Link]
```

### Example Alert Rules
```yaml
# Critical: Service down
- alert: ServiceDown
  expr: up{job="myapp"} == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Service instance unavailable"

# Critical: High error rate
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    / sum(rate(http_requests_total[5m])) > 0.05
  for: 2m
  labels:
    severity: critical

# Warning: High latency
- alert: HighLatency
  expr: |
    histogram_quantile(0.95, 
      rate(http_request_duration_bucket[5m])) > 1
  for: 5m
  labels:
    severity: warning

# Info: High resource usage
- alert: HighMemoryUsage
  expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.85
  for: 10m
  labels:
    severity: warning
```

## Monitoring Tool Stack

```
┌─────────────────────────────────────────────────────────┐
│                   Monitoring Tool Selection                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Self-hosted solutions                                  │
│   ├─ Prometheus + Grafana - Metrics                    │
│   ├─ Loki + Grafana - Logs                             │
│   ├─ Jaeger/Zipkin - Distributed tracing              │
│   └─ ELK Stack - Comprehensive logging                │
│                                                         │
│   Cloud solutions                                       │
│   ├─ AWS CloudWatch - AWS native                      │
│   ├─ Datadog - Full-stack monitoring                  │
│   ├─ New Relic - APM                                  │
│   └─ Sentry - Error tracking                          │
│                                                         │
│   Open source/Managed                                   │
│   ├─ Grafana Cloud - Managed Grafana                   │
│   ├─ Grafana Enterprise - Enterprise                   │
│   └─ Honeycomb - Distributed tracing                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Practice Exercises

```
1. Choose monitoring tool stack
2. Configure basic metrics collection
3. Set up log collection
4. Configure critical alerts
5. Create monitoring dashboard
6. Test alert notifications
7. Regularly review alert rules
```

**Good monitoring lets you know about problems before users complain.**
