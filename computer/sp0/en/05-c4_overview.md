# 5. c4: A C Compiler in Four Functions

## 5.1 The World's Smallest C Compiler

Robert Swierczek wrote an amazing C compiler - c4. The entire compiler is only 528 lines of C code, yet it can:
- Compile a subset of C language
- **Self-compile** (compile c4.c with c4)
- Generate its own virtual machine bytecode

Source code at: [_code/c4/c4.c](../_code/c4/c4.c)

## 5.2 Features Supported by c4

### Supported:
- **Data types**: `char`, `int`, pointers
- **Control structures**: `if/else`, `while`, `return`
- **Operators**: arithmetic, logic, bitwise, comparison
- **Function calls**: system functions and custom functions
- **Global/local variables**

### Not supported:
- `struct`, `union`
- `float`, `double`
- Arrays (pointers instead)
- Preprocessor macros (`#include`, `#define`)
- Standard library (built-in some common functions)

## 5.3 The Four Core Functions

c4's core consists of four functions:

```c
void next()       // Lexer: read next token
void expr(int lev) // Expression parser: handle operator precedence
void stmt()        // Statement parser: handle control structures
int main()         // Main: file reading, symbol table, VM execution
```

The entire compile-interpret flow:
```
Source → next() (lexical analysis) 
       → stmt() + expr() (syntax/semantic analysis + code generation)
       → VM instructions 
       → VM execution in main()
```

## 5.4 Compile and Run c4

```bash
cd _code/c4

# Compile c4
gcc -o c4 c4.c

# View help
./c4

# Compile hello.c and run
./c4 hello.c

# View generated assembly (-s option)
./c4 -s hello.c
```

## 5.5 c4 VM Architecture

c4 has a built-in stack-based VM with these registers:

```c
int *pc, *sp, *bp, a, cycle;  // vm registers
```

- `pc`: program counter, points to next instruction
- `sp`: stack pointer, points to top of stack
- `bp`: base pointer, for accessing local variables
- `a`: accumulator, stores operation results

Memory regions:
```c
char *data;   // data segment pointer
int *e;       // code emission pointer
int *sym;     // symbol table pointer
int *sp;      // stack pointer
```

## 5.6 c4 Instruction Set

c4 has 31 instructions, divided into categories:

### Control flow:
```c
enum { LEA ,IMM ,JMP ,JSR ,BZ  ,BNZ ,ENT ,ADJ ,LEV ,... };
// LEA: Load Effective Address
// IMM: Load Immediate
// JMP: Jump
// JSR: Jump to SubRoutine
// BZ:  Branch if Zero
// BNZ: Branch if Not Zero
// ENT: Enter function
// ADJ: Adjust stack
// LEV: Leave function
```

### Memory access:
```c
LI  ,   // Load Integer
LC  ,   // Load Char
SI  ,   // Store Integer
SC  ,   // Store Char
PSH ,   // Push to stack
```

### Arithmetic/logic:
```c
OR  ,XOR ,AND ,EQ  ,NE  ,LT  ,GT  ,LE  ,GE  ,
SHL ,SHR ,ADD ,SUB ,MUL ,DIV ,MOD ,
```

### System calls:
```c
OPEN,READ,CLOS,PRTF,MALC,FREE,MSET,MCMP,EXIT
// PRTF: printf, MALC: malloc, EXIT: exit
```

## 5.7 The Miracle of Self-Compilation

The most amazing part: c4 can compile itself!

```bash
# Compile c4 with gcc
gcc -o c4 c4.c

# Compile c4.c with c4 (generates new VM instructions)
./c4 c4.c hello.c

# Now hello is a version compiled by c4 itself!
./hello
```

This self-compilation ability demonstrates the power of a small, self-contained compiler.

## 5.8 Code Structure Analysis

### 5.8.1 Lexer next()

`next()` function is responsible for:
1. Skip whitespace
2. Handle newlines (optionally print source and generated instructions)
3. Parse identifiers and keywords
4. Parse numeric/character/string constants
5. Handle operators and symbols

Core of lexical analysis is **hashing identifiers**:

```c
tk = tk * 147 + *p++;  // simple hash function
tk = (tk << 6) + (p - pp);  // add length
```

### 5.8.2 Expression Parser expr()

Uses **precedence climbing** (or Pratt parser) method:

```c
void expr(int lev) {
    // ... handle unary operators, prefix, atomic expressions ...
    
    while (tk >= lev) {  // handle binary operators by precedence
        if (tk == '+') { next(); expr(Mul); *++e = ADD; }
        if (tk == '-') { next(); expr(Mul); *++e = SUB; }
        // ...
    }
}
```

### 5.8.3 Statement Parser stmt()

Handles control structures:

```c
void stmt() {
    if (tk == If) {
        // if (condition) statement [else statement]
        expr(Assign);
        *++e = BZ; b = ++e;  // emit conditional jump
        stmt();
        if (tk == Else) {
            *b = (int)(e + 3);
            *++e = JMP; b = ++e;
            next();
            stmt();
        }
        *b = (int)(e + 1);
    }
    else if (tk == While) {
        // while (condition) statement
        a = e + 1;
        expr(Assign);
        *++e = BZ; b = ++e;
        stmt();
        *++e = JMP; *++e = (int)a;
        *b = (int)(e + 1);
    }
    // ...
}
```

## 5.9 From C to VM Instruction Translation

Let's trace compilation of a simple program:

```c
int main() {
    return 2 + 3;
}
```

Generated instructions:
```
IMM 2        ; load immediate 2
PSH          ; push to stack
IMM 3        ; load immediate 3
ADD          ; pop two values and add
LEV          ; return
```

Execution flow:
```
Stack: []          ; initial empty stack
IMM 2 → Stack: [2]
PSH  → Stack: []
ADD  → Stack: [5]  ; 2+3=5
LEV  → return 5
```

## 5.10 Summary

In this chapter we:
- Met the world's smallest C compiler c4
- Understood the four core functions
- Learned c4's VM architecture and instruction set
- Witnessed the miracle of self-compilation

## 5.11 Exercises

1. Download and compile c4, try running hello.c
2. Use `c4 -s hello.c` to view generated instructions
3. Try adding a small feature to c4.c (like ++, -- operators)
4. Research how c4 handles recursive function calls
5. Trace compilation of a complex expression
