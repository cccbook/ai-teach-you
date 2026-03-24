# 26. 部署策略與藍綠部署

## 部署策略概述

```
┌─────────────────────────────────────────────────────────┐
│                   部署策略对比                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   直接部署       最简单，但有停机                       │
│   滚动部署       零停机，但时间长                       │
│   蓝绿部署       零停机，可快速回滚                     │
│   金丝雀部署     风险可控，适合关键系统                 │
│   A/B 测试       可同时验证多个版本                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 藍綠部署

### 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                   蓝绿部署                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   阶段 1：生产环境（蓝）运行 v1.0                       │
│                                                         │
│   ┌─────────────┐                                      │
│   │   蓝环境    │  ← 当前生产                           │
│   │   v1.0      │                                      │
│   └─────────────┘                                      │
│                                                         │
│   阶段 2：部署到绿环境                                   │
│                                                         │
│   ┌─────────────┐    ┌─────────────┐                    │
│   │   蓝环境    │    │   绿环境    │                    │
│   │   v1.0      │    │   v1.1      │ ← 新版本         │
│   └─────────────┘    └─────────────┘                    │
│                                                         │
│   阶段 3：验证后切换                                    │
│                                                         │
│   ┌─────────────┐    ┌─────────────┐                    │
│   │   蓝环境    │ ←  │   绿环境    │                    │
│   │   v1.1      │    │   v1.1      │ ← 变成生产        │
│   └─────────────┘    └─────────────┘                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### AI 輔助實現

```
你：
请帮我用 Kubernetes 实现蓝绿部署。

AI：
## Kubernetes 蓝绿部署

### 1. 部署蓝环境（当前生产）
```yaml
# blue-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0
        ports:
        - containerPort: 80
```

### 2. 部署绿环境（新版本）
```yaml
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: myapp
        image: myapp:v1.1  # 新版本
        ports:
        - containerPort: 80
```

### 3. Service 切换
```yaml
# 切换前（指向蓝）
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # 切换这里
  ports:
  - port: 80
    targetPort: 80

# 切换后（指向绿）
spec:
  selector:
    app: myapp
    version: green  # 修改这里
```

### 4. 切换脚本
```bash
#!/bin/bash

# 验证绿环境
kubectl get pods -l version=green

# 切换流量
kubectl patch service myapp \
  -p '{"spec":{"selector":{"version":"green"}}}'

# 验证切换
kubectl get service myapp

# 观察日志
kubectl logs -l version=green -f

# 回滚（如果需要）
kubectl patch service myapp \
  -p '{"spec":{"selector":{"version":"blue"}}}'
```
```

## 金絲雀部署

### 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                   金丝雀部署                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Step 1：10% 流量到新版本                             │
│                                                         │
│   90% ──→ v1.0 (稳定版)                               │
│   10% ──→ v1.1 (金丝雀)                               │
│                                                         │
│   Step 2：观察指标                                     │
│                                                         │
│   - 错误率                                            │
│   - 响应时间                                          │
│   - 用户反馈                                          │
│                                                         │
│   Step 3：逐步增加                                     │
│                                                         │
│   50% ──→ v1.0                                        │
│   50% ──→ v1.1                                        │
│                                                         │
│   Step 4：100% 切换                                   │
│                                                         │
│   100% ──→ v1.1                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### AI 輔助實現

```
你：
请帮我实现 Kubernetes 金丝雀部署。

AI：
## Kubernetes 金丝雀部署

### 1. 基础部署（稳定版）
```yaml
# stable-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9  # 90% 流量
  selector:
    matchLabels:
      app: myapp
      track: stable
  template:
    metadata:
      labels:
        app: myapp
        track: stable
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0
```

### 2. 金丝雀部署
```yaml
# canary-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1  # 10% 流量
  selector:
    matchLabels:
      app: myapp
      track: canary
  template:
    metadata:
      labels:
        app: myapp
        track: canary
    spec:
      containers:
      - name: myapp
        image: myapp:v1.1
```

### 3. 单一 Service
```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp  # 匹配所有版本
  ports:
  - port: 80
    targetPort: 80
```

### 4. 自动金丝雀工具：Argo Rollouts
```yaml
# rollout.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {}  # 手动暂停
      - setWeight: 30
      - pause: {duration: 10m}
      - setWeight: 50
      - pause: {}
      analysis:
        templates:
        - templateName: success-rate
        args:
        - name: service-name
          value: myapp-canary
```
```

### 5. 监控和分析
```yaml
# analysis-template.yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 1m
    successCondition: result[0] >= 0.95
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(http_requests_total{
            job="{{args.service-name}}",
            status!~"5.*"}[1m]))
          /
          sum(rate(http_requests_total{
            job="{{args.service-name}}"}[1m]))
