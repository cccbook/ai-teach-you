# SQL (Structured Query Language)

## 概述

SQL 是用於管理和操作關聯式資料庫的標準程式語言。用於查詢、插入、更新、刪除資料，以及管理資料庫結構。

## 基本查詢

### SELECT

```sql
-- 基本查詢
SELECT * FROM users;

-- 指定欄位
SELECT id, name, email FROM users;

-- 條件查詢
SELECT * FROM users WHERE age >= 18;

-- 排序
SELECT * FROM users ORDER BY created_at DESC;

-- 分頁
SELECT * FROM users LIMIT 10 OFFSET 20;
```

### WHERE 條件

```sql
-- 比較運算子
SELECT * FROM users WHERE age > 18;
SELECT * FROM users WHERE name = '王小明';
SELECT * FROM users WHERE age != 25;

-- AND / OR
SELECT * FROM users WHERE age > 18 AND city = '台北';
SELECT * FROM users WHERE city = '台北' OR city = '高雄';

-- IN / BETWEEN
SELECT * FROM users WHERE id IN (1, 2, 3);
SELECT * FROM users WHERE age BETWEEN 18 AND 30;

-- LIKE 模糊搜尋
SELECT * FROM users WHERE name LIKE '王%';
SELECT * FROM users WHERE email LIKE '%@example.com';
```

## 聚合函數

```sql
-- 計數
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM users WHERE is_active = true;

-- 總和、平均、最大、最小
SELECT SUM(price) FROM orders;
SELECT AVG(age) FROM users;
SELECT MAX(price) FROM products;
SELECT MIN(age) FROM users;

-- GROUP BY
SELECT city, COUNT(*) FROM users GROUP BY city;
SELECT category, AVG(price) FROM products GROUP BY category;

-- HAVING
SELECT city, COUNT(*) as cnt 
FROM users 
GROUP BY city 
HAVING cnt > 10;
```

## 多表查詢

### JOIN

```sql
-- INNER JOIN
SELECT orders.id, users.name, orders.total
FROM orders
INNER JOIN users ON orders.user_id = users.id;

-- LEFT JOIN
SELECT users.name, orders.id
FROM users
LEFT JOIN orders ON users.id = orders.user_id;

-- 多表 JOIN
SELECT o.id, u.name, p.title
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id;
```

### 子查詢

```sql
-- 在 WHERE 中使用
SELECT * FROM users 
WHERE age > (SELECT AVG(age) FROM users);

-- 在 FROM 中使用
SELECT city, cnt
FROM (
    SELECT city, COUNT(*) as cnt
    FROM users
    GROUP BY city
) city_counts
WHERE cnt > 5;
```

## 資料操作

### INSERT

```sql
-- 單筆新增
INSERT INTO users (name, email, age)
VALUES ('王小明', 'wang@example.com', 25);

-- 多筆新增
INSERT INTO users (name, email, age) VALUES
    ('王小明', 'wang@example.com', 25),
    ('陳小美', 'chen@example.com', 30);
```

### UPDATE

```sql
-- 更新資料
UPDATE users SET age = 26 WHERE id = 1;

-- 多欄位更新
UPDATE users 
SET age = 26, city = '高雄'
WHERE id = 1;
```

### DELETE

```sql
-- 刪除資料
DELETE FROM users WHERE id = 1;

-- 清空資料表
DELETE FROM users;
```

## 資料庫結構

### CREATE TABLE

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ALTER

```sql
-- 新增欄位
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- 修改欄位
ALTER TABLE users MODIFY COLUMN age INTEGER DEFAULT 18;
```

### DROP

```sql
-- 刪除資料表
DROP TABLE users;

-- 刪除資料庫
DROP DATABASE mydb;
```

## 參考資源

- [W3Schools SQL](https://www.w3schools.com/sql/)
- [PostgreSQL 文檔](https://www.postgresql.org/docs/)
