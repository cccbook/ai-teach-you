#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_OBJECTS 100
#define MAX_SYMBOLS 1000

typedef struct {
    char name[64];
    int address;
} Symbol;

typedef struct {
    char name[64];
    Symbol symbols[MAX_SYMBOLS];
    int sym_count;
    char references[MAX_SYMBOLS][64];
    int ref_count;
} ObjectFile;

typedef struct {
    ObjectFile objects[MAX_OBJECTS];
    int obj_count;
    Symbol symbols[MAX_SYMBOLS];
    int sym_count;
} Linker;

void add_object(Linker *l, const char *name, Symbol *syms, int sym_count) {
    if (l->obj_count >= MAX_OBJECTS) return;
    ObjectFile *obj = &l->objects[l->obj_count++];
    strncpy(obj->name, name, 63);
    obj->sym_count = sym_count;
    obj->ref_count = 0;
    for (int i = 0; i < sym_count; i++) {
        obj->symbols[i] = syms[i];
        l->symbols[l->sym_count++] = syms[i];
    }
}

void add_reference(Linker *l, int obj_idx, const char *ref_name) {
    if (obj_idx >= l->obj_count) return;
    ObjectFile *obj = &l->objects[obj_idx];
    if (obj->ref_count < MAX_SYMBOLS) {
        strncpy(obj->references[obj->ref_count++], ref_name, 63);
    }
}

int resolve_references(Linker *l) {
    for (int i = 0; i < l->obj_count; i++) {
        ObjectFile *obj = &l->objects[i];
        for (int j = 0; j < obj->ref_count; j++) {
            int found = 0;
            for (int k = 0; k < l->sym_count; k++) {
                if (strcmp(obj->references[j], l->symbols[k].name) == 0) {
                    found = 1;
                    printf("解析符號: %s -> 地址 0x%x\n", obj->references[j], l->symbols[k].address);
                    break;
                }
            }
            if (!found) {
                printf("Error: Undefined symbol: %s\n", obj->references[j]);
                return -1;
            }
        }
    }
    return 0;
}

void* link(Linker *l) {
    if (resolve_references(l) != 0) return NULL;
    void *exec = malloc(1024);
    printf("Executable linked successfully\n");
    return exec;
}

int main() {
    Linker l;
    memset(&l, 0, sizeof(Linker));
    
    Symbol obj1_syms[] = {{"main", 0x1000}, {"foo", 0x2000}};
    add_object(&l, "a.o", obj1_syms, 2);
    
    Symbol obj2_syms[] = {{"bar", 0x3000}};
    add_object(&l, "b.o", obj2_syms, 1);
    add_reference(&l, 1, "foo");
    
    void *exec = link(&l);
    if (exec) {
        printf("Link complete. Executable at %p\n", exec);
        free(exec);
    }
    
    return 0;
}
