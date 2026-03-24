# JSON (JavaScript Object Notation)

## 概述

JSON 是一種輕量級的資料交換格式，易於人類閱讀和機器解析。現已成為 Web API 和設定檔的標準格式。

## 語法

### 基本類型

```json
{
    "string": "Hello, World!",
    "number": 42,
    "float": 3.14,
    "boolean": true,
    "null": null,
    "array": [1, 2, 3],
    "object": {"key": "value"}
}
```

### 巢狀結構

```json
{
    "user": {
        "id": 1,
        "name": "王小明",
        "email": "wang@example.com",
        "roles": ["admin", "user"],
        "address": {
            "city": "台北",
            "zip": "100"
        }
    }
}
```

## JavaScript 操作

```javascript
// 解析 JSON
const jsonString = '{"name": "王小明", "age": 25}';
const obj = JSON.parse(jsonString);
console.log(obj.name); // "王小明"

// 轉換為 JSON
const data = { name: "王小明", age: 25 };
const jsonStr = JSON.stringify(data);
console.log(jsonStr); // '{"name":"王小明","age":25}'

// 格式化輸出
const pretty = JSON.stringify(data, null, 2);
console.log(pretty);
```

## Python 操作

```python
import json

# 解析 JSON
json_string = '{"name": "王小明", "age": 25}'
data = json.loads(json_string)
print(data["name"])  # "王小明"

# 轉換為 JSON
data = {"name": "王小明", "age": 25}
json_str = json.dumps(data)
print(json_str)  # '{"name": "王小明", "age": 25}'

# 格式化輸出
pretty = json.dumps(data, indent=2, ensure_ascii=False)
print(pretty)
```

## 與 XML 比較

| 特性 | JSON | XML |
|------|------|-----|
| 語法簡潔度 | 簡潔 | 較繁瑣 |
| 資料類型 | 原生支援 | 需要自訂 |
| 註解 | 不支援 | 支援 |
| 檔案大小 | 較小 | 較大 |
| 解析速度 | 快 | 較慢 |

## 應用場景

- RESTful API 資料格式
- 設定檔（package.json, tsconfig.json）
- NoSQL 資料庫文件
- 應用程式間資料交換

## 參考資源

- [JSON 官方網站](https://www.json.org/)
- [RFC 8259](https://tools.ietf.org/html/rfc8259)
