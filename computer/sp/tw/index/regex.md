# 正規表達式 (Regular Expression)

## 概述

正規表達式（Regex）是一種用於描述字元模式的強大工具。它使用字元和特殊符號的組合來匹配、搜尋和替換文字。幾乎所有程式語言都支援正規表達式，是文字處理不可或缺的工具。

## 歷史

- **1950s**：Stephen Kleene 發明正規集合
- **1968**：Ken Thompson 將 regex 引入 QED 編輯器
- **1970s**：grep 命令使用 regex
- **1997**：Perl 相容正規表達式（PCRE）
- **現在**：Unicode 正規表達式

## 基本語法

### 1. 字元類

```python
import re

# 基本匹配
pattern = r"abc"           # 精確匹配
pattern = r"[abc]"         # a, b, 或 c
pattern = r"[^abc]"        # 非 a, b, c
pattern = r"[a-z]"         # a 到 z
pattern = r"[A-Za-z]"      # 字母
pattern = r"[0-9]"         # 數字
pattern = r"."             # 任意字元（換行符除外）
```

### 2. 數量詞

```python
# 數量詞
pattern = r"a*"           # 0 次或多次
pattern = r"a+"           # 1 次或多次
pattern = r"a?"           # 0 次或 1 次
pattern = r"a{3}"         # 恰好 3 次
pattern = r"a{2,4}"       # 2 到 4 次
pattern = r"a{2,}"        # 2 次或更多
```

### 3. 錨點

```python
# 錨點
pattern = r"^abc"         # 開頭匹配
pattern = r"abc$"         # 結尾匹配
pattern = r"\bword\b"     # 完整單詞邊界
pattern = r"\Bword\B"     # 非單詞邊界
```

### 4. 分組

```python
# 分組
pattern = r"(abc)"        # 捕獲組
pattern = r"(?:abc)"      # 非捕獲組
pattern = r"(?P<name>abc)"  # 命名組
pattern = r"a(b|c)d"      # a + (b 或 c) + d
```

### 5. 特殊字元

```python
# 特殊字元
pattern = r"\d"           # 數字 [0-9]
pattern = r"\D"           # 非數字
pattern = r"\w"           # 字母數字底線 [a-zA-Z0-9_]
pattern = r"\W"           # 非字母數字
pattern = r"\s"           # 空白字元
pattern = r"\S"           # 非空白字元
pattern = r"\n"           # 換行符
pattern = r"\t"           # Tab
```

### 6.  lookahead / lookbehind

```python
# lookahead
pattern = r"foo(?=bar)"   # foo 後面是 bar
pattern = r"foo(?!bar)"  # foo 後面不是 bar

# lookbehind
pattern = r"(?<=foo)bar"  # bar 前面是 foo
pattern = r"(?<!foo)bar" # bar 前面不是 foo
```

## 實際範例

### 1. Email 驗證

```python
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
emails = ["test@example.com", "invalid@", "user@domain.org"]
for email in emails:
    match = re.match(email_pattern, email)
    print(f"{email}: {'Valid' if match else 'Invalid'}")
```

### 2. 電話號碼

```python
phone_pattern = r'(\+886|0)?[0-9]{9}'
phones = ["0988123456", "+886988123456", "02-12345678"]
for phone in phones:
    match = re.findall(phone_pattern, phone)
    print(f"{phone}: {match}")
```

### 3. 提取 HTML 標籤內容

```python
html = "<title>Hello</title><p>World</p>"
pattern = r'<(\w+)>(.*?)</\1>'
matches = re.findall(pattern, html)
for tag, content in matches:
    print(f"Tag: {tag}, Content: {content}")
```

### 4. 文字替換

```python
text = "The quick brown fox"
pattern = r'\b(\w)\w+\b'
# 替換為首字母
result = re.sub(pattern, r'\1', text)
print(result)  # T q b f
```

## Python re 模組

```python
import re

# search: 搜尋第一個匹配
match = re.search(r'\d+', 'abc123def')
print(match.group())  # 123

# findall: 找到所有匹配
matches = re.findall(r'\d+', 'a1b2c3')
print(matches)  # ['1', '2', '3']

# sub: 替換
result = re.sub(r'\d', 'X', 'a1b2c3')
print(result)  # aXbXcX

# split: 分割
parts = re.split(r'[,;]', 'a,b;c,d')
print(parts)  # ['a', 'b', 'c', 'd']

# compile: 編譯提升效能
pattern = re.compile(r'\d+')
match = pattern.match('123')
```

## 為什麼學習正規表達式？

1. **文字處理**：強大的文字搜尋和替換
2. **資料驗證**：驗證格式（Email、電話等）
3. **資料提取**：從文字中提取資訊
4. **跨語言**：幾乎所有語言都支援

## 參考資源

- "Mastering Regular Expressions"
- regex101.com（線上測試工具）
- Python re 文件
