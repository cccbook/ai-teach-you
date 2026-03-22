# 2. Memory Model——Stack, Heap, and Static Memory

## 2.1 Memory When a Program Executes

When a C program runs, the OS allocates a block of virtual memory. This memory is divided into different regions, each with different purposes.

```
+------------------+ High address
|   Kernel Space   |  (Kernel space) - OS reserved
+------------------+
|      Stack        |  (Stack) - grows downward
|       ↓          |
|                  |
|     Unused        |
|                  |
|       ↑          |
|      Heap         |  (Heap) - grows upward
+------------------+
|      BSS         |  (Block Started by Symbol) - uninitialized globals
+------------------+
|      Data         |  (Data) - initialized globals
+------------------+
|      Text         |  (Text) - program code
+------------------+ 0x400000 (Low address)
```

## 2.2 Memory Region Details

### 2.2.1 Text Segment (Code Region)

Stores program execution instructions.

Features:
- **Read-only** - prevents program from accidentally modifying its own code
- **Executable** - CPU can execute instructions in this memory
- **Shareable** - multiple instances of the same program can share the same code

```c
int add(int a, int b) {
    return a + b;
}
// The machine code for add is stored in Text segment
```

### 2.2.2 Data Segment (Initialized Global/Static Variables)

Stores initialized globals and static variables.

```c
int initialized_global = 42;      // Data segment
const char *name = "Alice";       // Data segment (pointer itself)

static int count = 100;           // Data segment

int main() {
    static int counter = 0;       // Data segment (static in function)
    return 0;
}
```

### 2.2.3 BSS Segment (Uninitialized Global/Static Variables)

"Block Started by Symbol" - stores uninitialized or zero-initialized globals.

```c
int uninitialized_global;         // BSS segment (automatically set to 0)
int zero_global = 0;              // BSS segment (optimized to uninitialized)

static int uninitialized_static;   // BSS segment

int main() {
    static int static_local;      // BSS segment
    return 0;
}
```

Why separate Data and BSS? **Saves disk space**. BSS doesn't need to store actual data, only the size, and the OS initializes it to zero at runtime.

### 2.2.4 Heap Segment

Dynamic memory allocation region, managed by `malloc`/`free` during execution.

```c
#include <stdlib.h>

int main() {
    // Allocate 100 ints
    int *arr = (int *)malloc(100 * sizeof(int));
    
    if (arr == NULL) {
        return 1;  // Allocation failed
    }
    
    arr[0] = 42;   // Use allocated memory
    free(arr);     // Free memory
    
    return 0;
}
```

Features:
- **Manual management** - programmer responsible for allocation/deallocation
- **Grows upward** - new allocations move heap top upward
- **Flexible size** - size can be determined at runtime

### 2.2.5 Stack Segment

Stores function call information and local variables.

```c
void function_c() {
    int c = 3;      // Stack Frame C
}

void function_b() {
    int b = 2;      // Stack Frame B
    function_c();
}

void function_a() {
    int a = 1;      // Stack Frame A
    function_b();
}

int main() {
    function_a();
    return 0;
}
```

Call order: `main` → `function_a` → `function_b` → `function_c`

Stack layout (high to low):
```
+------------------+ High address
|   function_c     |  ← currently here
+------------------+
|   function_b     |
+------------------+
|   function_a     |
+------------------+
|      main        |
+------------------+ Low address
```

## 2.3 Stack Frame

Each function call creates a "stack frame" containing:
- Return address (where to continue after function returns)
- Old base pointer
- Function parameters
- Local variables

x86-64 stack frame:
```
+------------------+  rbp (base pointer)
|   Old RBP        |
+------------------+
|   Return Address  |
+------------------+  rsp (stack pointer)
|   Param 3         |
+------------------+
|   Param 2         |
+------------------+
|   Param 1         |
+------------------+
|   Return Address  |
+------------------+
|   Old RBP        |
+------------------+ ← rbp
|   Local Var 1    |
+------------------+
|   Local Var 2    |
+------------------+ ← rsp
```

## 2.4 Heap vs Stack

| Feature | Stack | Heap |
|---------|-------|------|
| Allocation | Automatic (on function entry) | Manual (malloc/free) |
| Deallocation | Automatic (on function exit) | Manual (free) |
| Size | Small (default 8MB) | Large (limited by system) |
| Speed | Fast | Slow |
| Fragmentation | No | Possible |
| Allocation failure | Usually no | Possible (OOM) |
| Lifetime | Function scope | Until freed |

## 2.5 Common Memory Errors

### 2.5.1 Memory Leak

Allocated memory but forgot to free:

```c
void leak() {
    int *ptr = (int *)malloc(sizeof(int));
    *ptr = 42;
    // Forgot free(ptr)!
    // Every call to leak() leaks sizeof(int) bytes
}
```

### 2.5.2 Double Free

```c
void double_free() {
    int *ptr = (int *)malloc(sizeof(int));
    free(ptr);
    free(ptr);  // Error! ptr already freed
}
```

### 2.5.3 Use After Free

```c
void use_after_free() {
    int *ptr = (int *)malloc(sizeof(int));
    *ptr = 42;
    free(ptr);
    int x = *ptr;  // Error! ptr's memory was freed
}
```

### 2.5.4 Buffer Overflow

```c
void buffer_overflow() {
    char buffer[10];
    strcpy(buffer, "This is too long!");  // Overflow!
}
```

### 2.5.5 Stack Overflow

```c
void infinite_recursion() {
    int arr[1000000];  // Try to allocate huge array on stack
    infinite_recursion();  // Infinite recursion
}
```

## 2.6 View Memory with GDB

```bash
# Compile (with debug info)
gcc -g -o memory_demo memory_demo.c

# Start GDB
gdb ./memory_demo

# In GDB
(gdb) break main
(gdb) run
(gdb) info registers
(gdb) x/20x $sp      # View stack (hex)
(gdb) x/20x &global_var  # View global variable
(gdb) print &heap_var    # Print heap variable address
```

## 2.7 View Memory Layout with size

```bash
size ./a.out
```

Example output:
```
text    data     bss     dec     hex filename
1672     608       8    2288     8f0 a.out
```

- `text`: code size
- `data`: initialized globals
- `bss`: uninitialized globals
- `dec`: total (decimal)
- `hex`: total (hex)

## 2.8 Summary

In this chapter we learned:
- Program memory divided into: Text, Data, BSS, Heap, Stack
- Purpose and characteristics of each region
- Stack for function calls, heap for dynamic allocation
- Common memory error types

## 2.9 Exercises

1. Write a program and print addresses of different variables with `printf("%p\n", &var)`
2. Use `size` to compare segment sizes of different programs
3. Create a memory leak and detect it with Valgrind
4. Research your system's default stack size limit
