#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SCOPES 100
#define MAX_SYMBOLS 1000

typedef struct {
    char name[64];
    char type[32];
    char kind[32];
    int address;
} Symbol;

typedef struct {
    Symbol symbols[MAX_SYMBOLS];
    int count;
} Scope;

typedef struct {
    Scope scopes[MAX_SCOPES];
    int scope_count;
} SymbolTable;

void enter_scope(SymbolTable *st) {
    if (st->scope_count < MAX_SCOPES) {
        st->scopes[st->scope_count].count = 0;
        st->scope_count++;
    }
}

void exit_scope(SymbolTable *st) {
    if (st->scope_count > 0) {
        st->scope_count--;
    }
}

void define_symbol(SymbolTable *st, const char *name, const char *type, const char *kind, int address) {
    if (st->scope_count == 0) return;
    Scope *current = &st->scopes[st->scope_count - 1];
    if (current->count < MAX_SYMBOLS) {
        Symbol *sym = &current->symbols[current->count++];
        strncpy(sym->name, name, 63);
        strncpy(sym->type, type, 31);
        strncpy(sym->kind, kind, 31);
        sym->address = address;
    }
}

Symbol* lookup_symbol(SymbolTable *st, const char *name) {
    for (int i = st->scope_count - 1; i >= 0; i--) {
        Scope *scope = &st->scopes[i];
        for (int j = 0; j < scope->count; j++) {
            if (strcmp(scope->symbols[j].name, name) == 0) {
                return &scope->symbols[j];
            }
        }
    }
    return NULL;
}

int main() {
    SymbolTable st;
    st.scope_count = 0;
    enter_scope(&st);
    
    define_symbol(&st, "x", "int", "variable", 0);
    define_symbol(&st, "main", "function", "function", 0);
    
    enter_scope(&st);
    define_symbol(&st, "x", "int", "parameter", 8);
    define_symbol(&st, "y", "double", "variable", 16);
    
    Symbol *sym = lookup_symbol(&st, "x");
    if (sym) printf("lookup('x'): type=%s, kind=%s, address=%d\n", sym->type, sym->kind, sym->address);
    
    sym = lookup_symbol(&st, "y");
    if (sym) printf("lookup('y'): type=%s, kind=%s, address=%d\n", sym->type, sym->kind, sym->address);
    
    sym = lookup_symbol(&st, "main");
    if (sym) printf("lookup('main'): type=%s, kind=%s, address=%d\n", sym->type, sym->kind, sym->address);
    
    exit_scope(&st);
    sym = lookup_symbol(&st, "x");
    if (sym) printf("After exit_scope, lookup('x'): type=%s, kind=%s, address=%d\n", sym->type, sym->kind, sym->address);
    
    return 0;
}
