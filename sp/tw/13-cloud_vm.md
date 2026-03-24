# 13. 雲端技術與虛擬機

## 13.1 虛擬化技術

[程式檔案：13-1-virtualization.py](../_code/13/13-1-virtualization.py)
```python
"""
虛擬化技術
"""

# 1. 模擬虛擬化（Full Virtualization）
class VirtualMachine:
    """完整虛擬機"""
    
    def __init__(self, name, memory_mb=1024, cpu_cores=1):
        self.name = name
        self.memory = memory_mb * 1024 * 1024  # bytes
        self.cpu_cores = cpu_cores
        self.virtual_disks = []
        self.virtual_nics = []
        self.state = 'stopped'
    
    def start(self):
        """啟動虛擬機"""
        self.state = 'running'
        print(f"虛擬機 {self.name} 啟動")
        print(f"  CPU: {self.cpu_cores} 核心")
        print(f"  記憶體: {self.memory // (1024*1024)} MB")
    
    def stop(self):
        """停止虛擬機"""
        self.state = 'stopped'
        print(f"虛擬機 {self.name} 停止")
    
    def add_disk(self, size_gb):
        """新增虛擬磁碟"""
        disk = {'size': size_gb * 1024**3, 'name': f"{self.name}-disk{len(self.virtual_disks)}"}
        self.virtual_disks.append(disk)
        print(f"新增磁碟: {disk['name']}, {size_gb}GB")
    
    def add_network(self):
        """新增虛擬網卡"""
        nic = {'mac': f"52:54:00:{':'.join(f'{random.randint(0,255):02x}' for _ in range(2))}"}
        self.virtual_nics.append(nic)
        print(f"新增網卡: {nic['mac']}")

# 2. 容器虛擬化
class Container:
    """容器"""
    
    def __init__(self, image, name=None):
        self.image = image
        self.name = name or image
        self.environment = {}
        self.mounts = []
        self.limits = {'cpu': 1.0, 'memory': '512m'}
        self.state = 'created'
    
    def run(self):
        """執行容器"""
        self.state = 'running'
        print(f"容器 {self.name} 執行中 (image: {self.image})")
        print(f"  CPU limit: {self.limits['cpu']}")
        print(f"  Memory: {self.limits['memory']}")
    
    def stop(self):
        """停止容器"""
        self.state = 'stopped'
        print(f"容器 {self.name} 停止")
    
    def set_env(self, key, value):
        """設定環境變數"""
        self.environment[key] = value
    
    def mount(self, host_path, container_path):
        """掛載目錄"""
        self.mounts.append({'host': host_path, 'container': container_path})

# 3. 虛擬化類型比較
print("""
=== 虛擬化類型 ===

1. 完整虛擬化（Full）
   - 模擬完整硬體
   - 例: QEMU, VirtualBox
   - 需要 Hypervisor

2. 半虛擬化（Para）
   - 修改 Guest OS
   - 例: Xen, VMware
   - 效能較好

3. 容器虛擬化
   - 共享核心
   - 例: Docker, LXC
   - 輕量快速

4. 作業系統層虛擬化
   - 例: FreeBSD Jails, Solaris Zones
""")

# 測試
vm = VirtualMachine("test-vm", memory_mb=2048, cpu_cores=2)
vm.add_disk(40)
vm.add_disk(100)
vm.add_network()
vm.start()
vm.stop()
```

## 13.2 Docker 容器技術

[程式檔案：13-2-docker.py](../_code/13/13-2-docker.py)
```python
"""
Docker 概念與操作
"""

# Docker 核心概念
class Docker:
    """Docker 模擬"""
    
    def __init__(self):
        self.images = {}
        self.containers = {}
        self.networks = {}
        self.volumes = {}
    
    # 映像檔操作
    def pull(self, image_name):
        """拉取映像檔"""
        print(f"拉取映像檔: {image_name}")
        self.images[image_name] = {
            'name': image_name,
            'layers': [],
            'size': 100  # MB
        }
    
    def build(self, dockerfile, tag):
        """建構映像檔"""
        print(f"建構映像檔: {tag}")
        self.images[tag] = {'name': tag, 'dockerfile': dockerfile}
    
    def images_list(self):
        """列出映像檔"""
        print("=== 映像檔 ===")
        for name, img in self.images.items():
            print(f"  {name} ({img['size']}MB)")
    
    # 容器操作
    def run(self, image, name=None, detach=False, ports=None, env=None, volumes=None):
        """執行容器"""
        container_id = f"{random.randint(1000,9999)}"
        container = {
            'id': container_id,
            'image': image,
            'name': name or f"happy_{container_id}",
            'status': 'running',
            'ports': ports or {},
            'env': env or {},
            'volumes': volumes or []
        }
        self.containers[container_id] = container
        print(f"執行容器: {container['name']} ({container_id})")
        if ports:
            print(f"  連接埠: {ports}")
        return container_id
    
    def ps(self, all=False):
        """列出容器"""
        print("=== 容器 ===")
        for cid, c in self.containers.items():
            status = c['status']
            if all or status == 'running':
                print(f"  {cid[:12]} {c['name']} {c['image']} {status}")
    
    def stop(self, container_id):
        """停止容器"""
        if container_id in self.containers:
            self.containers[container_id]['status'] = 'exited'
            print(f"停止容器: {container_id}")
    
    def rm(self, container_id):
        """刪除容器"""
        if container_id in self.containers:
            del self.containers[container_id]
            print(f"刪除容器: {container_id}")
    
    # 網路操作
    def network_create(self, name, driver='bridge'):
        """建立網路"""
        self.networks[name] = {'name': name, 'driver': driver}
        print(f"建立網路: {name} (driver: {driver})")
    
    # 卷操作
    def volume_create(self, name):
        """建立卷"""
        self.volumes[name] = {'name': name}
        print(f"建立卷: {name}")

# Dockerfile 概念
print("""
=== Dockerfile 範例 ===

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]

指令說明:
- FROM: 基礎映像檔
- WORKDIR: 工作目錄
- COPY: 複製檔案
- RUN: 執行指令
- EXPOSE: 宣告連接埠
- CMD: 預設命令
- ENV: 環境變數
""")

# docker-compose 概念
print("""
=== docker-compose.yml ===

version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE=db
    depends_on:
      - db
  
  db:
    image: postgres:13
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
""")

# 測試
docker = Docker()
docker.pull("nginx:latest")
docker.pull("postgres:13")
docker.images_list()
docker.run("nginx:latest", ports={"80": 8080}, detach=True)
docker.ps()
```

