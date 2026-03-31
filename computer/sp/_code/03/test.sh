#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 03 - Interpreter & VM"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 03-1-interpreter 03-1-interpreter.c
gcc -o 03-2-stack-vm 03-2-stack-vm.c
gcc -o 03-3-gc 03-3-gc.c
gcc -o 03-4-lisp 03-4-lisp.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 03-1-interpreter.c ---"
./03-1-interpreter
echo "Expected: Variable lookup demo"

echo ""
echo "--- Test: 03-2-stack-vm.c ---"
./03-2-stack-vm
echo "Expected: Stack VM result: 30"

echo ""
echo "--- Test: 03-3-gc.c ---"
./03-3-gc
echo "Expected: GC memory management demo"

echo ""
echo "--- Test: 03-4-lisp.c ---"
./03-4-lisp
echo "Expected: LISP eval demo (+ 2 3) => 5"

echo ""
echo "==================================="
echo "All Chapter 03 tests passed!"
echo "==================================="
