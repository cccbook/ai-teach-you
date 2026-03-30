# 23. Containerization and Docker

## Why Containers

```
┌─────────────────────────────────────────────────────────┐
│                   Problems Containers Solve                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Development: "It works on my machine!"               │
│                    ↓                                    │
│   Containerization: "It works anywhere!"                │
│                                                         │
│   • Consistent dev, test, production environments       │
│   • Fast startup and destruction                       │
│   • Resource isolation                                 │
│   • Easy scaling                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Docker Core Concepts

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Core                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Image                                                 │
│   │ Read-only template, snapshot of filesystem          │
│                                                         │
│   Container                                             │
│   │ Running instance of image, writable layer           │
│                                                         │
│   Dockerfile                                            │
│   │ Instruction file for building images                │
│                                                         │
│   Registry                                              │
│   │ Service for storing and distributing images         │
│   │ (Docker Hub, ECR, GCR)                            │
│                                                         │
│   Docker Compose                                        │
│   │ Define multi-container applications                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Dockerfile

### Basic Dockerfile

```
You:
Please create a Dockerfile for a Node.js application.

AI:
## Dockerfile

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001

# Copy build artifacts
COPY --from=builder --chown=nodeuser:nodejs /app/dist ./dist
COPY --from=builder --chown=nodeuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodeuser:nodejs /app/package.json ./

# Switch user
USER nodeuser

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "dist/main.js"]
```

### Dockerfile Optimization

```
You:
How can this Dockerfile be optimized?

AI:
## Dockerfile Optimization

### 1. Use multi-stage build
Reduces final image size

### 2. Combine RUN instructions
Reduces image layers

### Before:
```dockerfile
RUN npm install
RUN npm audit fix
RUN npm run build
```

### After:
```dockerfile
RUN npm ci && \
    npm audit fix && \
    npm run build && \
    npm prune --production
```

### 3. Use .dockerignore
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

### 4. Leverage build cache
```dockerfile
# Copy dependencies first
COPY package*.json ./
RUN npm ci

# Then copy source code
COPY . .
RUN npm run build
```

### 5. Use smaller base images
```dockerfile
# Size comparison
node:20          # ~1.1GB
node:20-alpine   # ~180MB
```
```

## Docker Compose

### Basic Configuration

```
You:
Please help me create Docker Compose configuration with:
- Node.js app
- PostgreSQL database
- Redis cache

AI:
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

### Development vs Production Configuration

```
You:
Should development and production use different Docker configs?

AI:
## Development vs Production Configuration

### Development environment
```yaml
# docker-compose.yml
services:
  app:
    build: .
    volumes:
      - .:/app          # Hot reload
      - /app/node_modules
    command: npm run dev
```

### Production environment
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

### Using Different Configs
```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
```

## Common Application Scenarios

### 1. Frontend Application

```
You:
Please create a Dockerfile for a React application.

AI:
## React Dockerfile

```dockerfile
# Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Nginx server
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

### 2. Python Application

```
You:
Please create a Dockerfile for a FastAPI application.

AI:
## FastAPI Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Create user
RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Multi-Service Application

```
You:
Please create Docker configuration for microservices architecture.

AI:
## Microservices Docker Compose

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

## Docker Networking

```
You:
How do Docker containers communicate?

AI:
## Docker Networks

### 1. Default bridge network
Containers communicate via service names

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

### 2. Port exposure
```yaml
services:
  web:
    ports:
      - "3000:3000"      # host:container
      - "8080-8090:8080" # port range
```

### 3. External access
```yaml
services:
  web:
    expose:
      - "3000"    # Only internal
    ports:
      - "8080:3000"  # External access
```

### 4. DNS resolution
```bash
# Access other containers from inside container
ping db          # Service name
ping db:5432     # With port
```

## Docker Debugging

```
You:
Container failed to start, how to debug?

AI:
## Docker Debugging

### 1. View logs
```bash
docker logs <container_id>
docker logs -f <container_id>        # Follow
docker logs --tail 100 <container_id> # Last 100 lines
```

### 2. Enter container
```bash
docker exec -it <container_id> /bin/sh
docker exec -it <container_id> /bin/bash
```

### 3. Check container status
```bash
docker ps -a                          # All containers
docker inspect <container_id>        # Detailed info
docker stats <container_id>          # Resource usage
```

### 4. Check network
```bash
docker network ls
docker network inspect <network_name>
```

### 5. Common issues
```bash
# Port conflict
docker port <container_id>

# Permission issue
docker exec -u root <container_id> chown -R user:user /path

# File permission
docker exec <container_id> ls -la /path
```

### 6. Clean rebuild
```bash
docker-compose down
docker-compose up --build --force-recreate
```

## Docker Security

```
You:
What security considerations for Docker containers?

AI:
## Docker Security Best Practices

### 1. Don't run as root
```dockerfile
RUN adduser -m -u 1001 appuser
USER appuser
```

### 2. Use minimal base images
```dockerfile
# Smaller than node:alpine
FROM gcr.io/distroless/nodejs18-debian11
```

### 3. Don't store sensitive info
```dockerfile
# Wrong
ENV API_KEY=secret123

# Correct: inject at runtime
docker run -e API_KEY=secret123 myapp
```

### 4. Limit resources
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
```

### 5. Regularly update images
```bash
docker pull node:20-alpine
docker-compose pull
docker-compose up -d
```

### 6. Scan for vulnerabilities
```bash
# Install Trivy
trivy image myapp:latest

# Scan in CI
trivy fs --severity HIGH .
```

## Practice Exercises

```
1. Create Dockerfile for your application
2. Create docker-compose.yml
3. Configure development environment
4. Configure production environment
5. Set up health checks
6. Configure monitoring
7. Run security scan
```

**Docker is the foundation of modern deployment. Master it, and your applications can run anywhere.**
