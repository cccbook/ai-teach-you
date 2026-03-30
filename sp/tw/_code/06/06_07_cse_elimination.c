#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_EXPR 100
#define MAX_LINE 256

typedef struct {
    char lhs[32];
    char rhs[64];
} Instruction;

int main() {
    Instruction ir[] = {
        {"a", "b + c"},
        {"d", "b + c + 1"},
        {"e", "a + d"}
    };
    int n = 3;
    
    char seen_exprs[MAX_EXPR][64];
    char seen_vars[MAX_EXPR][32];
    int seen_count = 0;
    
    printf("=== Common Subexpression Elimination ===\n\n");
    printf("Original IR:\n");
    for (int i = 0; i < n; i++) {
        printf("  %s = %s\n", ir[i].lhs, ir[i].rhs);
    }
    
    printf("\nOptimized IR:\n");
    for (int i = 0; i < n; i++) {
        int found = -1;
        for (int j = 0; j < seen_count; j++) {
            if (strcmp(ir[i].rhs, seen_exprs[j]) == 0) {
                found = j;
                break;
            }
        }
        
        if (found >= 0) {
            printf("  %s = %s  // CSE: reused temp var\n", ir[i].lhs, seen_vars[found]);
        } else {
            printf("  %s = %s\n", ir[i].lhs, ir[i].rhs);
            if (ir[i].lhs[0] == 't') {
                strcpy(seen_exprs[seen_count], ir[i].rhs);
                strcpy(seen_vars[seen_count], ir[i].lhs);
                seen_count++;
            }
        }
    }
    
    printf("\nData structures:\n");
    printf("  seen_exprs[]: tracks computed expressions\n");
    printf("  seen_vars[]: maps expression -> temp variable\n");
    
    return 0;
}
