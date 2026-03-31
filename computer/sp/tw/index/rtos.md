# RTOS (Real-Time Operating System)

## 概述

即時作業系統（RTOS）是保證在確定的時間內回應事件的作業系統。RTOS 廣泛應用於工業控制、汽車電子、航空航天等需要確定性回應的領域。

## 歷史

- **1978**：早期的 RTOS 出現
- **1980s**：VxWorks、QNX 發展
- **1990s**：RTLinux
- **2000s**：多種開源 RTOS
- **現在**：物聯網嵌入式應用

## RTOS 特點

### 1. 確定性

```c
// 確定性任務調度
void task_function(void *param) {
    // 執行時間確定
    for (int i = 0; i < 100; i++) {
        process();
    }
}

// 設定任務優先級
osPriority_t priority = osPriorityHigh;
osThreadDef(task_function, priority, 1, 0);
```

### 2. 搶佔式排程

```c
// 搶佔式排程確保高優先級任務立即執行
void high_priority_task(void *arg) {
    while (1) {
        // 及時處理緊急事件
        handle_critical_event();
    }
}

void low_priority_task(void *arg) {
    while (1) {
        // 普通任務
        process_data();
    }
}
```

### 3. 中斷處理

```c
// 快速中斷處理
void ISR_Handler(void) {
    // 最小化 ISR 中的處理
    // 標記事件，延後到任務處理
    event_pending = 1;
}

// 延後中斷服務
void deferred_handler(void *arg) {
    while (1) {
        if (event_pending) {
            process_event();
            event_pending = 0;
        }
        osDelay(1);
    }
}
```

### 4. 優先級繼承

```c
// 避免優先級反轉
// 當高優先級任務等待低優先級任務持有的資源時
// 臨時提升低優先級任務的優先級
mutex_t resource_mutex;

// 獲取資源時
void lock_resource() {
    mutex_lock(&resource_mutex);
    // 進入臨界區
}

// 釋放資源時
void unlock_resource() {
    mutex_unlock(&resource_mutex);
}
```

## RTOS 核心概念

### 1. 任務（Task）

```c
// 任務控制區塊
typedef struct {
    void *stack;
    uint32_t stack_size;
    osPriority priority;
    const char *name;
    uint32_t execution_time;
} osThreadDef_t;
```

### 2. 訊息佇列

```c
osMessageQId msg_queue;
osMessageQDef(queue, 16, uint32_t);

void producer(void *arg) {
    uint32_t msg = 1;
    osMessagePut(msg_queue, msg, 0);
}

void consumer(void *arg) {
    osEvent event = osMessageGet(msg_queue, osWaitForever);
}
```

### 3. 訊號量

```c
osSemaphoreId sem_id;
osSemaphoreDef(sem);

void task1(void *arg) {
    osSemaphoreWait(sem_id, osWaitForever);
    // 使用共享資源
    osSemaphoreRelease(sem_id);
}
```

## 為什麼學習 RTOS？

1. **嵌入式開發**：硬即時需求
2. **工業控制**：確定性控制
3. **物聯網**：資源受限環境
4. **效能優化**：確定性延遲

## 參考資源

- "Real-Time Systems"
- FreeRTOS 文檔
- Micrium uC/OS
