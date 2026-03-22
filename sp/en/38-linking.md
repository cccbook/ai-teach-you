# 38. Static Analysis——How Linker Resolves Symbols

## 38.1 Linker's Tasks

Main tasks of the linker:
1. **Symbol resolution**: Find symbol definitions
2. **Relocation**: Fix address references
3. **Symbol binding**: Determine final symbol addresses

## 38.2 Symbol Types

| Type | Description |
|------|-------------|
| Strong symbol | Function, initialized global variable |
| Weak symbol | Uninitialized, global variable |
| UND | Undefined (external reference) |

## 38.3 Symbol Resolution Rules

1. Multiple strong symbols → Link error
2. One strong symbol + multiple weak symbols → Choose strong symbol
3. Multiple weak symbols → Choose any one

## 38.4 Relocation

### 38.4.1 Relocation Entries

Object files contain relocation information telling the linker what needs to be fixed:

```bash
readelf -r hello.o
```

## 38.5 Common Problems

### 38.5.1 Undefined Symbol

```bash
# Link error
undefined reference to `foo'
```

Solution: Include the library or object file that defines `foo`.

### 38.5.2 Multiple Definition

```bash
# Link error
multiple definition of `x'
```

Solution: Use `static` or `__attribute__((weak))`.

## 38.6 Summary

In this chapter we learned:
- Linker's basic tasks
- Symbol resolution rules
- Relocation concepts
- Common linking problems

## 38.7 Exercises

1. Experiment with symbol priority rules
2. Use `nm` to analyze object files
3. Research use cases for weak symbols
