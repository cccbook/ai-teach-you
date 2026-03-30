#!/bin/bash
# 測試腳本 - Chapter 01

cd "$(dirname "$0")"

echo "========================================="
echo "Testing Chapter 01"
echo "========================================="
echo ""

# 測試 01-1-rectangle.c
echo "[TEST] 01-1-rectangle.c - OOP Rectangle"
gcc 01-1-rectangle.c -o 01-1-rectangle 2>&1
if [ $? -eq 0 ]; then
    ./01-1-rectangle
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 01-2-comparison.c
echo "[TEST] 01-2-comparison.c - Comparison operators"
gcc 01-2-comparison.c -o 01-2-comparison 2>&1
if [ $? -eq 0 ]; then
    ./01-2-comparison
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

echo "========================================="
echo "Chapter 01 Tests Complete"
echo "========================================="
