#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STACK 100
#define MAX_VARS 100
#define MAX_BYTECODE 200

typedef enum { 
    OP_LOAD_CONST, OP_LOAD_VAR, OP_STORE_VAR, 
    OP_ADD, OP_SUB, OP_MUL, OP_DIV, 
    OP_PRINT, OP_HALT 
} OpCode;

typedef struct {
    OpCode op;
    int value;
    char name[32];
} Instruction;

Instruction bytecode[MAX_BYTECODE];
int bc_count = 0;

int stack[MAX_STACK];
int sp = 0;
int variables[MAX_VARS];
int var_count = 0;

void push(int v) { stack[sp++] = v; }
int pop() { return stack[--sp]; }

void emit(OpCode op, int value, const char* name) {
    bytecode[bc_count].op = op;
    bytecode[bc_count].value = value;
    if (name) strcpy(bytecode[bc_count].name, name);
    bc_count++;
}

int get_var(const char* name) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(bytecode[i].name, name) == 0) return variables[i];
    }
    return 0;
}

void set_var(const char* name, int value) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(bytecode[i].name, name) == 0) { variables[i] = value; return; }
    }
    strcpy(bytecode[var_count].name, name);
    variables[var_count++] = value;
}

void run_vm() {
    int pc = 0;
    while (pc < bc_count) {
        switch(bytecode[pc].op) {
            case OP_LOAD_CONST:
                push(bytecode[pc].value);
                pc += 2;
                break;
            case OP_LOAD_VAR:
                push(get_var(bytecode[pc].name));
                pc += 2;
                break;
            case OP_STORE_VAR:
                set_var(bytecode[pc].name, pop());
                pc += 2;
                break;
            case OP_ADD: {
                int b = pop(), a = pop();
                push(a + b);
                pc++;
                break;
            }
            case OP_SUB: {
                int b = pop(), a = pop();
                push(a - b);
                pc++;
                break;
            }
            case OP_MUL: {
                int b = pop(), a = pop();
                push(a * b);
                pc++;
                break;
            }
            case OP_DIV: {
                int b = pop(), a = pop();
                push(a / b);
                pc++;
                break;
            }
            case OP_PRINT:
                printf("%d\n", pop());
                pc++;
                break;
            case OP_HALT:
                return;
        }
    }
}

void reset_vm() {
    sp = 0;
    var_count = 0;
    bc_count = 0;
}

int main() {
    // 編譯: let a = 10; let b = 20; print(a + b);
    reset_vm();
    emit(OP_LOAD_CONST, 10, NULL);
    emit(OP_STORE_VAR, 0, "a");
    emit(OP_LOAD_CONST, 20, NULL);
    emit(OP_STORE_VAR, 0, "b");
    emit(OP_LOAD_VAR, 0, "a");
    emit(OP_LOAD_VAR, 0, "b");
    emit(OP_ADD, 0, NULL);
    emit(OP_PRINT, 0, NULL);
    emit(OP_HALT, 0, NULL);
    
    printf("Executing bytecode:\n");
    run_vm();
    
    return 0;
}
