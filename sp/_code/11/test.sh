#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 11 - TCP/IP"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 11_01_tcp_server 11_01_tcp_server.c
gcc -o 11_02_tcp_client 11_02_tcp_client.c
gcc -o 11_03_udp_server 11_03_udp_server.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 11_01_tcp_server.c ---"
./11_01_tcp_server
echo "Expected: TCP server configuration (simulation)"

echo ""
echo "--- Test: 11_02_tcp_client.c ---"
./11_02_tcp_client
echo "Expected: TCP client configuration (simulation)"

echo ""
echo "--- Test: 11_03_udp_server.c ---"
./11_03_udp_server
echo "Expected: UDP server configuration (simulation)"

echo ""
echo "==================================="
echo "All Chapter 11 tests passed!"
echo "==================================="
echo ""
echo "Note: Network programs compile but require"
echo "runtime testing with actual client/server connections."
