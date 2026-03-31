#!/bin/bash
# 測試腳本 - 第4章：丘奇的λ演算

echo "=== 第4章測試 ==="
echo ""

echo "1. 測試λ演算語法解析器..."
python3 04-1-lambda-syntax.py
echo ""

echo "2. 測試Church編碼..."
python3 04-2-church-encoding.py
echo ""

echo "3. 測試SKI組合子..."
python3 04-3-combinators.py
echo ""

echo "=== 第4章測試完成 ==="
