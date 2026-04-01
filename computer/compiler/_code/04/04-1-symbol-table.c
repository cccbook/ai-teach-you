#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "04-1-symbol-table.h"

SymbolTable* createSymbolTable() {
    SymbolTable* table = (SymbolTable*)malloc(sizeof(SymbolTable));
    table->current = (Scope*)malloc(sizeof(Scope));
    table->current->level = 0;
    table->current->symbols = NULL;
    table->current->parent = NULL;
    table->nextOffset = 0;
    return table;
}

void enterScope(SymbolTable* table) {
    Scope* newScope = (Scope*)malloc(sizeof(Scope));
    newScope->level = table->current->level + 1;
    newScope->symbols = NULL;
    newScope->parent = table->current;
    table->current = newScope;
}

void exitScope(SymbolTable* table) {
    if (table->current->parent) {
        Scope* oldScope = table->current;
        table->current = table->current->parent;
        free(oldScope);
    }
}

Symbol* lookup(SymbolTable* table, char* name) {
    Scope* scope = table->current;
    while (scope) {
        Symbol* sym = scope->symbols;
        while (sym) {
            if (strcmp(sym->name, name) == 0) {
                return sym;
            }
            sym = sym->next;
        }
        scope = scope->parent;
    }
    return NULL;
}

Symbol* lookupLocal(SymbolTable* table, char* name) {
    Symbol* sym = table->current->symbols;
    while (sym) {
        if (strcmp(sym->name, name) == 0) {
            return sym;
        }
        sym = sym->next;
    }
    return NULL;
}

void insert(SymbolTable* table, char* name, Type* type) {
    if (lookupLocal(table, name)) {
        fprintf(stderr, "Error: Symbol '%s' already defined\n", name);
        return;
    }
    
    Symbol* sym = (Symbol*)malloc(sizeof(Symbol));
    sym->name = strdup(name);
    sym->type = type;
    sym->scope = table->current->level;
    sym->offset = table->nextOffset;
    sym->isFunction = false;
    sym->isVariable = false;
    sym->isParam = false;
    
    if (type->kind == TYPE_INT || type->kind == TYPE_FLOAT ||
        type->kind == TYPE_DOUBLE || type->kind == TYPE_CHAR) {
        table->nextOffset += type->size;
    }
    
    sym->next = table->current->symbols;
    table->current->symbols = sym;
}

void setVariable(Symbol* sym) {
    sym->isVariable = true;
}

void setFunction(Symbol* sym) {
    sym->isFunction = true;
}

void setParam(Symbol* sym) {
    sym->isParam = true;
}

Type* createType(TypeKind kind) {
    Type* type = (Type*)malloc(sizeof(Type));
    type->kind = kind;
    type->base = NULL;
    type->size = 4;
    type->arraySize = 0;
    return type;
}

Type* createPointerType(Type* base) {
    Type* type = createType(TYPE_POINTER);
    type->base = base;
    type->size = 8;
    return type;
}

Type* createArrayType(Type* base, int size) {
    Type* type = createType(TYPE_ARRAY);
    type->base = base;
    type->arraySize = size;
    type->size = base->size * size;
    return type;
}

Type* createFunctionType(Type* returnType) {
    Type* type = createType(TYPE_FUNCTION);
    type->base = returnType;
    return type;
}

static const char* typeKindToString(TypeKind kind) {
    switch (kind) {
        case TYPE_INT: return "int";
        case TYPE_FLOAT: return "float";
        case TYPE_DOUBLE: return "double";
        case TYPE_CHAR: return "char";
        case TYPE_VOID: return "void";
        case TYPE_POINTER: return "pointer";
        case TYPE_ARRAY: return "array";
        case TYPE_FUNCTION: return "function";
        default: return "unknown";
    }
}

void printSymbolTable(SymbolTable* table) {
    printf("\n=== Symbol Table ===\n");
    Scope* scope = table->current;
    while (scope) {
        printf("Scope Level: %d\n", scope->level);
        Symbol* sym = scope->symbols;
        while (sym) {
            printf("  %s : %s", sym->name, typeKindToString(sym->type->kind));
            if (sym->isVariable) printf(" [variable]");
            if (sym->isFunction) printf(" [function]");
            if (sym->isParam) printf(" [param]");
            printf(" (offset: %d)\n", sym->offset);
            sym = sym->next;
        }
        scope = scope->parent;
    }
    printf("====================\n\n");
}

int main() {
    SymbolTable* table = createSymbolTable();
    
    Type* intType = createType(TYPE_INT);
    Type* floatType = createType(TYPE_FLOAT);
    floatType->size = 4;
    
    insert(table, "x", intType);
    insert(table, "y", floatType);
    setVariable(lookup(table, "x"));
    setVariable(lookup(table, "y"));
    
    printf("Before entering new scope:");
    printSymbolTable(table);
    
    enterScope(table);
    insert(table, "z", intType);
    setVariable(lookup(table, "z"));
    
    printf("After entering new scope:");
    printSymbolTable(table);
    
    exitScope(table);
    
    printf("After exiting scope:");
    printSymbolTable(table);
    
    return 0;
}
