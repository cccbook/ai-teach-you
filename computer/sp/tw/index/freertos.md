# FreeRTOS

## 概述

FreeRTOS 是一個熱門的開源即時作業系統，專為資源受限的嵌入式系統設計。FreeRTOS 支援多種微控制器架構，功耗低、程式碼精簡，廣泛應用於物聯網和嵌入式裝置。

## 歷史

- **2003**：Richard Barry 發布 FreeRTOS
- **2017**：Amazon 收購
- **現在**：AWS IoT 支援

## 基本使用

### 1. 任務建立

```c
#include "FreeRTOS.h"
#include "task.h"

void vTaskFunction(void *pvParameters) {
    for (;;) {
        // 任務程式碼
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

int main() {
    xTaskCreate(
        vTaskFunction,          // 任務函數
        "TaskName",             // 任務名稱
        configMINIMAL_STACK_SIZE, // 堆疊大小
        NULL,                   // 參數
        1,                      // 優先級
        NULL                    // 任務控制塊指標
    );
    
    vTaskStartScheduler();
    
    return 0;
}
```

### 2. 延遲和計時

```c
// 相對延遲
vTaskDelay(pdMS_TO_TICKS(1000));  // 延遲 1 秒

// 絕對延遲（可用於週期性任務）
TickType_t xLastWakeTime = xTaskGetTickCount();
const TickType_t xPeriod = pdMS_TO_TICKS(100);

for (;;) {
    vTaskDelayUntil(&xLastWakeTime, xPeriod);
}
```

### 3. 訊號量

```c
SemaphoreHandle_t xSemaphore;

xSemaphore = xSemaphoreCreateBinary();

void ISR_Handler(void) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    xSemaphoreGiveFromISR(xSemaphore, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

void task_function(void *param) {
    for (;;) {
        if (xSemaphoreTake(xSemaphore, portMAX_DELAY) == pdTRUE) {
            // 處理事件
        }
    }
}
```

### 4. 訊息佇列

```c
QueueHandle_t xQueue;

xQueue = xQueueCreate(10, sizeof(int));

void producer(void *param) {
    int value = 42;
    xQueueSend(xQueue, &value, 0);
}

void consumer(void *param) {
    int value;
    xQueueReceive(xQueue, &value, portMAX_DELAY);
}
```

### 5. 互斥鎖

```c
SemaphoreHandle_t xMutex;

xMutex = xSemaphoreCreateMutex();

void task_function(void *param) {
    if (xSemaphoreTake(xMutex, portMAX_DELAY) == pdTRUE) {
        // 臨界區域
        xSemaphoreGive(xMutex);
    }
}
```

### 6. 軟體計時器

```c
void timer_callback(TimerHandle_t xTimer) {
    // 計時器回調
}

TimerHandle_t xTimer;

xTimer = xTimerCreate(
    "Timer",                    // 名稱
    pdMS_TO_TICKS(1000),       // 週期
    pdTRUE,                    // 自動重載
    NULL,                      // ID
    timer_callback             // 回調函數
);

xTimerStart(xTimer, 0);
```

## 配置

```c
// FreeRTOSConfig.h
#define configUSE_PREEMPTION        1
#define configUSE_PORT_OPTIMIZED_TASK_SELECTION  1
#define configUSE_TICKLESS_IDLE    0
#define configCPU_CLOCK_HZ         ( 72000000UL )
#define configTICK_RATE_HZ        ( 1000 )
#define configMAX_PRIORITIES      ( 5 )
#define configMINIMAL_STACK_SIZE  ( 128 )
#define configTOTAL_HEAP_SIZE     ( 17 * 1024 )
```

## 為什麼使用 FreeRTOS？

1. **開源免費**：商業友好
2. **輕量級**：資源受限環境
3. **跨平台**：多種 MCU 支援
4. **社群活躍**：大量文件和範例

## 參考資源

- FreeRTOS.org
- "Mastering FreeRTOS"
