# 25. 主流雲端平台概覽

## 雲端平台選擇

```
┌─────────────────────────────────────────────────────────┐
│                   主要雲端平台                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   AWS         最早，最大生态                            │
│   ├─ EC2, S3, Lambda, RDS, ECS, EKS                   │
│   └─ 90+ 种服务                                        │
│                                                         │
│   Azure      微软生态，企业友好                         │
│   ├─ Virtual Machines, Blob Storage, Functions         │
│   └─ 优秀的 Windows/AD 集成                            │
│                                                         │
│   GCP         Google 技术，机器学习强                   │
│   ├─ Compute Engine, Cloud Storage, Cloud Functions    │
│   └─ Kubernetes 原生支持                               │
│                                                         │
│   阿里云     中国市场，本地化                           │
│   ├─ ECS, OSS, 函数计算, RDS                          │
│   └─ 优秀的中国合规支持                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助雲端決策

```
你：
我们团队 5 人，开发一个 SaaS 产品，
需要：Web 应用、数据库、文件存储、CDN。
预算有限，目标中国市场。
请推荐云平台。

AI：
## 云平台推荐：阿里云

### 理由
1. **目标市场**：中国大陆用户访问延迟低
2. **合规**：ICP 备案支持
3. **成本**：入门级 ECS 便宜
4. **生态**：一站式服务

### 推荐配置

| 服务 | 规格 | 月费用（约） |
|------|------|-------------|
| ECS | 2核4G | ¥200 |
| RDS MySQL | 1核1G | ¥60 |
| OSS | 按量 | ¥20 |
| CDN | 按量 | ¥50 |
| SLB | 固定带宽 | ¥30 |
| **总计** | | **¥360/月** |

### 架构图
```
用户 ──→ CDN ──→ OSS (静态资源)
                └─→ SLB ──→ ECS (应用)
                              └─→ RDS (数据库)
```

### 如果目标是海外市场
推荐：
- **AWS** - 最成熟
- **Vercel/Netlify** - 前端专用，极便宜

### 架构
```
用户 ──→ Vercel (前端)
             ↓
         Lambda/API Gateway (后端)
             ↓
         RDS (数据库)
             ↓
         S3 (文件存储)
```
```

## 核心服務對比

### 計算服務

| 服务 | AWS | Azure | GCP | 阿里云 |
|------|-----|-------|-----|--------|
| 虚拟机 | EC2 | Virtual Machines | Compute Engine | ECS |
| 容器 | ECS/EKS | AKS | GKE | ACK |
| 无服务器 | Lambda | Functions | Cloud Functions | 函数计算 |
| Kubernetes | EKS | AKS | GKE | ACK |

```
你：
Lambda 和 ECS 有什么区别？

AI：
## Lambda vs ECS

### Lambda (无服务器)
```
优点：
✓ 自动扩展
✓ 按调用计费
✓ 无需管理服务器
✓ 毫秒级计费

缺点：
✗ 冷启动延迟
✗ 有执行时间限制（15分钟）
✗ 不适合长时间运行
✗ 调试复杂

适合场景：
- 短时任务
- Web API
- 事件驱动
- 后端即服务
```

### ECS (容器服务)
```
优点：
✓ 完全控制
✓ 无时间限制
✓ 可长时间运行
✓ 熟悉的 Docker 环境

缺点：
✗ 需要管理服务器
✗ 需要配置扩展
✗ 学习曲线

适合场景：
- 长期运行的服务
- 复杂的状态管理
- 需要持久连接
- 微服务架构
```

### 选择建议
```
请求量波动大 → Lambda
稳定流量 → ECS/EC2
有状态服务 → ECS
无状态函数 → Lambda
```

## 儲存服務

### 對象儲存

| 服务 | AWS | Azure | GCP | 阿里云 |
|------|-----|-------|-----|--------|
| 对象存储 | S3 | Blob Storage | Cloud Storage | OSS |
| 块存储 | EBS | Managed Disks | Persistent Disk | 云盘 |
| 文件存储 | EFS | Files | Filestore | NAS |

```
你：
什么时候用对象存储 vs 数据库？

AI：
## 选择指南

### 对象存储（OSS/S3）
- 非结构化文件：图片、视频、文档
- 不需要查询
- 按需存储

```javascript
// 上传文件到 S3
const { PutObjectCommand } = require('@aws-sdk/client-s3');

await s3.send(new PutObjectCommand({
  Bucket: 'my-bucket',
  Key: 'uploads/user-123/avatar.jpg',
  Body: fileBuffer,
  ContentType: 'image/jpeg'
}));
```

### 数据库
- 结构化数据
- 需要查询和索引
- 需要事务支持

```javascript
// 保存用户信息到数据库
await db.users.update({
  where: { id: userId },
  data: { avatarUrl: 'https://s3...' }
});
```

### 混合使用
```
用户上传图片
    ↓
保存到对象存储 → 返回 URL
    ↓
数据库保存 URL
```

### 什么时候两者结合
- 用户头像 → OSS + 数据库 URL
- 帖子图片 → OSS + 数据库 URL
- 日志文件 → OSS（查询时导入）
- 备份数据 → OSS
```

## 資料庫服務

