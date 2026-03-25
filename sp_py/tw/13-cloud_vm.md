# 13. 雲端技術與虛擬機

雲端運算已經徹底改變了現代資訊科技的運作方式。從小型新創公司到大型企業，從網站托管到大規模資料處理，雲端平台提供了前所未有的彈性和規模。本章將深入探討虛擬化技術的原理、Docker 容器化、Kubernetes 容器編排、雲端服務模型，以及分散式系統的核心概念。這些技術構成了現代雲端基礎設施的基石。

## 13.1 虛擬化技術

### 13.1.1 虛擬化的基本概念

虛擬化（Virtualization）是一種將單一實體資源抽象為多個邏輯資源的技術。在計算領域，虛擬化使得單一實體伺服器可以同時執行多個隔離的作業系統執行個體，每個執行個體稱為虛擬機（Virtual Machine, VM）。虛擬化技術的歷史可以追溯到 1960 年代 IBM 大型機的分区技術，但真正的普及是在 x86 架構的伺服器虛擬化出現之後。

**虛擬化的核心價值**

虛擬化解決了傳統實體伺服器部署的多個痛點：

| 價值主張 | 說明 | 商業效益 |
|----------|------|----------|
| 資源整合 | 將多台伺服器的工作負載整合到較少的高效能伺服器 | 降低硬體和資料中心成本 |
| 隔離性 | 每個 VM 完全隔離，一個 VM 的問題不會影響其他 VM | 提高穩定性和安全性 |
| 彈性 | 根據需求快速建立、複製、遷移 VM | 提高營運敏捷性 |
| 簡化管理 | 集中的虛擬化管理平台 | 降低維運成本 |
| 災難復原 | VM 快照和遷移能力 | 簡化備份和復原流程 |

### 13.1.2 虛擬化類型

根據虛擬化的實現方式和抽象層次，可以分為幾種主要類型：

**完整虛擬化（Full Virtualization）**

完整虛擬化完全模擬底層硬體，Guest OS 無需任何修改即可運行。這種方式保持了最高的相容性，任何原本可以在實體硬體上運行的作業系統都可以在 VM 中運行。

完整虛擬化的實現通常依賴於二進制翻譯（Binary Translation）技術。當 Guest OS 執行特權指令（如修改記憶體管理暫存器）時，Hypervisor 會截獲這些指令，進行等效的模擬執行，而非讓 Guest OS 直接操作硬體。二進制翻譯的缺點是效能開銷較大，因為每次特權指令執行都需要 Hypervisor 介入。

**半虛擬化（Paravirtualization）**

半虛擬化要求修改 Guest OS，使其明確知道自己在虛擬環境中運行。Guest OS 不直接執行特權指令，而是透過 Hypercall 介面呼叫 Hypervisor 提供的服務。這種方式避免了昂貴的二進制翻譯，效能顯著提升，但犧牲了與未修改 OS 的相容性。

Xen 是半虛擬化的典型代表。Xen 的 Guest OS 需要修改以使用 Hypercall，而非直接存取硬體。這種設計在 2000 年代初期被廣泛使用，但隨著硬體輔助虛擬化的普及，半虛擬化的重要性有所下降。

| 特性 | 完整虛擬化 | 半虛擬化 |
|------|------------|----------|
| Guest OS 修改 | 不需要 | 需要 |
| 相容性 | 極高 | 受限於支援的 OS |
| 效能 | 較低（二進制翻譯） | 較高 |
| 複雜度 | 較低 | 較高 |

**硬體輔助虛擬化（Hardware-Assisted Virtualization）**

Intel VT-x 和 AMD-V 是 x86 架構的硬體虛擬化擴展，提供硬體級別的虛擬化支援。這些擴展引入了兩種 CPU 操作模式：

- **Root Mode**：供 Hypervisor 使用，具有完整硬體控制權
- **Non-Root Mode**：供 Guest OS 使用，受 Hypervisor 控制

當 Guest OS 執行特權指令時，CPU 自動切換到 Root Mode，讓 Hypervisor 處理。這種硬體支援大幅降低了虛擬化開銷，使得虛擬機的效能接近原生硬體。

### 13.1.3 Hypervisor 架構

Hypervisor（又稱虛擬機監視器，Virtual Machine Monitor, VMM）是管理虛擬機的核心軟體。根據與硬體的關係，Hypervisor 分為兩種架構：

