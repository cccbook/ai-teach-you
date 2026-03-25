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