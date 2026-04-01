#ifndef SYMBOL_TABLE_H
#define SYMBOL_TABLE_H

#include <stdbool.h>

typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_DOUBLE,
    TYPE_CHAR,
    TYPE_VOID,
    TYPE_POINTER,
    TYPE_ARRAY,
    TYPE_FUNCTION
} TypeKind;

typedef struct Type {
    TypeKind kind;
    struct Type* base;
    int size;
    int arraySize;
} Type;

typedef struct Symbol {
    char* name;
    Type* type;
    int scope;
    int offset;
    bool isFunction;
    bool isVariable;
    bool isParam;
    struct Symbol* next;
} Symbol;

typedef struct Scope {
    int level;
    Symbol* symbols;
    struct Scope* parent;
} Scope;

typedef struct SymbolTable {
    Scope* current;
    int nextOffset;
} SymbolTable;

SymbolTable* createSymbolTable();
void enterScope(SymbolTable* table);
void exitScope(SymbolTable* table);
Symbol* lookup(SymbolTable* table, char* name);
Symbol* lookupLocal(SymbolTable* table, char* name);
void insert(SymbolTable* table, char* name, Type* type);
void setVariable(Symbol* sym);
void setFunction(Symbol* sym);
void setParam(Symbol* sym);
void printSymbolTable(SymbolTable* table);

Type* createType(TypeKind kind);
Type* createPointerType(Type* base);
Type* createArrayType(Type* base, int size);
Type* createFunctionType(Type* returnType);

#endif
