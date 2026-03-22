# 29. 關聯式資料庫設計

## 資料庫設計的藝術

```
┌─────────────────────────────────────────────────────────┐
│                 数据库设计原则                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   好设计：                                              │
│   ├─ 数据一致性                                         │
│   ├─ 查询效率高                                         │
│   ├─ 易于扩展                                           │
│   └─ 减少冗余                                           │
│                                                         │
│   坏设计：                                              │
│   ├─ 数据更新异常                                       │
│   ├─ 插入/删除异常                                      │
│   └─ 存储空间浪费                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 正規化

### 標準化級別

```
你：
数据库范式是什么？为什么要规范化？

AI：
## 数据库规范化

### 第一范式 (1NF)
```
要求：每个列都是原子的，不可再分

❌ 违反 1NF：
user_address: "北京市朝阳区建国路88号, 100022"

✅ 符合 1NF：
city: "北京"
district: "朝阳区"
street: "建国路88号"
zip_code: "100022"
```

### 第二范式 (2NF)
```
要求：满足 1NF + 非主键列完全依赖主键

❌ 违反 2NF（订单表）：
order_id | product_id | product_name | quantity
   1     |     1       | 手机         |    2
   1     |     2       | 耳机         |    1

product_name 只依赖 product_id，不完全依赖主键

✅ 符合 2NF：
订单表：order_id | product_id | quantity
商品表：product_id | product_name
```

### 第三范式 (3NF)
```
要求：满足 2NF + 非主键列之间没有传递依赖

❌ 违反 3NF（学生表）：
student_id | name | department | department_phone
    1      | 张三 | 计算机系   | 010-123456

department_phone 依赖 department，department 依赖 student_id

✅ 符合 3NF：
学生表：student_id | name | department_id
院系表：department_id | department_name | phone
```

### 规范化 vs 反规范化
```
规范化：
✓ 数据一致性
✓ 存储空间小
✓ 更新容易

反规范化：
✓ 查询快
✓ 减少 JOIN
✓ 实现简单

实际选择：根据业务场景权衡
```
```

## AI 輔助 ER 設計

### 從需求生成 ER 圖

```
你：
请为电商系统设计数据库 schema，包含：
- 用户（登录、注册）
- 商品（名称、价格、库存）
- 订单（下单、状态）
- 购物车

AI：
## 电商数据库设计

### ER 图
```
┌─────────────┐         ┌─────────────┐
│    users    │         │  addresses  │
├─────────────┤         ├─────────────┤
│ id (PK)     │───┐     │ id (PK)     │
│ email       │   │     │ user_id (FK)│
│ password    │   └───→ │ street      │
│ name        │         │ city        │
│ created_at  │         └─────────────┘
└─────────────┘               │
       │                      │
       │         ┌─────────────┴─────────────┐
       │         │                           │
       ↓         ↓                           ↓
┌─────────────┐  ┌─────────────┐     ┌─────────────┐
│ categories  │  │   orders    │     │   carts     │
├─────────────┤  ├─────────────┤     ├─────────────┤
│ id (PK)     │  │ id (PK)     │     │ id (PK)     │
│ name        │  │ user_id (FK)│     │ user_id (FK)│
│ parent_id   │  │ status      │     └─────────────┘
└─────────────┘  │ total_amount│           │
       │         │ created_at  │           ↓
       │         └─────────────┘     ┌─────────────┐
       │                │           │ cart_items  │
       ↓                │           ├─────────────┤
┌─────────────┐         │           │ id (PK)     │
│  products   │         │           │ cart_id (FK)│
├─────────────┤         │           │ product_id  │
│ id (PK)     │         │           │ quantity    │
│ name        │         │           └─────────────┘
│ price       │         │
│ stock       │         └───────┬─────────┐
│ category_id │                 │         │
│ created_at  │                 ↓         ↓
└─────────────┘         ┌─────────────┐ ┌─────────────┐
       │                 │ order_items│ │  payments   │
       │                 ├─────────────┤ ├─────────────┤
       └────────────────→│ id (PK)     │ │ id (PK)     │
                        │ order_id(FK)│ │ order_id(FK)│
                        │ product_id  │ │ amount      │
                        │ quantity    │ │ status      │
                        │ price       │ │ paid_at     │
                        └─────────────┘ └─────────────┘
```

