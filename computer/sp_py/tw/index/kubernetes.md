# Kubernetes (K8s)

## 概述

Kubernetes 是 Google 開發的容器編排平台，自動化容器部署、擴展和管理。Kubernetes 是雲端原生運算基金會（CNCF）的旗艦專案，是現代雲端架構的核心。

## 歷史

- **2014**：Google 開源 Kubernetes
- **2016**：Kubernetes 1.0
- **2018**：CNCF 畢業
- **現在**：容器編排標準

## Kubernetes 架構

```
┌──────────────────────────────────────────────┐
│              Control Plane                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────────┐    │
│  │ API Server │ │ Scheduler │ │ Controller │    │
│  └─────────┘ └─────────┘ └─────────────┘    │
└──────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────┐
│              Nodes                            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│  │ Pod     │ │ Pod     │ │ Pod     │        │
│  └─────────┘ └─────────┘ └─────────┘        │
│         ↑         ↑         ↑                │
│    ┌────────┐ ┌────────┐ ┌────────┐          │
│    │ kubelet│ │ kube-proxy│ │ Container Runtime │          │
│    └────────┘ └────────┘ └────────┘          │
└──────────────────────────────────────────────┘
```

## 基本使用

### 1. Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
```

### 2. Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 3
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
        image: myapp:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### 3. Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

### 4. ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  config.json: |
    {"key": "value"}
  database.url: "postgres://db:5432"
```

### 5. Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: YWRtaW4=
  password: cGFzc3dvcmQ=
```

### 6. Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

### 7. Helm

```bash
# 安裝 Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 新增 repo
helm repo add stable https://charts.helm.sh/stable

# 安裝 chart
helm install myrelease stable/nginx-ingress

# 升級
helm upgrade myrelease stable/nginx-ingress
```

## 為什麼使用 Kubernetes？

1. **自動化**：自動部署和擴展
2. **可移植性**：雲端無關
3. **自癒**：自動恢復
4. **擴展性**：水平擴展

## 參考資源

- Kubernetes 官方文檔
- "Kubernetes in Action"
- CKAD/CKA 認證
