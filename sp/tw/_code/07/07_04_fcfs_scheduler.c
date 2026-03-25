#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int pid;
    char name[32];
    int burst_time;
    int remaining_time;
    int priority;
} Process;

typedef struct {
    Process *queue[100];
    int front;
    int rear;
    int count;
} FCFSScheduler;

void fcfs_init(FCFSScheduler *s) {
    s->front = s->rear = s->count = 0;
}

void fcfs_add(FCFSScheduler *s, Process *p) {
    s->queue[s->rear++] = p;
    s->count++;
}

Process* fcfs_next(FCFSScheduler *s) {
    if (s->count == 0) return NULL;
    Process *p = s->queue[s->front++];
    s->count--;
    return p;
}

int main() {
    FCFSScheduler sched;
    fcfs_init(&sched);
    
    Process p1 = {1, "P1", 10, 10, 1};
    Process p2 = {2, "P2", 5, 5, 2};
    
    fcfs_add(&sched, &p1);
    fcfs_add(&sched, &p2);
    
    Process *p = fcfs_next(&sched);
    printf("Running: %s (burst: %d)\n", p->name, p->burst_time);
    
    p = fcfs_next(&sched);
    printf("Running: %s (burst: %d)\n", p->name, p->burst_time);
    
    return 0;
}
