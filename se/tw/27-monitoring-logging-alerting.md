# 27. 監控、日誌與告警

## 可觀測性的三個支柱

```
┌─────────────────────────────────────────────────────────┐
│                   可观测性 (Observability)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐                                       │
│   │   Metrics   │  指标 - 聚合的数字数据                  │
│   │   指标      │  CPU、请求数、延迟百分位               │
│   └─────────────┘                                       │
│                                                         │
│   ┌─────────────┐                                       │
│   │   Logs      │  日志 - 事件记录                      │
│   │   日志      │  错误堆栈、访问日志                    │
│   └─────────────┘                                       │
│                                                         │
│   ┌─────────────┐                                       │
│   │  Traces     │  链路追踪 - 请求的完整路径             │
│   │   追踪      │  分布式调用、服务依赖                  │
│   └─────────────┘                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 指標監控 (Metrics)

### 核心指標

```
你：
Web 应用的 KPI 指标有哪些？

AI：
## Web 应用核心指标

### 黄金信号 (Golden Signals)

| 指标 | 描述 | 目标值 |
|------|------|--------|
| 延迟 (Latency) | 请求响应时间 | P99 < 500ms |
| 流量 (Traffic) | QPS、并发数 | 取决于业务 |
| 错误 (Errors) | 5xx 比例 | < 0.1% |
| 饱和度 (Saturation) | CPU/内存使用 | < 80% |

### 应用层指标
```
- 请求速率 (requests/sec)
- 错误率 (errors/sec)
- 延迟分布 (P50, P95, P99)
- 并发连接数
- 队列长度
```

### 数据库指标
```
- 查询延迟
- 连接池使用率
- 慢查询数量
- 死锁次数
- 复制延迟 (主从)
```

### 业务指标
```
- 活跃用户数
- 订单转化率
- API 调用成功率
- 任务完成率
```

### 告警规则示例
```yaml
# Prometheus 告警规则
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
```

## 日誌管理

### 日誌級別

```
你：
日志级别应该如何设计？

AI：
## 日志级别设计

### 标准级别
```
DEBUG   - 详细开发信息，生产环境关闭
INFO    - 正常操作信息
WARN    - 警告，可能有问题
ERROR   - 错误，需要关注
FATAL   - 致命错误，系统不可用
```

### 使用指南
```javascript
// DEBUG - 详细调试信息
logger.debug(`Processing item ${i} of ${total}`);

// INFO - 重要操作
logger.info(`User ${userId} logged in`);
logger.info(`Order ${orderId} created`);

// WARN - 需要注意的情况
logger.warn(`Rate limit approaching for user ${userId}`);
logger.warn(`Config using default value for ${key}`);

// ERROR - 错误但可处理
logger.error(`Failed to send email to ${email}`, { error });

// FATAL - 系统级错误
logger.fatal(`Database connection lost: ${error.message}`);
```

### 生产环境建议
```
日志级别 = WARN  # 或 ERROR
        ↓
只记录重要问题
        ↓
节省存储成本
        ↓
提高可读性
```
```

### 結構化日誌

```
你：
请帮我实现结构化日志。

AI：
## 结构化日志

### Node.js 示例
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

// 使用
logger.info('User created', {
  userId: '123',
  email: 'test@example.com',
  action: 'register'
});

// 输出
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

### Python 示例
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
```

### 日誌聚合架構

```
┌─────────────────────────────────────────────────────────┐
│                   日志收集流程                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   应用日志                                              │
│      ↓                                                  │
│   Container/VM                                          │
│      ↓                                                  │
│   日志收集器 (Fluentd/Filebeat)                          │
│      ↓                                                  │
│   日志存储 (Elasticsearch/Loki)                         │
│      ↓                                                  │
│   可视化 (Kibana/Grafana)                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 鏈路追蹤 (Traces)

```
你：
请解释链路追踪的概念。

AI：
## 链路追踪

### 为什么需要
```
微服务架构中，一个请求可能调用 10+ 个服务
    ↓
很难定位是哪个服务慢
    ↓
需要链路追踪
```

### 核心概念
```
Span - 一次操作（一个函数/一次调用）
  ├─ name: "handle-request"
  ├─ start_time: 10:00:00
  ├─ end_time: 10:00:01
  └─ tags: { service: "api", method: "GET" }

Trace - 完整的请求链路
  └─ Spans: [span1, span2, span3, ...]
```

### OpenTelemetry 示例
```javascript
const { trace } = require('@opentelemetry/api');

// 创建 tracer
const tracer = trace.getTracer('my-app');

// 使用
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

### 分布式追踪示例
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

发现：payment-service 是瓶颈（70ms）
```
```

## 告警設計

### 告警分級

```
你：
如何设计有效的告警规则？

AI：
## 告警设计原则

### 告警级别

| 级别 | 名称 | 响应时间 | 含义 |
|------|------|----------|------|
| P1 | 紧急 | 5 分钟 | 服务不可用 |
| P2 | 严重 | 15 分钟 | 核心功能受损 |
| P3 | 警告 | 1 小时 | 需要关注 |
| P4 | 提示 | 工作时间 | 可后续处理 |

### 设计原则

**1. 告警疲劳**
```
❌ 太多告警 → 忽略
✅ 精准告警 → 及时响应
```

**2. 告警必须可操作**
```
❌ "服务 CPU > 50%"
✅ "服务 CPU > 90% 超过 5 分钟"

❌ "出现错误"
✅ "5xx 错误率 > 1% 超过 5 分钟"
```

**3. 包含上下文**
```yaml
annotations:
  summary: "服务响应缓慢"
  description: |
    {{ $labels.service }} 的 P99 延迟过高
    
    当前值: {{ $value }}ms
    阈值: 1000ms
    持续时间: {{ $duration }}
    
    查看详情: [链接]
```

### 示例告警规则
```yaml
# Critical: 服务不可用
- alert: ServiceDown
  expr: up{job="myapp"} == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "服务实例不可用"

# Critical: 高错误率
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    / sum(rate(http_requests_total[5m])) > 0.05
  for: 2m
  labels:
    severity: critical

# Warning: 高延迟
- alert: HighLatency
  expr: |
    histogram_quantile(0.95, 
      rate(http_request_duration_bucket[5m])) > 1
  for: 5m
  labels:
    severity: warning

# Info: 资源使用率高
- alert: HighMemoryUsage
  expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.85
  for: 10m
  labels:
    severity: warning
```

## 監控工具棧

```
┌─────────────────────────────────────────────────────────┐
│                   监控工具选择                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   自托管方案                                            │
│   ├─ Prometheus + Grafana - 指标                        │
│   ├─ Loki + Grafana - 日志                             │
│   ├─ Jaeger/Zipkin - 链路追踪                          │
│   └─ ELK Stack - 综合日志                              │
│                                                         │
│   云服务方案                                            │
│   ├─ AWS CloudWatch - AWS 原生                         │
│   ├─ Datadog - 全方位监控                              │
│   ├─ New Relic - 应用性能监控                          │
│   └─ Sentry - 错误追踪                                 │
│                                                         │
│   开源/托管                                            │
│   ├─ Grafana Cloud - 托管 Grafana                      │
│   ├─ Grafana Enterprise - 企业版                        │
│   └─ Honeycomb - 分布式追踪                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 實踐練習

```
1. 选择监控工具栈
2. 配置基础指标收集
3. 设置日志收集
4. 配置关键告警
5. 创建监控仪表板
6. 测试告警通知
7. 定期审查告警规则
```

**好的監控讓你在用戶投訴之前就知道問題。**
