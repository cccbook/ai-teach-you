#include <stdio.h>
#include <stdlib.h>

#define NUM_REGS 256

typedef enum {OP_LOADK, OP_ADD, OP_SUB, OP_MUL, OP_PRINT, OP_HALT} OpCode;

typedef struct {
    int regs[NUM_REGS];
    int pc;
} RegisterVM;

void run(RegisterVM *vm, int *bc, int len) {
    while (vm->pc < len) {
        int opcode = bc[vm->pc++];
        switch (opcode) {
            case OP_LOADK: {
                int reg = bc[vm->pc++];
                int val = bc[vm->pc++];
                vm->regs[reg] = val;
                break;
            }
            case OP_ADD: {
                int d = bc[vm->pc++], l = bc[vm->pc++], r = bc[vm->pc++];
                vm->regs[d] = vm->regs[l] + vm->regs[r];
                break;
            }
            case OP_SUB: {
                int d = bc[vm->pc++], l = bc[vm->pc++], r = bc[vm->pc++];
                vm->regs[d] = vm->regs[l] - vm->regs[r];
                break;
            }
            case OP_MUL: {
                int d = bc[vm->pc++], l = bc[vm->pc++], r = bc[vm->pc++];
                vm->regs[d] = vm->regs[l] * vm->regs[r];
                break;
            }
            case OP_PRINT: {
                int reg = bc[vm->pc++];
                printf("Register VM result: %d\n", vm->regs[reg]);
                break;
            }
            case OP_HALT:
                return;
        }
    }
}

int main() {
    printf("=== Register-based VM Demo ===\n");
    
    RegisterVM vm = {0};
    
    int bc1[] = {
        OP_LOADK, 0, 1,
        OP_LOADK, 1, 2,
        OP_ADD, 2, 0, 1,
        OP_PRINT, 2,
        OP_HALT
    };
    printf("\nExecuting: R2 = R0 + R1 where R0=1, R1=2\n");
    run(&vm, bc1, 13);
    
    vm.pc = 0;
    for (int i = 0; i < NUM_REGS; i++) vm.regs[i] = 0;
    
    int bc2[] = {
        OP_LOADK, 0, 5,
        OP_LOADK, 1, 3,
        OP_MUL, 2, 0, 1,
        OP_PRINT, 2,
        OP_HALT
    };
    printf("\nExecuting: R2 = R0 * R1 where R0=5, R1=3\n");
    run(&vm, bc2, 13);
    
    vm.pc = 0;
    for (int i = 0; i < NUM_REGS; i++) vm.regs[i] = 0;
    
    int bc3[] = {
        OP_LOADK, 0, 10,
        OP_LOADK, 1, 4,
        OP_LOADK, 2, 2,
        OP_ADD, 3, 1, 2,
        OP_MUL, 4, 0, 3,
        OP_PRINT, 4,
        OP_HALT
    };
    printf("\nExecuting: R4 = R0 * (R1 + R2) where R0=10, R1=4, R2=2\n");
    run(&vm, bc3, 21);
    
    return 0;
}
