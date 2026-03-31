# Let AI Teach You System Programming

> Using c4 to understand compilers, mini-riscv-os to understand operating systems, and xv6 to understand UNIX

---

## Table of Contents

### Part I: C Language and Memory Model

* [1. From High-Level Language to Machine Code——The Essence of C](01-c_basics.md)
* [2. Memory Model——Stack, Heap, and Static Memory](02-memory_model.md)
* [3. Pointers and Pointer Arithmetic——The Core of C](03-pointers.md)
* [4. Pointer Applications——Arrays, Strings, and Function Pointers](04-pointer_applications.md)

### Part II: From C to Assembly——Compiler Basics

* [5. c4: A C Compiler in Four Functions](05-c4_overview.md)
* [6. Lexical Analysis——Converting Source Code to Tokens](06-lexer.md)
* [7. Syntax Analysis——Expressions and Precedence](07-parser.md)
* [8. Code Generation——From Syntax Tree to VM Instructions](08-codegen.md)
* [9. Virtual Machine——Stack-Based Instruction Set Architecture](09-virtual_machine.md)

### Part III: Building Your Own Compiler Toolchain - cpy0

* [10. cpy0 Toolchain Overview——From Source to RISC-V Executable](10-cpy0_overview.md)
* [11. Clang Frontend——C Language to LLVM IR](11-clang_frontend.md)
* [12. ll0 Backend——LLVM IR to RISC-V Assembly](12-ll0_backend.md)
* [13. rv0 Assembler——Assembly to Object File](13-rv0_assembler.md)
* [14. rv0 Virtual Machine——RISC-V Instruction Set Simulator](14-rv0_vm.md)
* [15. py0 Compiler——Python to qd0 Bytecode](15-py0_compiler.md)
* [16. qd0c Converter——qd0 Bytecode to LLVM IR](16-qd0_to_llvm.md)

### Part IV: RISC-V Processor Architecture

* [17. RISC-V Instruction Set——The Philosophy of RISC](17-riscv_instructions.md)
* [18. Assembly and Disassembly——Reading Machine Language](18-assembly.md)
* [19. Calling Conventions——Stack Frames and Register Usage](19-call_convention.md)
* [20. LLVM IR——Modern Compiler's Intermediate Representation](20-llvm_ir.md)

### Part V: Building OS from Scratch with mini-riscv-os

* [21. First OS——UART and Hello World](21-helloos.md)
* [22. Privilege Mode Switching——Context Switch Basics](22-context_switch.md)
* [23. Multitasking——Task Switching and Scheduling](23-multitasking.md)
* [24. Timer Interrupts——Preemptive Scheduling](24-timer_interrupt.md)

### Part VI: xv6 Deep Dive

* [25. xv6 Architecture Overview——UNIX v6 on RISC-V](25-xv6_overview.md)
* [26. Boot Process——From BIOS to Kernel](26-boot.md)
* [27. Process Management——fork, exec, and wait](27-process.md)
* [28. File System——inode and Journaling](28-filesystem.md)
* [29. Virtual File System——VFS Abstraction Layer](29-vfs.md)
* [30. Memory Management——Paging and Swapping](30-memory.md)
* [31. Scheduler——CFS and Real-Time Scheduling](31-scheduler.md)

### Part VII: Modern Toolchain Practice

* [32. GCC Toolchain——From Source to Executable](32-gcc_toolchain.md)
* [33. LLVM/Clang——Modular Compiler Framework](33-llvm_clang.md)
* [34. Cross-Compilation——Compiling RISC-V on x86](34-cross_compile.md)
* [35. Debugging Tools——GDB and LLDB](35-debugging.md)
* [36. Profiling——perf and Flame Graphs](36-profiling.md)

### Part VIII: Advanced Topics

* [37. Linker Scripts——Controlling Memory Layout](37-linker_script.md)
* [38. Static Analysis——How Linker Resolves Symbols](38-linking.md)
* [39. OS Virtualization——From xv6 to Modern Kernels](39-os_virtualization.md)
* [40. Container Technology——namespace and cgroup](40-containers.md)
* [41. Future of System Programming——eBPF and WebAssembly](41-future.md)

---

## Core Code

### Reference Sources

* [c4](https://github.com/rswier/c4) - C compiler in four functions with stack-based VM
* [mini-riscv-os](https://github.com/cccriscv/mini-riscv-os) - DIY RISC-V OS (10 stages)
* [xv6-riscv](https://github.com/mit-pdos/xv6-riscv) - MIT teaching UNIX v6 (RISC-V version)
* [cpy0/c0computer](https://github.com/ccc-c/c0computer) - DIY compiler toolchain by ccc
* [riscv2os](https://github.com/riscv2os/riscv2os) - RISC-V processor to OS learning project

### Book Example Code

* [_code/c4/](_code/c4/) - c4 compiler source code
* [_code/c4/hello.c](_code/c4/hello.c) - c4 test example
* [_code/mini-riscv-os/](_code/mini-riscv-os/) - 10-stage OS
* [_code/xv6/](_code/xv6/) - xv6-riscv source code
* [_code/cpy0/](_code/cpy0/) - DIY compiler toolchain
* [_code/riscv2os/](_code/riscv2os/) - RISC-V learning project
* [_code/examples/](_code/examples/) - Additional example programs

---

*Last updated: 2026-03-22*
