#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_REGISTERS 256

typedef enum {OP_LOADK, OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_PRINT, OP_HALT} OpCode;

typedef struct {
    int registers[NUM_REGISTERS];
    int pc;
} RegisterVM;

void reg_init(RegisterVM *vm) {
    vm->pc = 0;
    memset(vm->registers, 0, sizeof(vm->registers));
}

void reg_run(RegisterVM *vm, int *bytecode, int len) {
    while (vm->pc < len) {
        int op = bytecode[vm->pc++];
        
        switch (op) {
            case OP_LOADK: {
                int reg = bytecode[vm->pc++];
                int const_val = bytecode[vm->pc++];
                vm->registers[reg] = const_val;
                break;
            }
            case OP_ADD: {
                int dest = bytecode[vm->pc++];
                int left = bytecode[vm->pc++];
                int right = bytecode[vm->pc++];
                vm->registers[dest] = vm->registers[left] + vm->registers[right];
                break;
            }
            case OP_SUB: {
                int dest = bytecode[vm->pc++];
                int left = bytecode[vm->pc++];
                int right = bytecode[vm->pc++];
                vm->registers[dest] = vm->registers[left] - vm->registers[right];
                break;
            }
            case OP_MUL: {
                int dest = bytecode[vm->pc++];
                int left = bytecode[vm->pc++];
                int right = bytecode[vm->pc++];
                vm->registers[dest] = vm->registers[left] * vm->registers[right];
                break;
            }
            case OP_DIV: {
                int dest = bytecode[vm->pc++];
                int left = bytecode[vm->pc++];
                int right = bytecode[vm->pc++];
                vm->registers[dest] = vm->registers[left] / vm->registers[right];
                break;
            }
            case OP_PRINT: {
                int reg = bytecode[vm->pc++];
                printf("%d\n", vm->registers[reg]);
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
    RegisterVM vm;
    reg_init(&vm);
    
    int bytecode[] = {
        OP_LOADK, 0, 1,
        OP_LOADK, 1, 2,
        OP_ADD, 2, 0, 1,
        OP_PRINT, 2,
        OP_HALT
    };
    
    printf("Register VM Execution:\n");
    reg_run(&vm, bytecode, sizeof(bytecode)/sizeof(bytecode[0]));
    
    return 0;
}