**Type 1 Hypervisor（裸機虛擬化）**

Type 1 Hypervisor 直接運行在硬體上，沒有底層作業系統。這種架構提供了最高的效能和安全性，常用於企業資料中心和雲端環境。

```
┌─────────────────────────────────────────────┐
│                    硬體                       │
│  CPU │ 記憶體 │ 網路 │ 儲存                 │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│               Type 1 Hypervisor              │
│     (無作業系統，直接控制硬體)               │
└─────────────────────────────────────────────┘
          │              │              │
          ▼              ▼              ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │ Guest VM1 │  │ Guest VM2 │  │ Guest VM3 │
    │   (OS)    │  │   (OS)    │  │   (OS)    │
    └──────────┘  └──────────┘  └──────────┘
```

典型 Type 1 Hypervisor 包括：

| 產品 | 開發商 | 特點 |
|------|--------|------|
| VMware ESXi | VMware | 企業級、功能豐富 |
| Microsoft Hyper-V | Microsoft | 整合 Windows 生態 |
| Xen | Linux Foundation | 開源、雲端广泛使用 |
| KVM | 開源社區 | 整合 Linux 核心 |

**Type 2 Hypervisor（托管虛擬化）**

Type 2 Hypervisor 運行在傳統作業系統之上，依賴宿主作業系統提供裝置驅動和基礎設施。這種架構更易於部署和管理，常用於開發測試環境和個人桌面虛擬化。

```
┌─────────────────────────────────────────────┐
│                    硬體                       │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│              Host Operating System           │
│           (Windows / Linux / macOS)         │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│               Type 2 Hypervisor              │
│      (VirtualBox, VMware Workstation)        │
└─────────────────────────────────────────────┘
          │              │
          ▼              ▼
    ┌──────────┐  ┌──────────┐
    │ Guest VM1 │  │ Guest VM2 │
    └──────────┘  └──────────┘
```

典型 Type 2 Hypervisor 包括：

| 產品 | 開發商 | 平台 |
|------|--------|------|
| VirtualBox | Oracle | 跨平台開源 |
| VMware Workstation | VMware | Windows/Linux |
| VMware Fusion | VMware | macOS |
| Parallels Desktop | Parallels | macOS |

### 13.1.4 網路虛擬化

網路虛擬化是雲端環境的關鍵技術，使得 VM 可以像實體伺服器一樣連接到網路：

**虛擬交換機**

虛擬交換機（如 VMware vSwitch、Linux bridge、Open vSwitch）在 VM 之間和 VM 與實體網路之間轉發流量：

- **vSwitch**：同一主機上的 VM 之間流量交換
- **分散式 vSwitch**：跨多個主機的統一網路管理
- **Overlay 網路**：VXLAN、Geneve 等封裝協定支援多租戶

**SR-IOV 與 Passthrough**

對於高效能網路需求，Single Root I/O Virtualization (SR-IOV) 允許 VM 直接存取實體網路卡，繞過 Hypervisor 的軟體交換，實現接近原生的網路效能：

- **SR-IOV**：一個實體裝置虛擬化為多個虛擬功能（VF）
- **PCI Passthrough**：將整個 PCIe 裝置直接分配給 VM

## 13.2 Docker 容器技術

### 13.2.1 容器 vs 虛擬機

容器和虛擬機都是隔離執行環境的技術，但實現方式有根本差異：

```
虛擬機架構：
┌──────────────────────────────────────────────────┐
│  Host Hardware                                     │
└──────────────────────────────────────────────────┘
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Guest OS    │ │  Guest OS   │ │  Guest OS    │
├──────────────┤ ├──────────────┤ ├──────────────┤
│   App A      │ │   App B     │ │   App C      │
└──────────────┘ └──────────────┘ └──────────────┘
        ▲              ▲              ▲
        │              │              │
   完整 OS        完整 OS         完整 OS

容器架構：
┌──────────────────────────────────────────────────┐
│  Host OS / Kernel                                  │
└──────────────────────────────────────────────────┘
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   App A      │ │   App B     │ │   App C      │
│   Libs       │ │   Libs      │ │   Libs       │
├──────────────┤ ├──────────────┤ ├──────────────┤
│   Container  │ │   Container  │ │   Container  │
└──────────────┘ └──────────────┘ └──────────────┘
        │              │              │
   共享 Kernel    共享 Kernel    共享 Kernel
```

