# 24. Infrastructure as Code

## IaC Concept

```
┌─────────────────────────────────────────────────────────┐
│              Infrastructure as Code (IaC)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Traditional:                                          │
│   Manual clicks in cloud console → Error-prone → Hard to replicate│
│                                                         │
│   IaC:                                                 │
│   Code defines infrastructure → Git management → Replicable, versionable│
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Common IaC Tools

| Tool | Characteristics | Best For |
|------|---------------|----------|
| Terraform | Multi-cloud, declarative | Cross-cloud architecture |
| Pulumi | Uses programming languages | Complex logic |
| AWS CDK | Uses programming languages | AWS-specific |
| Ansible | Procedural, SSH | Configuration management |
| CloudFormation | AWS native | AWS-specific |

## AI-Assisted Terraform

### Basic Configuration

```
You:
Please help me create Terraform configuration to deploy a simple web application.

AI:
## Terraform Configuration

```hcl
# main.tf

# Provider configuration
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
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

# Subnet
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

# Internet gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "myapp-igw"
  }
}

# Route table
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

# Security group
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

# IAM role
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

# ECS task definition
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

# ECS cluster
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

### Variable Configuration

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

### Output Configuration

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

## Pulumi vs Terraform

```
You:
Which is better, Pulumi or Terraform?

AI:
## Pulumi vs Terraform Comparison

### Terraform
```hcl
# Uses HCL language
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
// Uses TypeScript/Python/Go
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("mybucket", {
  bucket: "my-unique-bucket-name",
  tags: {
    Name: "MyBucket",
    Environment: "Production",
  },
});
```

### Comparison

| Feature | Terraform | Pulumi |
|---------|-----------|--------|
| Language | HCL (DSL) | TypeScript/Python/Go |
| Learning curve | Medium | Lower (if familiar with programming) |
| Loops/conditionals | Limited | Full programming capability |
| Testing | HCL testing framework | Standard testing frameworks |
| State management | Remote state | Remote state |
| Ecosystem | Mature | Growing |
| Multi-cloud support | Excellent | Excellent |

### Suggestions
- Simple infrastructure → Terraform
- Complex logic/dynamic resources → Pulumi
- Team familiar with TypeScript → Pulumi
```

## IaC Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    IaC Workflow                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Write code                                            │
│      ↓                                                  │
│   terraform plan / pulumi preview                        │
│      ↓                                                  │
│   Code review (PR)                                      │
│      ↓                                                  │
│   terraform apply / pulumi up                           │
│      ↓                                                  │
│   Infrastructure change                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Complete Workflow Example

```
# 1. Initialize
terraform init

# 2. Plan changes
terraform plan -out=plan.tfplan

# 3. Review plan
terraform show plan.tfplan

# 4. Apply changes
terraform apply plan.tfplan

# 5. Verify
aws ec2 describe-instances --filters "Name=vpc-id,Values=vpc-xxx"

# 6. Destroy (test environment)
terraform destroy
```

## Modularization

```
You:
How to organize large Terraform projects?

AI:
## Recommended Directory Structure

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
├── modules.tf  # Shared modules
└── backend.tf  # Backend configuration
```

### Using Modules
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

## State Management

```
You:
How to manage Terraform state files?

AI:
## Remote State

### Configure backend
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Why Important
1. Team collaboration - shared state
2. State locking - prevents concurrent modifications
3. State backup - S3 versioning
4. Sensitive data - encrypted storage

### State locking
```bash
# DynamoDB table for locking
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

## Security

```
You:
What are IaC security best practices?

AI:
## IaC Security

### 1. Don't store plaintext secrets
```hcl
# Wrong
variable "db_password" {
  default = "mysecretpassword"
}

# Correct: use secrets manager
data "aws_secretsmanager_secret" "db" {
  name = "prod/db-password"
}

data "aws_secretsmanager_secret_version" "db" {
  secret_id = data.aws_secretsmanager_secret.db.id
}
```

### 2. Principle of least privilege
```hcl
# IAM policy
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

### 3. Sensitive outputs
```hcl
output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}
```

### 4. Drift detection
```bash
# Periodically check infrastructure changes
terraform plan -detailed-exitcode

# Or use tools
terraformer import
```

### 5. Scanning tools
```bash
# tfsec
tfsec .

# checkov
checkov -d .
```

## Practice Exercises

```
1. Choose an IaC tool (Terraform/Pulumi)
2. Initialize your first project
3. Create basic network configuration
4. Deploy a simple service
5. Configure remote state
6. Organize code with modules
7. Set up CI/CD integration
```

**IaC makes your infrastructure versionable, reviewable, and reproducible. Good IaC practice is the foundation of DevOps.**
