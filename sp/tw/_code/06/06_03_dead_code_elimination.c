#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_IR 50

typedef struct {
    char name[32];
    int is_used;
} Variable;

typedef struct {
    char ir[MAX_IR][64];
    int count;
    Variable vars[20];
    int var_count;
} DeadCodeElim;

void analyze_usage(DeadCodeElim *dce) {
    for (int i = 0; i < dce->var_count; i++) {
        dce->vars[i].is_used = 0;
    }
    
    for (int i = 1; i < dce->count; i++) {
        char *eq = strchr(dce->ir[i], '=');
        if (eq) {
            for (int j = 0; j < dce->var_count; j++) {
                if (strstr(eq + 1, dce->vars[j].name)) {
                    dce->vars[j].is_used = 1;
                }
            }
        }
    }
}

int is_dead(DeadCodeElim *dce, char *lhs) {
    for (int i = 0; i < dce->var_count; i++) {
        if (strcmp(dce->vars[i].name, lhs) == 0) {
            return !dce->vars[i].is_used;
        }
    }
    return 0;
}

void eliminate_dead(DeadCodeElim *dce) {
    analyze_usage(dce);
    
    printf("After dead code elimination:\n");
    for (int i = 0; i < dce->count; i++) {
        char *eq = strchr(dce->ir[i], '=');
        if (eq) {
            char lhs[32];
            strncpy(lhs, dce->ir[i], eq - dce->ir[i]);
            lhs[eq - dce->ir[i]] = '\0';
            
            if (!is_dead(dce, lhs)) {
                printf("%s\n", dce->ir[i]);
            }
        } else {
            printf("%s\n", dce->ir[i]);
        }
    }
}

int main() {
    DeadCodeElim dce;
    memset(&dce, 0, sizeof(dce));
    
    strcpy(dce.ir[dce.count++], "x = 1");
    strcpy(dce.ir[dce.count++], "y = 2");
    strcpy(dce.ir[dce.count++], "z = x + y");
    
    strcpy(dce.vars[dce.var_count].name, "x");
    dce.var_count++;
    strcpy(dce.vars[dce.var_count].name, "y");
    dce.var_count++;
    strcpy(dce.vars[dce.var_count].name, "z");
    dce.var_count++;
    
    eliminate_dead(&dce);
    return 0;
}
