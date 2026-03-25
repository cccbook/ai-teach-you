#!/bin/bash
# 測試腳本 - Chapter 04

cd "$(dirname "$0")"

echo "========================================="
echo "Testing Chapter 04"
echo "========================================="
echo ""

# 測試 04_01_symbol_table.c
echo "[TEST] 04_01_symbol_table.c - Symbol table"
gcc 04_01_symbol_table.c -o 04_01_symbol_table 2>&1
if [ $? -eq 0 ]; then
    ./04_01_symbol_table
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 04_02_compiler.c
echo "[TEST] 04_02_compiler.c - Simple compiler"
gcc 04_02_compiler.c -o 04_02_compiler 2>&1
if [ $? -eq 0 ]; then
    ./04_02_compiler
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 04_03_linker.c
echo "[TEST] 04_03_linker.c - Linker simulation"
gcc 04_03_linker.c -o 04_03_linker 2>&1
if [ $? -eq 0 ]; then
    ./04_03_linker
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 04_04_loader.c
echo "[TEST] 04_04_loader.c - Loader simulation"
gcc 04_04_loader.c -o 04_04_loader 2>&1
if [ $? -eq 0 ]; then
    ./04_04_loader
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

echo "========================================="
echo "Chapter 04 Tests Complete"
echo "========================================="
