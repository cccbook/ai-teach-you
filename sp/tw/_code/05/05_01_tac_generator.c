#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INSTRUCTIONS 100
#define MAX_TEMP 50
#define MAX_LABEL 50

typedef struct {
    char instructions[MAX_INSTRUCTIONS][128];
    int count;
    int temp_counter;
    int label_counter;
} TACGenerator;

char* new_temp(TACGenerator *g) {
    static char temp[16];
    sprintf(temp, "t%d", g->temp_counter++);
    return temp;
}

char* new_label(TACGenerator *g) {
    static char label[16];
    sprintf(label, "L%d", g->label_counter++);
    return label;
}

void emit_add(TACGenerator *g, char *result, char *left, char *right) {
    sprintf(g->instructions[g->count++], "%s = %s + %s", result, left, right);
}

void emit_sub(TACGenerator *g, char *result, char *left, char *right) {
    sprintf(g->instructions[g->count++], "%s = %s - %s", result, left, right);
}

void emit_mul(TACGenerator *g, char *result, char *left, char *right) {
    sprintf(g->instructions[g->count++], "%s = %s * %s", result, left, right);
}

void emit_div(TACGenerator *g, char *result, char *left, char *right) {
    sprintf(g->instructions[g->count++], "%s = %s / %s", result, left, right);
}

void emit_load(TACGenerator *g, char *dest, char *address) {
    sprintf(g->instructions[g->count++], "%s = *%s", dest, address);
}

void emit_store(TACGenerator *g, char *source, char *address) {
    sprintf(g->instructions[g->count++], "*%s = %s", address, source);
}

void emit_branch(TACGenerator *g, char *label) {
    sprintf(g->instructions[g->count++], "goto %s", label);
}

void emit_cond_branch(TACGenerator *g, char *cond, char *true_label, char *false_label) {
    sprintf(g->instructions[g->count++], "if %s goto %s", cond, true_label);
    sprintf(g->instructions[g->count++], "goto %s", false_label);
}

void emit_label(TACGenerator *g, char *label) {
    sprintf(g->instructions[g->count++], "%s:", label);
}

void emit_call(TACGenerator *g, char *func, char **args, int arg_count) {
    char args_str[256] = "";
    for (int i = 0; i < arg_count; i++) {
        if (i > 0) strcat(args_str, ", ");
        strcat(args_str, args[i]);
    }
    sprintf(g->instructions[g->count++], "call %s(%s)", func, args_str);
}

void emit_return(TACGenerator *g, char *value) {
    sprintf(g->instructions[g->count++], "return %s", value);
}

int main() {
    TACGenerator g;
    memset(&g, 0, sizeof(TACGenerator));
    
    char *t0 = new_temp(&g);
    char *t1 = new_temp(&g);
    
    emit_mul(&g, t0, "2", "3");
    emit_add(&g, t1, t0, "4");
    
    printf("Generated TAC:\n");
    for (int i = 0; i < g.count; i++) {
        printf("%s\n", g.instructions[i]);
    }
    
    return 0;
}
