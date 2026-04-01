#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    OP_LOAD,
    OP_STORE,
    OP_ADD,
    OP_SUB,
    OP_MUL,
    OP_DIV,
    OP_JMP,
    OP_JZ,
    OP_HALT
} OpCode;

typedef struct {
    OpCode opcode;
    int operand;
} Instruction;

typedef struct {
    int* stack;
    int sp;
    int ip;
    int* memory;
    int memory_size;
} VM;

VM* createVM(int memory_size) {
    VM* vm = (VM*)malloc(sizeof(VM));
    vm->stack = (int*)malloc(1024 * sizeof(int));
    vm->sp = 0;
    vm->ip = 0;
    vm->memory_size = memory_size;
    vm->memory = (int*)malloc(memory_size * sizeof(int));
    return vm;
}

void push(VM* vm, int value) {
    vm->stack[vm->sp++] = value;
}

int pop(VM* vm) {
    return vm->stack[--vm->sp];
}

void execute(VM* vm, Instruction* program, int program_size) {
    while (vm->ip < program_size) {
        Instruction* instr = &program[vm->ip++];
        
        switch (instr->opcode) {
            case OP_LOAD:
                push(vm, vm->memory[instr->operand]);
                break;
            case OP_STORE:
                vm->memory[instr->operand] = pop(vm);
                break;
            case OP_ADD: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a + b);
                break;
            }
            case OP_SUB: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a - b);
                break;
            }
            case OP_MUL: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a * b);
                break;
            }
            case OP_JMP:
                vm->ip = instr->operand;
                break;
            case OP_JZ:
                if (pop(vm) == 0) {
                    vm->ip = instr->operand;
                }
                break;
            case OP_HALT:
                return;
        }
    }
}

int main() {
    VM* vm = createVM(100);
    
    Instruction program[] = {
        {OP_LOAD, 0},    // load 10
        {OP_LOAD, 1},    // load 20
        {OP_ADD, 0},     // add
        {OP_STORE, 2},   // store to result
        {OP_HALT, 0}
    };
    
    vm->memory[0] = 10;
    vm->memory[1] = 20;
    
    execute(vm, program, 5);
    
    printf("Result: %d\n", vm->memory[2]);
    
    return 0;
}
