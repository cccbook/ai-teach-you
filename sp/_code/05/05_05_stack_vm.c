#include <stdio.h>
#include <stdlib.h>

#define MAX_STACK 256

typedef enum {OP_ICONST, OP_IADD, OP_ISUB, OP_IMUL, OP_PRINT, OP_HALT} OpCode;

typedef struct {
    int stack[MAX_STACK];
    int sp;
} StackVM;

void push(StackVM *vm, int val) { 
    if (vm->sp < MAX_STACK) vm->stack[vm->sp++] = val; 
}

int pop(StackVM *vm) { 
    return vm->sp > 0 ? vm->stack[--vm->sp] : 0; 
}

void run(StackVM *vm, OpCode *bc, int len) {
    for (int pc = 0; pc < len; pc++) {
        switch (bc[pc]) {
            case OP_ICONST: 
                push(vm, bc[++pc]); 
                break;
            case OP_IADD: { 
                int b = pop(vm), a = pop(vm); 
                push(vm, a + b); 
                break; 
            }
            case OP_ISUB: { 
                int b = pop(vm), a = pop(vm); 
                push(vm, a - b); 
                break; 
            }
            case OP_IMUL: { 
                int b = pop(vm), a = pop(vm); 
                push(vm, a * b); 
                break; 
            }
            case OP_PRINT: 
                printf("Stack VM result: %d\n", pop(vm)); 
                break;
            case OP_HALT: 
                return;
        }
    }
}

int main() {
    printf("=== Stack-based VM Demo ===\n");
    
    StackVM vm = {0};
    
    OpCode bc1[] = {OP_ICONST, 1, OP_ICONST, 2, OP_IADD, OP_PRINT, OP_HALT};
    printf("\nExecuting: 1 + 2\n");
    run(&vm, bc1, 7);
    
    vm.sp = 0;
    OpCode bc2[] = {OP_ICONST, 5, OP_ICONST, 3, OP_IMUL, OP_PRINT, OP_HALT};
    printf("\nExecuting: 5 * 3\n");
    run(&vm, bc2, 7);
    
    vm.sp = 0;
    OpCode bc3[] = {OP_ICONST, 10, OP_ICONST, 4, OP_ICONST, 2, OP_IADD, OP_IMUL, OP_PRINT, OP_HALT};
    printf("\nExecuting: 10 * (4 + 2)\n");
    run(&vm, bc3, 11);
    
    return 0;
}
