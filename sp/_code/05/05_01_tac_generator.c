#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INSTRUCTIONS 100

typedef struct {
    char instructions[MAX_INSTRUCTIONS][128];
    int count;
    int temp_counter;
} TACGenerator;

char* new_temp(TACGenerator *g) {
    static char temp[16];
    sprintf(temp, "t%d", g->temp_counter++);
    return temp;
}

void emit_add(TACGenerator *g, char *result, char *left, char *right) {
    sprintf(g->instructions[g->count++], "%s = %s + %s", result, left, right);
}

void emit_mul(TACGenerator *g, char *result, char *left, char *right) {
    sprintf(g->instructions[g->count++], "%s = %s * %s", result, left, right);
}

void emit_sub(TACGenerator *g, char *result, char *left, char *right) {
    sprintf(g->instructions[g->count++], "%s = %s - %s", result, left, right);
}

void emit_assign(TACGenerator *g, char *result, char *value) {
    sprintf(g->instructions[g->count++], "%s = %s", result, value);
}

void print_ir(TACGenerator *g) {
    printf("=== TAC (Three-Address Code) ===\n");
    for (int i = 0; i < g->count; i++) {
        printf("%d: %s\n", i, g->instructions[i]);
    }
}

int main() {
    TACGenerator g;
    memset(&g, 0, sizeof(TACGenerator));
    
    char *t0 = new_temp(&g);
    char *t1 = new_temp(&g);
    char *t2 = new_temp(&g);
    
    emit_mul(&g, t0, "2", "3");
    emit_add(&g, t1, t0, "4");
    emit_mul(&g, t2, t1, "2");
    
    print_ir(&g);
    
    printf("\n=== Evaluating ===\n");
    printf("t0 = 2 * 3 = %d\n", 2 * 3);
    printf("t1 = t0 + 4 = %d\n", 2 * 3 + 4);
    printf("t2 = t1 * 2 = %d\n", (2 * 3 + 4) * 2);
    
    return 0;
}
