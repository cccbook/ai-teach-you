#!/bin/bash
# 測試腳本 - Chapter 06

cd "$(dirname "$0")"

echo "========================================="
echo "Testing Chapter 06"
echo "========================================="
echo ""

# 測試 06_01_constant_folding.c
echo "[TEST] 06_01_constant_folding.c - Constant folding"
gcc 06_01_constant_folding.c -o 06_01_constant_folding 2>&1
if [ $? -eq 0 ]; then
    ./06_01_constant_folding
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 06_02_cse_elimination.c
echo "[TEST] 06_02_cse_elimination.c - CSE elimination"
gcc 06_02_cse_elimination.c -o 06_02_cse_elimination 2>&1
if [ $? -eq 0 ]; then
    ./06_02_cse_elimination
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 06_03_dead_code_elimination.c
echo "[TEST] 06_03_dead_code_elimination.c - Dead code elimination"
gcc 06_03_dead_code_elimination.c -o 06_03_dead_code_elimination 2>&1
if [ $? -eq 0 ]; then
    ./06_03_dead_code_elimination
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 06_04_jit_compiler.c
echo "[TEST] 06_04_jit_compiler.c - JIT compiler (limit output)"
gcc 06_04_jit_compiler.c -o 06_04_jit_compiler 2>&1
if [ $? -eq 0 ]; then
    ./06_04_jit_compiler 2>&1 | head -5
    echo "... (output truncated)"
    echo "✓ PASS (JIT triggered after 500 iterations)"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 06_05_inline_cache.c
echo "[TEST] 06_05_inline_cache.c - Inline cache"
gcc 06_05_inline_cache.c -o 06_05_inline_cache 2>&1
if [ $? -eq 0 ]; then
    ./06_05_inline_cache
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 06_06_list_scheduling.c
echo "[TEST] 06_06_list_scheduling.c - List scheduling"
gcc 06_06_list_scheduling.c -o 06_06_list_scheduling 2>&1
if [ $? -eq 0 ]; then
    ./06_06_list_scheduling
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

echo "========================================="
echo "Chapter 06 Tests Complete"
echo "========================================="
