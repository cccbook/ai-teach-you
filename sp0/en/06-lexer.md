# 6. Lexical Analysis——Converting Source Code to Tokens

## 6.1 Lexer's Task

Lexical analysis (Scanning) is the compiler's first phase. Its tasks:
- Read source code characters
- Group characters into meaningful units (Tokens)
- Skip whitespace and comments
- Report lexical errors

```
Source: "int x = 42;"
         ↓
Token stream: [INT] [IDENT:x] [ASSIGN] [NUM:42] [SEMICOLON]
```

## 6.2 Token Structure

```c
enum TokenType {
    // Terminals
    NUM = 128,    // numeric constant
    IDENT,        // identifier
    STRING,       // string constant
    
    // Keywords
    INT, CHAR, IF, ELSE, WHILE, RETURN, SIZEOF,
    
    // Operators
    ASSIGN,       // =
    PLUS, MINUS,  // + -
    MUL, DIV,     // * /
    EQ, NE, LT, GT, LE, GE,  // == != < > <= >=
    AND, OR, NOT, // && || !
    // ...
};
```

c4's Token definitions:
```c
enum {
  Num = 128, Fun, Sys, Glo, Loc, Id,
  Char, Else, Enum, If, Int, Return, Sizeof, While,
  Assign, Cond, Lor, Lan, Or, Xor, And, Eq, Ne, Lt, Gt, Le, Ge, Shl, Shr, Add, Sub, Mul, Div, Mod, Inc, Dec, Brak
};
```

## 6.3 c4's next() Function Structure

```c
void next() {
    char *pp;
    
    while (tk = *p) {  // read next character
        ++p;
        
        if (tk == '\n') {
            // handle newline
        }
        else if (tk == '#') {
            // handle preprocessor (skip)
        }
        else if (isalpha(tk) || tk == '_') {
            // identifier or keyword
        }
        else if (isdigit(tk)) {
            // numeric constant
        }
        else if (tk == '/') {
            // division or comment
        }
        else if (tk == '\'' || tk == '"') {
            // character or string constant
        }
        else if (tk is operator) {
            // handle operators
        }
        // ...
    }
}
```

## 6.4 Identifier Parsing

Identifiers are sequences starting with letters, containing letters, digits, underscores:

```c
else if ((tk >= 'a' && tk <= 'z') || 
         (tk >= 'A' && tk <= 'Z') || 
         tk == '_') {
    pp = p - 1;  // remember start position
    
    // read remaining characters
    while ((*p >= 'a' && *p <= 'z') || 
           (*p >= 'A' && *p <= 'Z') || 
           (*p >= '0' && *p <= '9') || 
           *p == '_')
        tk = tk * 147 + *p++;
    
    tk = (tk << 6) + (p - pp);  // hash = hash << 6 + length
    
    // look up in symbol table
    id = sym;
    while (id[Tk]) {
        if (tk == id[Hash] && !memcmp((char *)id[Name], pp, p - pp)) {
            tk = id[Tk];  // found, it's a keyword or declared identifier
            return;
        }
        id = id + Idsz;
    }
    
    // new identifier
    id[Name] = (int)pp;
    id[Hash] = tk;
    tk = id[Tk] = Id;  // default to Id
    return;
}
```

## 6.5 Numeric Constant Parsing

c4 supports decimal, hex, octal:

```c
else if (tk >= '0' && tk <= '9') {
    if (ival = tk - '0') { 
        // decimal
        while (*p >= '0' && *p <= '9') 
            ival = ival * 10 + *p++ - '0';
    }
    else if (*p == 'x' || *p == 'X') {
        // hexadecimal
        while ((tk = *++p) && 
               ((tk >= '0' && tk <= '9') || 
                (tk >= 'a' && tk <= 'f') || 
                (tk >= 'A' && tk <= 'F')))
            ival = ival * 16 + (tk & 15) + (tk >= 'A' ? 9 : 0);
    }
    else { 
        // octal
        while (*p >= '0' && *p <= '7') 
            ival = ival * 8 + *p++ - '0';
    }
    tk = Num;
    return;
}
```

## 6.6 Character and String Constants

