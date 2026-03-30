#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_METHODS 100
#define MAX_TIER1 50
#define MAX_TIER2 50

typedef struct {
    char name[64];
    int invocation_count;
    int compiled_tier;
    void *code;
} Method;

typedef struct {
    Method methods[MAX_METHODS];
    int method_count;
    void *tier1_cache[MAX_TIER1];
    void *tier2_cache[MAX_TIER2];
    int tier1_count;
    int tier2_count;
    int tier1_threshold;
    int tier2_threshold;
} JITCompiler;

void init_jit(JITCompiler *jit) {
    jit->method_count = 0;
    jit->tier1_count = 0;
    jit->tier2_count = 0;
    jit->tier1_threshold = 1000;
    jit->tier2_threshold = 10000;
}

Method* find_method(JITCompiler *jit, const char *name) {
    for (int i = 0; i < jit->method_count; i++) {
        if (strcmp(jit->methods[i].name, name) == 0) {
            return &jit->methods[i];
        }
    }
    return NULL;
}

void execute_method(JITCompiler *jit, const char *name) {
    Method *m = find_method(jit, name);
    if (!m) {
        m = &jit->methods[jit->method_count++];
        strcpy(m->name, name);
        m->invocation_count = 0;
        m->compiled_tier = 0;
    }
    
    m->invocation_count++;
    
    if (m->compiled_tier == 2) {
        printf("Executing tier-2 compiled code for %s\n", name);
    } else if (m->compiled_tier == 1) {
        printf("Executing tier-1 compiled code for %s\n", name);
        if (m->invocation_count >= jit->tier2_threshold) {
            printf("Upgrading to tier-2 for %s\n", name);
            m->compiled_tier = 2;
        }
    } else {
        printf("Interpreting %s (count: %d)\n", name, m->invocation_count);
        if (m->invocation_count >= jit->tier1_threshold) {
            printf("Compiling %s with tier-1\n", name);
            m->compiled_tier = 1;
        }
    }
}

int main() {
    JITCompiler jit;
    init_jit(&jit);
    
    for (int i = 0; i < 500; i++) {
        execute_method(&jit, "hotMethod");
    }
    
    return 0;
}
