# Docker

## 概述

Docker 是流行的容器平台，使用容器化技術打包和執行應用程式。Docker 容器比傳統虛擬機更輕量，啟動更快，是現代雲端原生應用的基礎。

## 歷史

- **2013**：Docker 發布
- **2014**：Docker Hub
- **2017**：Docker Enterprise
- **現在**：容器標準

## Docker 基本使用

### 1. 基本命令

```bash
# 列出容器
docker ps
docker ps -a

# 執行容器
docker run hello-world
docker run -d -p 8080:80 nginx

# 停止/啟動容器
docker stop container_id
docker start container_id

# 刪除容器
docker rm container_id

# 檢視日誌
docker logs -f container_id
```

### 2. Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]
```

### 3. 建立映像

```bash
# 建立映像
docker build -t myapp:latest .

# 列出映像
docker images

# 刪除映像
docker rmi image_id

# 推送至 registry
docker push myapp:latest
```

### 4. Docker Compose

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=db:5432
    depends_on:
      - db
    volumes:
      - ./data:/app/data

  db:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### 5. Docker 網路

```bash
# 建立網路
docker network create mynetwork

# 執行並連接
docker run --network mynetwork -d nginx

# 在同一網路的容器可以透過容器名稱通訊
```

### 6. 資料卷

```bash
# 建立資料卷
docker volume create mydata

# 使用資料卷
docker run -v mydata:/data mysql

# 綁定主機目錄
docker run -v /host/path:/container/path nginx
```

## 為什麼使用 Docker？

1. **一致環境**：開發/生產環境一致
2. **快速部署**：秒級啟動
3. **隔離**：應用隔離
4. **輕量**：共用核心

## 參考資源

- Docker 官方文檔
- "Docker: Up & Running"
