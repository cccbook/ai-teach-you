# Python

## 概述

Python 是一種高階、通用、解釋型的程式語言，以其簡潔易讀的語法著稱。廣泛應用於 Web 開發、資料科學、人工智慧、自動化等領域。

## 特點

- **簡潔易讀**：縮排定義程式碼區塊
- **跨平台**：支援 Windows、macOS、Linux
- **豐富生態**：數十萬個第三方套件
- **直譯執行**：無需編譯即可執行

## 基本語法

### 變數與資料類型

```python
# 變數
name = "王小明"
age = 25
price = 19.99
is_active = True

# 資料結構
numbers = [1, 2, 3, 4, 5]
person = {"name": "王小明", "age": 25}
unique_items = {1, 2, 3}
```

### 函數

```python
def greet(name, greeting="你好"):
    return f"{greeting}，{name}！"

# 匿名函數
square = lambda x: x ** 2
```

### 類別

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"你好，我是 {self.name}"
```

## Web 框架

| 框架 | 特點 |
|------|------|
| FastAPI | 現代、高性能、自動化 API 文件 |
| Django | 全端框架、ORM、管理介面 |
| Flask | 輕量、彈性、微框架 |

## 參考資源

- [Python 官方網站](https://www.python.org/)
- [Python 文件](https://docs.python.org/zh-tw/3/)
