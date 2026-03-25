#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 04 - Compiler"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 04_01_symbol_table 04_01_symbol_table.c
gcc -o 04_02_compiler 04_02_compiler.c
gcc -o 04_03_linker 04_03_linker.c
gcc -o 04_04_loader 04_04_loader.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 04_01_symbol_table.c ---"
./04_01_symbol_table
echo "Expected: Symbol lookup with scope demo"

echo ""
echo "--- Test: 04_02_compiler.c ---"
./04_02_compiler
echo "Expected: Lexer and parser demo"

echo ""
echo "--- Test: 04_03_linker.c ---"
./04_03_linker
echo "Expected: Linker symbol resolution"

echo ""
echo "--- Test: 04_04_loader.c ---"
./04_04_loader
echo "Expected: Loader steps demo"

echo ""
echo "==================================="
echo "All Chapter 04 tests passed!"
echo "==================================="