| 特性 | 虛擬機 | 容器 |
|------|--------|------|
| 隔離層次 | 硬體 | OS（透過 Namespace/Cgroup） |
| 開機時間 | 分鐘級 | 秒級（百毫秒級） |
| 效能損耗 | 5-10% | 1-3%（部分場景接近零損耗） |
| 映像檔大小 | GB 級（完整 OS） | MB 級（精簡環境） |
| 部署密度 | 數十個 VM/主機 | 數百個容器/主機 |
| 啟動隔離 | 完整硬體模擬 | 程序級隔離 |
| 安全性 | 強（完整 OS 隔離） | 中等（共用 Kernel） |

### 13.2.2 Docker 架構

Docker 是目前最流行的容器平台，其架構由多個元件組成：

```
┌──────────────────────────────────────────────────────────────┐
│                      Docker Client                          │
│                  (docker CLI 工具)                          │
└───────────────────────────┬──────────────────────────────────┘
                            │ REST API (Unix Socket)
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    Docker Daemon (dockerd)                  │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐ │
│  │  Containerd    │  │    Graph       │  │   Network     │ │
│  │  (Container    │  │    Driver      │  │   Driver      │ │
│  │   Runtime)     │  │  (Image Layer) │  │               │ │
│  └────────────────┘  └────────────────┘  └───────────────┘ │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    Container Runtime                         │
│                    (runc / runhcs)                          │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                      Linux Kernel                           │
│                  (Namespace / Cgroup / Seccomp)              │
└──────────────────────────────────────────────────────────────┘
```

**核心元件**

| 元件 | 說明 |
|------|------|
| Docker Client | 命令列工具，與 Daemon 溝通 |
| Docker Daemon | 後台服務，管理容器、影像、網路等 |
| containerd | 容器執行時，負責容器生命週期管理 |
| runc | 底層容器執行器，根據 OCI 規範創建容器 |
| Docker Registry | 存放 Docker 影像的服務（如 Docker Hub） |

### 13.2.3 Docker 核心概念

**Docker 影像（Image）**

Docker 影像是一種分層的唯讀範本，用於創建容器。影像由多個層組成，每層代表 Dockerfile 中的一個指令：

```dockerfile
# 多階段構建範例
# 第一階段：構建
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 第二階段：運行
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Dockerfile 指令詳解**

| 指令 | 說明 | 範例 |
|------|------|------|
| FROM | 指定基礎影像 | `FROM python:3.11-slim` |
| RUN | 執行命令（創建層） | `RUN pip install flask` |
| COPY/ADD | 複製檔案到影像 | `COPY ./app /app` |
| WORKDIR | 設定工作目錄 | `WORKDIR /app` |
| ENV | 設定環境變數 | `ENV PORT=8080` |
| EXPOSE | 宣告監聽連接埠 | `EXPOSE 3000` |
| CMD | 容器啟動命令 | `CMD ["python", "app.py"]` |
| ENTRYPOINT | 入口點（不可覆蓋） | `ENTRYPOINT ["./entry.sh"]` |
| VOLUME | 宣告持久化掛載點 | `VOLUME ["/data"]` |
| ARG | 構建時變數 | `ARG VERSION=1.0` |
| ENV | 執行時環境變數 | `ENV NODE_ENV=production` |

**Docker 容器（Container）**

容器是影像的運行實例。容器的生命週期：

```
Created → Starting → Running → Stopped → Removed
              ↓         ↑
           Restarting
```

關鍵操作：
```bash
# 建立並啟動容器
docker run -d --name myapp -p 8080:3000 -v /data:/data myimage

# 列出執行中的容器
docker ps

# 列出所有容器
docker ps -a

# 停止/啟動容器
docker stop myapp
docker start myapp

# 查看容器日誌
docker logs -f myapp

# 進入容器內部
docker exec -it myapp /bin/sh

