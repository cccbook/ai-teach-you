# 25. Major Cloud Platforms Overview

## Cloud Platform Selection

```
┌─────────────────────────────────────────────────────────┐
│                   Major Cloud Platforms                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   AWS         Earliest, largest ecosystem              │
│   ├─ EC2, S3, Lambda, RDS, ECS, EKS                   │
│   └─ 90+ services                                       │
│                                                         │
│   Azure      Microsoft ecosystem, enterprise-friendly   │
│   ├─ Virtual Machines, Blob Storage, Functions         │
│   └─ Great Windows/AD integration                      │
│                                                         │
│   GCP         Google technology, strong ML             │
│   ├─ Compute Engine, Cloud Storage, Cloud Functions    │
│   └─ Native Kubernetes support                         │
│                                                         │
│   Alibaba Cloud Chinese market, localization           │
│   ├─ ECS, OSS, Function Compute, RDS                  │
│   └─ Excellent China compliance support               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Cloud Decision

```
You:
Our team has 5 people, developing a SaaS product,
needs: web app, database, file storage, CDN.
Limited budget, targeting Chinese market.
Please recommend a cloud platform.

AI:
## Cloud Platform Recommendation: Alibaba Cloud

### Reasons
1. **Target market**: Low latency for mainland China users
2. **Compliance**: ICP filing support
3. **Cost**: Affordable entry-level ECS
4. **Ecosystem**: One-stop services

### Recommended Configuration

| Service | Spec | Monthly Cost (approx) |
|---------|------|----------------------|
| ECS | 2 vCPU 4GB | ¥200 |
| RDS MySQL | 1 vCPU 1GB | ¥60 |
| OSS | Pay-as-you-go | ¥20 |
| CDN | Pay-as-you-go | ¥50 |
| SLB | Fixed bandwidth | ¥30 |
| **Total** | | **¥360/month** |

### Architecture
```
User ──→ CDN ──→ OSS (static assets)
                └─→ SLB ──→ ECS (application)
                              └─→ RDS (database)
```

### If Targeting Overseas Market
Recommendations:
- **AWS** - Most mature
- **Vercel/Netlify** - Frontend-specific, very affordable

### Architecture
```
User ──→ Vercel (frontend)
              ↓
          Lambda/API Gateway (backend)
              ↓
          RDS (database)
              ↓
          S3 (file storage)
```
```

## Core Services Comparison

### Compute Services

| Service | AWS | Azure | GCP | Alibaba Cloud |
|---------|-----|-------|-----|---------------|
| Virtual machine | EC2 | Virtual Machines | Compute Engine | ECS |
| Container | ECS/EKS | AKS | GKE | ACK |
| Serverless | Lambda | Functions | Cloud Functions | Function Compute |
| Kubernetes | EKS | AKS | GKE | ACK |

```
You:
What's the difference between Lambda and ECS?

AI:
## Lambda vs ECS

### Lambda (Serverless)
```
Pros:
✓ Auto-scaling
✓ Pay per invocation
✓ No server management
✓ Millisecond billing

Cons:
✗ Cold start latency
✗ Execution time limit (15 minutes)
✗ Not for long-running processes
✗ Complex debugging

Best for:
- Short tasks
- Web APIs
- Event-driven
- Backend-as-a-service
```

### ECS (Container Service)
```
Pros:
✓ Complete control
✓ No time limit
✓ Long-running processes
✓ Familiar Docker environment

Cons:
✗ Server management required
✗ Manual scaling configuration
✗ Learning curve

Best for:
- Long-running services
- Complex state management
- Persistent connections
- Microservices architecture
```

### Selection Guide
```
Large request variance → Lambda
Stable traffic → ECS/EC2
Stateful services → ECS
Stateless functions → Lambda
```

## Storage Services

### Object Storage

| Service | AWS | Azure | GCP | Alibaba Cloud |
|---------|-----|-------|-----|---------------|
| Object storage | S3 | Blob Storage | Cloud Storage | OSS |
| Block storage | EBS | Managed Disks | Persistent Disk | Cloud Disk |
| File storage | EFS | Files | Filestore | NAS |

```
You:
When to use object storage vs database?

AI:
## Selection Guide

### Object Storage (OSS/S3)
- Unstructured files: images, videos, documents
- No querying needed
- Pay-as-you-go storage

```javascript
// Upload file to S3
const { PutObjectCommand } = require('@aws-sdk/client-s3');

await s3.send(new PutObjectCommand({
  Bucket: 'my-bucket',
  Key: 'uploads/user-123/avatar.jpg',
  Body: fileBuffer,
  ContentType: 'image/jpeg'
}));
```

### Database
- Structured data
- Needs querying and indexing
- Needs transaction support

```javascript
// Save user info to database
await db.users.update({
  where: { id: userId },
  data: { avatarUrl: 'https://s3...' }
});
```

### Hybrid Use
```
User uploads image
    ↓
Save to object storage → Return URL
    ↓
Save URL to database
```

### When to Combine Both
- User avatars → OSS + database URL
- Post images → OSS + database URL
- Log files → OSS (import when querying)
- Backup data → OSS
```

## Database Services

