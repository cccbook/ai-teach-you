#include <stdio.h>
#include <stdlib.h>

#define MAX_QUEUE_SIZE 100

typedef struct {
    int pid;
    char name[16];
    int burst_time;
    int arrival_time;
    int remaining_time;
} Process;

Process queue[MAX_QUEUE_SIZE];
int front = 0;
int rear = 0;
int count = 0;

void enqueue(Process p) {
    if (count < MAX_QUEUE_SIZE) {
        queue[rear] = p;
        rear = (rear + 1) % MAX_QUEUE_SIZE;
        count++;
    }
}

Process* dequeue() {
    if (count > 0) {
        Process* p = &queue[front];
        front = (front + 1) % MAX_QUEUE_SIZE;
        count--;
        return p;
    }
    return NULL;
}

int is_empty() {
    return count == 0;
}

void print_queue() {
    printf("Ready Queue: ");
    if (is_empty()) {
        printf("(empty)\n");
        return;
    }
    int idx = front;
    for (int i = 0; i < count; i++) {
        printf("P%d(burst=%d) ", queue[idx].pid, queue[idx].burst_time);
        idx = (idx + 1) % MAX_QUEUE_SIZE;
    }
    printf("\n");
}

int main() {
    printf("=== FCFS (First-Come-First-Serve) Scheduler ===\n\n");
    
    enqueue((Process){1, "P1", 10, 0, 10});
    enqueue((Process){2, "P2", 5, 0, 5});
    enqueue((Process){3, "P3", 8, 0, 8});
    
    print_queue();
    
    printf("\n=== Execution ===\n");
    int time = 0;
    int total_wait = 0;
    int wait_time = 0;
    
    while (!is_empty()) {
        Process* p = dequeue();
        wait_time = time;
        printf("Time %d: Running %s (burst %d)\n", 
               time, p->name, p->burst_time);
        
        for (int t = 0; t < p->burst_time; t++) {
            printf("  [Time %d] %s executing...\n", time + t, p->name);
        }
        
        total_wait += wait_time;
        time += p->burst_time;
        printf("  -> %s completed at time %d\n", p->name, time);
    }
    
    printf("\n=== Statistics ===\n");
    printf("Total turnaround time: %d\n", time);
    printf("Average waiting time: %.2f\n", (float)total_wait / 3);
    
    return 0;
}