```c
else if (tk == '\'' || tk == '"') {
    pp = data;  // remember data segment position
    while (*p != 0 && *p != tk) {  // read until end
        if ((ival = *p++) == '\\') {  // handle escape
            if ((ival = *p++) == 'n') ival = '\n';
        }
        if (tk == '"') *data++ = ival;  // string goes to data segment
    }
    ++p;  // skip closing quote
    if (tk == '"') 
        ival = (int)pp;  // string: ival is pointer
    else 
        tk = Num;  // character: ival is ASCII value
    return;
}
```

## 6.7 Operator Handling

### Single character operators:
```c
else if (tk == '*') { tk = Mul; return; }
else if (tk == '+') { tk = Add; return; }
else if (tk == '-') { tk = Sub; return; }
else if (tk == '/') { tk = Div; return; }
```

### Multi-character operators:
```c
else if (tk == '=') { 
    if (*p == '=') { ++p; tk = Eq; }  // ==
    else tk = Assign;                  // =
    return; 
}

else if (tk == '!') { 
    if (*p == '=') { ++p; tk = Ne; }  // !=
    return; 
}

else if (tk == '<') { 
    if (*p == '=') { ++p; tk = Le; }      // <=
    else if (*p == '<') { ++p; tk = Shl; }  // <<
    else tk = Lt;                          // <
    return; 
}

else if (tk == '>') { 
    if (*p == '=') { ++p; tk = Ge; }      // >=
    else if (*p == '>') { ++p; tk = Shr; }  // >>
    else tk = Gt;                          // >
    return; 
}
```

## 6.8 Skipping Comments

C99 supports `//` single-line comments:
```c
else if (tk == '/') {
    if (*p == '/') {
        ++p;
        while (*p != 0 && *p != '\n') ++p;  // skip to line end
    }
    else {
        tk = Div;  // it's division
        return;
    }
}
```

## 6.9 Skipping Whitespace

c4's design is clever: whitespace falls through the loop start, `continue` is implicit in the loop logic:

```c
while (tk = *p) {  // if whitespace, tk = ' ', loop body will enter
    ++p;
    if (tk == '\n') { ... }
    // ... other handling
    // whitespace won't trigger any if, goes to next loop iteration
}
```

## 6.10 Lexer Example

Input: `int x = 42;`
Token stream:

| Position | Lexeme | Token |
|----------|--------|-------|
| 1-3 | int | INT |
| 4 | (blank) | (skip) |
| 5 | x | IDENT (hash) |
| 6 | (blank) | (skip) |
| 7 | = | Assign |
| 8 | (blank) | (skip) |
| 9-10 | 42 | Num (val=42) |
| 11 | ; | ; |

## 6.11 Symbol Table Structure

c4's symbol table is a simple static array:

```c
int *sym;  // symbol table

enum { Tk, Hash, Name, Class, Type, Val, HClass, HType, HVal, Idsz };
// Idsz = 10, each identifier occupies 10 ints
```

Each identifier's structure:
```c
id[Tk]     // Token type (keyword or Id)
id[Hash]   // hash value
id[Name]   // name string pointer
id[Class]  // class (Glo, Loc, Fun, Sys)
id[Type]   // type (INT, CHAR, PTR+n)
id[Val]    // value (variable address or function offset)
id[HClass] // saved class (for nested scope)
id[HType]  // saved type
id[HVal]   // saved value
```

## 6.12 Keyword Initialization

Before parsing starts, keywords are added to symbol table:

```c
p = "char else enum if int return sizeof while ";
i = Char; 
while (i <= While) { 
    next(); 
    id[Tk] = i++;  // "char" -> Tk=Char, "else" -> Tk=Else, ...
}

// built-in functions
i = OPEN; 
while (i <= EXIT) { 
    next(); 
    id[Class] = Sys; 
    id[Type] = INT; 
    id[Val] = i++; 
}
```

## 6.13 Summary

In this chapter we learned:
- Lexer's task: convert character stream to token stream
- c4's token types and representation
- Identifier parsing (hash table lookup)
- Numeric constant parsing (dec/hex/oct)
- String and character handling
- Operator recognition (single, double characters)
- c4's symbol table structure

## 6.14 Exercises

1. Use c4 -s to compile hello.c and observe the token stream
2. Add `break` keyword support to c4
3. Research how to add `float` type support
4. Implement a simple lexer (can use flex or hand-written)
5. Compare hand-written lexer vs lex/flex
