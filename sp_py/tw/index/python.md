# Python

## 概述

Python 是一種廣泛使用的高階直譯式程式語言，由 Guido van Rossum 於 1991 年首次發布。Python 以簡潔易讀的語法著稱，擁有豐富的標準庫和活躍的生態系統，適用於網頁開發、資料科學、人工智慧、自動化等各種領域。

## 歷史

- **1991 年**：Guido van Rossum 發布 Python 0.9.0
- **2000 年**：Python 2.0 發布
- **2008 年**：Python 3.0 發布（重大改革）
- **2020 年**：Python 2 停止維護
- **現在**：Python 3.12 為最新穩定版

## 核心特性

### 1. 動態類型

```python
# 變數無需事先宣告類型
x = 10          # int
x = "hello"     # 變成 str
x = [1, 2, 3]   # 變成 list

# 類型註釋（型別提示）
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### 2. 資料結構

```python
# 列表（List）
numbers = [1, 2, 3, 4, 5]
numbers.append(6)
print(numbers[0])  # 1

# 元組（Tuple）- 不可變
point = (10, 20)
x, y = point

# 字典（Dictionary）
person = {"name": "John", "age": 30}
print(person["name"])

# 集合（Set）
fruits = {"apple", "banana", "orange"}
fruits.add("grape")
```

### 3. 函數式編程

```python
# lambda 表達式
square = lambda x: x ** 2
print(square(5))  # 25

# map, filter, reduce
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

from functools import reduce
total = reduce(lambda x, y: x + y, numbers)
```

### 4. 類別與物件導向

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, I'm {self.name}"

person = Person("John", 30)
print(person.greet())

# 繼承
class Student(Person):
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self.grade = grade
```

### 5. 生成器與迭代器

```python
# 生成器
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)

# 列表推導式
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

## 常用標準庫

```python
import os
import sys
import json
import re
import datetime
import collections
import itertools
```

## 專案範例：簡易計算器

```python
class Calculator:
    def __init__(self):
        self.history = []
    
    def calculate(self, expression):
        try:
            result = eval(expression)
            self.history.append((expression, result))
            return result
        except Exception as e:
            return f"Error: {e}"
    
    def history(self):
        return self.history

calc = Calculator()
print(calc.calculate("2 + 3 * 4"))  # 14
print(calc.calculate("10 / 2"))    # 5.0
```

## 為什麼學習 Python？

1. **易學易用**：語法簡潔，適合初學者
2. **多功能**：網頁、資料科學、AI、自動化
3. **豐富庫**：pip 生態龐大
4. **跨平台**：Windows、macOS、Linux
5. **社群活躍**：大量資源和支援

## 參考資源

- Python 官方文檔：docs.python.org
- "Fluent Python" by Luciano Ramalho
- "Automate the Boring Stuff with Python"
