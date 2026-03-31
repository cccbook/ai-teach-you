#!/bin/bash
# 測試腳本 - Chapter 03

cd "$(dirname "$0")"

echo "========================================="
echo "Testing Chapter 03"
echo "========================================="
echo ""

# 測試 03-1-interpreter.c
echo "[TEST] 03-1-interpreter.c - Simple interpreter"
gcc 03-1-interpreter.c -o 03-1-interpreter 2>&1
if [ $? -eq 0 ]; then
    ./03-1-interpreter
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 03-2-stack-vm.c
echo "[TEST] 03-2-stack-vm.c - Stack-based VM"
gcc 03-2-stack-vm.c -o 03-2-stack-vm 2>&1
if [ $? -eq 0 ]; then
    ./03-2-stack-vm
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 03-3-gc.c
echo "[TEST] 03-3-gc.c - Garbage collection"
gcc 03-3-gc.c -o 03-3-gc 2>&1
if [ $? -eq 0 ]; then
    ./03-3-gc
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 03-4-lisp.c
echo "[TEST] 03-4-lisp.c - Simple LISP interpreter"
gcc 03-4-lisp.c -o 03-4-lisp 2>&1
if [ $? -eq 0 ]; then
    ./03-4-lisp
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

echo "========================================="
echo "Chapter 03 Tests Complete"
echo "========================================="
