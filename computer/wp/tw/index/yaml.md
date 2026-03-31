# YAML (YAML Ain't Markup Language)

## 概述

YAML 是一種人性化的資料序列化格式，常用於設定檔。強調可讀性，使用縮排表示層級結構。

## 基本語法

### 純量

```yaml
# 字串
name: "王小明"
message: '單引號也可以'

# 數字
age: 25
price: 19.99
negative: -10

# 布林值
is_active: true
is_deleted: false

# Null
middle_name: null
nickname: ~
```

### 物件和巢狀

```yaml
user:
    name: 王小明
    age: 25
    email: wang@example.com
    address:
        city: 台北
        zip: "100"
```

### 陣列

```yaml
fruits:
    - 蘋果
    - 香蕉
    - 橘子

users:
    - name: 王小明
      age: 25
    - name: 陳小美
      age: 30
```

### 複合格式

```yaml
companies:
    - name: ABC公司
      employees:
          - name: 王小明
            position: 工程師
          - name: 陳小美
            position: 設計師
      founded: 2020
```

## Python 操作

```python
import yaml

# 讀取 YAML
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 寫入 YAML
data = {
    'database': {
        'host': 'localhost',
        'port': 5432,
        'users': ['admin', 'guest']
    }
}

with open('output.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, allow_unicode=True)
```

## JavaScript 操作

```javascript
import yaml from 'js-yaml';
import fs from 'fs';

// 讀取 YAML
const config = yaml.load(fs.readFileSync('config.yaml', 'utf8'));

// 寫入 YAML
const data = {
    server: {
        host: 'localhost',
        port: 3000
    }
};
const yamlStr = yaml.dump(data);
fs.writeFileSync('output.yaml', yamlStr);
```

## 常用設定檔

### Docker Compose

```yaml
version: '3.8'
services:
    web:
        build: .
        ports:
            - "3000:3000"
    db:
        image: postgres:15
        volumes:
            - db_data:/var/lib/postgresql/data

volumes:
    db_data:
```

### GitHub Actions

```yaml
name: CI
on: [push]
jobs:
    build:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v3
            - name: Setup Node.js
              uses: actions/setup-node@v3
              with:
                  node-version: '18'
            - run: npm install
            - run: npm test
```

## YAML 與 JSON

```yaml
# YAML
name: 王小明
age: 25

# JSON 等價
{
    "name": "王小明",
    "age": 25
}
```

YAML 是 JSON 的超集，所有 JSON 格式都是有效的 YAML。

## 參考資源

- [YAML 官方網站](https://yaml.org/)
- [YAML 規範](https://yaml.org/spec/1.2.2/)
