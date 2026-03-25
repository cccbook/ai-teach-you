#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int pid;
    char name[32];
    char state[16];
    int priority;
    int registers[16];
    char memory[256];
    int file_handles[10];
    int parent;
    int children[10];
    int child_count;
} PCB;

PCB* pcb_create(int pid, const char *name) {
    PCB *pcb = malloc(sizeof(PCB));
    pcb->pid = pid;
    strncpy(pcb->name, name, 31);
    strcpy(pcb->state, "NEW");
    pcb->priority = 0;
    pcb->parent = 0;
    pcb->child_count = 0;
    memset(pcb->registers, 0, sizeof(pcb->registers));
    memset(pcb->memory, 0, sizeof(pcb->memory));
    memset(pcb->file_handles, -1, sizeof(pcb->file_handles));
    return pcb;
}

int main() {
    PCB *p = pcb_create(1, "main");
    printf("PCB created: PID=%d, Name=%s, State=%s\n", p->pid, p->name, p->state);
    free(p);
    return 0;
}
