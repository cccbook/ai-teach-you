# 24. 基礎設施即程式碼

## IaC 的概念

```
┌─────────────────────────────────────────────────────────┐
│              Infrastructure as Code (IaC)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   传统方式：                                            │
│   手动点击云控制台 → 容易出错 → 难以重现               │
│                                                         │
│   IaC 方式：                                           │
│   代码定义基础设施 → Git 管理 → 可重现、可版本化        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 常見 IaC 工具

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| Terraform | 多云支持，声明式 | 跨云架构 |
| Pulumi | 用编程语言 | 复杂逻辑 |
| AWS CDK | 用编程语言 | AWS 专用 |
| Ansible | 过程式，SSH | 配置管理 |
| CloudFormation | AWS 原生 | AWS 专用 |

## AI 輔助 Terraform

### 基礎配置

```
你：
请帮我创建 Terraform 配置，部署一个简单的 Web 应用。

AI：
## Terraform 配置

```hcl
# main.tf

# Provider 配置
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "myapp-vpc"
  }
}

# 子网
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "myapp-subnet-${count.index + 1}"
  }
}

# 互联网网关
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "myapp-igw"
  }
}

# 路由表
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "myapp-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.main.id
}

# 安全组
resource "aws_security_group" "web" {
  name        = "myapp-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "myapp-sg"
  }
}

# IAM 角色
resource "aws_iam_role" "app_role" {
  name = "myapp-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

# ECS 任务定义
resource "aws_ecs_task_definition" "app" {
  family                   = "myapp-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.app_role.arn

  container_definitions = jsonencode([{
    name      = "myapp"
    image     = "nginx:alpine"
    essential = true
    portMappings = [{
      containerPort = 80
      protocol      = "tcp"
    }]
  }])
}

# ALB
resource "aws_lb" "main" {
  name               = "myapp-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = aws_subnet.public[*].id

  tags = {
    Name = "myapp-alb"
  }
}

resource "aws_lb_target_group" "app" {
  name     = "myapp-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled  = true
    path     = "/"
    protocol = "HTTP"
  }
}

resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.main.arn
  port             = "80"
  protocol         = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# ECS 服务
resource "aws_ecs_cluster" "main" {
  name = "myapp-cluster"
}

resource "aws_ecs_service" "app" {
  name            = "myapp-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.web.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "myapp"
    container_port   = 80
  }

  depends_on = [aws_lb.main]
}
```

### 變量配置

```
# variables.tf

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "desired_count" {
  description = "Number of ECS tasks"
  type        = number
  default     = 2
}
```

### 输出配置

```
# outputs.tf

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = aws_lb.main.dns_name
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}
```
```

## Pulumi vs Terraform

```
你：
Pulumi 和 Terraform 哪个更好？

AI：
## Pulumi vs Terraform 对比

### Terraform
```hcl
# 用 HCL 语言
resource "aws_s3_bucket" "mybucket" {
  bucket = "my-unique-bucket-name"
  
  tags = {
    Name        = "MyBucket"
    Environment = "Production"
  }
}
```

### Pulumi
```typescript
// 用 TypeScript/Python/Go
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("mybucket", {
  bucket: "my-unique-bucket-name",
  tags: {
    Name: "MyBucket",
    Environment: "Production",
  },
});
```

### 对比

| 特性 | Terraform | Pulumi |
|------|-----------|--------|
| 语言 | HCL (DSL) | TypeScript/Python/Go |
| 学习曲线 | 中等 | 较低（如果熟悉编程语言） |
| 循环/条件 | 有限 | 完整编程能力 |
| 测试 | HCL 测试框架 | 标准测试框架 |
| 状态管理 | 远程状态 | 远程状态 |
| 生态 | 成熟 | 成长中 |
| 多云支持 | 优秀 | 优秀 |

### 建议
- 简单基础设施 → Terraform
- 复杂逻辑/动态资源 → Pulumi
- 团队熟悉 TypeScript → Pulumi
```

## IaC 工作流

```
┌─────────────────────────────────────────────────────────┐
│                    IaC 工作流                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   编写代码                                              │
│      ↓                                                  │
│   terraform plan / pulumi preview                        │
│      ↓                                                  │
│   代码审查 (PR)                                          │
│      ↓                                                  │
│   terraform apply / pulumi up                           │
│      ↓                                                  │
│   基础设施变更                                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 完整工作流示例

```
# 1. 初始化
terraform init

# 2. 规划变更
terraform plan -out=plan.tfplan

# 3. 审查计划
terraform show plan.tfplan

# 4. 应用变更
terraform apply plan.tfplan

# 5. 验证
aws ec2 describe-instances --filters "Name=vpc-id,Values=vpc-xxx"

# 6. 销毁（测试环境）
terraform destroy
```

## 模組化

```
你：
如何组织大型 Terraform 项目？

AI：
## 推荐的目录结构

```
├── environments/
│   ├── production/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   │
│   └── staging/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   ├── ecs/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   └── rds/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── modules.tf  # 共享模块
└── backend.tf  # 后端配置
```

### 使用模块
```hcl
# environments/production/main.tf

module "vpc" {
  source = "../../modules/vpc"
  
  environment = "production"
  cidr_block  = "10.1.0.0/16"
}

module "ecs" {
  source = "../../modules/ecs"
  
  environment = "production"
  vpc_id      = module.vpc.vpc_id
  subnets     = module.vpc.private_subnets
}
```
```

## 狀態管理

```
你：
Terraform 状态文件如何管理？

AI：
## 远程状态

### 配置后端
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "ap-northeast-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### 为什么重要
1. 团队协作 - 共享状态
2. 状态锁定 - 防止并发修改
3. 状态备份 - S3 版本控制
4. 敏感信息 - 加密存储

### 状态锁定
```bash
# DynamoDB 表用于锁定
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```
```

## 安全性

```
你：
IaC 有哪些安全最佳实践？

AI：
## IaC 安全

### 1. 不存储明文密钥
```hcl
# 错误
variable "db_password" {
  default = "mysecretpassword"
}

# 正确：使用 secrets manager
data "aws_secretsmanager_secret" "db" {
  name = "prod/db-password"
}

data "aws_secretsmanager_secret_version" "db" {
  secret_id = data.aws_secretsmanager_secret.db.id
}
```

### 2. 最小权限原则
```hcl
# IAM 策略
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "s3:GetObject",
      "s3:PutObject"
    ],
    "Resource": "arn:aws:s3:::mybucket/*"
  }]
}
```

### 3. 敏感输出
```hcl
output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}
```

### 4. drift 检测
```bash
# 定期检查基础设施变更
terraform plan -detailed-exitcode

# 或使用工具
terraformer import
```

### 5. 扫描工具
```bash
# tfsec
tfsec .

# checkov
checkov -d .
```
```

## 實踐練習

```
1. 选择 IaC 工具（Terraform/Pulumi）
2. 初始化第一个项目
3. 创建基础网络配置
4. 部署一个简单服务
5. 配置远程状态
6. 使用模块组织代码
7. 设置 CI/CD 集成
```

**IaC 讓你的基礎設施可以版本化、審查、重現。好的 IaC 實踐是 DevOps 的基石。**
