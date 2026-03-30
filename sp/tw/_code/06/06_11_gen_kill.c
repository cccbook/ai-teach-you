#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_VARS 50
#define MAX_DEFS 100

typedef struct {
    char var[32];
    char expr[64];
    int killed;
} Statement;

typedef struct {
    int gen[MAX_DEFS];
    int gen_count;
    int kill[MAX_DEFS];
    int kill_count;
} GenKill;

void compute_gen_kill(Statement stmts[], int n, GenKill* result, int all_defs[][2], int def_count) {
    result->gen_count = 0;
    result->kill_count = 0;
    
    printf("Computing GEN and KILL sets:\n\n");
    
    for (int i = 0; i < n; i++) {
        char def[64];
        sprintf(def, "%s=%s", stmts[i].var, stmts[i].expr);
        
        result->gen[result->gen_count++] = i;
        printf("  GEN[%d]: %s (adds definition)\n", i, def);
        
        for (int j = 0; j < def_count; j++) {
            if (all_defs[j][0] == i) continue;
            if (strcmp(stmts[i].var, stmts[all_defs[j][0]].var) == 0) {
                result->kill[result->kill_count++] = all_defs[j][1];
                printf("  KILL[%d]: kills definition %d\n", i, all_defs[j][1]);
            }
        }
    }
}

int main() {
    Statement stmts[] = {
        {"a", "10", 0},
        {"b", "a + 5", 0},
        {"a", "20", 0},
        {"c", "a + b", 0}
    };
    int n = 4;
    
    int all_defs[][2] = {
        {0, 0},
        {1, 1},
        {2, 2},
        {3, 3}
    };
    int def_count = 4;
    
    GenKill result;
    
    printf("=== GEN and KILL Sets ===\n\n");
    printf("Statements:\n");
    for (int i = 0; i < n; i++) {
        printf("  [%d] %s = %s\n", i, stmts[i].var, stmts[i].expr);
    }
    
    compute_gen_kill(stmts, n, &result, all_defs, def_count);
    
    printf("\nResult:\n");
    printf("  GEN: {");
    for (int i = 0; i < result.gen_count; i++) {
        printf("%d%s", result.gen[i], i < result.gen_count - 1 ? ", " : "");
    }
    printf("}\n");
    printf("  KILL: {");
    for (int i = 0; i < result.kill_count; i++) {
        printf("%d%s", result.kill[i], i < result.kill_count - 1 ? ", " : "");
    }
    printf("}\n");
    
    return 0;
}
