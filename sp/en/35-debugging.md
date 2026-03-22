# 35. Debugging Tools——GDB and LLDB

## 35.1 Why Debugging?

Compiled code lacks:
- Variable names
- Source code locations
- Function structure

Debuggers help us:
- Set breakpoints
- Step through code
- Inspect variables
- Analyze crashes

## 35.2 GDB Basic Usage

### 35.2.1 Compile for Debugging

```bash
gcc -g hello.c -o hello
```

### 35.2.2 Start

```bash
gdb ./hello
```

### 35.2.3 Common Commands

```bash
(gdb) run              # Execute
(gdb) break main       # Break at main
(gdb) break hello.c:10 # Break at line number
(gdb) continue          # Continue execution
(gdb) next             # Next line (don't enter functions)
(gdb) step             # Next line (enter functions)
(gdb) print x          # Print variable
(gdb) info locals      # Print all local variables
(gdb) info registers    # Print registers
(gdb) backtrace        # Show call stack
(gdb) quit             # Exit
```

## 35.3 Breakpoints

### 35.3.1 Set Breakpoints

```bash
(gdb) break foo        # Function name
(gdb) break *0x400544  # Address
(gdb) break hello.c:10 # Line number
```

### 35.3.2 Conditional Breakpoints

```bash
(gdb) break foo if x > 10
```

### 35.3.3 Watchpoints

```bash
(gdb) watch global_var      # Watch writes
(gdb) rwatch global_var    # Watch reads
(gdb) awatch global_var    # Watch reads/writes
```

## 35.4 Inspecting Data

### 35.4.1 Print Variables

```bash
(gdb) print x         # Decimal
(gdb) print /x x      # Hexadecimal
(gdb) print /d x      # Decimal
(gdb) print /t x      # Binary
```

### 35.4.2 Pointers and Arrays

```bash
(gdb) print *ptr      # Dereference
(gdb) print ptr[0]    # Array element
(gdb) print *ptr@len  # C-style array
```

### 35.4.3 Structures

```bash
(gdb) print struct_var.member
(gdb) print *struct_ptr->member
```

## 35.5 Call Stack

### 35.5.1 backtrace

```bash
(gdb) backtrace
#0  foo () at hello.c:5
#1  0x0000555555555149 in bar () at hello.c:10
#2  0x0000555555555156 in main () at hello.c:15
```

### 35.5.2 Switch Frames

```bash
(gdb) frame 1
(gdb) print x  # View variables in that frame
```

## 35.6 LLDB

### 35.6.1 Command Comparison

| GDB | LLDB |
|-----|------|
| run | process launch |
| break | breakpoint set |
| next | thread step-inst-over |
| step | thread step-inst |
| print | frame variable |
| bt | thread backtrace |
| info registers | register read |
| x | memory read |

### 35.6.2 LLDB Example

```bash
lldb ./hello
(lldb) breakpoint set --name main
(lldb) process launch
(lldb) frame variable
(lldb) thread step-over
(lldb) thread backtrace
```

## 35.7 Core Dumps

### 35.7.1 Generate Core Dump

```bash
# Linux
ulimit -c unlimited
./hello  # Crash
ls -l core*

# macOS
./hello  # Crash
# Core dump in /cores/
```

### 35.7.2 Analyze Core Dump

```bash
gdb ./hello core
(gdb) bt  # Show stack at crash time
```

## 35.8 Summary

In this chapter we learned:
- GDB basic usage
- Breakpoints and watchpoints
- Inspecting data
- Call stack
- LLDB commands
- Core dump analysis

## 35.9 Exercises

1. Debug a buggy program using GDB
2. Implement conditional breakpoints
3. Research GDB Python interface
4. Compare GDB and LLDB
5. Analyze a real core dump
