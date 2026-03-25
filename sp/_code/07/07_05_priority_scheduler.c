#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_QUEUE_SIZE 100
#define TIME_QUANTUM 4

typedef struct {
    int pid;
    char name[16];
    int priority;
    int burst_time;
    int remaining_time;
} Process;

Process queue[MAX_QUEUE_SIZE];
int count = 0;
int time_slice_counter = 0;
int current_process = -1;

void add_process(Process p) {
    if (count < MAX_QUEUE_SIZE) {
        queue[count++] = p;
    }
}

int find_highest_priority() {
    int highest = -1;
    int highest_priority = 999;
    
    for (int i = 0; i < count; i++) {
        if (queue[i].remaining_time > 0 && queue[i].priority < highest_priority) {
            highest_priority = queue[i].priority;
            highest = i;
        }
    }
    return highest;
}

int find_shortest_job() {
    int shortest = -1;
    int shortest_burst = 999999;
    
    for (int i = 0; i < count; i++) {
        if (queue[i].remaining_time > 0 && queue[i].burst_time < shortest_burst) {
            shortest_burst = queue[i].burst_time;
            shortest = i;
        }
    }
    return shortest;
}

void round_robin_simulation() {
    printf("=== Round Robin Scheduler (Time Quantum = %d) ===\n\n", TIME_QUANTUM);
    
    printf("Initial processes:\n");
    for (int i = 0; i < count; i++) {
        printf("  P%d: burst=%d, priority=%d\n", 
               queue[i].pid, queue[i].burst_time, queue[i].priority);
    }
    
    printf("\n=== Execution ===\n");
    
    int time = 0;
    int completed = 0;
    
    while (completed < count) {
        int idx = find_highest_priority();
        if (idx < 0) break;
        
        Process* p = &queue[idx];
        
        int exec_time = (p->remaining_time < TIME_QUANTUM) ? 
                        p->remaining_time : TIME_QUANTUM;
        
        printf("Time %d-%d: Running P%d (remaining=%d)\n",
               time, time + exec_time, p->pid, p->remaining_time);
        
        p->remaining_time -= exec_time;
        time += exec_time;
        
        if (p->remaining_time <= 0) {
            printf("  -> P%d completed\n", p->pid);
            completed++;
        } else {
            printf("  -> P%d preempted, re-queued\n", p->pid);
        }
    }
    
    printf("\nTotal execution time: %d\n", time);
}

void priority_simulation() {
    printf("\n=== Priority Scheduler ===\n\n");
    
    printf("Initial processes:\n");
    for (int i = 0; i < count; i++) {
        printf("  P%d: burst=%d, priority=%d\n", 
               queue[i].pid, queue[i].burst_time, queue[i].priority);
    }
    
    printf("\n=== Execution (Higher priority = lower number) ===\n");
    
    int time = 0;
    int completed = 0;
    
    while (completed < count) {
        int idx = find_highest_priority();
        if (idx < 0) break;
        
        Process* p = &queue[idx];
        
        printf("Time %d: Running P%d (priority=%d, burst=%d)\n",
               time, p->pid, p->priority, p->burst_time);
        
        time += p->burst_time;
        p->remaining_time = 0;
        printf("  -> P%d completed at time %d\n", p->pid, time);
        completed++;
    }
}

int main() {
    add_process((Process){1, "P1", 3, 10, 10});
    add_process((Process){2, "P2", 1, 5, 5});
    add_process((Process){3, "P2", 2, 8, 8});
    
    printf("Priority Scheduler:\n");
    printf("Processes added with priorities (lower = higher priority)\n");
    printf("Always schedules highest priority ready process\n");
    printf("May cause starvation of low priority processes\n");
    
    printf("\n");
    priority_simulation();
    
    for (int i = 0; i < count; i++) {
        queue[i].remaining_time = queue[i].burst_time;
    }
    
    printf("\n");
    round_robin_simulation();
    
    return 0;
}
