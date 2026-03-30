# 22. Continuous Deployment and Delivery

## Two Meanings of CD

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Continuous Delivery                                  │
│   │                                                     │
│   └→ Code ready to deploy, but human confirms deploy    │
│                                                         │
│   Continuous Deployment                                │
│   │                                                     │
│   └→ Code automatically deployed to production         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Evolution of Deployment Process

```
Traditional                         Modern
──────────                          ────────
Dev → Test → Queue → Deploy        PR → CI → CD → Deploy
   │      │      │      │              │
   ▼      ▼      ▼      ▼              ▼
  Weeks   Days   Days   Hours        Minutes
```

## AI-Assisted CD Configuration

### Basic CD Configuration

```
You:
Please help me configure automatic deployment from GitHub to server.

AI:
## GitHub Actions CD Configuration

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:  # Allow manual trigger

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

### SSH Key Configuration

```
You:
How to configure SSH key for deployment?

AI:
## SSH Deploy Key Configuration

### 1. Generate deploy key
```bash
ssh-keygen -t ed25519 -C "deploy@yourapp.com"
# Save to ~/.ssh/deploy_key
```

### 2. Add public key to server
```bash
cat ~/.ssh/deploy_key.pub >> ~/.ssh/authorized_keys
```

### 3. Configure key in GitHub
1. Go to repo Settings → Secrets and variables → Actions
2. Add these secrets:
   - SERVER_HOST: Server IP
   - SERVER_USER: Username
   - SERVER_SSH_KEY: Private key content

### 4. Verify connection
```bash
ssh -i ~/.ssh/deploy_key user@server_host
```
```

## Deployment Strategies

### 1. Direct Deployment

```
┌─────────────────────────────────────────┐
│                                          │
│   Current version: v1.0.0               │
│                                          │
│   Deploy v1.1.0:                        │
│                                          │
│   v1.0.0 ──→ [Stop] ──→ [Delete]       │
│                    ↓                     │
│            v1.1.0 ──→ [Start]           │
│                                          │
└─────────────────────────────────────────┘

Pros: Simple
Cons: Downtime
```

### 2. Rolling Deployment

```
┌─────────────────────────────────────────┐
│                                          │
│   3 instances rolling update:            │
│                                          │
│   Instance 1: v1.0.0 ──→ v1.1.0        │
│   Instance 2: v1.0.0 ──→ [Updating]     │
│   Instance 3: v1.0.0 ──→ v1.1.0        │
│                                          │
│   Always 2 instances online             │
│                                          │
└─────────────────────────────────────────┘

Pros: Zero downtime
Cons: Longer deployment time
```

### 3. Blue-Green Deployment

```
┌─────────────────────────────────────────┐
│                                          │
│   Blue environment (production): v1.0.0 │
│   Green environment (new): v1.1.0       │
│                                          │
│   After verifying green is normal:      │
│   Switch traffic to green               │
│                                          │
│   Can rollback in seconds if issues     │
│                                          │
└─────────────────────────────────────────┘

Pros: Fast rollback
Cons: High resource cost
```

### 4. Canary Deployment

```
┌─────────────────────────────────────────┐
│                                          │
│   Traffic distribution:                 │
│                                          │
│   90% ──→ v1.0.0                        │
│   10% ──→ v1.1.0 (canary)              │
│                                          │
│   Observe canary performance:           │
│   - Error rate                           │
│   - Response time                        │
│   - User feedback                        │
│                                          │
│   Gradually increase traffic to 100%     │
│                                          │
└─────────────────────────────────────────┘

Pros: Controllable risk
Cons: Complex configuration
```

Have AI help you choose deployment strategy:

```
You:
Our team has 5 people, 1000 users, 100 daily active users,
limited budget. Please recommend deployment strategy.

AI:
## Deployment Strategy Recommendation

### Recommended: Rolling deployment + Blue-Green standby

Reasons:
1. Limited resources, no need for full dual environment
2. Small user base, downtime window impact is limited
3. Small team, needs simple and reliable solution

### Specific Approach

**Daily work: Rolling deployment**
- 3 instances rolling update
- Zero downtime

**Key releases: Blue-green standby**
- Use blue-green for major version updates
- Switch after verification

### Implementation Suggestions
```yaml
# Rolling deployment config (example)
deployment:
  strategy: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```
```

## Rollback Strategy

```
You:
How to rollback after failed deployment?

AI:
## Rollback Strategy

### 1. Using Git rollback
```bash
# View recent deployments
git log --oneline -10

# Rollback to previous version
git revert HEAD
git push

# Or force rollback (use with caution)
git revert -m 1 <commit>
```

