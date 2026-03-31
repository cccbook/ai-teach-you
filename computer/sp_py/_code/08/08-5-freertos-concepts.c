// FreeRTOS 核心概念

// 1. 佇列（Queue）
QueueHandle_t xQueue;

void producer(void *pvParameters) {
    int data = 1;
    xQueueSend(xQueue, &data, portMAX_DELAY);
}

void consumer(void *pvParameters) {
    int data;
    xQueueReceive(xQueue, &data, portMAX_DELAY);
}

// 2. 訊號量（Semaphore）
SemaphoreHandle_t xSemaphore;

void task1(void *pvParameters) {
    xSemaphoreTake(xSemaphore, portMAX_DELAY);
    // 進入臨界區
    // ...
    xSemaphoreGive(xSemaphore);
}

// 3. 互斥鎖（Mutex）
SemaphoreHandle_t xMutex;

void access_resource(void *pvParameters) {
    xSemaphoreTake(xMutex, portMAX_DELAY);
    // 獨佔存取資源
    xSemaphoreGive(xMutex);
}

// 4. 軟體定時器
void vTimerCallback(TimerHandle_t xTimer) {
    printf("定時器觸發\n");
}

// 5. 堆疊溢位檢測
void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName) {
    printf("堆疊溢位: %s\n", pcTaskName);
}