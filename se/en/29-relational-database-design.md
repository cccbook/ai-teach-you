# 29. Relational Database Design

## The Art of Database Design

```
┌─────────────────────────────────────────────────────────┐
│               Database Design Principles                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Good design:                                          │
│   ├─ Data consistency                                  │
│   ├─ High query efficiency                             │
│   ├─ Easy to extend                                   │
│   └─ Reduced redundancy                               │
│                                                         │
│   Bad design:                                          │
│   ├─ Update anomalies                                 │
│   ├─ Insert/delete anomalies                         │
│   └─ Wasted storage space                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Normalization

### Normalization Levels

```
You:
What is database normalization? Why normalize?

AI:
## Database Normalization

### First Normal Form (1NF)
```
Requirement: Each column is atomic, indivisible

❌ Violates 1NF:
user_address: "123 Main St, 100022"

✅ Conforms to 1NF:
city: "New York"
district: "Manhattan"
street: "123 Main St"
zip_code: "100022"
```

### Second Normal Form (2NF)
```
Requirement: Conforms to 1NF + non-key columns fully depend on primary key

❌ Violates 2NF (order table):
order_id | product_id | product_name | quantity
   1     |     1       | Phone        |    2
   1     |     2       | Headphones   |    1

product_name only depends on product_id, not fully on composite key

✅ Conforms to 2NF:
Orders: order_id | product_id | quantity
Products: product_id | product_name
```

### Third Normal Form (3NF)
```
Requirement: Conforms to 2NF + no transitive dependencies

❌ Violates 3NF (student table):
student_id | name | department | department_phone
    1      | John | CS        | 010-123456

department_phone depends on department, which depends on student_id

✅ Conforms to 3NF:
Students: student_id | name | department_id
Departments: department_id | department_name | phone
```

### Normalization vs Denormalization
```
Normalization:
✓ Data consistency
✓ Less storage space
✓ Easier updates

Denormalization:
✓ Faster queries
✓ Fewer JOINs
✓ Simpler implementation

Reality: Choose based on business scenario
```

## AI-Assisted ER Design

### Generate ER Diagram from Requirements

```
You:
Please design a database schema for an e-commerce system with:
- Users (login, registration)
- Products (name, price, inventory)
- Orders (ordering, status)
- Shopping cart

AI:
## E-commerce Database Design

### ER Diagram
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
      │          │ created_at  │           ↓
      │          └─────────────┘     ┌─────────────┐
      │                 │           │ cart_items  │
      ↓                 │           ├─────────────┤
┌─────────────┐         │           │ id (PK)     │
│  products   │         │           │ cart_id (FK)│
├─────────────┤         │           │ product_id  │
│ id (PK)     │         │           │ quantity    │
│ name        │         │           └─────────────┘
│ price       │         └───────┬─────────┐
│ stock       │                 │         │
│ category_id │                 ↓         ↓
│ created_at  │         ┌─────────────┐ ┌─────────────┐
└─────────────┘         │ order_items│ │  payments   │
      │                 ├─────────────┤ ├─────────────┤
      │                 │ id (PK)     │ │ id (PK)     │
      └────────────────→│ order_id(FK)│ │ order_id(FK)│
                        │ product_id  │ │ amount      │
                        │ quantity    │ │ status      │
                        │ price       │ │ paid_at     │
                        └─────────────┘ └─────────────┘
```

### SQL DDL
```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Addresses table
CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  street VARCHAR(255),
  city VARCHAR(100),
  postal_code VARCHAR(20),
  is_default BOOLEAN DEFAULT FALSE
);

-- Categories table
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  parent_id INTEGER REFERENCES categories(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
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

-- Orders table
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  status VARCHAR(50) DEFAULT 'pending',
  total_amount DECIMAL(10, 2) NOT NULL,
  shipping_address_id INTEGER REFERENCES addresses(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(id),
  product_id INTEGER NOT NULL REFERENCES products(id),
  quantity INTEGER NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  
  CONSTRAINT positive_quantity CHECK (quantity > 0)
);

-- Payments table
CREATE TABLE payments (
  id SERIAL PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(id),
  amount DECIMAL(10, 2) NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  paid_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_addresses_user_id ON addresses(user_id);
```

## Index Design

```
You:
How to design indexes?

AI:
## Index Design

### When to Create Indexes
```
✅ Create indexes:
├─ Primary keys (auto-created)
├─ Frequently queried WHERE conditions
├─ JOIN conditions
├─ ORDER BY / GROUP BY columns
└─ Unique constraints

