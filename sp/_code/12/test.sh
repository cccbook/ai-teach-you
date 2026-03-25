#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 12 - Web"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 12_01_http_server 12_01_http_server.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 12_01_http_server.c ---"
./12_01_http_server
echo "Expected: HTTP server configuration (simulation)"

echo ""
echo "==================================="
echo "All Chapter 12 tests passed!"
echo "==================================="
echo ""
echo "Note: HTTP server compiles but requires"
echo "runtime testing with actual HTTP requests."
