# 10. 記憶體管理

## 10.1 記憶體管理概述

記憶體管理是程式執行時的關鍵功能，包括堆記憶體配置、垃圾回收、記憶體池管理等。

## 10.2 堆記憶體配置

[程式檔案：10-1-malloc.c](../_code/10/10-1-malloc.c)
```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int* arr = (int*)malloc(10 * sizeof(int));
    for (int i = 0; i < 10; i++) {
        arr[i] = i * i;
    }
    for (int i = 0; i < 10; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    free(arr);
    return 0;
}
```

## 10.3 malloc 與 free 的實現

### 簡單的記憶體配置器

```c
typedef struct block {
    size_t size;
    struct block* next;
    int free;
} block_t;

#define BLOCK_SIZE sizeof(block_t)

void* my_malloc(size_t size) {
    block_t* block = sbrk(0);
    if (sbrk(BLOCK_SIZE + size) == (void*)-1) {
        return NULL;
    }
    block->size = size;
    block->free = 0;
    block->next = NULL;
    return (void*)(block + 1);
}

void my_free(void* ptr) {
    if (!ptr) return;
    block_t* block = ((block_t*)ptr) - 1;
    block->free = 1;
}
```

## 10.4 記憶體池

記憶體池（Memory Pool）是一种預先分配記憶體的技術：

```c
typedef struct mem_pool {
    void* start;
    void* end;
    size_t block_size;
} mem_pool_t;

mem_pool_t* create_pool(size_t block_size, size_t num_blocks) {
    mem_pool_t* pool = malloc(sizeof(mem_pool_t));
    pool->block_size = block_size;
    pool->start = malloc(block_size * num_blocks);
    pool->end = ((char*)pool->start) + (block_size * num_blocks);
    return pool;
}

void* pool_alloc(mem_pool_t* pool) {
    return pool->start;
}
```

## 10.5 垃圾回收

### 參考計數

```c
typedef struct object {
    int ref_count;
    void (*finalize)(struct object*);
} object_t;

void retain(object_t* obj) {
    obj->ref_count++;
}

void release(object_t* obj) {
    obj->ref_count--;
    if (obj->ref_count == 0) {
        obj->finalize(obj);
        free(obj);
    }
}
```

### 標記-清除

```c
void mark_sweep() {
    // 標記階段：從根集合標記所有可達物件
    mark_roots();
    mark_reachable();
    
    // 清除階段：釋放未標記的物件
    sweep_heap();
}
```

## 10.6 記憶體對齊

記憶體對齊是硬體要求：

| 類型 | 大小 | 對齊要求 |
|-----|------|---------|
| char | 1 | 1 |
| short | 2 | 2 |
| int | 4 | 4 |
| long | 8 | 8 |
| double | 8 | 8 |

## 10.7 本章小結

本章介紹了記憶體管理的核心概念：
- 堆記憶體配置（malloc/free）
- 簡單的記憶體配置器實現
- 記憶體池技術
- 垃圾回收機制
- 記憶體對齊

## 練習題

1. 實作一個簡單的記憶體配置器。
2. 比較不同記憶體配置策略的效能。
3. 實作標記-清除垃圾回收演算法。
4. 研究現代記憶體配置器的設計。
