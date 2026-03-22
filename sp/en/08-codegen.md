# 8. Code Generation——From Syntax Tree to VM Instructions

## 8.1 Code Generator's Task

Code generation is the compiler phase that converts syntax analysis results to target program code. In c4, the target is the VM's bytecode.

```
Syntax analysis → AST/direct generation → VM instructions → VM execution
```

c4 uses "semantic-directed translation": code is emitted directly during syntax analysis, no explicit syntax tree needed.

## 8.2 c4's Code Emission

c4 uses a global pointer `e` to emit code:

```c
int *e;  // current position in emitted code

// Emit one instruction
*++e = opcode;    // increment pointer first, then store value
```

Emitted memory layout:
```
Memory: [opcode][operand][opcode][operand]...
         ↑
         e points to current position
```

## 8.3 Backpatching

Many instructions need jump target addresses, but the target isn't known when the jump is emitted. c4 uses "backpatching" technique:

```c
// Emit conditional jump
*++e = BNZ;  // Branch if Not Zero
d = ++e;     // remember patch position, d points to target to fill

// ... emit instructions after jump ...

// Patch: fill in target address
*d = (int)(e + 1);  // calculate and fill target
```

## 8.4 Expression Code Generation

### 8.4.1 Immediate Values

```c
if (tk == Num) { 
    *++e = IMM;    // load immediate instruction
    *++e = ival;   // immediate value
    next(); 
}
```

Generated instructions:
```
IMM 42     ; load immediate 42
```

### 8.4.2 Variable Loading

```c
if (d[Class] == Loc) { 
    *++e = LEA; *++e = loc - d[Val];  // local address
}
else if (d[Class] == Glo) { 
    *++e = IMM; *++e = d[Val];  // global address
}
*++e = (ty = d[Type]) == CHAR ? LC : LI;  // load value
```

Generated instructions:
```
LEA -8     ; load local variable address (relative to bp)
LI         ; load integer value
```

### 8.4.3 Addition

```c
else if (tk == Add) {
    next(); *++e = PSH;    // save left operand
    expr(Mul);
    *++e = ADD;            // pop and add
}
```

Generated instructions (for `a + b`):
```
... a's code ...
PSH         ; push to stack
... b's code ...
ADD         ; pop two values and add
```

Execution:
```
Initial: [a]           ; a in accumulator
PSH: [] [a]          ; Stack: [a], Accumulator: a
b: [b]               ; Accumulator: b
ADD: [a+b]           ; Stack: [], Accumulator: a+b
```

### 8.4.4 Assignment

```c
if (tk == Assign) {
    next();
    if (*e == LC || *e == LI) 
        *e = PSH;  // preserve load instruction, become save pointer
    else { printf("bad lvalue\n"); exit(-1); }
    expr(Assign);   // right side value
    *++e = SC;       // store to pointer
}
```

Generated instructions (for `x = 5`):
```
LEA -8     ; x's address
PSH        ; save address
IMM 5      ; load 5
SC         ; store
```

## 8.5 Function Call Code Generation

### 8.5.1 Function Call

```c
if (tk == '(') {
    next();
    t = 0;
    while (tk != ')') { 
        expr(Assign); 
        *++e = PSH;  // argument on stack
        ++t; 
        if (tk == ',') next(); 
    }
    next();
    if (d[Class] == Sys) 
        *++e = d[Val];  // system call
    else if (d[Class] == Fun) { 
        *++e = JSR; 
        *++e = d[Val];  // jump to function
    }
    if (t) { *++e = ADJ; *++e = t; }  // cleanup arguments
}
```

Generated instructions (for `printf("Hello")`):
```
IMM addr_of_string  ; string pointer
PSH                 ; push argument
PRTF                ; call printf
ADJ 1               ; cleanup 1 argument
```

### 8.5.2 Function Entry and Exit

Function entry (ENT):
```c
*++e = ENT; 
*++e = i - loc;  // stack frame size
```

Equivalent to:
```
push bp
bp = sp
sp = sp - frame_size
```

Function exit (LEV):
```c
*++e = LEV;
```

Equivalent to:
```
sp = bp
pop bp
pc = *sp; sp++
```

## 8.6 Control Structure Code Generation

### 8.6.1 if-else

```c
if (tk == If) {
    next();
    expr(Assign);          // condition
    *++e = BZ; b = ++e;     // emit conditional jump, remember patch position
    stmt();                // then statement
    
    if (tk == Else) {
        *b = (int)(e + 3);  // patch: skip else block
        *++e = JMP; b = ++e;
        next();
        stmt();            // else statement
    }
    *b = (int)(e + 1);     // patch: skip then or else block
}
```

Generated instructions:
```
... condition code ...
BZ .L1           ; if condition false, goto else
... then block ...
JMP .L2          ; skip else block
.L1:
... else block ...
.L2:
```

### 8.6.2 while

```c
if (tk == While) {
    next();
    a = e + 1;             ; remember loop start position
    expr(Assign);          // condition
    *++e = BZ; b = ++e;    // emit exit jump
    stmt();                ; loop body
    *++e = JMP; *++e = (int)a;  ; jump back to loop start
    *b = (int)(e + 1);     ; patch: exit target
}
```

Generated instructions:
```
.L0:              ; loop start
... condition code ...
BZ .L1            ; if condition false, exit
... loop body ...
JMP .L0           ; jump back to loop start
.L1:              ; loop exit
```

### 8.6.3 return

```c
if (tk == Return) {
    next();
    if (tk != ';') expr(Assign);
    *++e = LEV;            // emit exit instruction
    if (tk == ';') next();
}
```

## 8.7 Complete Example

Source:
```c
int main() {
    int a;
    a = 10;
    if (a > 5) {
        return a - 3;
    }
    return 0;
}
```

Generated VM instructions:
```
ENT  3            ; enter main, 3 local spaces
LEA  -4            ; a's address
PSH  
IMM  10            ; load 10
SC               ; a = 10
IMM  -4           ; a's address
LI               ; load a
PSH  
IMM  5            ; load 5
GT               ; a > 5
BZ  .L1           ; condition false, goto .L1
IMM  -4           ; a's address
LI               ; load a
PSH  
IMM  3            ; load 3
SUB               ; a - 3
LEV               ; return
JMP  .L2          ; jump to function end
.L1:
IMM  0            ; load 0
LEV               ; return 0
.L2:
```

## 8.8 Code Generation Strategy Comparison

### 8.8.1 c4's Strategy: Semantic-Directed Translation

Pros:
- Simple and direct
- No need to build syntax tree
- Memory efficient

Cons:
- Hard to optimize
- Complex error handling

### 8.8.2 Modern Compiler Strategy

1. **Syntax tree → Intermediate Representation (IR)**
2. **Optimization**
3. **Target code generation**

```
Source → Token → AST → IR → Optimized IR → Target code
              ↑                      ↑
           Parser              Code Gen
```

## 8.9 Summary

In this chapter we learned:
- Code generation basics
- c4's instruction emission mechanism
- Backpatching technique
- Expression, assignment, function call code generation
- if-else, while, return code generation
- Complete example instruction sequence

## 8.10 Exercises

1. Manually trace code generation for `a = (b + c) * d`
2. Add `for` loop support to c4
3. Add `do-while` loop support to c4
4. Research how modern compilers implement dead code elimination
5. Implement simple constant folding optimization