# 查看容器資源使用
docker stats myapp
```

**容器網路**

Docker 提供多種網路模式：

| 模式 | 說明 | 使用場景 |
|------|------|----------|
| bridge | 預設模式，容器在私有網路中 | 單一主機上的容器通訊 |
| host | 容器直接使用主機網路 | 高效能網路應用 |
| overlay | 跨主機容器網路 | Docker Swarm 叢集 |
| macvlan | 容器有獨立 MAC 位址 | 需直接回應網路請求 |
| none | 禁用網路 | 隔離容器 |

### 13.2.4 Docker Compose

Docker Compose 用於定義和管理多容器應用：

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://db:5432/myapp
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./app:/app
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

## 13.3 Kubernetes 與容器編排

### 13.3.1 容器編排的需求

當容器數量增加到數百甚至數千時，手動管理變得不可行。容器編排平台解決了以下問題：

- **部署**：如何將應用部署到多個節點
- **擴展**：如何根據負載自動調整副本數
- **網路**：如何讓分散在不同節點的容器互相發現和通訊
- **儲存**：如何持久化資料和管理共享儲存
- **滾動更新**：如何在零停機時間內更新應用
- **自我修復**：如何自動重啟失敗的容器

### 13.3.2 Kubernetes 架構

Kubernetes（又稱 K8s）是 Google 開源的容器編排平台，已成為容器編排的事實標準：

```
┌──────────────────────────────────────────────────────────────┐
│                      Control Plane                          │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────────────┐ │
│  │ API Server  │  │   etcd      │  │   Scheduler       │ │
│  │ (HTTP API)  │◄─┤ (分散式儲存)│◄─┤ (節點調度)        │ │
│  └─────────────┘  └─────────────┘  └───────────────────┘ │
│  ┌─────────────────────────────┐  ┌───────────────────┐   │
│  │   Controller Manager        │  │   Cloud Manager   │   │
│  │   (狀態調控)               │  │   (雲端整合)      │   │
│  └─────────────────────────────┘  └───────────────────┘   │
└───────────────────────────┬───────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│     Node 1        │ │     Node 2        │ │     Node 3        │
│  ┌──────────────┐ │ │  ┌──────────────┐ │ │  ┌──────────────┐ │
│  │   Kubelet   │ │ │  │   Kubelet   │ │ │  │   Kubelet   │ │
│  │   Kube-proxy│ │ │  │   Kube-proxy│ │ │  │   Kube-proxy│ │
│  └──────────────┘ │ │  └──────────────┘ │ │  └──────────────┘ │
│  ┌──────┐┌──────┐│ │  ┌──────┐┌──────┐│ │  ┌──────┐┌──────┐│
│  │ Pod A││ Pod B││ │  │ Pod C││ Pod D││ │  │ Pod E││ Pod F││
│  └──────┘└──────┘│ │  └──────┘└──────┘│ │  └──────┘└──────┘│
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

**Control Plane 元件**

| 元件 | 功能 |
|------|------|
| API Server | 暴露 Kubernetes API，所有元件透過它通訊 |
| etcd | 高可用鍵值儲存，保存叢集所有狀態 |
| Scheduler | 根據資源需求和策略選擇節點部署 Pod |
| Controller Manager | 執行控制迴圈，維護期望狀態 |

**Node 元件**

| 元件 | 功能 |
|------|------|
| Kubelet | 確保容器在 Pod 中運行，管理節點資源 |
| Kube-proxy | 維護網路規則，實現 Service 的網路存取 |
| Container Runtime | 實際執行容器（通常是 containerd） |

### 13.3.3 Kubernetes 核心資源

**Pod**

Pod 是 Kubernetes 的最小部署單元。一個 Pod 包含一或多個共享網路和儲存的容器：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
    version: v1
spec:
  containers:
  - name: nginx
    image: nginx:1.25-alpine
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
      initialDelaySeconds: 3
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 5
```

**Deployment**

Deployment 管理 Pod 的部署和更新：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:2.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secret
              key: database-url
        - name: CACHE_URL
          valueFrom:
            configMapKeyRef:
              name: myapp-config
              key: cache-url
```

**Service**

Service 為一組 Pod 提供穩定的存取端點：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP  # ClusterIP / NodePort / LoadBalancer
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: admin
    port: 443
    targetPort: 8443
```

**Ingress**

Ingress 提供 HTTP/HTTPS 路由到 Service：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/limit-rps: "100"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### 13.3.4 Helm 與 Helm Chart

Helm 是 Kubernetes 的套件管理工具，類似 apt/yum 之於 Linux。Helm Chart 封裝了 Kubernetes 資源的集合：

```bash
# 安裝 Chart
helm install myapp ./myapp-chart