```
You:
When to choose RDS vs DynamoDB?

AI:
## RDS vs DynamoDB

### RDS (Relational)
```
Use when:
✓ Need complex queries (JOIN, GROUP BY)
✓ Need transactions (ACID)
✓ Need SQL ecosystem
✓ Fixed data structure

Limitations:
✗ Scaling has limits
✗ Need to manage capacity

Typical use cases:
- Order systems
- User systems
- Blog systems
```

### DynamoDB (NoSQL)
```
Use when:
✓ Extreme scale (no limits)
✓ High read/write performance
✓ Simple query patterns
✓ Need pay-per-use

Limitations:
✗ Weak complex query capability
✗ No JOIN support
✗ Learning curve

Typical use cases:
- Real-time bidding
- Gaming player data
- IoT data
- High-traffic APIs
```

### Selection Decision Tree
```
Need complex queries?
├─ Yes → RDS
└─ No
  │
  Data volume > 10TB?
  ├─ Yes → DynamoDB/Cassandra
  └─ No
    │
    Need SQL syntax?
    ├─ Yes → RDS
    └─ No → DynamoDB
```

### Modern Choices
| Requirement | Recommendation |
|-------------|---------------|
| Web app data | PostgreSQL (RDS) |
| Caching | Redis |
| Search | Elasticsearch/OpenSearch |
| Time-series data | InfluxDB/TimescaleDB |
| Graph data | Neo4j/Neptune |
```

## Serverless vs Traditional

```
You:
What scenarios is Serverless suitable for?

AI:
## Serverless Scenarios

### Suitable scenarios ✅
```
1. Web backend APIs
   - API Gateway → Lambda → DynamoDB
   - Auto-scaling, pay per invocation

2. Event-driven
   - S3 upload → Lambda → Process
   - Scheduled tasks (CloudWatch Events)

3. Data processing
   - Image processing (thumbnails, watermarks)
   - Format conversion (PDF generation)

4. Background tasks
   - Send emails
   - Generate reports
   - Batch processing
```

### Not suitable scenarios ❌
```
1. Long-running tasks
   - ML training
   - Video transcoding

2. Persistent state needed
   - WebSocket long connections
   - Game servers

3. Complex dependencies
   - Many microservice dependencies
   - Complex transactions

4. Low latency requirements
   - Real-time trading
   - Game servers
```

### Cost Comparison
```
Lambda:
- First 4 million requests/month free
- $0.20 per million requests beyond
- $0.0000166667 per GB-second

EC2 (2 vCPU 4GB):
- ~$50/month (reserved)
- Unlimited runtime

Break-even point:
- 4 million requests/month → Lambda cheaper
- 50 million requests/month → Need detailed calculation
```

## Hybrid Cloud Strategy

```
You:
When do we need multi-cloud strategy?

AI:
## Multi-Cloud Strategy

### When needed
- **Compliance requirements**: Some data must stay in China
- **Avoid lock-in**: Don't depend on single vendor
- **Cost optimization**: Different vendors have different price advantages
- **High availability**: Cross-region disaster recovery

### Multi-cloud challenges
```
✗ Increased complexity
✗ High learning cost
✗ Data consistency is hard
✗ Network latency
✗ High operations cost
```

### Recommended hybrid scenarios

```
Scenario 1: China + Overseas
├─ China → Alibaba Cloud
└─ Overseas → AWS/GCP

Scenario 2: Primary + Backup
├─ Primary → AWS
└─ DR → Azure

Scenario 3: Choose by service
├─ ML → GCP
├─ Database → AWS RDS
└─ Frontend/CDN → Vercel
```

### Signals to avoid multi-cloud
```
⚠️ Team < 10 people
⚠️ Limited budget
⚠️ No special compliance requirements
⚠️ First time on cloud
```

### Recommendations
```
Most cases: Choose one cloud
Special cases: Primary cloud + simple backup
Only large enterprises: True multi-cloud
```

## AI-Assisted Migration

```
You:
How to migrate an application from on-premises to cloud?

AI:
## Cloud Migration Strategy

### Migration Steps

```
1. Assessment phase
   ├─ Inventory assets
   ├─ Dependency analysis
   └─ Cost estimation

2. Planning phase
   ├─ Choose migration strategy
   └─ Create timeline

3. Implementation phase
   ├─ Set up cloud environment
   ├─ Migrate data
   ├─ Migrate application
   └─ Test and verify

4. Optimization phase
   ├─ Performance optimization
   └─ Cost optimization
```

### Migration Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| Lift & Shift | Direct migration | Fast cloud adoption |
| Replatform | Adjust some configs | Optimize without rewriting |
| Refactor | Restructure for cloud-native | Long-term cost optimization |
| Re-architect | Complete rebuild | Disruptive innovation |

### Migration tools
```bash
# AWS
aws Server Migration Service
aws Database Migration Service

# Azure
Azure Migrate
Azure Site Recovery

# General
Terraform IaC
Docker containerization
```

## Practice Exercises

```
1. Understand your project's cloud needs
2. Compare 2-3 cloud platforms
3. Evaluate costs
4. Design basic architecture
5. Try free tiers
6. Create migration plan (if needed)
```

**Choosing a cloud platform is not a one-time decision. You can adjust strategy as requirements change.**