```
你：
什么情况选择 RDS vs DynamoDB？

AI：
## RDS vs DynamoDB

### RDS (关系型)
```
场景：
✓ 需要复杂查询（JOIN、GROUP BY）
✓ 需要事务（ACID）
✓ 需要 SQL 生态
✓ 固定数据结构

限制：
✗ 扩展有上限
✗ 需要管理容量

典型用例：
- 订单系统
- 用户系统
- 博客系统
```

### DynamoDB (NoSQL)
```
场景：
✓ 超大规模（无上限）
✓ 高读写性能
✓ 简单查询模式
✓ 需要按量付费

限制：
✗ 复杂查询能力弱
✗ 不支持 JOIN
✗ 学习曲线

典型用例：
- 实时竞价
- 游戏玩家数据
- IoT 数据
- 高流量 API
```

### 选择决策树
```
需要复杂查询吗？
├─ 是 → RDS
└─ 否
  │
  数据量超过 10TB？
  ├─ 是 → DynamoDB/Cassandra
  └─ 否
    │
    需要 SQL 语法？
    ├─ 是 → RDS
    └─ 否 → DynamoDB
```

### 现代选择
| 需求 | 推荐 |
|------|------|
| Web 应用数据 | PostgreSQL (RDS) |
| 缓存 | Redis |
| 搜索 | Elasticsearch/OpenSearch |
| 时序数据 | InfluxDB/TimescaleDB |
| 图数据 | Neo4j/Neptune |
```

## 無伺服器 vs 傳統

```
你：
Serverless 适合什么场景？

AI：
## Serverless 场景

### 适合的场景 ✅
```
1. Web 后端 API
   - API Gateway → Lambda → DynamoDB
   - 自动扩展，按调用付费

2. 事件驱动
   - S3 上传 → Lambda → 处理
   - 定时任务（CloudWatch Events）

3. 数据处理
   - 图片处理（缩略图、水印）
   - 格式转换（PDF 生成）

4. 后台任务
   - 发送邮件
   - 生成报告
   - 批量处理
```

### 不适合的场景 ❌
```
1. 长时间运行任务
   - 机器学习训练
   - 视频转码

2. 需要持久状态
   - WebSocket 长连接
   - 游戏服务器

3. 复杂依赖
   - 大量微服务依赖
   - 复杂事务

4. 低延迟要求
   - 实时交易
   - 游戏服务器
```

### 成本对比
```
Lambda：
- 前 400 万请求/月免费
- 超出 $0.20/百万请求
- 计算 $0.0000166667/GB-秒

EC2 (2核4G)：
- 约 $50/月（预留）
- 无限运行时间

临界点：
- 400万请求/月 → Lambda 更便宜
- 5000万请求/月 → 需要详细计算
```

## 混合雲策略

```
你：
什么时候需要多云策略？

AI：
## 多云策略

### 什么时候需要
- **合规要求**：某些数据必须在中国
- **避免锁定**：不被单一厂商绑定
- **成本优化**：不同厂商价格优势不同
- **高可用**：跨区域容灾

### 多云挑战
```
✗ 复杂度增加
✗ 学习成本高
✗ 数据一致性难
✗ 网络延迟
✗ 运维成本
```

### 推荐的混合场景

```
场景 1：国内 + 海外
├─ 中国 → 阿里云
└─ 海外 → AWS/GCP

场景 2：主云 + 备份
├─ 主 → AWS
└─ 灾备 → Azure

场景 3：按服务选云
├─ 机器学习 → GCP
├─ 数据库 → AWS RDS
└─ 前端/CDN → Vercel
```

### 避免多云的信号
```
⚠️ 团队 < 10 人
⚠️ 预算有限
⚠️ 没有特殊合规要求
⚠️ 第一次上云
```

### 建议
```
大多数情况：选择一个云
特殊情况：选择主云 + 简单备份
只有大企业：真正的多云
```
```

## AI 輔助遷移

```
你：
如何将应用从本地迁移到云端？

AI：
## 云迁移策略

### 迁移步骤

```
1. 评估阶段
   ├─ 盘点资产
   ├─ 依赖分析
   └─ 成本估算

2. 规划阶段
   ├─ 选择迁移策略
   └─ 制定时间表

3. 实施阶段
   ├─ 搭建云环境
   ├─ 迁移数据
   ├─ 迁移应用
   └─ 测试验证

4. 优化阶段
   ├─ 性能优化
   └─ 成本优化
```

### 迁移策略

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| Lift & Shift | 直接迁移 | 快速上云 |
| Replatform | 调整部分配置 | 优化但不重写 |
| Refactor | 重构为云原生 | 长期成本优化 |
| Re-architect | 完全重建 | 颠覆性创新 |

### 迁移工具
```bash
# AWS
aws Server Migration Service
aws Database Migration Service

# Azure
Azure Migrate
Azure Site Recovery

# 通用
Terraform IaC
Docker 容器化
```
```

## 實踐練習

```
1. 了解你项目的云需求
2. 比较 2-3 个云平台
3. 评估成本
4. 设计基础架构
5. 尝试免费套餐
6. 制定迁移计划（如果需要）
```

**選擇雲平台不是一次性的決定。隨著需求變化，可以調整策略。**
