#include <stdio.h>
#include <string.h>

typedef struct {
    char var[32];
    int used;
} VarInfo;

typedef struct {
    char lhs[32];
    char rhs[64];
} Instruction;

int is_live(Instruction instr, VarInfo vars[], int n) {
    if (strstr(instr.rhs, "return") != NULL) return 1;
    if (strstr(instr.lhs, "printf") != NULL) return 0;
    return vars[0].used > 0;
}

int main() {
    Instruction ir[] = {
        {"x", "10"},
        {"y", "x + 5"},
        {"z", "100"},
        {"unused", "x + y"},
        {"result", "y + z"}
    };
    int n = 5;
    
    VarInfo vars[] = {
        {"x", 1},
        {"y", 1},
        {"z", 1},
        {"unused", 0},
        {"result", 1}
    };
    
    printf("=== Dead Code Elimination ===\n\n");
    printf("Original IR:\n");
    for (int i = 0; i < n; i++) {
        printf("  %s = %s\n", ir[i].lhs, ir[i].rhs);
    }
    
    printf("\nLive variables:\n");
    for (int i = 0; i < 5; i++) {
        printf("  %s: %s\n", vars[i].var, vars[i].used ? "live" : "dead");
    }
    
    printf("\nOptimized IR (dead code removed):\n");
    for (int i = 0; i < n; i++) {
        int live = 0;
        for (int j = 0; j < 5; j++) {
            if (strcmp(ir[i].lhs, vars[j].var) == 0 && vars[j].used) {
                live = 1;
                break;
            }
        }
        if (live) {
            printf("  %s = %s\n", ir[i].lhs, ir[i].rhs);
        } else {
            printf("  // REMOVED: %s = %s (dead code)\n", ir[i].lhs, ir[i].rhs);
        }
    }
    
    printf("\nAlgorithm:\n");
    printf("  1. Compute liveness of each variable\n");
    printf("  2. Mark assignments to dead variables\n");
    printf("  3. Remove dead assignments\n");
    
    return 0;
}
