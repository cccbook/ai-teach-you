# 15. py0 Compiler——Python to qd0 Bytecode

## 15.1 Why DIY Python Compiler?

Python is a dynamic language, usually executed via interpreter. But Python code can also be compiled to bytecode for better performance.

```
Python (.py)  →  Bytecode (.pyc)  →  Interpreter execution
                  or
                Compile to IR  →  Machine code
```

## 15.2 py0 Compiler Architecture

py0 compiles Python subset to qd0 (custom VM) bytecode.

Location: [_code/cpy0/py0/](../_code/cpy0/py0/)

## 15.3 Supported Python Syntax

py0 supports subset of Python:
- Basic types: int, float, str, bool
- Variable declaration and assignment
- Arithmetic and comparison operators
- if/else conditionals
- while loops
- Function definition and calls
- print function
- Basic built-in functions

**Not supported**: classes, exceptions, import, list comprehensions, etc.

## 15.4 qd0 Bytecode

qd0 is a simple stack-based VM bytecode.

### 15.4.1 Instruction Set

| Instruction | Description | Stack change |
|-------------|-------------|-------------|
| LOAD_CONST | Load constant | → value |
| LOAD_FAST | Load local variable | → value |
| STORE_FAST | Store local variable | value → |
| LOAD_GLOBAL | Load global variable | → value |
| BINARY_OP | Binary operation | a, b → result |
| COMPARE_OP | Comparison | a, b → result |
| POP_JUMP_IF_FALSE | Conditional jump | value → |
| JUMP_ABSOLUTE | Unconditional jump | |
| CALL_FUNCTION | Function call | args → result |
| RETURN_VALUE | Return value | value → |
| MAKE_FUNCTION | Create function | code → func |
| PRINT | Print | value → |

### 15.4.2 Bytecode Format

```
+------------------+
| Header           |  Magic + version
+------------------+
| Constants Pool   |  Constants table
+------------------+
| Names Pool       |  Names table
+------------------+
| Functions Pool   |  Functions table
+------------------+
| Code Object      |
|  - instructions  |
|  - locals        |
|  - stack size    |
+------------------+
```

## 15.5 py0 Compiler Implementation

### 15.5.1 Lexer

```c
// token types
enum {
    tok_int = 256, tok_float, tok_string, tok_ident,
    tok_def, tok_if, tok_else, tok_while, tok_return,
    tok_and, tok_or, tok_not,
    // ...
};

// lexical analysis
void next_token() {
    skip_whitespace();
    if (isdigit(c)) return scan_number();
    if (isalpha(c) || c == '_') return scan_ident();
    // ...
}
```

### 15.5.2 Parser

Uses recursive descent parser:

```c
// parse program
AST *parse_program() {
    AST *ast = new_node(AST_PROGRAM);
    while (tok != tok_eof) {
        if (tok == tok_def) {
            add_child(ast, parse_function());
        } else {
            add_child(ast, parse_statement());
        }
    }
    return ast;
}

// parse function definition
AST *parse_function() {
    expect(tok_def);
    char *name = ident;
    expect(tok_ident);
    expect('(');
    // parse parameters...
    expect(')');
    expect(':');
    AST *body = parse_block();
    return new_function_node(name, params, body);
}

// parse expression
AST *parse_expr(int precedence) {
    AST *left = parse_atom();
    while (is_binary_op(tok) && precedence_of(tok) >= precedence) {
        OpType op = tok;
        next_token();
        AST *right = parse_expr(precedence_of(op) + 1);
        left = new_binary_node(op, left, right);
    }
    return left;
}
```

### 15.5.3 Code Generator

Translate AST to qd0 bytecode:

