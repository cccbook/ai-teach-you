#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PROCESSES 100

typedef struct {
    int pid;
    char name[32];
    char state[16];
    int priority;
    int registers[16];
    int memory[10];
    int file_handles[10];
    int parent;
    int child_count;
} PCB;

typedef struct {
    PCB processes[MAX_PROCESSES];
    int count;
    int next_pid;
} Kernel;

void kernel_init(Kernel *k) {
    k->count = 0;
    k->next_pid = 1;
}

PCB* create_process(Kernel *k, const char *name, int priority) {
    if (k->count >= MAX_PROCESSES) return NULL;
    
    PCB *p = &k->processes[k->count++];
    p->pid = k->next_pid++;
    strncpy(p->name, name, 31);
    strcpy(p->state, "NEW");
    p->priority = priority;
    p->parent = 0;
    p->child_count = 0;
    memset(p->registers, 0, sizeof(p->registers));
    memset(p->memory, 0, sizeof(p->memory));
    memset(p->file_handles, 0, sizeof(p->file_handles));
    
    return p;
}

int main() {
    Kernel k;
    kernel_init(&k);
    
    PCB *p1 = create_process(&k, "init", 0);
    printf("Created process: %s (PID: %d)\n", p1->name, p1->pid);
    
    PCB *p2 = create_process(&k, "shell", 1);
    printf("Created process: %s (PID: %d)\n", p2->name, p2->pid);
    
    printf("Total processes: %d\n", k.count);
    
    return 0;
}
