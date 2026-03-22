# 26. Deployment Strategies and Blue-Green Deployment

## Deployment Strategy Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Deployment Strategy Comparison             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Direct deployment       Simplest, but has downtime     │
│   Rolling deployment      Zero downtime, but slow        │
│   Blue-green deployment  Zero downtime, fast rollback    │
│   Canary deployment      Controllable risk, good for critical systems │
│   A/B testing           Can verify multiple versions    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Blue-Green Deployment

### Core Concept

```
┌─────────────────────────────────────────────────────────┐
│                   Blue-Green Deployment                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Phase 1: Production (Blue) running v1.0              │
│                                                         │
│   ┌─────────────┐                                      │
│   │   Blue Env  │  ← Current production                │
│   │   v1.0      │                                      │
│   └─────────────┘                                      │
│                                                         │
│   Phase 2: Deploy to green environment                  │
│                                                         │
│   ┌─────────────┐    ┌─────────────┐                    │
│   │   Blue Env  │    │  Green Env  │                    │
│   │   v1.0      │    │   v1.1      │ ← New version     │
│   └─────────────┘    └─────────────┘                    │
│                                                         │
│   Phase 3: Switch after verification                    │
│                                                         │
│   ┌─────────────┐    ┌─────────────┐                    │
│   │   Blue Env  │ ← │  Green Env  │                    │
│   │   v1.1      │    │   v1.1      │ ← Becomes production│
│   └─────────────┘    └─────────────┘                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### AI-Assisted Implementation

```
You:
Please help me implement blue-green deployment using Kubernetes.

AI:
## Kubernetes Blue-Green Deployment

### 1. Deploy blue environment (current production)
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

### 2. Deploy green environment (new version)
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
        image: myapp:v1.1  # New version
        ports:
        - containerPort: 80
```

### 3. Service switch
```yaml
# Before switch (pointing to blue)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change this
  ports:
  - port: 80
    targetPort: 80

# After switch (pointing to green)
spec:
  selector:
    app: myapp
    version: green  # Change this
```

### 4. Switch script
```bash
#!/bin/bash

# Verify green environment
kubectl get pods -l version=green

# Switch traffic
kubectl patch service myapp \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Verify switch
kubectl get service myapp

# Observe logs
kubectl logs -l version=green -f

# Rollback if needed
kubectl patch service myapp \
  -p '{"spec":{"selector":{"version":"blue"}}}'
```

## Canary Deployment

### Core Concept

```
┌─────────────────────────────────────────────────────────┐
│                   Canary Deployment                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Step 1: 10% traffic to new version                   │
│                                                         │
│   90% ──→ v1.0 (stable)                               │
│   10% ──→ v1.1 (canary)                               │
│                                                         │
│   Step 2: Observe metrics                              │
│                                                         │
│   - Error rate                                         │
│   - Response time                                     │
│   - User feedback                                     │
│                                                         │
│   Step 3: Gradually increase                           │
│                                                         │
│   50% ──→ v1.0                                        │
│   50% ──→ v1.1                                        │
│                                                         │
│   Step 4: 100% switch                                 │
│                                                         │
│   100% ──→ v1.1                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### AI-Assisted Implementation

```
You:
Please help me implement Kubernetes canary deployment.

AI:
## Kubernetes Canary Deployment

### 1. Base deployment (stable)
```yaml
# stable-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9  # 90% traffic
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

### 2. Canary deployment
```yaml
# canary-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1  # 10% traffic
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

### 3. Single Service
```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp  # Matches all versions
  ports:
  - port: 80
    targetPort: 80
```

### 4. Automated canary tool: Argo Rollouts
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
      - pause: {}  # Manual pause
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

### 5. Monitoring and analysis
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

## Rolling Deployment

```
You:
Please implement Kubernetes rolling deployment configuration.

AI:
## Kubernetes Rolling Deployment

### 1. Rolling update configuration
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
      maxSurge: 2        # Can exceed desired replicas
      maxUnavailable: 0  # Available instances during update
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

### 2. Rolling process

```
Desired replicas: 6

Step 1: Add 2 new instances
┌──┬──┬──┬──┬──┬──┐
│v1│v1│v1│v1│v1│v1│  +2 v2 → 8 instances
└──┴──┴──┴──┴──┴──┘

Step 2: After ready, remove 2 old instances
┌──┬──┬──┬──┬──┬──┐
│v1│v1│v1│v1│v2│v2│  -2 v1 → 6 instances
└──┴──┴──┴──┴──┴──┘

Step 3: Repeat until all updated
┌──┬──┬──┬──┬──┬──┐
│v2│v2│v2│v2│v2│v2│  All updated
└──┴──┴──┴──┴──┴──┘
```

### 3. Rollback
```bash
# View deployment history
kubectl rollout history deployment/myapp

# Rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific version
kubectl rollout undo deployment/myapp --to-revision=2
```

## A/B Testing Deployment

```
You:
Please help me implement weight-based A/B testing.

AI:
## A/B Testing Deployment

### 1. Using Ingress
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
# 90% traffic to A version
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
# 10% traffic to B version
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

### 2. Header-based routing
```yaml
annotations:
  nginx.ingress.kubernetes.io/canary: "true"
  nginx.ingress.kubernetes.io/canary-by-header: "X-User-Type"
  nginx.ingress.kubernetes.io/canary-by-header-value: "premium"
```

### 3. Deployment configuration
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

## Deployment Monitoring

```
You:
What metrics to monitor after deployment?

AI:
## Deployment Monitoring Checklist

### 1. Health metrics
```yaml
# Application layer
- Error rate (5xx ratio)
- Success rate (2xx ratio)
- Request latency (P50, P95, P99)
- QPS (requests per second)

# Infrastructure layer
- CPU usage
- Memory usage
- Network I/O
- Disk I/O
```

### 2. Business metrics
```yaml
- Order conversion rate
- User login success rate
- Key feature usage
- Revenue-related metrics
```

### 3. Canary-specific metrics
```yaml
# Compare metrics
canary_vs_baseline:
- Error rate difference
- Latency difference
- Business metrics difference

# Threshold alerts
alerts:
- canary_error_rate > baseline + 1%
- canary_latency > baseline + 20%
```

### 4. Monitoring dashboard
```
┌────────────────────────────────────────────────────┐
│         Deployment Monitoring Dashboard              │
├────────────────────────────────────────────────────┤
│                                                    │
│   Version Information                              │
│   ├─ Current version: v1.1.0                      │
│   ├─ Deploy time: 2024-01-15 10:30               │
│   └─ Deploy method: Canary 10%                   │
│                                                    │
│   Traffic Distribution                             │
│   ├─ v1.0: 90%                                   │
│   └─ v1.1: 10%                                   │
│                                                    │
│   Real-time Metrics                                │
│   ├─ Error rate: 0.1% / 0.2%                     │
│   ├─ P99 latency: 120ms / 135ms                  │
│   └─ QPS: 1000 / 100                             │
│                                                    │
└────────────────────────────────────────────────────┘
```

## Practice Exercises

```
1. Choose deployment strategy suitable for your project
2. Configure rolling update/blue-green/canary
3. Set up health checks
4. Configure monitoring and alerts
5. Practice rollback process
6. Document deployment steps
```

**Good deployment strategies make you confident to deploy, iterate quickly, and rollback safely.**
