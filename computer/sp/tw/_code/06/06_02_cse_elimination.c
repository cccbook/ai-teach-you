#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_IR 100

typedef struct {
    char lhs[32];
    char rhs[64];
    int is_temp;
} Instr;

typedef struct {
    Instr instructions[MAX_IR];
    int count;
    char seen[50][64];
    int seen_count;
} CSEOptimizer;

void add_seen(CSEOptimizer *opt, char *expr, char *temp) {
    if (opt->seen_count < 50) {
        strcpy(opt->seen[opt->seen_count++], expr);
    }
}

int is_duplicate(CSEOptimizer *opt, char *expr) {
    for (int i = 0; i < opt->seen_count; i++) {
        if (strcmp(opt->seen[i], expr) == 0) {
            return 1;
        }
    }
    return 0;
}

void cse_optimize(CSEOptimizer *opt, char input[MAX_IR][64], int input_count) {
    opt->count = 0;
    opt->seen_count = 0;
    
    for (int i = 0; i < input_count; i++) {
        char *eq = strchr(input[i], '=');
        if (eq) {
            char rhs[64];
            strcpy(rhs, eq + 1);
            
            if (is_duplicate(opt, rhs)) {
                continue;
            }
            
            char lhs[32];
            strncpy(lhs, input[i], eq - input[i]);
            lhs[eq - input[i]] = '\0';
            
            strcpy(opt->instructions[opt->count].lhs, lhs);
            strcpy(opt->instructions[opt->count].rhs, rhs);
            opt->instructions[opt->count].is_temp = (lhs[0] == 't');
            opt->count++;
            
            if (lhs[0] == 't') {
                add_seen(opt, rhs, lhs);
            }
        } else {
            strcpy(opt->instructions[opt->count].lhs, "");
            strcpy(opt->instructions[opt->count].rhs, input[i]);
            opt->count++;
        }
    }
}

int main() {
    CSEOptimizer opt;
    memset(&opt, 0, sizeof(opt));
    
    char ir[MAX_IR][64] = {
        "a = b + c",
        "d = b + c + 1"
    };
    
    cse_optimize(&opt, ir, 2);
    
    printf("After CSE:\n");
    for (int i = 0; i < opt.count; i++) {
        if (opt.instructions[i].lhs[0]) {
            printf("%s = %s\n", opt.instructions[i].lhs, opt.instructions[i].rhs);
        } else {
            printf("%s\n", opt.instructions[i].rhs);
        }
    }
    
    return 0;
}
