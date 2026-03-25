# 執行緒 (Thread)

## 概述

執行緒是程序內的執行單元，是 CPU 調度的基本單位。一個程序可以包含多個執行緒，同一程序內的執行緒共享資源（記憶體、檔案），但各有自己的堆疊和暫存器。

## 歷史

- **1980s**：Mach 引入執行緒概念
- **1990s**：POSIX threads 標準化
- **2000s**：NPTL（Native POSIX Threads）
- **現在**：多核並發必備

## 執行緒模型

### 1. 執行緒 vs 程序

```
程序 A                 程序 B
┌──────────────┐      ┌──────────────┐
│ 執行緒 1     │      │ 執行緒 1     │
│ (堆疊, 暫存) │      │ (堆疊, 暫存) │
├──────────────┤      ├──────────────┤
│ 執行緒 2     │      │              │
│ (堆疊, 暫存) │      │              │
├──────────────┤      │              │
│ 執行緒 3     │      │              │
│ (堆疊, 暫存) │      │              │
├──────────────┤      │              │
│ 共享資源:    │      │ 共享資源:    │
│ - 記憶體    │      │ - 記憶體    │
│ - 檔案      │      │ - 檔案      │
│ - 全域變數  │      │ - 全域變數  │
└──────────────┘      └──────────────┘
```

### 2. POSIX Threads

```c
#include <pthread.h>

void* thread_function(void *arg) {
    int *num = (int *)arg;
    printf("執行緒執行: %d\n", *num);
    sleep(1);
    return NULL;
}

int main() {
    pthread_t thread;
    int arg = 42;
    
    // 建立執行緒
    pthread_create(&thread, NULL, thread_function, &arg);
    
    // 等待執行緒結束
    pthread_join(thread, NULL);
    
    printf("執行緒完成\n");
    return 0;
}
```

### 3. 執行緒同步

```c
// Mutex
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

pthread_mutex_lock(&mutex);
// 臨界區域
pthread_mutex_unlock(&mutex);

// 條件變數
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
pthread_cond_wait(&cond, &mutex);
pthread_cond_signal(&cond);
pthread_cond_broadcast(&cond);
```

### 4. 執行緒本地儲存

```c
// TLS - Thread Local Storage
__thread int counter;  // GCC 擴展

// 或使用
pthread_key_t key;
pthread_key_create(&key, NULL);
pthread_setspecific(key, value);
void *val = pthread_getspecific(key);
```

### 5. 執行緒取消

```c
// 取消執行緒
pthread_cancel(thread);

// 設置取消點
pthread_testcancel();

// 清理處理
void cleanup(void *arg) {
    printf("清理\n");
}

pthread_cleanup_push(cleanup, NULL);
// 臨界區域
pthread_cleanup_pop(1);
```

### 6. C++11 Threads

```cpp
#include <thread>
#include <mutex>
#include <future>

void worker(int id) {
    std::cout << "執行緒 " << id << "\n";
}

int main() {
    std::thread t1(worker, 1);
    std::thread t2(worker, 2);
    
    t1.join();
    t2.join();
}

// async
std::future<int> fut = std::async([]() {
    return 42;
});
int result = fut.get();
```

## 執行緒池

```c
typedef struct {
    pthread_t *threads;
    int thread_count;
    void (*task_fn)(void *);
    void *task_arg;
    pthread_mutex_t lock;
    pthread_cond_t cond;
    int shutdown;
} thread_pool_t;

void thread_pool_init(thread_pool_t *pool, int num_threads);
void thread_pool_submit(thread_pool_t *pool, void (*fn)(void*), void *arg);
void thread_pool_destroy(thread_pool_t *pool);
```

## 為什麼學習執行緒？

1. **並發**：多核並行
2. **效能**：回應性提升
3. **同步**：正確同步
4. **現代 C++**：標準支援

## 參考資源

- "The POSIX Threads Programming"
- Pthreads Tutorial
- C++11 Threads
