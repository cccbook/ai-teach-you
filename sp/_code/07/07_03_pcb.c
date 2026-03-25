#include <stdio.h>
#include <string.h>

typedef enum {
    NEW,
    READY,
    RUNNING,
    BLOCKED,
    TERMINATED
} ProcessState;

typedef struct {
    int pid;
    char name[32];
    ProcessState state;
    int priority;
    int program_counter;
    int registers[8];
    int memory_base;
    int memory_limit;
} PCB;

const char* state_to_string(ProcessState state) {
    switch(state) {
        case NEW: return "NEW";
        case READY: return "READY";
        case RUNNING: return "RUNNING";
        case BLOCKED: return "BLOCKED";
        case TERMINATED: return "TERMINATED";
        default: return "UNKNOWN";
    }
}

void print_pcb(PCB* pcb) {
    printf("PCB Information:\n");
    printf("  PID: %d\n", pcb->pid);
    printf("  Name: %s\n", pcb->name);
    printf("  State: %s\n", state_to_string(pcb->state));
    printf("  Priority: %d\n", pcb->priority);
    printf("  PC: 0x%x\n", pcb->program_counter);
    printf("  Memory: [0x%x - 0x%x]\n", 
           pcb->memory_base, pcb->memory_limit);
}

void save_context(PCB* pcb, int* regs) {
    for (int i = 0; i < 8; i++) {
        pcb->registers[i] = regs[i];
    }
}

void restore_context(PCB* pcb, int* regs) {
    for (int i = 0; i < 8; i++) {
        regs[i] = pcb->registers[i];
    }
}

int main() {
    printf("=== Process Control Block Demo ===\n\n");
    
    PCB pcb = {
        .pid = 1234,
        .name = "main",
        .state = NEW,
        .priority = 0,
        .program_counter = 0x400000,
        .memory_base = 0x10000,
        .memory_limit = 0x20000
    };
    
    print_pcb(&pcb);
    
    printf("\n=== State Transitions ===\n");
    printf("NEW -> READY\n");
    pcb.state = READY;
    printf("Current state: %s\n", state_to_string(pcb.state));
    
    printf("\nREADY -> RUNNING\n");
    pcb.state = RUNNING;
    printf("Current state: %s\n", state_to_string(pcb.state));
    
    printf("\nRunning -> BLOCKED (waiting for I/O)\n");
    pcb.state = BLOCKED;
    printf("Current state: %s\n", state_to_string(pcb.state));
    
    printf("\nBLOCKED -> READY\n");
    pcb.state = READY;
    printf("Current state: %s\n", state_to_string(pcb.state));
    
    printf("\nREADY -> RUNNING\n");
    pcb.state = RUNNING;
    printf("Current state: %s\n", state_to_string(pcb.state));
    
    printf("\nRUNNING -> TERMINATED\n");
    pcb.state = TERMINATED;
    printf("Current state: %s\n", state_to_string(pcb.state));
    
    return 0;
}
