#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MEGAMORPHIC_THRESHOLD 4

typedef enum {STATE_UNINIT, STATE_MONO, STATE_POLY, STATE_MEGA} CacheState;

typedef struct {
    char method_name[64];
    CacheState state;
    char cached_class[64];
    void *monomorphic_target;
    char poly_targets[10][64];
    void *poly_addrs[10];
    int poly_count;
} InlineCache;

void init_cache(InlineCache *cache, const char *method) {
    strcpy(cache->method_name, method);
    cache->state = STATE_UNINIT;
    cache->poly_count = 0;
}

void* lookup(InlineCache *cache, const char *receiver_class) {
    if (cache->state == STATE_UNINIT) {
        cache->state = STATE_MONO;
        strcpy(cache->cached_class, receiver_class);
        cache->monomorphic_target = (void*)0x1000;
        printf("Cache: monomorphic, class=%s\n", receiver_class);
        return cache->monomorphic_target;
    }
    
    if (cache->state == STATE_MONO) {
        if (strcmp(receiver_class, cache->cached_class) == 0) {
            printf("Cache hit: monomorphic\n");
            return cache->monomorphic_target;
        } else {
            cache->state = STATE_POLY;
            strcpy(cache->poly_targets[cache->poly_count], cache->cached_class);
            cache->poly_addrs[cache->poly_count] = cache->monomorphic_target;
            cache->poly_count++;
            strcpy(cache->poly_targets[cache->poly_count], receiver_class);
            cache->poly_addrs[cache->poly_count] = (void*)0x2000;
            cache->poly_count++;
            printf("Cache: polymorphic transition\n");
            return cache->poly_addrs[cache->poly_count - 1];
        }
    }
    
    if (cache->state == STATE_POLY) {
        for (int i = 0; i < cache->poly_count; i++) {
            if (strcmp(receiver_class, cache->poly_targets[i]) == 0) {
                printf("Cache hit: polymorphic\n");
                return cache->poly_addrs[i];
            }
        }
        
        if (cache->poly_count < MEGAMORPHIC_THRESHOLD) {
            strcpy(cache->poly_targets[cache->poly_count], receiver_class);
            cache->poly_addrs[cache->poly_count] = (void*)(0x3000 + cache->poly_count);
            cache->poly_count++;
            printf("Cache: added new polymorphic target\n");
            return cache->poly_addrs[cache->poly_count - 1];
        } else {
            cache->state = STATE_MEGA;
            printf("Cache: megamorphic\n");
        }
    }
    
    printf("Cache: megamorphic lookup\n");
    return NULL;
}

int main() {
    InlineCache cache;
    init_cache(&cache, "getClass");
    
    lookup(&cache, "ClassA");
    lookup(&cache, "ClassA");
    lookup(&cache, "ClassB");
    lookup(&cache, "ClassC");
    lookup(&cache, "ClassD");
    
    return 0;
}
