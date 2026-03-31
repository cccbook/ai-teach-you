# 第 20 章：部署與優化

## 概述

本章介紹如何將全端應用程式部署到生產環境，包括 Docker 容器化、Nginx 配置、CI/CD 流程和效能優化。

## 20.1 Dockerfile

將 FastAPI 後端容器化。

[程式檔案：20-1-dockerfile](../_code/20/20-1-dockerfile)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 20.2 Docker Compose

使用 Docker Compose 管理多容器應用。

[程式檔案：20-2-docker-compose.yml](../_code/20/20-2-docker-compose.yml)

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

## 20.3 Nginx 配置

配置 Nginx 作為反向代理和靜態檔案服務器。

[程式檔案：20-3-nginx-config](../_code/20/20-3-nginx-config)

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name example.com;

        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## 20.4 Supervisor 配置

使用 Supervisor 管理進程。

[程式檔案：20-4-supervisor-config](../_code/20/20-4-supervisor-config)

```ini
[program:uvicorn]
command=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/uvicorn.err.log
stdout_logfile=/var/log/uvicorn.out.log
```

## 20.5 CI/CD 流程

使用 GitHub Actions 自動化部署。

[程式檔案：20-5-github-actions.yml](../_code/20/20-5-github-actions.yml)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} ./backend
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_TOKEN }} | docker login -u ${{ secrets.DOCKER_USER }} --password-stdin
          docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            docker pull myapp:${{ github.sha }}
            docker-compose up -d
```

## 20.6 Gunicorn 配置

使用 Gunicorn 運行 Python WSGI 應用。

[程式檔案：20-6-gunicorn-config.py](../_code/20/20-6-gunicorn-config.py)

```python
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
timeout = 30
graceful_timeout = 30

max_requests = 1000
max_requests_jitter = 50

accesslog = "-"
errorlog = "-"
loglevel = "info"

preload_app = True
```

## 20.7 Uvicorn 設定

Uvicorn ASGI 伺服器配置。

[程式檔案：20-7-uvicorn-settings.py](../_code/20/20-7-uvicorn-settings.py)

```python
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "change-me-in-production"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Uvicorn settings
UVICORN_CONFIG = {
    "app": "main:app",
    "host": "0.0.0.0",
    "port": 8000,
    "reload": settings.debug,
    "workers": 4,
    "log_level": "info",
    "access_log": True,
}
```

## 20.8 Heroku 部署

部署到 Heroku 平台。

[程式檔案：20-8-heroku-deploy.sh](../_code/20/20-8-heroku-deploy.sh)

```bash
#!/bin/bash
set -e

echo "Deploying to Heroku..."

git add .
git commit -m "Deploy"
git push heroku main

heroku run python -m alembic upgrade head

heroku restart
```

## 20.9 AWS 部署

部署到 AWS 雲端平台。

[程式檔案：20-9-aws-deploy.sh](../_code/20/20-9-aws-deploy.sh)

```bash
#!/bin/bash
set -e

echo "Deploying to AWS..."

ECR_REPOSITORY="myapp"
ECR_IMAGE="${ECR_REGISTRY}/${ECR_REPOSITORY}:${GITHUB_SHA}"

aws ecr get-login-password --region $AWS_REGION | docker login -u AWS --password-stdin $ECR_REGISTRY

docker build -t $ECR_IMAGE ./backend
docker push $ECR_IMAGE

aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE --force-new-deployment

aws ecs wait services-stable --cluster $ECS_CLUSTER --services $ECS_SERVICE

echo "Deployment complete!"
```

## 20.10 效能優化技巧

[程式檔案：20-10-optimization-tips.md](../_code/20/20-10-optimization-tips.md)

```markdown
# Performance Optimization Tips

## Backend (FastAPI)

1. **Database Optimization**
   - Use indexes on frequently queried columns
   - Implement database connection pooling
   - Use async database drivers (asyncpg for PostgreSQL)
   - Implement query caching with Redis

2. **API Optimization**
   - Use response models to limit returned fields
   - Implement pagination for large datasets
   - Use background tasks for heavy operations
   - Enable compression (gzip)

3. **Caching Strategy**
   - Cache frequently accessed data
   - Use ETag for conditional requests
   - Implement cache invalidation

## Frontend (React)

1. **Bundle Optimization**
   - Code splitting with React.lazy
   - Tree shaking unused code
   - Minimize third-party dependencies
   - Use production builds

2. **Rendering Optimization**
   - Use React.memo for expensive components
   - Implement virtualization for long lists
   - Debounce/throttle frequent updates
   - Use useMemo and useCallback

3. **Network Optimization**
   - Compress API responses
   - Implement request caching
   - Use CDN for static assets
   - Preload critical resources

## General

1. **Monitoring**
   - Set up application monitoring
   - Track Core Web Vitals
   - Monitor error rates

2. **Security**
   - Use HTTPS
   - Implement rate limiting
   - Sanitize user input
   - Keep dependencies updated
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| Docker | 容器化技術 |
| Docker Compose | 多容器編排 |
| Nginx | 反向代理和負載均衡 |
| CI/CD | 自動化部署流程 |
| Gunicorn/Uvicorn | WSGI/ASGI 伺服器 |
| 效能優化 | 前後端優化策略 |

## 練習題

1. 使用 Docker 部署 FastAPI 應用
2. 配置 Nginx 反向代理
3. 設定 GitHub Actions CI/CD
4. 實作 API 回應快取
