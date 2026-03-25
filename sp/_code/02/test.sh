#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 02 - Grammar & Parsing"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 02-1-regex 02-1-regex.c -lm
gcc -o 02-2-token 02-2-token.c
gcc -o 02-3-parser 02-3-parser.c
gcc -o 02-4-ast 02-4-ast.c
gcc -o 02-5-traverse 02-5-traverse.c
gcc -o 02-6-interpreter 02-6-interpreter.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 02-1-regex.c ---"
./02-1-regex
echo "Expected: Extract numbers from text"

echo ""
echo "--- Test: 02-2-token.c ---"
./02-2-token
echo "Expected: Token type definitions"

echo ""
echo "--- Test: 02-3-parser.c ---"
./02-3-parser
echo "Expected: 2+3 => 5, 10-4*2 => 2, (10-4)*2 => 12"

echo ""
echo "--- Test: 02-4-ast.c ---"
./02-4-ast
echo "Expected: AST structure and result: 14"

echo ""
echo "--- Test: 02-5-traverse.c ---"
./02-5-traverse
echo "Expected: Preorder, postorder, inorder traversal"

echo ""
echo "--- Test: 02-6-interpreter.c ---"
./02-6-interpreter
echo "Expected: 2+3 => 5, 10-4*2 => 2, (10-4)*2 => 12"

echo ""
echo "==================================="
echo "All Chapter 02 tests passed!"
echo "==================================="
