#!/usr/bin/env python3
# 02-1-regex-example.py - 正則表達式範例

import re

# 基本模式
pattern = r"[0-9]+"  # 匹配一個或多個數字
text = "年齡是 25 歲，體重 65.5 公斤"

matches = re.findall(pattern, text)
print("匹配結果:", matches)  # ['25', '65', '5']

# 電子郵件正則表達式
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = "聯絡: user@example.com 或 admin@test.org"
print("Email:", re.findall(email_pattern, emails))

# 手機號碼（台灣格式）
phone_pattern = r"09[0-9]{8}"
print("電話匹配:", re.match(phone_pattern, "0912345678") is not None)

print("\n正則表達式範例完成")