# 7. Syntax Analysis——Expressions and Precedence

## 7.1 Syntax Analyzer's Task

Syntax analysis (Parsing) is the compiler's second phase. Its tasks:
- Receive token stream
- Validate syntax structure
- Build intermediate representation (syntax tree, AST)

```
Token stream: [INT] [IDENT:x] [ASSIGN] [NUM:42] [SEMICOLON]
                    ↓
Syntax tree:
    =
   / \
  x   42
```

## 7.2 Precedence Climbing Parser

c4 uses "Precedence Climbing" method to parse expressions. This method is suitable for parsing C's binary operators.

Core idea:
- Each operator has two precedences: enter and exit
- Recursive descent: parse left side first, then decide whether to continue based on precedence

```c
void expr(int lev) {
    // 1. Handle unary operators (prefix)
    // 2. Parse atomic expression (number, identifier, parenthesis)
    // 3. Handle binary operators according to precedence
    
    while (tk >= lev) {
        if (tk == '+') { next(); expr(Mul); *++e = ADD; }
        if (tk == '-') { next(); expr(Mul); *++e = SUB; }
        // ...
    }
}
```

## 7.3 Operator Precedence Table

C operator precedence (high to low):

| Precedence | Operators | Associativity |
|-----------|-----------|---------------|
| 15 | () [] -> | Left to right |
| 14 | ! ~ ++ -- - * & sizeof | Right to left |
| 13 | * / % | Left to right |
| 12 | + - | Left to right |
| 11 | << >> | Left to right |
| 10 | < <= > >= | Left to right |
| 9 | == != | Left to right |
| 8 | & | Left to right |
| 7 | ^ | Left to right |
| 6 | \| | Left to right |
| 5 | && | Left to right |
| 4 | \|\| | Left to right |
| 3 | ?: | Right to left |
| 2 | = += -= etc | Right to left |
| 1 | , | Left to right |

c4 precedence values:
```c
// Assign is lowest
// Cond (?:) 
// Lor (||)
// Lan (&&)
// Or (|)
// Xor (^)
// And (&)
// Eq, Ne (=, !=)
// Lt, Gt, Le, Ge (<, >, <=, >=)
// Shl, Shr (<<, >>)
// Add, Sub (+, -)
// Mul, Div, Mod (*, /, %)
// Inc, Dec (++, --)
```

## 7.4 Atomic Expressions

### 7.4.1 Numeric Constants

```c
if (tk == Num) { 
    *++e = IMM;      // emit IMM instruction
    *++e = ival;    // emit immediate value
    next(); 
    ty = INT;        // type is int
}
```

### 7.4.2 String Constants

```c
else if (tk == '"') {
    *++e = IMM;
    *++e = ival;      // ival is string's data segment address
    next();
    while (tk == '"') next();  // handle consecutive strings
    data = (char *)((int)data + sizeof(int) & -sizeof(int));
    ty = PTR;         // type is pointer
}
```

### 7.4.3 sizeof

```c
else if (tk == Sizeof) {
    next(); 
    if (tk == '(') next(); 
    ty = INT; 
    if (tk == Int) next(); 
    else if (tk == Char) { next(); ty = CHAR; }
    while (tk == Mul) { next(); ty = ty + PTR; }  // pointer levels
    if (tk == ')') next();
    *++e = IMM; 
    *++e = (ty == CHAR) ? sizeof(char) : sizeof(int);
    ty = INT;
}
```

### 7.4.4 Identifiers

Identifiers can be:
- Variable reference
- Function call
- Constant (defined in symbol table)

```c
else if (tk == Id) {
    d = id;  // remember identifier
    next();
    
    if (tk == '(') {  // function call
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
        ty = d[Type];
    }
    else {  // variable reference
        if (d[Class] == Loc) { 
            *++e = LEA; *++e = loc - d[Val];  // local variable address
        }
        else if (d[Class] == Glo) { 
            *++e = IMM; *++e = d[Val];  // global address
        }
        *++e = (ty = d[Type]) == CHAR ? LC : LI;  // load value
    }
}
```

## 7.5 Unary Operators

### 7.5.1 Address-of `&`

```c
else if (tk == And) {
    next(); 
    expr(Inc);
    if (*e == LC || *e == LI) --e;  // remove load instruction
    else { printf("%d: bad address-of\n", line); exit(-1); }
    ty = ty + PTR;  // type becomes pointer
}
```

### 7.5.2 Dereference `*`

