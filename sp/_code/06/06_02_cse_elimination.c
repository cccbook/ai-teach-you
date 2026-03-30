#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_EXPRS 100

typedef struct {
    char lhs[32];
    char rhs[64];
    char canonical[64];
} ExprEntry;

int canonicalize(const char* expr, char* result) {
    strcpy(result, expr);
    for (int i = 0; result[i]; i++) {
        if (result[i] == ' ') {
            memmove(&result[i], &result[i+1], strlen(&result[i]));
            i--;
        }
    }
    return 0;
}

int main() {
    printf("=== Common Subexpression Elimination Demo ===\n");
    
    printf("\nBefore CSE:\n");
    printf("  a = b + c\n");
    printf("  d = b + c + 1\n");
    printf("  e = b + c\n");
    
    ExprEntry seen[64];
    int seen_count = 0;
    
    const char* ir_before[] = {
        "a = b + c",
        "d = b + c + 1",
        "e = b + c"
    };
    
    printf("\nAfter CSE:\n");
    for (int i = 0; i < 3; i++) {
        char canonical[64];
        const char* expr = ir_before[i];
        
        char* eq = strchr(expr, '=');
        if (eq) {
            char rhs[64];
            strcpy(rhs, eq + 1);
            canonicalize(rhs, canonical);
            
            int found = -1;
            for (int j = 0; j < seen_count; j++) {
                if (strcmp(canonical, seen[j].canonical) == 0) {
                    found = j;
                    break;
                }
            }
            
            if (found >= 0) {
                printf("  %s = %s  (reused t%d)\n", ir_before[i], seen[found].rhs, found);
            } else {
                char new_temp[16];
                sprintf(new_temp, "t%d", seen_count);
                strcpy(seen[seen_count].lhs, ir_before[i]);
                strcpy(seen[seen_count].rhs, new_temp);
                strcpy(seen[seen_count].canonical, canonical);
                seen_count++;
                printf("  t%d = %s\n", seen_count - 1, rhs);
                printf("  %s = t%d\n", ir_before[i], seen_count - 1);
            }
        }
    }
    
    return 0;
}
