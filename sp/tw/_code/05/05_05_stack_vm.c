#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STACK 256
#define MAX_VARS 64

typedef enum {OP_ICONST, OP_ILOAD, OP_ISTORE, OP_IADD, OP_ISUB, OP_IMUL, 
              OP_IDIV, OP_PRINT, OP_HALT} OpCode;

typedef struct {
    int stack[MAX_STACK];
    int sp;
    int variables[MAX_VARS];
    int pc;
} StackVM;

void stack_init(StackVM *vm) {
    vm->sp = 0;
    vm->pc = 0;
    memset(vm->stack, 0, sizeof(vm->stack));
    memset(vm->variables, 0, sizeof(vm->variables));
}

void stack_push(StackVM *vm, int value) {
    if (vm->sp < MAX_STACK) {
        vm->stack[vm->sp++] = value;
    }
}

int stack_pop(StackVM *vm) {
    if (vm->sp > 0) {
        return vm->stack[--vm->sp];
    }
    return 0;
}

void stack_run(StackVM *vm, OpCode *bytecode, int len) {
    while (vm->pc < len) {
        OpCode op = bytecode[vm->pc++];
        
        switch (op) {
            case OP_ICONST: {
                int val = bytecode[vm->pc++];
                stack_push(vm, val);
                break;
            }
            case OP_ILOAD: {
                int idx = bytecode[vm->pc++];
                stack_push(vm, vm->variables[idx]);
                break;
            }
            case OP_ISTORE: {
                int idx = bytecode[vm->pc++];
                vm->variables[idx] = stack_pop(vm);
                break;
            }
            case OP_IADD: {
                int b = stack_pop(vm);
                int a = stack_pop(vm);
                stack_push(vm, a + b);
                break;
            }
            case OP_ISUB: {
                int b = stack_pop(vm);
                int a = stack_pop(vm);
                stack_push(vm, a - b);
                break;
            }
            case OP_IMUL: {
                int b = stack_pop(vm);
                int a = stack_pop(vm);
                stack_push(vm, a * b);
                break;
            }
            case OP_PRINT: {
                int val = stack_pop(vm);
                printf("%d\n", val);
                break;
            }
            case OP_HALT:
                return;
            default:
                break;
        }
    }
}

int main() {
    StackVM vm;
    stack_init(&vm);
    
    OpCode bytecode[] = {
        OP_ICONST, 1,
        OP_ICONST, 2,
        OP_IADD,
        OP_PRINT,
        OP_HALT
    };
    
    printf("Stack VM Execution:\n");
    stack_run(&vm, bytecode, sizeof(bytecode)/sizeof(bytecode[0]));
    
    return 0;
}