```c
void gen_code(AST *node) {
    switch (node->type) {
        case AST_INT:
            emit(LOAD_CONST);
            emit_const_index(node->value);
            break;
            
        case AST_IDENT:
            emit(LOAD_FAST);
            emit_var_index(node->name);
            break;
            
        case AST_ASSIGN:
            gen_code(node->right);
            emit(STORE_FAST);
            emit_var_index(node->left->name);
            break;
            
        case AST_BINOP:
            gen_code(node->left);
            emit(PSH);
            gen_code(node->right);
            emit(BINARY_OP);
            emit_op_code(node->op);
            break;
            
        case AST_IF:
            gen_code(node->cond);
            emit(POP_JUMP_IF_FALSE);
            int else_patch = emit_placeholder();
            gen_code(node->then);
            if (node->else_part) {
                emit(JUMP_ABSOLUTE);
                int end_patch = emit_placeholder();
                patch(else_patch);
                gen_code(node->else_part);
                patch(end_patch);
            } else {
                patch(else_patch);
            }
            break;
            
        case AST_WHILE:
            int loop_start = get_code_pos();
            gen_code(node->cond);
            emit(POP_JUMP_IF_FALSE);
            int exit_patch = emit_placeholder();
            gen_code(node->body);
            emit(JUMP_ABSOLUTE);
            emit_jump_target(loop_start);
            patch(exit_patch);
            break;
            
        case AST_CALL:
            for (int i = 0; i < node->args->count; i++) {
                gen_code(node->args->items[i]);
            }
            emit(CALL_FUNCTION);
            emit_int(node->args->count);
            break;
    }
}
```

## 15.6 Complete Example

### Input: test.py

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))
```

### Output: test.qd

```qd
; Constants
0
1
10
"fib"
"%d\n"

; Functions
function fib:
    instructions:
        LOAD_FAST 0           ; n
        LOAD_CONST 0         ; 0
        COMPARE_OP <=        ; n <= 1
        POP_JUMP_IF_FALSE L1 ; if not (n <= 1) goto L1
        LOAD_FAST 0           ; return n
        RETURN_VALUE
    L1:
        LOAD_FAST 0           ; n
        LOAD_CONST 0         ; 1
        BINARY_OP -          ; n - 1
        CALL_FUNCTION fib, 1  ; fib(n-1)
        LOAD_FAST 0           ; n
        LOAD_CONST 0         ; 1
        BINARY_OP -          ; n - 1
        CALL_FUNCTION fib, 1  ; fib(n-2)
        BINARY_OP +          ; fib(n-1) + fib(n-2)
        RETURN_VALUE

; Main
LOAD_CONST 2         ; 10
CALL_FUNCTION fib, 1 ; fib(10)
PRINT               ; print result
```

## 15.7 Using py0

```bash
# Basic usage
./py0/py0c/py0c test.py -o test.qd

# Or use Makefile
make test_py
```

## 15.8 py0c Architecture Diagram

```
+-------------------+
|   Python Source   |
+-------------------+
         ↓
+-------------------+
|   Lexer (scanner) |
+-------------------+
         ↓
+-------------------+
|   Token Stream     |
+-------------------+
         ↓
+-------------------+
|   Parser           |
+-------------------+
         ↓
+-------------------+
|   AST              |
+-------------------+
         ↓
+-------------------+
|   Code Generator   |
+-------------------+
         ↓
+-------------------+
|   qd0 Bytecode    |
+-------------------+
```

## 15.9 Comparison with Standard Python Interpreter

| Feature | py0 | CPython |
|---------|-----|---------|
| Syntax coverage | Subset | Complete |
| Speed | Fast (compiled) | Slow (interpreted) |
| Bytecode | qd0 | bytecode |
| VM | qd0 | CPython VM |
| Debugging | Basic | Complete |
| Standard library | None | Complete |

## 15.10 Summary

In this chapter we learned:
- Python compiler basics
- py0 compiler architecture design
- qd0 bytecode format
- Lexical and syntax analysis
- AST to bytecode translation
- Complete example
- py0 vs CPython comparison

## 15.11 Exercises

1. Add `for` loop support to py0
2. Add `+` string concatenation support to py0
3. Research how to add simple class support
4. Compare py0 and MicroPython design differences
5. Implement a simple qd0 interpreter
