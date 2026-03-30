# SQLite

## 概述

SQLite 是一個輕量級的嵌入式關聯式資料庫引擎，不需要单独的服务器进程，完全自包含在一个文件中。

## 特點

- **零配置**：無需安裝或配置
- **單一檔案**：整個資料庫在一個檔案中
- **跨平台**：支援所有主要作業系統
- **事務支援**：完整的 ACID 事務
- **高效能**：讀取速度可達每秒數十萬次

## 基本操作

### 命令列工具

```bash
# 進入 SQLite 命令列
sqlite3 mydatabase.db

# 基本命令
sqlite> .help              # 顯示幫助
sqlite> .tables            # 列出所有資料表
sqlite> .schema users      # 查看表結構
sqlite> .quit              # 退出
```

### Python 操作

```python
import sqlite3

# 連接資料庫
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# 查詢
cursor.execute('SELECT * FROM users WHERE age > ?', (18,))
results = cursor.fetchall()

# 新增
cursor.execute(
    'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
    ('王小明', 'wang@example.com', 25)
)

# 更新
cursor.execute(
    'UPDATE users SET age = ? WHERE id = ?',
    (26, 1)
)

# 刪除
cursor.execute('DELETE FROM users WHERE id = ?', (1,))

# 提交變更
conn.commit()

# 關閉連接
conn.close()
```

### JavaScript 操作

```javascript
const Database = require('better-sqlite3');
const db = new Database('mydatabase.db');

// 查詢
const users = db.prepare('SELECT * FROM users WHERE age > ?').all(18);

// 新增
const insert = db.prepare('INSERT INTO users (name, email) VALUES (?, ?)');
const result = insert.run('王小明', 'wang@example.com');

// 交易
const transaction = db.transaction(() => {
    db.prepare('INSERT INTO users (name) VALUES (?)').run('使用者1');
    db.prepare('INSERT INTO users (name) VALUES (?)').run('使用者2');
});
transaction();

db.close();
```

## 建立資料表

```sql
-- 使用 AUTOINCREMENT
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 建立索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_age ON users(age);

-- 外鍵約束
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 與其他資料庫比較

| 特性 | SQLite | PostgreSQL | MySQL |
|------|--------|------------|-------|
| 部署複雜度 | 簡單 | 中等 | 中等 |
| 併發支援 | 有限 | 強大 | 強大 |
| 儲存需求 | < 1MB | > 100MB | > 50MB |
| 適用場景 | 行動應用、本地儲存、測試 | 生產伺服器 | 生產伺服器 |
| 資料量限制 | < 1TB | 無限制 | 無限制 |

## Node.js ORM - Prisma

```prisma
// schema.prisma
generator client {
    provider = "prisma-client-js"
}

datasource db {
    provider = "sqlite"
    url      = "file:./dev.db"
}

model User {
    id    Int     @id @default(autoincrement())
    name  String
    email String  @unique
    posts Post[]
}

model Post {
    id        Int     @id @default(autoincrement())
    title     String
    content   String?
    userId    Int
    user      User    @relation(fields: [userId], references: [id])
}
```

## 備份與還原

```bash
# 備份
sqlite3 mydatabase.db ".backup backup.db"

# 還原
sqlite3 restored.db ".restore backup.db"

# 導出 SQL
sqlite3 mydatabase.db ".dump" > backup.sql

# 從 SQL 還原
sqlite3 mydatabase.db < backup.sql
```

## 參考資源

- [SQLite 官方網站](https://www.sqlite.org/)
- [SQLite Browser](https://sqlitebrowser.org/)
