#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_HEAP 100

typedef struct {
    int id;
    int size;
    int marked;
    void* data;
    int ref_count;
} Object;

Object* heap[MAX_HEAP];
int heap_count = 0;
int roots[10];
int root_count = 0;

Object* allocate(int size) {
    if (heap_count >= MAX_HEAP) return NULL;
    
    Object* obj = (Object*)malloc(sizeof(Object));
    obj->id = heap_count;
    obj->size = size;
    obj->marked = 0;
    obj->ref_count = 1;
    obj->data = malloc(size);
    
    heap[heap_count++] = obj;
    printf("  Allocated object %d (size: %d)\n", obj->id, size);
    
    return obj;
}

void add_root(Object* obj) {
    if (root_count < 10) {
        roots[root_count++] = obj->id;
        printf("  Added root: object %d\n", obj->id);
    }
}

void mark(Object* obj) {
    if (!obj || obj->marked) return;
    
    obj->marked = 1;
    printf("  Marked object %d\n", obj->id);
    
    int refs[] = {obj->id + 1 < heap_count ? obj->id + 1 : -1};
    for (int i = 0; refs[i] >= 0 && refs[i] < heap_count; i++) {
        if (heap[refs[i]]) {
            mark(heap[refs[i]]);
        }
    }
}

void mark_from_roots() {
    printf("\nMark phase:\n");
    for (int i = 0; i < root_count; i++) {
        mark(heap[roots[i]]);
    }
}

int sweep() {
    int freed = 0;
    printf("\nSweep phase:\n");
    
    for (int i = 0; i < heap_count; i++) {
        if (!heap[i]->marked) {
            printf("  Freeing unmarked object %d\n", heap[i]->id);
            free(heap[i]->data);
            free(heap[i]);
            heap[i] = NULL;
            freed++;
        }
    }
    
    return freed;
}

void collect() {
    printf("=== Mark-Sweep GC Collection ===\n");
    mark_from_roots();
    int freed = sweep();
    printf("\nGC completed, freed %d objects\n", freed);
}

void print_heap_status() {
    printf("\nHeap status:\n");
    for (int i = 0; i < heap_count; i++) {
        if (heap[i]) {
            printf("  Object %d: ref_count=%d, marked=%s\n",
                   heap[i]->id,
                   heap[i]->ref_count,
                   heap[i]->marked ? "yes" : "no");
        }
    }
}

int main() {
    printf("=== Mark-Sweep Garbage Collection ===\n\n");
    
    Object* obj1 = allocate(100);
    Object* obj2 = allocate(200);
    Object* obj3 = allocate(300);
    
    printf("\nAdding roots:\n");
    add_root(obj1);
    add_root(obj3);
    
    print_heap_status();
    
    printf("\nRemoving reference to obj3...\n");
    roots[1] = -1;
    
    collect();
    print_heap_status();
    
    printf("\nAlgorithm:\n");
    printf("  Phase 1: Mark - Mark all reachable objects from roots\n");
    printf("  Phase 2: Sweep - Free all unmarked objects\n");
    
    return 0;
}
