#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SPACE_SIZE 50

typedef struct {
    int id;
    int size;
    int alive;
    int forwarded_to;
} Object;

typedef struct {
    Object* objects[SPACE_SIZE];
    int count;
    int capacity;
} Space;

Space from_space = {.count = 0, .capacity = SPACE_SIZE};
Space to_space = {.count = 0, .capacity = SPACE_SIZE};
Space* current;

void init_space(Space* space) {
    space->count = 0;
    for (int i = 0; i < SPACE_SIZE; i++) {
        space->objects[i] = NULL;
    }
}

Object* allocate_in_space(Space* space, int size) {
    if (space->count >= space->capacity) return NULL;
    
    Object* obj = (Object*)malloc(sizeof(Object));
    obj->id = space->count;
    obj->size = size;
    obj->alive = 1;
    obj->forwarded_to = -1;
    
    space->objects[space->count++] = obj;
    return obj;
}

Object* allocate(int size) {
    Object* obj = allocate_in_space(current, size);
    if (obj) {
        printf("  Allocated object %d in %s (size: %d)\n",
               obj->id,
               current == &from_space ? "from_space" : "to_space",
               size);
    }
    return obj;
}

int is_in_from_space(Object* obj) {
    for (int i = 0; i < from_space.count; i++) {
        if (from_space.objects[i] == obj) return 1;
    }
    return 0;
}

Object* forward(Object* obj) {
    if (!obj) return NULL;
    
    if (obj->forwarded_to >= 0) {
        printf("  Object %d already forwarded to %d\n", obj->id, obj->forwarded_to);
        for (int i = 0; i < to_space.count; i++) {
            if (to_space.objects[i]->id == obj->forwarded_to) {
                return to_space.objects[i];
            }
        }
    }
    
    if (is_in_from_space(obj)) {
        Object* new_obj = allocate_in_space(&to_space, obj->size);
        new_obj->alive = 1;
        obj->forwarded_to = new_obj->id;
        printf("  Forwarded object %d -> %d\n", obj->id, new_obj->id);
        return new_obj;
    }
    
    return obj;
}

void collect(Object* roots[], int root_count) {
    printf("\n=== Copy GC Collection ===\n");
    printf("Swapping spaces...\n\n");
    
    Space* temp = current;
    current = &to_space;
    to_space = *temp;
    init_space(&to_space);
    
    printf("Copying live objects from %s to %s:\n",
           current == &from_space ? "to_space" : "from_space",
           current == &from_space ? "from_space" : "to_space");
    
    for (int i = 0; i < root_count; i++) {
        if (roots[i]) {
            roots[i] = forward(roots[i]);
        }
    }
    
    printf("\nAfter collection:\n");
    printf("  %s: %d objects\n", "from_space", from_space.count);
    printf("  %s: %d objects\n", "to_space", to_space.count);
    printf("  Total space: %d / %d\n", 
           from_space.count + to_space.count, 
           SPACE_SIZE * 2);
}

void print_space(Space* space, const char* name) {
    printf("  %s: [", name);
    for (int i = 0; i < space->count; i++) {
        printf("%d", space->objects[i]->id);
        if (i < space->count - 1) printf(", ");
    }
    printf("]\n");
}

int main() {
    printf("=== Copy Garbage Collection ===\n\n");
    
    current = &from_space;
    init_space(&from_space);
    init_space(&to_space);
    
    printf("Initial allocation:\n");
    Object* obj1 = allocate(100);
    Object* obj2 = allocate(200);
    Object* obj3 = allocate(300);
    
    Object* roots[] = {obj1, obj3};
    
    printf("\n");
    print_space(&from_space, "from_space");
    print_space(&to_space, "to_space");
    
    printf("\nRoots point to objects: 0, 2\n");
    
    collect(roots, 2);
    
    printf("\nAfter GC:\n");
    print_space(&from_space, "from_space");
    print_space(&to_space, "to_space");
    
    printf("\nCopy GC Properties:\n");
    printf("  + No memory fragmentation\n");
    printf("  + Mark + copy in one pass\n");
    printf("  + No sweep phase needed\n");
    printf("  - Uses only half of available memory\n");
    printf("  - Must copy all live objects\n");
    
    return 0;
}
