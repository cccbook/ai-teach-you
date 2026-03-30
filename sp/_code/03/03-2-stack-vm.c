#include <stdio.h>

#define MAX_STACK 100
#define MAX_VARS 100

typedef enum { 
    OP_LOAD_CONST, OP_LOAD_VAR, OP_STORE_VAR, 
    OP_ADD, OP_SUB, OP_MUL, OP_DIV, 
    OP_PRINT, OP_HALT 
} OpCode;

int stack[MAX_STACK];
int sp = 0;
int variables[MAX_VARS];

void push(int v) { 
    if (sp < MAX_STACK) stack[sp++] = v; 
}

int pop() { 
    return sp > 0 ? stack[--sp] : 0; 
}

void run_vm(int bytecode[], int pc) {
    while (1) {
        switch(bytecode[pc]) {
            case OP_LOAD_CONST: 
                push(bytecode[pc + 1]); 
                pc += 2; 
                break;
            case OP_LOAD_VAR: 
                push(variables[bytecode[pc + 1]]); 
                pc += 2; 
                break;
            case OP_STORE_VAR: 
                variables[bytecode[pc + 1]] = pop(); 
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
            default: 
                pc++;
        }
    }
}

int main() {
    int bytecode[] = {
        OP_LOAD_CONST, 10,
        OP_STORE_VAR, 0,
        OP_LOAD_CONST, 20,
        OP_STORE_VAR, 1,
        OP_LOAD_VAR, 0,
        OP_LOAD_VAR, 1,
        OP_ADD,
        OP_PRINT,
        OP_HALT
    };
    
    printf("執行 bytecode: 10 + 20\n");
    run_vm(bytecode, 0);
    
    return 0;
}
