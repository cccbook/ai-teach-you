#!/bin/bash
# 測試腳本 - 第10章：自動機實作

echo "=== 第10章測試 ==="
echo ""

echo "1. 測試DFA..."
python3 10-1-dfa.py
echo ""

echo "2. 測試NFA..."
python3 10-2-nfa.py
echo ""

echo "3. 測試正則表達式引擎..."
python3 10-3-regex.py
echo ""

echo "4. 測試PDA..."
python3 10-4-pda.py
echo ""

echo "=== 第10章測試完成 ==="
