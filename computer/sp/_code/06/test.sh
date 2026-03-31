#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 06 - Optimization"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 06_01_constant_folding 06_01_constant_folding.c
gcc -o 06_02_cse_elimination 06_02_cse_elimination.c
gcc -o 06_04_jit_compiler 06_04_jit_compiler.c
gcc -o 06_05_inline_cache 06_05_inline_cache.c
gcc -o 06_06_list_scheduling 06_06_list_scheduling.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 06_01_constant_folding.c ---"
./06_01_constant_folding
echo "Expected: Constant folding and algebraic simplification"

echo ""
echo "--- Test: 06_02_cse_elimination.c ---"
./06_02_cse_elimination
echo "Expected: Common subexpression elimination"

echo ""
echo "--- Test: 06_04_jit_compiler.c ---"
./06_04_jit_compiler
echo "Expected: JIT compiler simulation"

echo ""
echo "--- Test: 06_05_inline_cache.c ---"
./06_05_inline_cache
echo "Expected: Inline cache state transitions"

echo ""
echo "--- Test: 06_06_list_scheduling.c ---"
./06_06_list_scheduling
echo "Expected: List scheduling algorithm"

echo ""
echo "==================================="
echo "All Chapter 06 tests passed!"
echo "==================================="
