#!/bin/bash

set -e

echo "==================================="
echo "Testing Chapter 05 - IR, Object, VM, CPU"
echo "==================================="

cd "$(dirname "$0")"

echo ""
echo "Compiling test files..."
gcc -o 05_01_tac_generator 05_01_tac_generator.c
gcc -o 05_02_elf_parser 05_02_elf_parser.c
gcc -o 05_03_pe_parser 05_03_pe_parser.c
gcc -o 05_04_macho_parser 05_04_macho_parser.c
gcc -o 05_05_stack_vm 05_05_stack_vm.c
gcc -o 05_06_register_vm 05_06_register_vm.c

echo ""
echo "Running tests..."
echo ""

echo "--- Test: 05_01_tac_generator.c ---"
./05_01_tac_generator
echo "Expected: TAC generation demo"

echo ""
echo "--- Test: 05_02_elf_parser.c ---"
./05_02_elf_parser
echo "Expected: ELF header parsing"

echo ""
echo "--- Test: 05_03_pe_parser.c ---"
./05_03_pe_parser
echo "Expected: PE header parsing"

echo ""
echo "--- Test: 05_04_macho_parser.c ---"
./05_04_macho_parser
echo "Expected: Mach-O header parsing"

echo ""
echo "--- Test: 05_05_stack_vm.c ---"
./05_05_stack_vm
echo "Expected: Stack-based VM execution"

echo ""
echo "--- Test: 05_06_register_vm.c ---"
./05_06_register_vm
echo "Expected: Register-based VM execution"

echo ""
echo "==================================="
echo "All Chapter 05 tests passed!"
echo "==================================="
