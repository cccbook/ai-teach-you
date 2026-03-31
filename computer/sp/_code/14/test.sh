#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 14 - AI"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 14_01_quantization 14_01_quantization.c -lm
gcc -o 14_02_pruning 14_02_pruning.c -lm
gcc -o 14_03_distributed_training 14_03_distributed_training.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 14_01_quantization.c ---"
./14_01_quantization
echo "Expected: FP32 to INT8 quantization demo"

echo ""
echo "--- Test: 14_02_pruning.c ---"
./14_02_pruning
echo "Expected: Weight pruning demo"

echo ""
echo "--- Test: 14_03_distributed_training.c ---"
./14_03_distributed_training
echo "Expected: Distributed training communication patterns"

echo ""
echo "==================================="
echo "All Chapter 14 tests passed!"
echo "==================================="