# 查看已安裝的 Release
helm list

# 升級 Release
helm upgrade myapp ./myapp-chart --set image.tag=v2.0

# 回滾到上一版本
helm rollback myapp
```

### 13.3.5 自我修復與擴展

**HPA（水平 Pod 自動擴縮）**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**PodDisruptionBudget**

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2  # 或 maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```

## 13.4 IaaS、PaaS、SaaS 模型

### 13.4.1 雲端服務層級

雲端運算提供了不同抽象層次的服務，使用者根據需求選擇適合的層級：

| 模型 | 提供內容 | 使用者管理範圍 | 靈活性 | 複雜度 |
|------|----------|----------------|--------|--------|
| IaaS | 基礎設施（運算、儲存、網路） | OS、Runtime、資料 | 高 | 高 |
| PaaS | 平台（執行環境、資料庫、訊息佇列） | 應用程式、資料 | 中 | 中 |
| SaaS | 軟體（完整應用） | 僅使用和資料 | 低 | 低 |

```
┌────────────────────────────────────────────────────────────┐
│                        SaaS                                │
│              完整應用程式（Salesforce、Office 365）         │
├────────────────────────────────────────────────────────────┤
│                        PaaS                                │
│       執行環境（Heroku、GAE）+ 資料庫服務（AWS RDS）       │
├────────────────────────────────────────────────────────────┤
│                        IaaS                                │
│         虛擬機（EC2、GCE、Azure VM）+ 區塊儲存            │
├────────────────────────────────────────────────────────────┤
│                        實體基礎設施                         │
│                    裸機伺服器、網路設備                    │
└────────────────────────────────────────────────────────────┘
```

### 13.4.2 主要雲端平台服務

**AWS（Amazon Web Services）**

| 類別 | 服務 |
|------|------|
| 運算 | EC2、Lambda（無伺服器）、ECS/EKS（容器） |
| 儲存 | S3（物件儲存）、EBS（區塊儲存）、EFS（檔案儲存） |
| 資料庫 | RDS、 DynamoDB（NoSQL）、ElastiCache |
| 網路 | VPC、Route 53、CloudFront（CDN） |
| 安全 | IAM、KMS、WAF |

**GCP（Google Cloud Platform）**

| 類別 | 服務 |
|------|------|
| 運算 | Compute Engine、GKE、Kubernetes Engine、Cloud Functions |
| 儲存 | Cloud Storage、Persistent Disk、Filestore |
| 資料庫 | Cloud SQL、Cloud Spanner、Firestore |
| 網路 | VPC、Cloud DNS、Cloud CDN |
| ML/AI | Vertex AI、TensorFlow Enterprise |

**Azure（Microsoft Azure）**

| 類別 | 服務 |
|------|------|
| 運算 | Azure VM、Azure Kubernetes Service、Azure Functions |
| 儲存 | Azure Blob Storage、Azure Files、Azure Disk |
| 資料庫 | Azure SQL、Azure Cosmos DB、Azure Cache |
| 網路 | Azure Virtual Network、Azure DNS、Azure CDN |

## 13.5 雲端儲存與分散式系統

### 13.5.1 CAP 定理

Eric Brewer 提出的 CAP 定理指出，在分散式系統中，不可能同時滿足以下三個特性：

| 特性 | 說明 |
|------|------|
| Consistency（一致性） | 所有節點在任何時刻看到相同的資料 |
| Availability（可用性） | 每個請求都能收到回應（無論成功或失敗） |
| Partition Tolerance（分割容許性） | 網路分割（訊息丟失）時系統仍能運作 |

在真實的分散式系統中，網路分割是不可避免的，因此系統必須在一致性和可用性之間做出選擇：

- **CP 系統**：放棄可用性，在分割期間拒絕寫入或回應
- **AP 系統**：放棄強一致性，在分割期間繼續服務但可能返回過時資料

```
                    Consistency
                         ▲
                        / \
                       /   \
                      / CP  \
                     /       \
                    /─────────\
                   /    AP     \
                  /             \
                 ▼───────────────▼
          Availability        Partition Tolerance
```

### 13.5.2 一致性模型

一致性的強度有多種級別：

