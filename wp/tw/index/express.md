# Express.js

## 概述

Express.js 是 Node.js 最流行的 Web 應用框架，簡潔靈活，適合建立 API 和 Web 應用。

## 基本範例

```javascript
const express = require('express');
const app = express();

// 中間件
app.use(express.json());

// GET 路由
app.get('/api/users', (req, res) => {
    res.json([{ id: 1, name: '王小明' }]);
});

// POST 路由
app.post('/api/users', (req, res) => {
    const user = req.body;
    res.status(201).json(user);
});

// 路由參數
app.get('/api/users/:id', (req, res) => {
    const userId = req.params.id;
    res.json({ id: userId, name: 'User' });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

## 中間件

```javascript
// 日誌中間件
app.use((req, res, next) => {
    console.log(`${req.method} ${req.path}`);
    next();
});

// 錯誤處理中間件
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// 第三方中間件
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');

app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
```

## RESTful 路由

```javascript
// CRUD 路由
app.get('/api/items', getItems);
app.get('/api/items/:id', getItem);
app.post('/api/items', createItem);
app.put('/api/items/:id', updateItem);
app.delete('/api/items/:id', deleteItem);
```

## 參考資源

- [Express.js 官方網站](https://expressjs.com/)
- [Express.js 中文網](https://www.expressjs.com.cn/)
