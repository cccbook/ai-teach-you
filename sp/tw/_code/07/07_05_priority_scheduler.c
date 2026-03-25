#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int pid;
    char name[32];
    int burst_time;
    int priority;
} Process;

typedef struct {
    Process *heap[100];
    int size;
} PriorityQueue;

void swap(Process **a, Process **b) {
    Process *t = *a;
    *a = *b;
    *b = t;
}

void heapify(PriorityQueue *pq, int i) {
    int smallest = i;
    int left = 2*i + 1;
    int right = 2*i + 2;
    
    if (left < pq->size && pq->heap[left]->priority < pq->heap[smallest]->priority)
        smallest = left;
    if (right < pq->size && pq->heap[right]->priority < pq->heap[smallest]->priority)
        smallest = right;
    
    if (smallest != i) {
        swap(&pq->heap[i], &pq->heap[smallest]);
        heapify(pq, smallest);
    }
}

void pq_push(PriorityQueue *pq, Process *p) {
    pq->heap[pq->size++] = p;
    for (int i = pq->size/2 - 1; i >= 0; i--)
        heapify(pq, i);
}

Process* pq_pop(PriorityQueue *pq) {
    if (pq->size == 0) return NULL;
    Process *p = pq->heap[0];
    pq->heap[0] = pq->heap[--pq->size];
    heapify(pq, 0);
    return p;
}

int main() {
    PriorityQueue pq = {0};
    
    Process p1 = {1, "P1", 10, 3};
    Process p2 = {2, "P2", 5, 1};
    Process p3 = {3, "P3", 8, 2};
    
    pq_push(&pq, &p1);
    pq_push(&pq, &p2);
    pq_push(&pq, &p3);
    
    Process *p = pq_pop(&pq);
    printf("Next: %s (priority %d)\n", p->name, p->priority);
    
    return 0;
}