```

## 滾動部署

```
你：
请实现 Kubernetes 滚动部署配置。

AI：
## Kubernetes 滚动部署

### 1. 滚动更新配置
```yaml
# rolling-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # 最多超出期望副本数
      maxUnavailable: 0  # 更新过程中可用实例数
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 2. 滚动过程

```
期望副本：6

Step 1: 新增 2 个新实例
┌──┬──┬──┬──┬──┬──┐
│v1│v1│v1│v1│v1│v1│  +2 v2 → 8 个实例
└──┴──┴──┴──┴──┴──┘

Step 2: 等待就绪后，删除 2 个旧实例
┌──┬──┬──┬──┬──┬──┐
│v1│v1│v1│v1│v2│v2│  -2 v1 → 6 个实例
└──┴──┴──┴──┴──┴──┘

Step 3: 重复直到全部更新
┌──┬──┬──┬──┬──┬──┐
│v2│v2│v2│v2│v2│v2│  全部更新完成
└──┴──┴──┴──┴──┴──┘
```

### 3. 回滚
```bash
# 查看部署历史
kubectl rollout history deployment/myapp

# 回滚到上一个版本
kubectl rollout undo deployment/myapp

# 回滚到指定版本
kubectl rollout undo deployment/myapp --to-revision=2
```
```

## A/B 測試部署

```
你：
请帮我实现基于权重的 A/B 测试。

AI：
## A/B 测试部署

### 1. 使用 Ingress 实现
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ab
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-a
            port:
              number: 80
---
# 90% 流量到 A 版本
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-a
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "90"
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-a
            port:
              number: 80
---
# 10% 流量到 B 版本
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-b
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-b
            port:
              number: 80
```

### 2. 基于 Header 的分流
```yaml
annotations:
  nginx.ingress.kubernetes.io/canary: "true"
  nginx.ingress.kubernetes.io/canary-by-header: "X-User-Type"
  nginx.ingress.kubernetes.io/canary-by-header-value: "premium"
```

### 3. 部署配置
```yaml
# service-a.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-a
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: a
  template:
    metadata:
      labels:
        app: myapp
        version: a
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0
---
# service-b.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-b
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: b
  template:
    metadata:
      labels:
        app: myapp
        version: b
    spec:
      containers:
      - name: myapp
        image: myapp:v2.0
```
```

## 部署監控

```
你：
部署后应该监控哪些指标？

AI：
## 部署监控清单

### 1. 健康指标
```yaml
# 应用层
- 错误率 (5xx 比例)
- 成功率 (2xx 比例)
- 请求延迟 (P50, P95, P99)
- QPS (每秒请求数)

# 基础设施层
- CPU 使用率
- 内存使用率
- 网络 I/O
- 磁盘 I/O
```

### 2. 业务指标
```yaml
- 订单转化率
- 用户登录成功率
- 关键功能使用率
- 收入相关指标
```

### 3. 金丝雀特有指标
```yaml
# 对比指标
canary_vs_baseline:
- 错误率差异
- 延迟差异
- 业务指标差异

# 阈值告警
alerts:
- canary_error_rate > baseline + 1%
- canary_latency > baseline + 20%
```

### 4. 监控仪表板
```
┌────────────────────────────────────────────────────┐
│         部署监控仪表板                              │
├────────────────────────────────────────────────────┤
│                                                    │
│   版本信息                                          │
│   ├─ 当前版本：v1.1.0                             │
│   ├─ 部署时间：2024-01-15 10:30                    │
│   └─ 部署方式：Canary 10%                         │
│                                                    │
│   流量分布                                          │
│   ├─ v1.0: 90%                                    │
│   └─ v1.1: 10%                                   │
│                                                    │
│   实时指标                                          │
│   ├─ 错误率：0.1% / 0.2%                          │
│   ├─ P99延迟：120ms / 135ms                       │
│   └─ QPS：1000 / 100                              │
│                                                    │
└────────────────────────────────────────────────────┘
```

## 實踐練習

```
1. 选择适合你项目的部署策略
2. 配置滚动更新/蓝绿/金丝雀
3. 设置健康检查
4. 配置监控和告警
5. 演练回滚流程
6. 文档化部署步骤
```

**好的部署策略讓你敢於發布、快速迭代、安心回滾。**
