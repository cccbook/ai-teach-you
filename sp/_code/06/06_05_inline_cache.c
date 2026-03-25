#include <stdio.h>
#include <stdlib.h>

typedef enum {
    UNINITIALIZED,
    MONOMORPHIC,
    POLYMORPHIC,
    MEGAMORPHIC
} CacheState;

const char* state_name(CacheState state) {
    switch(state) {
        case UNINITIALIZED: return "Uninitialized";
        case MONOMORPHIC: return "Monomorphic";
        case POLYMORPHIC: return "Polymorphic";
        case MEGAMORPHIC: return "Megamorphic";
        default: return "Unknown";
    }
}

void* lookup_table[] = {NULL, NULL, NULL, NULL, NULL};
int lookup_count = 0;

void* generic_dispatch(void* receiver, int method_id) {
    printf("[Dispatch] Generic dispatch for receiver %p\n", receiver);
    return NULL;
}

void* inline_cache_miss(void* receiver, void* default_handler) {
    printf("[IC] Cache miss for receiver %p\n", receiver);
    return default_handler;
}

void* inline_cache_hit(void* method_addr) {
    printf("[IC] Cache hit! Direct jump to %p\n", method_addr);
    return method_addr;
}

int main() {
    printf("=== Inline Cache States Demo ===\n\n");
    
    printf("Inline Cache States:\n");
    printf("1. Uninitialized: First call, cache class\n");
    printf("2. Monomorphic: Same class, direct jump\n");
    printf("3. Polymorphic: Few classes, lookup table\n");
    printf("4. Megamorphic: Many classes, generic dispatch\n");
    
    printf("\n=== State Transitions Demo ===\n\n");
    
    CacheState state = UNINITIALIZED;
    void* cached_class = NULL;
    int class_count = 0;
    
    void* classA = (void*)0x1000;
    void* classB = (void*)0x2000;
    void* classC = (void*)0x3000;
    void* classD = (void*)0x4000;
    void* classE = (void*)0x5000;
    
    void* methodA = (void*)0xA000;
    void* methodB = (void*)0xB000;
    void* methodC = (void*)0xC000;
    void* methodD = (void*)0xD000;
    void* methodE = (void*)0xE000;
    
    printf("Call 1: receiver=classA\n");
    if (state == UNINITIALIZED) {
        printf("  State: %s -> ", state_name(state));
        state = MONOMORPHIC;
        cached_class = classA;
        lookup_table[class_count++] = methodA;
        printf("%s\n", state_name(state));
    }
    
    printf("Call 2: receiver=classA\n");
    if (state == MONOMORPHIC && cached_class == classA) {
        printf("  State: %s -> ", state_name(state));
        printf("Direct jump to cached method %p\n", methodA);
    }
    
    printf("Call 3: receiver=classB\n");
    if (state == MONOMORPHIC && cached_class != classB) {
        printf("  State: %s -> ", state_name(state));
        state = POLYMORPHIC;
        lookup_table[class_count++] = methodB;
        printf("%s (lookup table with %d entries)\n", state_name(state), class_count);
    }
    
    printf("Call 4: receiver=classC\n");
    if (state == POLYMORPHIC) {
        printf("  State: %s -> ", state_name(state));
        lookup_table[class_count++] = methodC;
        printf("%s (lookup table with %d entries)\n", state_name(state), class_count);
    }
    
    printf("Call 5: receiver=classD\n");
    if (state == POLYMORPHIC) {
        printf("  State: %s -> ", state_name(state));
        lookup_table[class_count++] = methodD;
        printf("%s (lookup table with %d entries)\n", state_name(state), class_count);
    }
    
    printf("Call 6: receiver=classE\n");
    if (state == POLYMORPHIC) {
        printf("  State: %s -> ", state_name(state));
        lookup_table[class_count++] = methodE;
        state = MEGAMORPHIC;
        printf("%s (switch to generic dispatch)\n", state_name(state));
    }
    
    printf("\nFinal state: %s\n", state_name(state));
    
    return 0;
}
