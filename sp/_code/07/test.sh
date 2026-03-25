#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 07 - OS Overview"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 07_01_kernel 07_01_kernel.c
gcc -o 07_02_shell 07_02_shell.c
gcc -o 07_03_pcb 07_03_pcb.c
gcc -o 07_04_fcfs_scheduler 07_04_fcfs_scheduler.c
gcc -o 07_05_priority_scheduler 07_05_priority_scheduler.c
gcc -o 07_06_page_table 07_06_page_table.c
gcc -o 07_07_virtual_memory 07_07_virtual_memory.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 07_01_kernel.c ---"
./07_01_kernel
echo "Expected: Kernel concepts and system calls"

echo ""
echo "--- Test: 07_02_shell.c ---"
echo "help" | ./07_02_shell
echo "Expected: Simple shell simulation"

echo ""
echo "--- Test: 07_03_pcb.c ---"
./07_03_pcb
echo "Expected: PCB state transitions"

echo ""
echo "--- Test: 07_04_fcfs_scheduler.c ---"
./07_04_fcfs_scheduler
echo "Expected: FCFS scheduling demo"

echo ""
echo "--- Test: 07_05_priority_scheduler.c ---"
./07_05_priority_scheduler
echo "Expected: Priority and round robin scheduling"

echo ""
echo "--- Test: 07_06_page_table.c ---"
./07_06_page_table
echo "Expected: Page table and address translation"

echo ""
echo "--- Test: 07_07_virtual_memory.c ---"
./07_07_virtual_memory
echo "Expected: Virtual memory and page replacement"

echo ""
echo "==================================="
echo "All Chapter 07 tests passed!"
echo "==================================="
