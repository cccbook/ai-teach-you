#!/bin/bash
# 測試腳本 - Chapter 02

cd "$(dirname "$0")"

echo "========================================="
echo "Testing Chapter 02"
echo "========================================="
echo ""

# 測試 02-1-regex.c
echo "[TEST] 02-1-regex.c - Regex operations"
gcc 02-1-regex.c -o 02-1-regex 2>&1
if [ $? -eq 0 ]; then
    ./02-1-regex
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 02-2-token.c
echo "[TEST] 02-2-token.c - Token structure"
gcc 02-2-token.c -o 02-2-token 2>&1
if [ $? -eq 0 ]; then
    ./02-2-token
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 02-3-parser.c
echo "[TEST] 02-3-parser.c - LL(1) Parser"
gcc 02-3-parser.c -o 02-3-parser 2>&1
if [ $? -eq 0 ]; then
    ./02-3-parser
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 02-4-ast.c
echo "[TEST] 02-4-ast.c - AST structures"
gcc 02-4-ast.c -o 02-4-ast 2>&1
if [ $? -eq 0 ]; then
    ./02-4-ast
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 02-5-traverse.c
echo "[TEST] 02-5-traverse.c - Tree traversal"
gcc 02-5-traverse.c -o 02-5-traverse 2>&1
if [ $? -eq 0 ]; then
    ./02-5-traverse
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 02-6-interpreter.c
echo "[TEST] 02-6-interpreter.c - Expression interpreter"
gcc 02-6-interpreter.c -o 02-6-interpreter 2>&1
if [ $? -eq 0 ]; then
    ./02-6-interpreter
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

echo "========================================="
echo "Chapter 02 Tests Complete"
echo "========================================="
