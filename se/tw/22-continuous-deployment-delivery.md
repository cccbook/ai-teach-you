# 22. 持續部署與交付

## CD 的兩種含義

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Continuous Delivery（持續交付）                      │
│   │                                                     │
│   └→ 代码随时可部署，但需要人工确认部署                 │
│                                                         │
│   Continuous Deployment（持續部署）                     │
│   │                                                     │
│   └→ 代码自动部署到生产环境                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 部署流程的演進

```
傳統方式                           現代方式
─────────                          ─────────
開發 → 測試 → 排隊 → 部署          PR → CI → CD → 部署
   │      │      │      │              │
   ▼      ▼      ▼      ▼              ▼
 數週     天     天     小時           分鐘
```

## AI 輔助 CD 配置

### 基礎 CD 配置

```
你：
请帮我配置从 GitHub 到服务器的自动部署。

AI：
## GitHub Actions CD 配置

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:  # 允许手动触发

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /var/www/app
            git pull origin main
            npm ci --production
            npm run build
            pm2 restart app

      - name: Health check
        run: |
          sleep 10
          curl -f https://yourapp.com/health || exit 1
```

### SSH 密鑰配置

```
你：
如何配置 SSH 密钥用于部署？

AI：
## SSH 部署密钥配置

### 1. 生成部署密钥
```bash
ssh-keygen -t ed25519 -C "deploy@yourapp.com"
# 保存到 ~/.ssh/deploy_key
```

### 2. 将公钥添加到服务器
```bash
cat ~/.ssh/deploy_key.pub >> ~/.ssh/authorized_keys
```

### 3. 在 GitHub 配置密钥
1. 进入仓库 Settings → Secrets and variables → Actions
2. 添加以下 secrets：
   - SERVER_HOST: 服务器 IP
   - SERVER_USER: 用户名
   - SERVER_SSH_KEY: 私钥内容

### 4. 验证连接
```bash
ssh -i ~/.ssh/deploy_key user@server_host
```
```

## 部署策略

### 1. 直接部署

```
┌─────────────────────────────────────────┐
│                                          │
│   当前版本：v1.0.0                       │
│                                          │
│   部署 v1.1.0：                          │
│                                          │
│   v1.0.0 ──→ [停止] ──→ [删除]         │
│                    ↓                      │
│            v1.1.0 ──→ [启动]             │
│                                          │
└─────────────────────────────────────────┘

优点：简单
缺点：有停机时间
```

### 2. 滾動部署

```
┌─────────────────────────────────────────┐
│                                          │
│   3 个实例滚动更新：                     │
│                                          │
│   实例1: v1.0.0 ──→ v1.1.0               │
│   实例2: v1.0.0 ──→ [更新中]             │
│   实例3: v1.0.0 ──→ v1.1.0               │
│                                          │
│   始终有 2 个实例在线                    │
│                                          │
└─────────────────────────────────────────┘

优点：零停机
缺点：部署时间长
```

### 3. 藍綠部署

```
┌─────────────────────────────────────────┐
│                                          │
│   蓝环境 (生产): v1.0.0                 │
│   绿环境 (新): v1.1.0                   │
│                                          │
│   验证绿环境正常后：                     │
│   切换流量到绿环境                       │
│                                          │
│   出现问题可秒级回滚                     │
│                                          │
└─────────────────────────────────────────┘

优点：快速回滚
缺点：资源成本高
```

### 4. 金絲雀部署

```
┌─────────────────────────────────────────┐
│                                          │
│   流量分配：                             │
│                                          │
│   90% ──→ v1.0.0                         │
│   10% ──→ v1.1.0 (金丝雀)               │
│                                          │
│   观察金丝雀表现：                       │
│   - 错误率                               │
│   - 响应时间                             │
│   - 用户反馈                             │
│                                          │
│   逐步增加流量，直到 100%               │
│                                          │
└─────────────────────────────────────────┘

优点：风险可控
缺点：配置复杂
```

讓 AI 幫你選擇部署策略：

```
你：
我们团队 5 人，用户量 1000，日活 100，
预算有限。请推荐部署策略。

AI：
## 部署策略推荐

### 推荐：滚动部署 + 蓝绿备用

原因：
1. 资源有限，不需要完整的双套环境
2. 用户量不大，停机窗口影响有限
3. 小团队，需要简单可靠的方案

### 具体做法

**日常工作：滚动部署**
- 3 个实例滚动更新
- 零停机

**关键发布：蓝绿备用**
- 大版本更新使用蓝绿
- 验证通过后切换

### 实施建议
```yaml
# 滚动部署配置（示例）
deployment:
  strategy: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```
```

## 回滾策略

```
你：
部署失败后如何回滚？

AI：
## 回滚策略

### 1. 使用 Git 回滚
```bash
# 查看最近部署
git log --oneline -10

# 回滚到上一个版本
git revert HEAD
git push

# 或者强制回滚（慎用）
git revert -m 1 <commit>
```

### 2. 使用容器回滚
```bash
# Docker Compose
docker-compose down
docker-compose pull
docker-compose up -d

# Kubernetes
kubectl rollout undo deployment/app

