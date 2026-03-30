# 23. 容器化與 Docker

## 為什麼需要容器

```
┌─────────────────────────────────────────────────────────┐
│                   容器解决的问题                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   開發環境：「在我機器上能跑啊！」                        │
│                    ↓                                    │
│   容器化：「在任何環境都能跑！」                          │
│                                                         │
│   • 一致的开发、测试、生产环境                           │
│   • 快速启动和销毁                                      │
│   • 资源隔离                                            │
│   • 易于扩展                                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Docker 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                    Docker 核心                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Image（镜像）                                         │
│   │ 文件系统的快照，只读模板                             │
│                                                         │
│   Container（容器）                                     │
│   │ 镜像的运行实例，可写层                               │
│                                                         │
│   Dockerfile                                            │
│   │ 构建镜像的指令文件                                   │
│                                                         │
│   Registry（仓库）                                       │
│   │ 存储和分发镜像的服务                                │
│   │ (Docker Hub, ECR, GCR)                             │
│                                                         │
│   Docker Compose                                        │
│   │ 定义多容器应用                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助 Dockerfile

### 基礎 Dockerfile

```
你：
请为 Node.js 应用创建 Dockerfile。

AI：
## Dockerfile

```dockerfile
# 构建阶段
FROM node:20-alpine AS builder

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

# 构建
RUN npm run build

# 生产阶段
FROM node:20-alpine AS production

WORKDIR /app

# 创建非 root 用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001

# 复制构建产物
COPY --from=builder --chown=nodeuser:nodejs /app/dist ./dist
COPY --from=builder --chown=nodeuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodeuser:nodejs /app/package.json ./

# 切换用户
USER nodeuser

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "dist/main.js"]
```

### 最佳化 Dockerfile

```
你：
这个 Dockerfile 可以怎么优化？

AI：
## Dockerfile 优化

### 1. 使用多阶段构建
减少最终镜像大小

### 2. 合并 RUN 指令
减少镜像层数

### 优化前：
```dockerfile
RUN npm install
RUN npm audit fix
RUN npm run build
```

### 优化后：
```dockerfile
RUN npm ci && \
    npm audit fix && \
    npm run build && \
    npm prune --production
```

### 3. 使用 .dockerignore
```dockerfile
# .dockerignore
node_modules
.git
*.md
.env*
dist
coverage
.nyc_output
```

### 4. 利用构建缓存
```dockerfile
# 先复制依赖文件
COPY package*.json ./
RUN npm ci

# 再复制源代码
COPY . .
RUN npm run build
```

### 5. 使用更小的基础镜像
```dockerfile
# 大小对比
node:20          # ~1.1GB
node:20-alpine   # ~180MB
```
```

## Docker Compose

### 基礎配置

```
你：
请帮我创建 Docker Compose 配置，包含：
- Node.js 应用
- PostgreSQL 数据库
- Redis 缓存

AI：
## docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/myapp
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    volumes:
      - .:/app
      - /app/node_modules
    command: npm run dev

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 開發 vs 生產配置

```
你：
开发和生产环境应该使用不同的 Docker 配置吗？

AI：
## 开发 vs 生产配置

### 开发环境
```yaml
# docker-compose.yml
services:
  app:
    build: .
    volumes:
      - .:/app          # 热更新
      - /app/node_modules
    command: npm run dev
```

### 生产环境
```yaml
# docker-compose.prod.yml
services:
  app:
    build:
      context: .
      target: production
    volumes:
      - app_data:/app
    command: npm start
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### 使用不同配置
```bash
# 开发
docker-compose up -d

# 生产
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
```

## 常見應用場景

### 1. 前端應用

```
你：
请为 React 应用创建 Dockerfile。

AI：
## React Dockerfile

```dockerfile
# 构建
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Nginx 服务
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf
```nginx
events {
  worker_connections 1024;
}

