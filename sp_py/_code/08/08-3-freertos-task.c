// FreeRTOS 任務範例
#include "FreeRTOS.h"
#include "task.h"

// 任務函數
void vTask1(void *pvParameters) {
    while(1) {
        // 執行任務工作
        printf("Task 1 running\n");
        vTaskDelay(pdMS_TO_TICKS(100));  // 延遲 100ms
    }
}

void vTask2(void *pvParameters) {
    while(1) {
        printf("Task 2 running\n");
        vTaskDelay(pdMS_TO_TICKS(200));
    }
}

int main() {
    // 建立任務
    xTaskCreate(vTask1, "Task1", 1000, NULL, 1, NULL);
    xTaskCreate(vTask2, "Task2", 1000, NULL, 2, NULL);
    
    // 啟動排程器
    vTaskStartScheduler();
    
    return 0;
}