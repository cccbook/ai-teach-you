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