http {
  include /etc/nginx/mime.types;
  default_type application/octet-stream;
  
  server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
      try_files $uri $uri/ /index.html;
    }
    
    location /api {
      proxy_pass http://backend:3000;
    }
  }
}
```

### 2. Python 應用

```
你：
请为 FastAPI 应用创建 Dockerfile。

AI：
## FastAPI Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 创建用户
RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
```

### 3. 多服務應用

```
你：
请为微服务架构创建 Docker 配置。

AI：
## 微服务 Docker Compose

```yaml
version: '3.8'

services:
  api-gateway:
    build: ./services/gateway
    ports:
      - "8080:8080"
    depends_on:
      - user-service
      - order-service

  user-service:
    build: ./services/users
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/users
    depends_on:
      db:
        condition: service_healthy

  order-service:
    build: ./services/orders
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/orders
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started

  db:
    image: postgres:15
    volumes:
      - pg_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: pass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
    depends_on:
      - api-gateway

volumes:
  pg_data:
  redis_data:
```

## Docker 網路

```
你：
Docker 容器之间如何通信？

AI：
## Docker 网络

### 1. 默认 bridge 网络
容器通过服务名通信

```yaml
services:
  web:
    networks:
      - my-network
  db:
    networks:
      - my-network

networks:
  my-network:
```

### 2. 端口暴露
```yaml
services:
  web:
    ports:
      - "3000:3000"      # 宿主机:容器
      - "8080-8090:8080" # 端口范围
```

### 3. 外部访问
```yaml
services:
  web:
    expose:
      - "3000"    # 仅内部可见
    ports:
      - "8080:3000"  # 外部可访问
```

### 4. DNS 解析
```bash
# 容器内访问其他容器
ping db          # 服务名
ping db:5432     # 带端口
```
```

## Docker 調試

```
你：
容器启动失败如何调试？

AI：
## Docker 调试

### 1. 查看日志
```bash
docker logs <container_id>
docker logs -f <container_id>        # 实时
docker logs --tail 100 <container_id> # 最近 100 行
```

### 2. 进入容器
```bash
docker exec -it <container_id> /bin/sh
docker exec -it <container_id> /bin/bash
```

### 3. 检查容器状态
```bash
docker ps -a                          # 所有容器
docker inspect <container_id>        # 详细信息
docker stats <container_id>          # 资源使用
```

### 4. 检查网络
```bash
docker network ls
docker network inspect <network_name>
```

### 5. 常见问题
```bash
# 端口冲突
docker port <container_id>

# 权限问题
docker exec -u root <container_id> chown -R user:user /path

# 文件权限
docker exec <container_id> ls -la /path
```

### 6. 清理重建
```bash
docker-compose down
docker-compose up --build --force-recreate
```
```

## Docker 安全

```
你：
Docker 容器有哪些安全注意事项？

AI：
## Docker 安全最佳实践

### 1. 不要用 root 运行
```dockerfile
RUN adduser -m -u 1001 appuser
USER appuser
```

### 2. 使用最小基础镜像
```dockerfile
# 比 node:alpine 更小
FROM gcr.io/distroless/nodejs18-debian11
```

### 3. 不存储敏感信息
```dockerfile
# 错误
ENV API_KEY=secret123

# 正确：运行时注入
docker run -e API_KEY=secret123 myapp
```

### 4. 限制资源
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
```

### 5. 定期更新镜像
```bash
docker pull node:20-alpine
docker-compose pull
docker-compose up -d
```

### 6. 扫描漏洞
```bash
# 安装 Trivy
trivy image myapp:latest

# CI 中扫描
trivy fs --severity HIGH .
```
```

## 實踐練習

```
1. 为你的应用创建 Dockerfile
2. 创建 docker-compose.yml
3. 配置开发环境
4. 配置生产环境
5. 设置健康检查
6. 配置监控
7. 运行安全扫描
```

**Docker 是現代部署的基礎。掌握它，讓你的應用可以在任何地方運行。**