# 查看回滚历史
kubectl rollout history deployment/app
```

### 3. 使用 PM2
```bash
# 查看历史
pm2 list
pm2 show <id>

# 回滚到上一个版本
pm2 revert <id>

# 或者指定版本
pm2 start ecosystem.config.js --only app@<version>
```

### 4. 使用数据库回滚
如果包含数据库迁移：
```bash
# Alembic (Python)
alembic downgrade -1

# Knex (Node.js)
knex migrate:down

# Prisma
prisma migrate revert
```

### 回滚检查清单
□ 代码已回滚
□ 数据库已回滚（如需要）
□ 依赖已更新
□ 健康检查通过
□ 监控无异常
```

## 資料庫遷移策略

```
你：
如何在 CD 中安全地处理数据库迁移？

AI：
## 数据库迁移最佳实践

### 1. 迁移原则
- 始终向后兼容
- 大迁移分步执行
- 先部署代码，再执行迁移
- 准备好回滚

### 2. CD 配置
```yaml
jobs:
  deploy:
    steps:
      - name: Run migrations
        run: |
          npm run migrate:up
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      
      - name: Deploy application
        run: |
          # 部署代码
      
      - name: Verify deployment
        run: |
          curl -f https://yourapp.com/health
```

### 3. 安全迁移模式

```javascript
// ❌ 危险：删除列
await knex.schema.alterTable('users', table => {
  table.dropColumn('old_field');
});

// ✅ 安全：添加 nullable 列
await knex.schema.alterTable('users', table => {
  table.string('new_field').nullable();
});

// 代码部署...
// 等待确认...

// ✅ 安全：删除旧列（下次部署）
await knex.schema.alterTable('users', table => {
  table.dropColumn('old_field');
});
```

### 4. 迁移检查
```bash
# 部署前检查
npm run migrate:check

# 部署后验证
npm run migrate:status
```

## 環境管理

### 環境配置

```
你：
如何在 CD 中管理不同环境的配置？

AI：
## 环境配置管理

### 1. 使用 GitHub Secrets
Settings → Secrets and variables → Actions

### 2. 环境变量配置
```yaml
jobs:
  deploy:
    environment: staging
    
    env:
      NODE_ENV: staging
      API_URL: https://api.staging.example.com
    
    steps:
      - name: Deploy
        run: |
          npm run deploy:staging
```

### 3. 多环境配置
```yaml
# 根据分支部署到不同环境
on:
  push:
    branches:
      - main        # → production
      - develop     # → staging
```

### 4. 配置分离
```
├── .env.example      # 示例配置
├── .env.staging      # 预发布配置
└── .env.production   # 生产配置
  (不提交到 Git)
```

## 健康檢查

```
你：
部署后如何配置健康检查？

AI：
## 健康检查配置

### 1. 应用端点
```javascript
// Express 示例
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});
```

### 2. Kubernetes 健康检查
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 5

readinessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 3
```

### 3. CI 健康检查
```yaml
- name: Health check
  run: |
    for i in {1..5}; do
      if curl -f https://yourapp.com/health; then
        exit 0
      fi
      sleep 10
    done
    exit 1
```

### 4. 深度健康检查
```javascript
app.get('/health', async (req, res) => {
  try {
    // 检查数据库
    await db.query('SELECT 1');
    
    // 检查缓存
    await redis.ping();
    
    // 检查外部服务
    await externalService.ping();
    
    res.json({ status: 'healthy' });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message
    });
  }
});
```
```

## 監控部署

```
你：
部署后需要监控哪些指标？

AI：
## 部署后监控清单

### 1. 基础指标
- [ ] 错误率 (5xx 比例)
- [ ] 响应时间 (P50, P95, P99)
- [ ] 请求量 (QPS)
- [ ] CPU/内存使用率

### 2. 应用指标
- [ ] 活跃连接数
- [ ] 队列长度
- [ ] 缓存命中率
- [ ] 数据库连接数

### 3. 业务指标
- [ ] 转化率
- [ ] 订单量
- [ ] 登录成功率
- [ ] API 调用成功率

### 4. 告警规则
```yaml
# 告警示例
alerts:
  - name: High Error Rate
    condition: error_rate > 0.01
    severity: critical
    
  - name: High Latency
    condition: p95_latency > 1000ms
    severity: warning
```

### 5. 监控工具
| 工具 | 用途 |
|------|------|
| Prometheus | 指标收集 |
| Grafana | 可视化 |
| PagerDuty | 告警 |
| Datadog | APM |
```

## CD 最佳實踐

```
□ 自动化所有步骤
□ 零停机部署
□ 可快速回滚
□ 有健康检查
□ 有监控告警
□ 配置即代码
□ 环境隔离
□ 记录每次部署
□ 定期演练回滚
```

## 實踐練習

```
1. 配置基础的 CD 流程
2. 设置自动回滚
3. 配置健康检查
4. 设置部署监控
5. 演练一次完整部署
6. 演练一次回滚
```

**好的 CD 讓你能在凌晨三點安心睡覺，因為你知道任何問題都可以快速回滾。**