| 模型 | 說明 | 效能影響 |
|------|------|----------|
| 強一致性（Linearizability） | 所有操作看似原子且即時執行 | 最低效能 |
| 順序一致性（Sequential） | 所有節點看到相同的操作順序 | 低效能 |
| 因果一致性（Causal） | 有因果關係的操作順序一致 | 中效能 |
| 最終一致性（Eventual） | 系統最終會收斂到一致狀態 | 高效能 |
| 讀取己寫入（Read-your-writes） | 讀取能看到自己的寫入 | 中效能 |

**最終一致性的實現**

Dynamo、Cassandra 等 AP 系統使用以下技術實現最終一致性：

- **向量時鐘**：追蹤版本因果關係
- **讀取修復**：讀取時檢測並修復過時資料
- **反熵（Anti-Entropy）**：背景同步修補資料庫
- **提示移交（Hinted Handoff）**：臨時處理節點故障

### 13.5.3 分散式共識演算法

在分散式系統中，多個節點需要就某些值達成一致。共識演算法是構建可靠分散式系統的基礎。

**Paxos**

Leslie Lamport 設計的 Paxos 是最經典的共識演算法，但複雜度很高。Paxos 確保：

- **一致性**：只有被多數節點接受的值才會被選定
- **有效性**：被選定的值必須是某個提議者的提議
- **結束性**（在合理條件下）：最終會選定一個值

Paxos 有兩個階段：

1. **準備階段（Prepare）**：提議者請求多數派的承諾
2. **接受階段（Accept）**：提議者請求多數派接受值

**Raft 共識演算法**

Diego Ongaro 設計的 Raft 是 Paxos 的簡化版本，更易於理解和實現。Raft 將共識問題分解為三個相對獨立的子問題：

| 子問題 | 說明 |
|--------|------|
| Leader 選舉 | 叢集選出一個 Leader，若 Leader 故障需重新選舉 |
| 日誌複製 | Leader 接收客戶端請求，複製到大多數節點 |
| 安全性 | 確保日誌一致性，Leader 只追加 |

Raft 的節點狀態：

```
           ┌────────┐
           │ Follower│
           └────┬────┘
                │ 選舉超時
                ▼
           ┌────────┐
           │Candidate│
           └────┬────┘
                │ 獲得多數票
                ▼
           ┌────────┐
           │ Leader │
           └────────┘
                │ 發現新 Leader 或更高 Term
                ▼
           ┌────────┐
           │ Follower│
           └────────┘
```

**應用場景**

| 系統 | 使用的共識演算法 | 應用場景 |
|------|-----------------|----------|
| etcd | Raft | Kubernetes 後端儲存 |
| Consul | Raft + gossip | 服務發現、配置 |
| ZooKeeper | Zab（Raft 變體） | 分散式鎖、協調 |
| TiDB | Raft | 分散式 SQL 資料庫 |
| CockroachDB | Raft | 分散式 SQL 資料庫 |

### 13.5.4 分散式交易

在分散式環境中，跨多個節點的交易需要特殊處理：

**Two-Phase Commit（2PC）**

2PC 是一種原子提交協定：

1. **準備階段**：協調者要求所有參與者「準備提交」
2. **提交階段**：所有參與者回應「可以提交」後，協調者下達提交命令

缺點：協調者故障可能導致叢集阻塞。

**Saga 模式**

Saga 將長事務拆分為多個本地事務，每個本地事務有對應的補償交易：

```
  Order Created → Payment Charged → Inventory Reserved → Order Completed
       ↓              ↓                   ↓
  Cancel Order  Refund Payment    Release Inventory
```

Saga 適用於不需要強一致性的場景，透過補償實現最終一致性。

### 13.5.5 分散式追蹤

在微服務架構中，一個請求可能跨越多個服務。分散式追蹤幫助理解請求路徑和效能瓶頸：

**OpenTelemetry 架構**

```
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Service A │──►│ Service B │──►│ Service C │
└────┬─────┘   └────┬─────┘   └────┬─────┘
     │               │               │
     ▼               ▼               ▼
┌─────────────────────────────────────────┐
│              OpenTelemetry SDK            │
│         (產生 Trace / Metrics)            │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│              Collector                    │
│         (接收、處理、轉發)                │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│         Backend (Jaeger, Zipkin, etc)   │
│           (儲存和視覺化追蹤)              │
└─────────────────────────────────────────┘
```
