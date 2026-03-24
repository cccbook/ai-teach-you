# NoSQL (Not Only SQL)

## 概述

NoSQL 是一類非關聯式資料庫的總稱，設計用於處理大規模資料、高吞吐量、靈活的資料模型需求。

## NoSQL 類型

### 文件資料庫

以 JSON 文件形式儲存資料：

```javascript
// MongoDB 文件範例
{
    "_id": ObjectId("..."),
    "name": "王小明",
    "email": "wang@example.com",
    "roles": ["admin", "user"],
    "address": {
        "city": "台北",
        "zip": "100"
    },
    "created_at": ISODate("2026-03-24")
}
```

### 鍵值資料庫

簡單的鍵值對儲存：

```python
# Redis
redis.set("user:1", '{"name": "王小明", "age": 25}')
user = redis.get("user:1")

# 設定過期時間
redis.setex("session:abc", 3600, "user_data")
```

### 列族資料庫

以列族為單位儲存：

```cassandra
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT,
    emails LIST<TEXT>,
    addresses MAP<TEXT, TEXT>
);
```

### 圖形資料庫

專門處理圖形結構資料：

```cypher
// Neo4j Cypher
CREATE (alice:Person {name: '王小明', age: 25})
CREATE (bob:Person {name: '陳小美', age: 30})
CREATE (alice)-[:KNOWS]->(bob)
```

## MongoDB 範例

```javascript
// 連接
const { MongoClient } = require('mongodb');
const client = new MongoClient('mongodb://localhost:27017');
const db = client.db('mydb');

// 查詢
const users = await db.collection('users').find({
    age: { $gte: 18 },
    city: '台北'
}).toArray();

// 新增
await db.collection('users').insertOne({
    name: '王小明',
    age: 25,
    tags: ['admin', 'user']
});

// 更新
await db.collection('users').updateOne(
    { _id: ObjectId('...') },
    { $set: { age: 26 } }
);

// 刪除
await db.collection('users').deleteOne({ _id: ObjectId('...') });
```

## 與 SQL 比較

| 特性 | SQL | NoSQL |
|------|-----|-------|
| 資料模型 | 固定的表結構 | 彈性的文件/鍵值 |
| 查詢語言 | SQL | 各有不同的 API |
| 交易 | 完整的 ACID | 通常只支援單文件 ACID |
| 擴展性 | 垂直擴展 | 水平擴展 |
| 適用場景 | 結構化資料、複雜查詢 | 大資料、靈活結構 |

## 常見 NoSQL 資料庫

| 類型 | 資料庫 |
|------|--------|
| 文件 | MongoDB, CouchDB |
| 鍵值 | Redis, DynamoDB, Memcached |
| 列族 | Cassandra, HBase |
| 圖形 | Neo4j, Amazon Neptune |

## 何時使用 NoSQL

- 需要彈性的資料模型
- 處理大量非結構化資料
- 需要水平擴展處理高併發
- 需要快速的開發迭代
- 快取、會話、排行榜等簡單資料

## 參考資源

- [MongoDB 官方網站](https://www.mongodb.com/)
- [Redis 官方網站](https://redis.io/)
- [Cassandra 官方網站](https://cassandra.apache.org/)