❌ Don't need indexes:
├─ Low cardinality columns (gender, status)
├─ Rarely queried columns
├─ Frequently updated columns
└─ Large text fields
```

### Index Types

| Type | Use Case | Example |
|------|----------|---------|
| B-Tree | Default, range queries | `>, <, BETWEEN` |
| Hash | Equality queries | `=, IN` |
| GIN | Full-text search, JSON | `tsvector` |
| GiST | Geospatial data | `PostGIS` |
| Composite | Multi-column queries | `(a, b, c)` |

### Composite Index Order
```sql
-- Composite index (status, user_id, created_at)

-- ✅ Index used effectively
WHERE status = 'pending'
WHERE status = 'pending' AND user_id = 1
WHERE status = 'pending' AND user_id = 1 AND created_at > '2024-01-01'

-- ❌ Index not used
WHERE user_id = 1                    -- Skips first column
WHERE created_at > '2024-01-01'    -- Skips first two columns
```

### Index Maintenance
```sql
-- Check index usage
SELECT 
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT 
  indexrelname,
  idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey';

-- Drop unused indexes
DROP INDEX IF EXISTS unused_index;
```

## Constraints and Triggers

```
You:
What database constraints are there?

AI:
## Common Constraints

### Primary Key Constraint
```sql
-- Single column primary key
CREATE TABLE users (
  id SERIAL PRIMARY KEY
);

-- Composite primary key
CREATE TABLE order_items (
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  PRIMARY KEY (order_id, product_id)
);
```

### Foreign Key Constraint
```sql
CREATE TABLE orders (
  user_id INTEGER REFERENCES users(id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
  ...
);

-- ON DELETE behavior:
-- CASCADE: Delete orders when user deleted
-- SET NULL: Set order user_id to NULL
-- RESTRICT: Prevent deletion
-- NO ACTION: Deferred check
```

### Unique Constraint
```sql
CREATE TABLE users (
  email VARCHAR(255) UNIQUE
  -- or
  CONSTRAINT unique_email UNIQUE (email)
);
```

### CHECK Constraint
```sql
CREATE TABLE products (
  price DECIMAL(10, 2) CHECK (price > 0),
  quantity INTEGER CHECK (quantity >= 0),
  
  CONSTRAINT valid_status CHECK (status IN ('active', 'inactive'))
);
```

### Trigger Examples
```sql
-- Auto-update updated_at
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

-- Inventory decrement
CREATE OR REPLACE FUNCTION decrease_stock()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT stock FROM products WHERE id = NEW.product_id) < NEW.quantity THEN
    RAISE EXCEPTION 'Insufficient stock';
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

## AI-Assisted SQL Optimization

```
You:
Please help me optimize this query:

SELECT * FROM orders o 
JOIN users u ON o.user_id = u.id 
JOIN order_items oi ON o.id = oi.order_id 
WHERE o.status = 'completed' 
AND o.created_at > '2024-01-01';

AI:
## Query Optimization

### Problem Analysis
1. `SELECT *` - Returns unnecessary fields
2. Missing WHERE clause indexes
3. Potential N+1 problem

### Optimized Version
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

### Required Indexes
```sql
-- Composite index covering query
CREATE INDEX idx_orders_status_created 
  ON orders(status, created_at DESC);

CREATE INDEX idx_order_items_order_id 
  ON order_items(order_id);
```

### For high-frequency queries, consider materialized view
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

-- Create index
CREATE UNIQUE INDEX idx_mv_orders ON completed_orders_view(order_id);

-- Refresh
REFRESH MATERIALIZED VIEW completed_orders_view;
```

## Migration and Version Control

```
You:
What are best practices for database migration?

AI:
## Database Migration

### Migration File Structure
```
migrations/
├── 001_create_users.sql
├── 002_create_products.sql
├── 003_add_user_phone.sql
└── 004_add_order_index.sql
```

### Migration Tools
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

### Safe Migration Principles
```sql
-- ❌ Dangerous: Drop column
ALTER TABLE users DROP COLUMN old_field;

-- ✅ Safe: Mark as deprecated first
ALTER TABLE users ADD COLUMN deprecated_at TIMESTAMP;

-- ✅ Safe: Step-by-step migration
-- Step 1: Add new column (code already updated)
ALTER TABLE users ADD COLUMN new_field VARCHAR(255);

-- Step 2: Migrate data
UPDATE users SET new_field = old_field WHERE new_field IS NULL;

-- Step 3: Verify data

-- Step 4: Drop old column (next deployment)
ALTER TABLE users DROP COLUMN old_field;
```

### Migration Rollback
```sql
-- Knex rollback
npx knex migrate:rollback

-- Alembic rollback
alembic downgrade -1

-- Manual rollback
BEGIN;
  -- rollback operations
ROLLBACK;  -- or
COMMIT;
```

## Practice Exercises

```
1. Design a business database
2. Draw ER diagram
3. Create complete schema
4. Add indexes
5. Write migration scripts
6. Write query examples
7. Analyze query performance
```

**Good database design is the foundation of the system. Time invested in design pays back in long-term stability and performance.**
