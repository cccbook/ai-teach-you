#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int pid;
    char name[16];
    int burst_time;
    int remaining_time;
    int priority;
} Process;

typedef struct {
    Process* processes[100];
    int count;
} PriorityQueue;

void swap(Process** a, Process** b) {
    Process* temp = *a;
    *a = *b;
    *b = temp;
}

int parent(int i) { return (i - 1) / 2; }
int left(int i) { return 2 * i + 1; }
int right(int i) { return 2 * i + 2; }

void heapify(PriorityQueue* pq, int i) {
    int smallest = i;
    int l = left(i);
    int r = right(i);
    
    if (l < pq->count && pq->processes[l]->burst_time < pq->processes[smallest]->burst_time)
        smallest = l;
    if (r < pq->count && pq->processes[r]->burst_time < pq->processes[smallest]->burst_time)
        smallest = r;
    
    if (smallest != i) {
        swap(&pq->processes[i], &pq->processes[smallest]);
        heapify(pq, smallest);
    }
}

void heappush(PriorityQueue* pq, Process* p) {
    pq->processes[pq->count++] = p;
    
    for (int i = pq->count - 1; i > 0; i--) {
        if (pq->processes[parent(i)]->burst_time > pq->processes[i]->burst_time) {
            swap(&pq->processes[parent(i)], &pq->processes[i]);
        }
    }
}

Process* heappop(PriorityQueue* pq) {
    if (pq->count == 0) return NULL;
    
    Process* min = pq->processes[0];
    pq->processes[0] = pq->processes[--pq->count];
    heapify(pq, 0);
    
    return min;
}

int main() {
    printf("=== SJF (Shortest Job First) Scheduler ===\n\n");
    
    PriorityQueue pq = {.count = 0};
    
    Process processes[] = {
        {1, "P1", 10, 10, 0},
        {2, "P2", 5, 5, 0},
        {3, "P3", 8, 8, 0},
        {4, "P4", 3, 3, 0}
    };
    
    printf("Adding processes:\n");
    for (int i = 0; i < 4; i++) {
        printf("  Added %s (burst: %d)\n", processes[i].name, processes[i].burst_time);
        heappush(&pq, &processes[i]);
    }
    
    printf("\nScheduling order (shortest first):\n");
    int total_wait = 0;
    int current_time = 0;
    
    while (pq.count > 0) {
        Process* p = heappop(&pq);
        printf("  [%02d-%02d] Running %s (burst: %d)\n",
               current_time, current_time + p->burst_time,
               p->name, p->burst_time);
        total_wait += current_time;
        current_time += p->burst_time;
    }
    
    printf("\nAverage waiting time: %.1f\n", (float)total_wait / 4);
    
    printf("\nProperties:\n");
    printf("  + Minimizes average waiting time\n");
    printf("  - Requires knowing burst time in advance\n");
    printf("  - Long jobs may starve\n");
    
    return 0;
}
