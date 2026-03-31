# XML (eXtensible Markup Language)

## 概述

XML 是一種可延伸的標記語言，用於結構化資料儲存和傳輸曾是 Web 服務和設定檔的主流格式。

## 基本語法

### 文件結構

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
    <element attribute="value">
        內容
    </element>
</root>
```

### 巢狀結構

```xml
<?xml version="1.0" encoding="UTF-8"?>
<users>
    <user id="1">
        <name>王小明</name>
        <email>wang@example.com</email>
        <roles>
            <role>admin</role>
            <role>user</role>
        </roles>
    </user>
</users>
```

## 元素 vs 屬性

```xml
<!-- 使用元素 -->
<user>
    <name>王小明</name>
    <age>25</age>
</user>

<!-- 使用屬性 -->
<user id="1" name="王小明" age="25" />
```

一般建議：
- **元素**：可包含子元素和文字的資料
- **屬性**：描述元素特徵的簡單資料

## XPath 查詢

```xpath
/users/user                    <!-- 選擇所有 user 元素 -->
/users/user[@id='1']          <!-- 選擇 id 為 1 的 user -->
/users/user/name               <!-- 選擇所有 name 子元素 -->
//user[age > 18]               <!-- 選擇 age 大於 18 的 user -->
```

## Python 操作

```python
from xml.etree import ElementTree as ET

# 解析 XML
xml_string = '''
<users>
    <user id="1">
        <name>王小明</name>
    </user>
</users>
'''

root = ET.fromstring(xml_string)
for user in root.findall('user'):
    print(user.find('name').text)

# 創建 XML
root = ET.Element('users')
user = ET.SubElement(root, 'user')
user.set('id', '1')
name = ET.SubElement(user, 'name')
name.text = '王小明'

xml_str = ET.tostring(root, encoding='unicode')
print(xml_str)
```

## JavaScript 操作

```javascript
// DOM 解析
const parser = new DOMParser();
const xml = parser.parseFromString(xmlString, "text/xml");

// 查詢元素
const users = xml.querySelectorAll("user");
users.forEach(user => {
    console.log(user.querySelector("name").textContent);
});

// 序列化
const serializer = new XMLSerializer();
const xmlString = serializer.serializeToString(xml);
```

## 與 JSON 比較

| 特性 | XML | JSON |
|------|-----|------|
| 語法 | 繁瑣 | 簡潔 |
| 資料類型 | 字串為主 | 原生支援 |
| 註解 | 支援 | 不支援 |
| 處理複雜度 | 較高 | 較低 |
| 現有系統支援 | 廣泛 | 日漸普遍 |

## 應用場景

- RSS/Atom 訂閱
- SOAP Web 服務
- 設定檔（Maven pom.xml）
- Office 文件格式（.docx, .xlsx）

## 參考資源

- [W3C XML 規範](https://www.w3.org/XML/)
- [XML Schema](https://www.w3.org/XML/Schema)