```c
else if (tk == Mul) {
    next(); 
    expr(Inc);
    if (ty > INT) ty = ty - PTR;  // remove one level of pointer
    else { printf("%d: bad dereference\n", line); exit(-1); }
    *++e = (ty == CHAR) ? LC : LI;
}
```

### 7.5.3 Logical NOT `!` and Bitwise NOT `~`

```c
else if (tk == '!') { 
    next(); 
    expr(Inc); 
    *++e = PSH; 
    *++e = IMM; 
    *++e = 0; 
    *++e = EQ; 
    ty = INT; 
}

else if (tk == '~') { 
    next(); 
    expr(Inc); 
    *++e = PSH; 
    *++e = IMM; 
    *++e = -1; 
    *++e = XOR; 
    ty = INT; 
}
```

### 7.5.4 Plus/Minus

```c
else if (tk == Sub) {
    next(); 
    *++e = IMM;
    if (tk == Num) { 
        *++e = -ival;  // negative immediate optimization
        next(); 
    } else { 
        *++e = -1; 
        *++e = PSH; 
        expr(Inc); 
        *++e = MUL; 
    }
    ty = INT;
}
```

## 7.6 Binary Operators

Binary operator parsing in the loop:

```c
while (tk >= lev) {
    if (tk == Assign) {
        next();
        if (*e == LC || *e == LI) 
            *e = PSH;  // preserve pointer
        else { printf("%d: bad lvalue in assignment\n", line); exit(-1); }
        expr(Assign); 
        *++e = (ty = t) == CHAR ? SC : SI;
    }
    else if (tk == Lor) { 
        next(); *++e = BNZ; d = ++e; 
        expr(Lan); *d = (int)(e + 1); ty = INT; 
    }
    else if (tk == Lan) { 
        next(); *++e = BZ; d = ++e; 
        expr(Or); *d = (int)(e + 1); ty = INT; 
    }
    else if (tk == Or) { 
        next(); *++e = PSH; expr(Xor); *++e = OR; ty = INT; 
    }
    // ... other operators
}
```

## 7.7 Precedence Parsing Example

Parsing `2 + 3 * 4`:

```
expr(Assign)
  tk = '+', lev = Assign
  tk != Assign, enter while
  tk = '+', continue
  tk = Num (2), handle
  exit while (tk < '+')

Back to upper level
  tk = '+'
  while (tk >= Add)
    next()
    expr(Mul)
      tk = Num (3), handle
      tk = '*', continue
      next()
      expr(Inc)
        tk = Num (4), handle
        exit
      emit MUL
    exit
    emit ADD
```

Generated instructions:
```
IMM 2
IMM 3
IMM 4
MUL
ADD
```

## 7.8 Pointer Arithmetic

Pointer `+` and `-` need special handling:

```c
else if (tk == Add) {
    next(); *++e = PSH; expr(Mul);
    if ((ty = t) > PTR) { 
        *++e = PSH; *++e = IMM; *++e = sizeof(int); 
        *++e = MUL;  // pointer + n = pointer + n * sizeof(type)
    }
    *++e = ADD;
}

else if (tk == Sub) {
    next(); *++e = PSH; expr(Mul);
    if (t > PTR && t == ty) { 
        *++e = SUB; 
        *++e = PSH; *++e = IMM; *++e = sizeof(int); 
        *++e = DIV; 
        ty = INT;  // ptr - ptr = element count
    }
    else if ((ty = t) > PTR) { 
        *++e = PSH; *++e = IMM; *++e = sizeof(int); 
        *++e = MUL; *++e = SUB; 
    }
    else *++e = SUB;
}
```

## 7.9 Parenthesized Expressions

Parentheses change precedence, also syntax for type casting:

```c
else if (tk == '(') {
    next();
    if (tk == Int || tk == Char) {  // type cast
        t = (tk == Int) ? INT : CHAR; 
        next();
        while (tk == Mul) { next(); t = t + PTR; }
        if (tk == ')') next();
        expr(Inc);
        ty = t;  // new type
    }
    else {
        expr(Assign);  // expression in parentheses
        if (tk == ')') next();
    }
}
```

## 7.10 Summary

In this chapter we learned:
- Precedence climbing parsing method
- Atomic expression handling (number, string, sizeof, identifier)
- Unary operators (&, *, !, ~, +, -)
- Binary operator parsing loop
- Pointer arithmetic handling
- Parentheses and type casting

## 7.11 Exercises

1. Trace parsing of `a = b = 5`
2. Trace parsing of `*p++` (note precedence)
3. Add ternary operator `?:` support to c4
4. Research how to implement short-circuit evaluation for `&&` and `||`
5. Compare precedence climbing vs recursive descent parser pros/cons
