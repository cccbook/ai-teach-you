#!/bin/bash
# 測試腳本 - 第7章：圖靈機模擬器實作

echo "=== 第7章測試 ==="
echo ""

echo "1. 測試基本圖靈機..."
python3 07-1-basic-turing-machine.py
echo ""

echo "2. 測試多帶圖靈機..."
python3 07-2-multi-tape.py
echo ""

echo "3. 測試非確定性圖靈機..."
python3 07-3-nondeterministic.py
echo ""

echo "4. 測試通用圖靈機..."
python3 07-4-universal.py
echo ""

echo "=== 第7章測試完成 ==="