### 2. Using container rollback
```bash
# Docker Compose
docker-compose down
docker-compose pull
docker-compose up -d

# Kubernetes
kubectl rollout undo deployment/app

# View rollback history
kubectl rollout history deployment/app
```

### 3. Using PM2
```bash
# View history
pm2 list
pm2 show <id>

# Rollback to previous version
pm2 revert <id>

# Or specify version
pm2 start ecosystem.config.js --only app@<version>
```

### 4. Database rollback
If migration is included:
```bash
# Alembic (Python)
alembic downgrade -1

# Knex (Node.js)
knex migrate:down

# Prisma
prisma migrate revert
```

### Rollback Checklist
□ Code rolled back
□ Database rolled back (if needed)
□ Dependencies updated
□ Health check passed
□ No monitoring anomalies
```

## Database Migration Strategy

```
You:
How to safely handle database migration in CD?

AI:
## Database Migration Best Practices

### 1. Migration principles
- Always backward compatible
- Split large migrations
- Deploy code first, then run migration
- Prepare rollback

### 2. CD configuration
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
          # Deploy code
      
      - name: Verify deployment
        run: |
          curl -f https://yourapp.com/health
```

### 3. Safe migration pattern

```javascript
// ❌ Dangerous: Drop column
await knex.schema.alterTable('users', table => {
  table.dropColumn('old_field');
});

// ✅ Safe: Add nullable column
await knex.schema.alterTable('users', table => {
  table.string('new_field').nullable();
});

// Deploy code...
// Wait for confirmation...

// ✅ Safe: Drop old column (next deployment)
await knex.schema.alterTable('users', table => {
  table.dropColumn('old_field');
});
```

### 4. Migration checks
```bash
# Pre-deployment check
npm run migrate:check

# Post-deployment verification
npm run migrate:status
```

## Environment Management

### Environment Configuration

```
You:
How to manage different environment configs in CD?

AI:
## Environment Configuration Management

### 1. Using GitHub Secrets
Settings → Secrets and variables → Actions

### 2. Environment variable configuration
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

### 3. Multi-environment configuration
```yaml
# Deploy to different environments based on branch
on:
  push:
    branches:
      - main        # → production
      - develop     # → staging
```

### 4. Config separation
```
├── .env.example      # Example config
├── .env.staging      # Staging config
└── .env.production   # Production config
  (Not committed to Git)
```

## Health Checks

```
You:
How to configure health checks after deployment?

AI:
## Health Check Configuration

### 1. Application endpoint
```javascript
// Express example
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});
```

### 2. Kubernetes health checks
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

### 3. CI health check
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

### 4. Deep health check
```javascript
app.get('/health', async (req, res) => {
  try {
    // Check database
    await db.query('SELECT 1');
    
    // Check cache
    await redis.ping();
    
    // Check external services
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

## Monitoring Deployments

```
You:
What metrics to monitor after deployment?

AI:
## Post-Deployment Monitoring Checklist

### 1. Basic metrics
- [ ] Error rate (5xx ratio)
- [ ] Response time (P50, P95, P99)
- [ ] Request volume (QPS)
- [ ] CPU/Memory usage

### 2. Application metrics
- [ ] Active connections
- [ ] Queue length
- [ ] Cache hit rate
- [ ] Database connections

### 3. Business metrics
- [ ] Conversion rate
- [ ] Order volume
- [ ] Login success rate
- [ ] API call success rate

### 4. Alert rules
```yaml
# Alert examples
alerts:
  - name: High Error Rate
    condition: error_rate > 0.01
    severity: critical
    
  - name: High Latency
    condition: p95_latency > 1000ms
    severity: warning
```

### 5. Monitoring tools
| Tool | Purpose |
|------|---------|
| Prometheus | Metric collection |
| Grafana | Visualization |
| PagerDuty | Alerting |
| Datadog | APM |
```

## CD Best Practices

```
□ Automate all steps
□ Zero downtime deployment
□ Fast rollback capability
□ Has health checks
□ Has monitoring alerts
□ Configuration as code
□ Environment isolation
□ Log every deployment
□ Regularly practice rollback
```

## Practice Exercises

```
1. Configure basic CD workflow
2. Set up automatic rollback
3. Configure health checks
4. Set up deployment monitoring
5. Practice a complete deployment
6. Practice a rollback
```

**Good CD lets you sleep peacefully at 3 AM because you know any issue can be quickly rolled back.**
