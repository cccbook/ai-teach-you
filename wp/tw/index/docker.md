# Docker

## 概述

Docker 是一個開源的容器化平台，讓開發者可以將應用程式及其依賴封裝在輕量級的容器中，確保在任何環境中都能一致運行。

## 核心概念

### 容器 vs 虛擬機

```
┌─────────────────────────────────────────────┐
│              Virtual Machine                │
│  ┌─────┐  ┌─────┐  ┌─────┐                │
│  │ App │  │ App │  │ App │   Guest OS     │
│  ├─────┤  ├─────┤  ├─────┤                │
│  │ Lib │  │ Lib │  │ Lib │                │
│  ├─────┤  ├─────┤  ├─────┤                │
│  │ OS  │  │ OS  │  │ OS  │                │
│  └─────┘  └─────┘  └─────┘                │
│              Hypervisor                     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│              Docker Container                │
│  ┌─────┐  ┌─────┐  ┌─────┐                │
│  │ App │  │ App │  │ App │                │
│  ├─────┤  ├─────┤  ├─────┤                │
│  │ Lib │  │ Lib │  │ Lib │   Shared Kernel│
│  └─────┘  └─────┘  └─────┘                │
└─────────────────────────────────────────────┘
```

### 映像檔（Image）

唯讀模板，用於建立容器：

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### 容器（Container）

映像檔的執行實例：

```bash
# 啟動容器
docker run nginx

# 互動模式
docker run -it ubuntu bash

# 後台執行
docker run -d nginx

# 映射連接埠
docker run -p 8080:80 nginx
```

## 基本命令

### 映像檔操作

```bash
# 列出映像檔
docker images

# 拉取映像檔
docker pull ubuntu:20.04

# 刪除映像檔
docker rmi ubuntu:20.04

# 構建映像檔
docker build -t myapp:latest .

# 查看映像檔歷史
docker history myapp:latest
```

### 容器操作

```bash
# 列出執行中的容器
docker ps

# 列出所有容器
docker ps -a

# 啟動/停止/刪除容器
docker start container_name
docker stop container_name
docker rm container_name

# 進入容器
docker exec -it container_name bash

# 查看日誌
docker logs -f container_name

# 查看資源使用
docker stats
```

### Docker Hub

```bash
# 登入
docker login

# 推送映像檔
docker tag myapp:latest username/myapp:latest
docker push username/myapp:latest

# 搜尋映像檔
docker search nginx
```

## Dockerfile

### 多階段建構

```dockerfile
# 建構階段
FROM node:18 AS builder
WORKDIR /app
COPY . .
RUN npm run build

# 生產階段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

### .dockerignore

```
node_modules
.git
*.log
.env
```

## Docker Compose

用於定義和執行多容器應用：

```yaml
version: '3.8'

services:
    web:
        build: .
        ports:
            - "3000:3000"
        environment:
            - NODE_ENV=production
        depends_on:
            - db
        volumes:
            - ./data:/app/data

    db:
        image: postgres:15
        environment:
            POSTGRES_USER: user
            POSTGRES_PASSWORD: password
            POSTGRES_DB: mydb
        volumes:
            - postgres_data:/var/lib/postgresql/data

    redis:
        image: redis:alpine

volumes:
    postgres_data:
```

```bash
# 啟動服務
docker-compose up -d

# 停止服務
docker-compose down

# 重新建構
docker-compose up -d --build

# 查看日誌
docker-compose logs -f
```

## 常用範例

### FastAPI 應用

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### React 應用

```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

## 參考資源

- [Docker 官方網站](https://www.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
