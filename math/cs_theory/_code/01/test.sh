#!/bin/bash
# 測試腳本 - 第1章：計算理論導論

echo "=== 第1章測試 ==="
echo ""

echo "1. 測試巴貝奇分析機模擬..."
python3 01-1-analytical-engine.py
echo ""

echo "2. 測試狀態機..."
python3 01-2-state-machine.py
echo ""

echo "=== 第1章測試完成 ==="