## 13.3 Kubernetes 與容器編排

[程式檔案：13-3-kubernetes.py](../_code/13/13-3-kubernetes.py)
```python
"""
Kubernetes
"""

class Kubernetes:
    """Kubernetes 模擬"""
    
    def __init__(self):
        self.pods = {}
        self.services = {}
        self.deployments = {}
        self.nodes = []
    
    # Pod 操作
    def create_pod(self, name, image, replicas=1):
        """建立 Pod"""
        pod = {
            'name': name,
            'image': image,
            'replicas': replicas,
            'status': 'Running',
            'labels': {}
        }
        self.pods[name] = pod
        print(f"建立 Pod: {name} (image: {image})")
    
    def get_pod(self, name):
        """取得 Pod 狀態"""
        if name in self.pods:
            pod = self.pods[name]
            print(f"Pod: {name}, Status: {pod['status']}")
            return pod
    
    def delete_pod(self, name):
        """刪除 Pod"""
        if name in self.pods:
            del self.pods[name]
            print(f"刪除 Pod: {name}")
    
    # Service 操作
    def create_service(self, name, selector, port, target_port):
        """建立 Service"""
        service = {
            'name': name,
            'selector': selector,
            'port': port,
            'target_port': target_port,
            'type': 'ClusterIP'
        }
        self.services[name] = service
        print(f"建立 Service: {name} (port: {port})")
    
    # Deployment 操作
    def create_deployment(self, name, image, replicas):
        """建立 Deployment"""
        deployment = {
            'name': name,
            'image': image,
            'replicas': replicas,
            'available_replicas': replicas
        }
        self.deployments[name] = deployment
        
        # 建立對應的 Pod
        for i in range(replicas):
            pod_name = f"{name}-{i}"
            self.create_pod(pod_name, image)
        
        print(f"建立 Deployment: {name} (replicas: {replicas})")
    
    def scale_deployment(self, name, replicas):
        """擴展 Deployment"""
        if name in self.deployments:
            self.deployments[name]['replicas'] = replicas
            print(f"擴展 Deployment {name} 到 {replicas} 個副本")

# Kubernetes 概念
print("""
=== Kubernetes 核心概念 ===

Pod:
- 最小的部署單元
- 一或多個容器
- 共享網路/儲存

Service:
- 服務發現
- 負載平衡
- 類型: ClusterIP, NodePort, LoadBalancer

Deployment:
- 宣告式更新
- 滾動更新
- 水平擴展

StatefulSet:
- 有狀態應用
- 穩定網路識別
- 穩定儲存

DaemonSet:
- 每個節點一個 Pod
- 日誌收集
- 監控代理
""")

# YAML 範例
print("""
=== deployment.yaml ===

apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
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
        image: myapp:1.0
        ports:
        - containerPort: 8080
        resources:
          limits:
            cpu: "500m"
            memory: "256Mi"
""")

# 測試
k8s = Kubernetes()
k8s.create_deployment("web", "nginx:1.19", 3)
k8s.create_service("web-svc", "app=web", 80, 8080)
k8s.scale_deployment("web", 5)
```

## 13.4 IaaS、PaaS、SaaS 模型

