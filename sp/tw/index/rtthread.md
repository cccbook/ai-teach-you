# RT-Thread

## 概述

RT-Thread 是中國開發的開源即時作業系統，專為嵌入式系統設計。RT-Thread 具有優秀的架構設計，支援納核心（Nano）和標準兩種模式，提供豐富的元件和軟體套件。

## 歷史

- **2006**：RT-Thread 1.0.0 發布
- **2019**：RT-Thread 4.0
- **現在**：物聯網和嵌入式廣泛使用

## 架構

```
┌─────────────────────────────────────┐
│         應用層                      │
├─────────────────────────────────────┤
│    元件層 (DFS, Finsh, NW stack)     │
├─────────────────────────────────────┤
│         核心層                      │
│    (核心、排程、驅動、IPC)           │
├─────────────────────────────────────┤
│         硬體抽象層                  │
│      (BSP, 驅動程式)                │
└─────────────────────────────────────┘
```

## 基本使用

### 1. 執行緒

```c
#include <rtthread.h>

void thread_entry(void *parameter) {
    while (1) {
        rt_kprintf("執行中\n");
        rt_thread_mdelay(1000);
    }
}

int thread_sample(void) {
    rt_thread_t tid = rt_thread_create(
        "thread",               // 名稱
        thread_entry,          // 入口
        RT_NULL,               // 參數
        2048,                  // 堆疊大小
        15,                    // 優先級
        10                     // 時間片
    );
    
    if (tid != RT_NULL) {
        rt_thread_startup(tid);
    }
    
    return 0;
}
MSH_CMD_EXPORT(thread_sample, thread sample);
```

### 2. 訊號量

```c
rt_sem_t sem;

sem = rt_sem_create("sem", 0, RT_IPC_FLAG_FIFO);

// 發送信號
rt_sem_release(sem);

// 等待信號
rt_sem_take(sem, RT_WAITING_FOREVER);
```

### 3. 訊息佇列

```c
rt_mq_t mq;

mq = rt_mq_create("mq", 40, 10, RT_IPC_FLAG_FIFO);

// 發送
rt_mq_send(mq, &msg, sizeof(msg));

// 接收
rt_mq_recv(mq, &msg, sizeof(msg), RT_WAITING_FOREVER);
```

### 4. 互斥鎖

```c
rt_mutex_t mutex;

mutex = rt_mutex_create("mutex", RT_IPC_FLAG_FIFO);

rt_mutex_take(mutex, RT_WAITING_FOREVER);
// 臨界區域
rt_mutex_release(mutex);
```

### 5. 軟體計時器

```c
void timer_callback(void *parameter) {
    rt_kprintf("計時器觸發\n");
}

rt_timer_t timer;

timer = rt_timer_create(
    "timer",
    timer_callback,
    RT_NULL,
    1000,
    RT_TIMER_FLAG_PERIODIC
);

rt_timer_start(timer);
```

### 6. 環境變數

```c
// 設定環境變數
rt_set_env_val("dbg", "1");

// 取得環境變數
char *value = rt_get_env_val("dbg");
```

## FinSH  shell

```bash
# RT-Thread 內建命令列 shell
msh /> list_thread
msh /> list_timer
msh /> list_sem
msh /> list_mq
msh /> free
```

## 為什麼使用 RT-Thread？

1. **國產**：中文文件和支援
2. **元件豐富**：完整的生態
3. **輕量級**：Nano 模式極小
4. **活躍**：持續開發

## 參考資源

- rt-thread.org
- RT-Thread 程式碼