### 建表 SQL
```sql
-- 用户表
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 地址表
CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  street VARCHAR(255),
  city VARCHAR(100),
  postal_code VARCHAR(20),
  is_default BOOLEAN DEFAULT FALSE
);

-- 分类表
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  parent_id INTEGER REFERENCES categories(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 商品表
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  stock INTEGER DEFAULT 0,
  category_id INTEGER REFERENCES categories(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CONSTRAINT positive_price CHECK (price > 0),
  CONSTRAINT positive_stock CHECK (stock >= 0)
);

-- 订单表
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  status VARCHAR(50) DEFAULT 'pending',
  total_amount DECIMAL(10, 2) NOT NULL,
  shipping_address_id INTEGER REFERENCES addresses(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 订单项表
CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(id),
  product_id INTEGER NOT NULL REFERENCES products(id),
  quantity INTEGER NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  
  CONSTRAINT positive_quantity CHECK (quantity > 0)
);

-- 支付表
CREATE TABLE payments (
  id SERIAL PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(id),
  amount DECIMAL(10, 2) NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  paid_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_addresses_user_id ON addresses(user_id);
```
```

## 索引設計

```
你：
如何设计索引？

AI：
## 索引设计

### 什么时候建索引
```
✅ 需要建索引：
├─ 主键（自动创建）
├─ 频繁查询的 WHERE 条件
├─ JOIN 的连接条件
├─ ORDER BY / GROUP BY 字段
└─ 唯一性约束

❌ 不需要建索引：
├─ 区分度低的字段（性别、状态）
├─ 很少查询的字段
├─ 频繁更新的字段
└─ 大文本字段
```

### 索引类型

| 类型 | 适用场景 | 示例 |
|------|----------|------|
| B-Tree | 默认，范围查询 | `>, <, BETWEEN` |
| Hash | 等值查询 | `=, IN` |
| GIN | 全文搜索, JSON | `tsvector` |
| GiST | 地理数据 | `PostGIS` |
| 复合索引 | 多字段查询 | `(a, b, c)` |

### 复合索引顺序
```sql
-- 复合索引 (status, user_id, created_at)

-- ✅ 有效使用索引
WHERE status = 'pending'
WHERE status = 'pending' AND user_id = 1
WHERE status = 'pending' AND user_id = 1 AND created_at > '2024-01-01'

-- ❌ 无法使用索引
WHERE user_id = 1                    -- 跳过第一列
WHERE created_at > '2024-01-01'    -- 跳过前两列
```

### 索引维护
```sql
-- 查看索引使用情况
SELECT 
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- 查找未使用的索引
SELECT 
  indexrelname,
  idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey';

-- 删除未使用索引
DROP INDEX IF EXISTS unused_index;
```
```

## 約束與觸發器

```
你：
数据库约束有哪些？

AI：
## 常用约束

### 主键约束
```sql
-- 单字段主键
CREATE TABLE users (
  id SERIAL PRIMARY KEY
);

-- 复合主键
CREATE TABLE order_items (
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  PRIMARY KEY (order_id, product_id)
);
```

### 外键约束
```sql
CREATE TABLE orders (
  user_id INTEGER REFERENCES users(id)
                   ON DELETE CASCADE
                   ON UPDATE CASCADE,
  ...
);

-- ON DELETE 行为：
-- CASCADE: 删除用户时删除订单
-- SET NULL: 删除用户时订单 user_id 设为 NULL
-- RESTRICT: 阻止删除
-- NO ACTION: 延迟检查
```

### 唯一约束
```sql
CREATE TABLE users (
  email VARCHAR(255) UNIQUE
  -- 或
  CONSTRAINT unique_email UNIQUE (email)
);
```

### CHECK 约束
```sql
CREATE TABLE products (
  price DECIMAL(10, 2) CHECK (price > 0),
  quantity INTEGER CHECK (quantity >= 0),
  
  CONSTRAINT valid_status CHECK (status IN ('active', 'inactive'))
);
```