[程式檔案：13-4-cloud-service.py](../_code/13/13-4-cloud-service.py)
```python
"""
雲端服務模型
"""

class CloudService:
    """雲端服務比較"""
    
    @staticmethod
    def compare_models():
        """比較服務模型"""
        print("""
=== IaaS vs PaaS vs SaaS ===

| 特性         | IaaS           | PaaS          | SaaS          |
|--------------|----------------|---------------|---------------|
| 提供內容     | 基礎設施       | 平台          | 軟體          |
| 使用者管理   | 作業系統以上   | 應用程式      | 無            |
| 控制權       | 高             | 中            | 低            |
| 範例         | AWS EC2        | Heroku        | Gmail         |
| 彈性         | 高             | 中            | 低            |
| 複雜度       | 高             | 中            | 低            |

=== IaaS ===
- 虛擬機器
- 儲存
- 網路
- 例: AWS EC2, GCP Compute Engine, Azure VM
- 使用者負責: OS、應用程式、資料

=== PaaS ===
- 執行環境
- 資料庫
- 開發框架
- 例: Heroku, Google App Engine, Azure App Service
- 使用者負責: 應用程式、資料

=== SaaS ===
- 完整軟體
- 透過瀏覽器存取
- 例: Salesforce, Microsoft 365, Google Workspace
- 使用者負責: 資料
""")
    
    @staticmethod
    def pricing_model():
        """定價模型"""
        print("""
=== 雲端定價模型 ===

1. 按需付費 (On-Demand)
   - 按小時/分鐘計費
   - 無長期承諾
   - 例: EC2 按需執行個體

2. 預留實例 (Reserved)
   - 一年/三年承諾
   - 折扣可達 60%
   - 例: AWS RI, Azure RI

3. .spot/搶佔式
   - 折扣可達 90%
   - 可能被回收
   - 例: AWS Spot, GCP Preemptible

4. 伺服器less
   - 按請求計費
   - 無須管理伺服器
   - 例: AWS Lambda, Cloud Functions
""")

# 雲端服務商比較
print("""
=== 主要雲端服務商 ===

AWS:
- 最早、最大
- 服務最完整
- 例: EC2, S3, Lambda, RDS

GCP:
- 技術領先
- 機器學習很強
- 例: Compute Engine, Cloud Storage, BigQuery

Azure:
- Microsoft 生態
- 企業市場強
- 例: VM, Azure SQL, Functions
""")

# 測試
CloudService.compare_models()
CloudService.pricing_model()
```

## 13.5 雲端儲存與分散式系統

[程式檔案：13-5-distributed-storage.py](../_code/13/13-5-distributed-storage.py)
```python
"""
雲端儲存與分散式系統
"""

import hashlib

# 分散式儲存
class DistributedStorage:
    """分散式儲存"""
    
    def __init__(self, num_nodes=3):
        self.nodes = [f"node-{i}" for i in range(num_nodes)]
        self.data = {}  # key -> [(node, data)]
        self.replication_factor = 2
    
    def put(self, key, value):
        """儲存資料"""
        # 簡單的資料分散：雜湊
        node_index = int(hashlib.md5(key.encode()).hexdigest(), 16) % len(self.nodes)
        
        nodes_to_store = []
        for i in range(self.replication_factor):
            idx = (node_index + i) % len(self.nodes)
            nodes_to_store.append(self.nodes[idx])
        
        self.data[key] = nodes_to_store
        print(f"儲存 '{key}' 到 {nodes_to_store}")
    
    def get(self, key):
        """取得資料"""
        if key in self.data:
            nodes = self.data[key]
            print(f"從 {nodes[0]} 讀取 '{key}'")
            return True
        return False
    
    def delete(self, key):
        """刪除資料"""
        if key in self.data:
            del self.data[key]
            print(f"刪除 '{key}'")

# CAP 定理
print("""
=== CAP 定理 ===

分散式系統最多只能滿足三個特性中的兩個：

C (Consistency) - 一致性
- 所有節點看到相同的資料

A (Availability) - 可用性
- 每個請求都會收到回應

P (Partition Tolerance) - 分區容錯
- 系統在網路分割時仍能運作

實際選擇:
- CP: 犧牲可用性 (如: ZooKeeper, etcd)
- AP: 犧牲一致性 (如: Cassandra, DynamoDB)
- CA: 不可能在分散式系統中實現
""")

# 一致性模型
print("""
=== 一致性模型 ===

1. 強一致性
   - 所有讀取都看到最新的寫入
   - 例: 傳統資料庫

2. 最終一致性
   - 最終會達到一致
   - 例: DynamoDB, Cassandra

3. 讀寫一致性
   - 讀取能看到自己寫入的結果
   - 例: Amazon S3

4. 因果一致性
   - 有因果關係的操作順序一致
   - 例: Cassandra (某些場景)
""")

# 分散式共識
print("""
=== 分散式共識 ===

Raft 共識演算法:
- Leader 選舉
- 日誌複製
- 安全性

Paxos:
- 提議-接受協議
- 更理論化

應用:
- 分散式鎖
- 服務發現
- 設定管理
""")

# 測試
storage = DistributedStorage(num_nodes=4)
storage.put("user:1", "John")
storage.put("user:2", "Jane")
storage.get("user:1")
storage.get("user:2")
storage.delete("user:1")
```