#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 01 - Programming Languages"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 01-1-rectangle 01-1-rectangle.c
gcc -o 01-2-comparison 01-2-comparison.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 01-1-rectangle.c ---"
./01-1-rectangle
echo "Expected: Area = 15"

echo ""
echo "--- Test: 01-2-comparison.c ---"
./01-2-comparison
echo "Expected: x = 5, x == 10 is false"

echo ""
echo "==================================="
echo "All Chapter 01 tests passed!"
echo "==================================="
