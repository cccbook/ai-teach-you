#include <stdio.h>
#include <stdlib.h>

#define MAX_HEAP 1000

typedef struct Object {
    int ref_count;
    int marked;
    int value;
    int in_use;
} Object;

Object* heap[MAX_HEAP];
int heap_count = 0;

Object* allocate(int value) {
    for (int i = 0; i < MAX_HEAP; i++) {
        if (!heap[i]->in_use) {
            heap[i]->ref_count = 1;
            heap[i]->marked = 0;
            heap[i]->value = value;
            heap[i]->in_use = 1;
            heap_count++;
            return heap[i];
        }
    }
    return NULL;
}

void reference(Object* obj) {
    if (obj) obj->ref_count++;
}

void dereference(Object** obj_ptr) {
    Object* obj = *obj_ptr;
    if (!obj) return;
    obj->ref_count--;
    if (obj->ref_count == 0) {
        printf("回收記憶體 (value=%d)\n", obj->value);
        obj->in_use = 0;
        heap_count--;
    }
    *obj_ptr = NULL;
}

void mark(Object* obj) {
    if (!obj || obj->marked) return;
    obj->marked = 1;
}

void sweep() {
    int freed = 0;
    for (int i = 0; i < MAX_HEAP; i++) {
        if (heap[i]->in_use && !heap[i]->marked) {
            printf("GC 回收物件 (value=%d)\n", heap[i]->value);
            heap[i]->in_use = 0;
            freed++;
            heap_count--;
        }
    }
    printf("GC 完成，回收 %d 個物件\n", freed);
}

void gc_collect() {
    for (int i = 0; i < MAX_HEAP; i++) {
        if (heap[i]->in_use) heap[i]->marked = 0;
    }
    for (int i = 0; i < MAX_HEAP; i++) {
        if (heap[i]->in_use && heap[i]->ref_count > 0) {
            mark(heap[i]);
        }
    }
    sweep();
}

void init_heap() {
    for (int i = 0; i < MAX_HEAP; i++) {
        heap[i] = (Object*)malloc(sizeof(Object));
        heap[i]->in_use = 0;
    }
}

void free_heap() {
    for (int i = 0; i < MAX_HEAP; i++) {
        free(heap[i]);
    }
}

int main() {
    init_heap();
    
    Object* a = allocate(10);
    Object* b = allocate(20);
    Object* c = allocate(30);
    
    printf("建立物件: a=%d, b=%d, c=%d\n", a->value, b->value, c->value);
    printf("引用計數: a=%d, b=%d, c=%d\n", a->ref_count, b->ref_count, c->ref_count);
    
    reference(a);
    reference(b);
    printf("\n增加引用後:\n");
    printf("引用計數: a=%d, b=%d\n", a->ref_count, b->ref_count);
    
    dereference(&a);
    printf("\ndereference(a) 後: a 的引用計數=%d\n", a ? a->ref_count : -1);
    
    dereference(&b);
    dereference(&c);
    
    printf("\n觸發 GC:\n");
    gc_collect();
    printf("堆中物件數: %d\n", heap_count);
    
    free_heap();
    return 0;
}
