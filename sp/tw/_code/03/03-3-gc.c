#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_HEAP 100
#define MAX_ROOTS 10

typedef enum { OBJ_NUM, OBJ_BINOP } ObjType;

typedef struct Object {
    int id;
    ObjType type;
    int value;
    int ref_count;
    struct Object* left;
    struct Object* right;
    int marked;
} Object;

Object* heap[MAX_HEAP];
int heap_count = 0;
Object* roots[MAX_ROOTS];
int root_count = 0;

Object* allocate_num(int value) {
    Object* obj = (Object*)malloc(sizeof(Object));
    obj->id = heap_count++;
    obj->type = OBJ_NUM;
    obj->value = value;
    obj->ref_count = 0;
    obj->marked = 0;
    obj->left = obj->right = NULL;
    heap[obj->id] = obj;
    return obj;
}

Object* allocate_binop(char op, Object* left, Object* right) {
    Object* obj = (Object*)malloc(sizeof(Object));
    obj->id = heap_count++;
    obj->type = OBJ_BINOP;
    obj->ref_count = 0;
    obj->marked = 0;
    obj->left = left;
    obj->right = right;
    heap[obj->id] = obj;
    return obj;
}

void add_root(Object* obj) {
    if (obj) roots[root_count++] = obj;
}

void remove_root(Object* obj) {
    for (int i = 0; i < root_count; i++) {
        if (roots[i] == obj) {
            roots[i] = roots[--root_count];
            break;
        }
    }
}

void mark(Object* obj) {
    if (!obj || obj->marked) return;
    obj->marked = 1;
    if (obj->type == OBJ_BINOP) {
        mark(obj->left);
        mark(obj->right);
    }
}

void sweep() {
    int freed = 0;
    for (int i = 0; i < heap_count; i++) {
        Object* obj = heap[i];
        if (obj && !obj->marked) {
            printf("GC 回收: Object(id=%d, type=%s, value=%d)\n",
                   obj->id, 
                   obj->type == OBJ_NUM ? "NUM" : "BINOP",
                   obj->value);
            free(obj);
            heap[i] = NULL;
            freed++;
        }
    }
    printf("GC 完成，回收 %d 個物件\n", freed);
}

void collect() {
    printf("開始 GC...\n");
    for (int i = 0; i < root_count; i++) {
        mark(roots[i]);
    }
    sweep();
    for (int i = 0; i < heap_count; i++) {
        if (heap[i]) heap[i]->marked = 0;
    }
}

int evaluate(Object* obj) {
    if (!obj) return 0;
    if (obj->type == OBJ_NUM) return obj->value;
    int l = evaluate(obj->left);
    int r = evaluate(obj->right);
    return l + r;  // 簡化：只支援加法
}

void gc_demo() {
    Object* a = allocate_num(10);
    Object* b = allocate_num(20);
    Object* c = allocate_binop('+', a, b);
    
    add_root(a);
    add_root(b);
    add_root(c);
    
    printf("建立物件後，堆中有 %d 個物件\n", heap_count);
    
    remove_root(a);
    remove_root(b);
    remove_root(c);
    
    collect();
    
    printf("GC 後，堆中剩餘 %d 個物件\n", heap_count);
}

int main() {
    gc_demo();
    return 0;
}