### 触发器示例
```sql
-- 自动更新 updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- 库存扣减
CREATE OR REPLACE FUNCTION decrease_stock()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT stock FROM products WHERE id = NEW.product_id) < NEW.quantity THEN
    RAISE EXCEPTION '库存不足';
  END IF;
  
  UPDATE products 
  SET stock = stock - NEW.quantity
  WHERE id = NEW.product_id;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_order_item_stock
  AFTER INSERT ON order_items
  FOR EACH ROW
  EXECUTE FUNCTION decrease_stock();
```
```

## AI 輔助 SQL 優化

```
你：
请帮我优化这个查询：

SELECT * FROM orders o 
JOIN users u ON o.user_id = u.id 
JOIN order_items oi ON o.id = oi.order_id 
WHERE o.status = 'completed' 
AND o.created_at > '2024-01-01';

AI：
## 查询优化

### 问题分析
1. `SELECT *` - 返回不必要字段
2. 缺少 WHERE 条件索引
3. 可能存在 N+1 问题

### 优化版本
```sql
SELECT 
  o.id AS order_id,
  o.created_at,
  o.total_amount,
  u.name AS user_name,
  u.email,
  oi.product_id,
  oi.quantity,
  oi.price
FROM orders o 
INNER JOIN users u ON o.user_id = u.id 
INNER JOIN order_items oi ON o.id = oi.order_id 
WHERE o.status = 'completed' 
  AND o.created_at > '2024-01-01'
ORDER BY o.created_at DESC;
```

### 需要添加的索引
```sql
-- 复合索引覆盖查询
CREATE INDEX idx_orders_status_created 
  ON orders(status, created_at DESC);

CREATE INDEX idx_order_items_order_id 
  ON order_items(order_id);
```

### 如果查询频率很高，考虑物化视图
```sql
CREATE MATERIALIZED VIEW completed_orders_view AS
SELECT 
  o.id AS order_id,
  o.created_at,
  o.total_amount,
  u.name AS user_name,
  u.email,
  json_agg(json_build_object(
    'product_id', oi.product_id,
    'quantity', oi.quantity,
    'price', oi.price
  )) AS items
FROM orders o 
INNER JOIN users u ON o.user_id = u.id 
INNER JOIN order_items oi ON o.id = oi.order_id 
WHERE o.status = 'completed'
GROUP BY o.id, o.created_at, o.total_amount, u.name, u.email;

-- 创建索引
CREATE UNIQUE INDEX idx_mv_orders ON completed_orders_view(order_id);

-- 刷新
REFRESH MATERIALIZED VIEW completed_orders_view;
```
```

## 遷移與版本控制

```
你：
数据库迁移的最佳实践是什么？

AI：
## 数据库迁移

### 迁移文件结构
```
migrations/
├── 001_create_users.sql
├── 002_create_products.sql
├── 003_add_user_phone.sql
└── 004_add_order_index.sql
```

### 迁移工具
```bash
# Node.js - Knex
npx knex migrate:make create_users
npx knex migrate:latest

# Python - Alembic
alembic revision -m "create users"
alembic upgrade head

# Go - golang-migrate
migrate create -ext .sql -dir ./migrations create_users
migrate -database DATABASE_URL -path ./migrations up
```

### 安全迁移原则
```sql
-- ❌ 危险：删除列
ALTER TABLE users DROP COLUMN old_field;

-- ✅ 安全：先标记废弃
ALTER TABLE users ADD COLUMN deprecated_at TIMESTAMP;

-- ✅ 安全：分步迁移
-- Step 1: 添加新列（代码已更新）
ALTER TABLE users ADD COLUMN new_field VARCHAR(255);

-- Step 2: 数据迁移
UPDATE users SET new_field = old_field WHERE new_field IS NULL;

-- Step 3: 验证数据

-- Step 4: 删除旧列（下次部署）
ALTER TABLE users DROP COLUMN old_field;
```

### 迁移回滚
```sql
-- Knex 回滚
npx knex migrate:rollback

-- Alembic 回滚
alembic downgrade -1

-- 手动回滚
BEGIN;
  -- 回滚操作
ROLLBACK;  -- 或
COMMIT;
```
```

## 實踐練習

```
1. 设计一个业务数据库
2. 绘制 ER 图
3. 创建完整 schema
4. 添加索引
5. 编写迁移脚本
6. 编写查询示例
7. 分析查询性能
```

**好的資料庫設計是系統的基石。花時間在設計上，回報是長期的穩定和效能。**
