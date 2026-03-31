#!/bin/bash
# 測試腳本 - Chapter 05

cd "$(dirname "$0")"

echo "========================================="
echo "Testing Chapter 05"
echo "========================================="
echo ""

# 測試 05_01_tac_generator.c
echo "[TEST] 05_01_tac_generator.c - TAC generator"
gcc 05_01_tac_generator.c -o 05_01_tac_generator 2>&1
if [ $? -eq 0 ]; then
    ./05_01_tac_generator
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 05_02_elf_parser.c
echo "[TEST] 05_02_elf_parser.c - ELF parser"
gcc 05_02_elf_parser.c -o 05_02_elf_parser 2>&1
if [ $? -eq 0 ]; then
    ./05_02_elf_parser
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 05_03_pe_parser.c
echo "[TEST] 05_03_pe_parser.c - PE parser"
gcc 05_03_pe_parser.c -o 05_03_pe_parser 2>&1
if [ $? -eq 0 ]; then
    ./05_03_pe_parser
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 05_04_macho_parser.c
echo "[TEST] 05_04_macho_parser.c - Mach-O parser"
gcc 05_04_macho_parser.c -o 05_04_macho_parser 2>&1
if [ $? -eq 0 ]; then
    ./05_04_macho_parser
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 05_05_stack_vm.c
echo "[TEST] 05_05_stack_vm.c - Stack VM"
gcc 05_05_stack_vm.c -o 05_05_stack_vm 2>&1
if [ $? -eq 0 ]; then
    ./05_05_stack_vm
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

# 測試 05_06_register_vm.c
echo "[TEST] 05_06_register_vm.c - Register VM"
gcc 05_06_register_vm.c -o 05_06_register_vm 2>&1
if [ $? -eq 0 ]; then
    ./05_06_register_vm
    echo "✓ PASS"
else
    echo "✗ FAIL"
fi
echo ""

echo "========================================="
echo "Chapter 05 Tests Complete"
echo "========================================="
