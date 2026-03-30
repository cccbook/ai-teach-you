# 8. 嵌入式作業系統

## 8.1 嵌入式系統特性與限制

### 8.1.1 嵌入式系統的定義與分類

嵌入式系統是專為特定功能設計的電腦系統，通常作為更大系統的一部分。與通用計算機不同，嵌入式系統有著獨特的設計約束和最佳化目標。

**嵌入式系統的分類**

| 分類標準 | 類型 | 說明 |
|----------|-------|------|
| 複雜度 | 微控制器 | 8/16 位元 MCU，資源極受限 |
| | 應用處理器 | 32 位元，支援 OS |
| | 系統單晶片 | 多核，整合週邊 |
| 即時性 | 無即時要求 | 消費電子、娛樂裝置 |
| | 軟即時 | 回應時間影響體驗 |
| | 硬即時 | 錯過截止時間後果嚴重 |
| 連網性 | 獨立裝置 | 無網路功能 |
| | 連網裝置 | WiFi、BLE、ZigBee |
| | 閘道裝置 | 多種協定橋接 |

**嵌入式系統的特點**

| 特點 | 說明 | 設計考量 |
|------|------|----------|
| 專用性 | 單一或少數功能 | 功能精簡、介面最佳化 |
| 資源受限 | CPU/記憶體/儲存有限 | 深度最佳化 |
| 即時性 | 確定性回應時間 | RTOS、優先級管理 |
| 功耗敏感 | 常用於行動裝置 | DVFS、省電模式 |
| 可靠性 | 長期穩定運行 | 看門狗、ECC |
| 成本敏感 | 大量生產 | BOM 成本最佳化 |

### 8.1.2 嵌入式系統的資源限制

**典型資源約束**

| 資源類型 | 低端微控制器 | 中端 MCU | 高端嵌入式 SoC |
|-----------|--------------|----------|----------------|
| CPU 時脈 | 8-16 MHz | 50-200 MHz | 500+ MHz - 2 GHz |
| RAM | 128B - 2KB | 16-512 KB | 256MB - 4GB |
| Flash/ROM | 4-32 KB | 128KB - 8MB | 4GB+ |
| 功耗 | μW - mW | mW | 100mW - 數W |
| 價格 | < $1 | $1-10 | $10-100+ |

**資源估算理論**

```c
// 嵌入式系統資源估算原理

// 程式碼大小估算：
// - Thumb-2 指令集平均：2-4 位元組/指令
// - 完整 C 程式每行約：4-8 位元組
// - 僅資料：實際大小 + 對齊填充

// RAM 使用估算：
// - 靜態資料：(全域變數 + 靜態變數) × 1（對齊）
// - 堆疊需求：最深呼叫鏈 × 每層最大區域變數 + 中斷堆疊
// - 堆積需求：動態配置峰值

// 計算範例：
// 任務：A/D 採集 + 簡單濾波 + UART 傳輸

// RAM 需求：
// - 全域緩衝區：128 位元組 (10 個樣本 × 12 位元 + 對齊)
// - 堆疊：64 位元組 (主函數 16 + 中斷 32 + 子函數 16)
// - 總計：約 200 位元組

// Flash 需求：
// - 程式碼：~4KB (約 1000 行 C)
// - 常數資料：~1KB
// - 總計：約 5KB
```

### 8.1.3 即時系統的理論基礎

即時系統對時間約束有嚴格要求，其設計理論與通用系統有本質不同。

**即時系統的分類**

```
┌─────────────────────────────────────────────────────────────┐
│                    即時系統分類                           │
├─────────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐│
│  │  硬即時系統   │  │  軟即時系統   │  │  確定性系統   ││
│  ├───────────────┤  ├───────────────┤  ├───────────────┤│
│  │ Deadline 必達 │  │ Deadline 最好 │  │ 回應時間可 ││
│  │ 否則後果嚴重  │  │ 達到，偶爾    │  │ 預測       ││
│  │               │  │ 違背可接受    │  │             ││
│  ├───────────────┤  ├───────────────┤  ├───────────────┤│
│  │ 安全氣囊      │  │ 音訊播放      │  │ 工業控制    ││
│  │ 航空控制      │  │ 網路電話      │  │ 馬達控制    ││
│  │ ABS 制動      │  │ 遊戲渲染      │  │ 馬達控制    ││
│  └───────────────┘  └───────────────┘  └───────────────┘│
│                                                         │
└─────────────────────────────────────────────────────────────┘
```

**即時系統的時間約束**

| 約束類型 | 說明 | 數學表示 |
|----------|------|----------|
| 響應時間 | 從事件到處理完成的時間 | $R = C + B + \sum_{h.p}{Ceiling(R, P_h)}$ |
| 潛伏時間 | 中斷到 ISR 執行的時間 | $L = L_{hw} + L_{os}$ |
| 截止時間 | 任務必須完成的時間 | $D$ |
| 週期 | 任務重複執行的間隔 | $T$ 或 $P$ |

### 8.1.4 嵌入式系統的功耗管理

功耗是嵌入式系統的關鍵設計考量。

**功耗組成**

| 組成 | 說明 | 影響因素 |
|------|------|----------|
| 動態功耗 | 電路切換消耗 | $P_{dyn} = CV^2f$ |
| 洩漏功耗 | 靜態電流消耗 | $P_{leak} = V \cdot I_{leak}$ |
| 短路功耗 | PMOS/NMOS 同時導通 | $P_{sc} = V \cdot I_{sc}$ |

**功耗最佳化策略**

| 策略 | 說明 | 應用場景 |
|------|------|----------|
| DVFS | 動態電壓/頻率調整 | 依負載調整 |
| PMU | 電源管理單元 | 進入低功耗模式 |
| 關閉時脈 | 停止未使用模組 | 未使用周邊 |
| 關閉電源 | 完全關閉模組 | 長時間不用 |

## 8.2 即時作業系統（RTOS）概念

### 8.2.1 RTOS 的設計原則

即時作業系統（Real-Time Operating System）提供確定性的任務排程和快速上下文切換。

**RTOS 與通用 OS 的核心差異**

| 特性 | RTOS | 通用 OS |
|------|-------|----------|
| 排程確定性 | 可預測、可證明 | 較難預測 |
| 上下文切換 | 微秒級 | 毫秒級 |
| 記憶體佔用 | 數 KB - 數百 KB | 數百 MB |
| 優先級反轉處理 | 必須處理 | 可選 |
| 開機時間 | 毫秒級 | 秒級 |

**RTOS 的核心元件**

```
┌─────────────────────────────────────────────────────────────┐
│                    RTOS 架構                               │
├─────────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────────┐│
│  │                 應用程式                              ││
│  └─────────────────────────────────────────────────────┘│
│                            │                              │
│                            ▼                              │
│  ┌─────────────────────────────────────────────────────┐│
│  │              API 層 (任務、排程、IPC)                  ││
│  └─────────────────────────────────────────────────────┘│
│                            │                              │
│                            ▼                              │
│  ┌─────────────────────────────────────────────────────┐│
│  │              核心層 (任務管理、排程器、計時器)          ││
│  └─────────────────────────────────────────────────────┘│
│                            │                              │
│                            ▼                              │
│  ┌─────────────────────────────────────────────────────┐│
│  │           BSP (Board Support Package)                ││
│  └─────────────────────────────────────────────────────┘│
│                            │                              │
│                            ▼                              │
│  ┌─────────────────────────────────────────────────────┐│
│  │                    硬體                              ││
│  └─────────────────────────────────────────────────────┘│
│                                                         │
└─────────────────────────────────────────────────────────────┘
```

### 8.2.2 任務管理與狀態機

RTOS 中的任務（Task）是執行的基本單位，相當於通用 OS 的執行緒。

**任務狀態機**

```
                    ┌──────────────────┐
                    │                  │
                    │    創建 (Create)  │
                    │                  │
                    └────────┬─────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│    ┌─────────────────────────────────────────────────────┐    │
│    │                     就緒 (Ready)                      │    │
│    │  任務已建立，等待獲得 CPU                              │    │
│    └─────────────────────────────────────────────────────┘    │
│                              ▲                              │
│                              │ 排程器選擇                    │
│                              │                              │
│    ┌─────────────────────────┴────────────────────────────┐  │
│    │                                                        │  │
│    │                         執行 (Running)                │  │
│    │                   任務正在 CPU 上執行                  │  │
│    │                                                        │  │
│    └──────────┬─────────────────────────────┬─────────────┘  │
│               │                             │                │
│               │ 自願讓出                  │ 時間片用完     │
│               ▼                             ▼                │
│    ┌───────────────────┐    ┌───────────────────────┐    │
│    │   延遲 (Delayed)   │    │    就緒 (Ready)       │    │
│    │ vTaskDelay() 暫停    │    │  回到就緒佇列         │    │
│    └───────────────────┘    └───────────────────────────┘    │
│                              │                              │
│                              ▼                              │
│    ┌─────────────────────────────────────────────────────┐    │
│    │                    阻塞 (Blocked)                    │    │
│    │    等待事件：I/O、訊號量、佇列、互斥鎖              │    │
│    └─────────────────────────────────────────────────────┘    │
│                              │                              │
│                              │ 事件發生                      │
│                              ▼                              │
│                        ┌──────────────────┐                  │
│                        │                  │                  │
│                        │     刪除       │                  │
│                        │   (Terminate)    │                  │
│                        └──────────────────┘                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**任務控制區塊（TCB）**

```c
// RTOS 任務控制區塊結構
typedef struct tskTaskControlBlock {
    volatile StackType_t* pxTopOfStack;    // 堆疊頂部指標
    StackType_t* pxStack;                  // 堆疊起始位址
    
    // 任務屬性
    char pcTaskName[configMAX_TASK_NAME_LEN];
    UBaseType_t uxPriority;               // 優先級 (0 最高)
    TaskParameters_t xRunTimeCounter;       // 執行時間計數
    
    // 狀態
    ListItem_t xStateListItem;            // 狀態鏈結節點
    ListItem_t xEventListItem;            // 事件鏈結節點
    
    // 通知
    uint32_t ulNotifiedValue[configTASK_NOTIFICATION_ARRAY_SIZE];
    uint8_t ucNotifyState;
    
    // 棧框架指標 (用于 context switch)
    #if portUSING_MPU_WRAPPERS
        xMPU_SETTINGS xMPUSettings;
    #endif
} tskTCB;
```

### 8.2.3 RTOS 排程器理論

**優先級排程**

RTOS 通常使用固定優先級搶占式排程：

| 排程類型 | 說明 | 範例 |
|----------|------|------|
| 固定優先級 | 每個任務優先級固定 | FreeRTOS, RT-Thread |
| 動態優先級 | 任務優先級可改變 | Rate Monotonic |
| 混合優先級 | 混合使用 | - |

**搶占式 vs 協作式**

| 模式 | 說明 | 優點 | 缺點 |
|------|------|------|------|
| 搶占式 | 高優先級任務可隨時中斷低優先級任務 | 即時響應好 | 鎖競爭多 |
| 協作式 | 任務主動讓出 CPU | 簡單確定 | 響應差 |

**Rate Monotonic Scheduling (RMS)**

RMS 是經典的即時排程理論：

```
定理（Liu & Layland, 1973）：
對於 n 個獨立週期任務，若使用固定優先級排程，
且優先級與週期成反比（短週期 = 高優先級），
則可排程條件為：

Σ (Ci/Ti) ≤ n(2^(1/n) - 1)

其中：
- Ci = 任務 i 的執行時間
- Ti = 任務 i 的週期
```

### 8.2.4 優先級反轉問題

優先級反轉是 RTOS 中的經典問題，可能導致系統失效。

**問題描述**

```
時間線：
|----T0----|----T1----|----T2----|----T3----|----T4----|

高優先級 H 任務 ────────────────────────── 等待
                  │                         
中優先級 M 任務 ─── 執行中 ─── 執行中 ──── 不等 H
                  │              │
低優先級 L 任務 ──── 等資源 ─── 執行中 ──── 等 H

結果：H 被 M 阻塞！M 的優先級低於 H，卻阻止了 H 執行。
```

**優先級繼承（Priority Inheritance）**

解決方案：讓持有資源的低優先級任務暫時繼承等待它的高優先級任務。

```c
// 優先級繼承示意
void priority_inheritance_example() {
    // 初始狀態
    // H 任務 (優先級 3) 等待資源 R
    // L 任務 (優先級 1) 持有資源 R
    // M 任務 (優先級 2) 執行中
    
    // 當 H 等待 L 持有的資源時：
    // L 暫時提升到優先級 3（與 H 相同）
    // M 無法搶占 L
    // L 快速釋放資源後恢復優先級 1
    // H 獲得資源，繼續執行
}
```

### 8.2.5 臨界區保護

RTOS 提供多種臨界區保護機制：

| 機制 | 說明 | 適用場景 |
|------|------|----------|
| 臨界區 | 全域中斷/排程禁用 | 極短臨界區 |
| 互斥鎖 | 遞迴安全互斥 | 資源保護 |
| 二元訊號量 | 簡單互斥 | 訊號同步 |
| 計數訊號量 | 資源計數 | 生產者/消費者 |

## 8.3 FreeRTOS、RT-Thread 介紹

### 8.3.1 FreeRTOS 架構

FreeRTOS 是最流行的開源 RTOS 之一，以精簡高效著稱。

**核心架構**

```
┌─────────────────────────────────────────────────────────────┐
│                    FreeRTOS 應用程式                        │
├─────────────────────────────────────────────────────────────┤
│  xTaskCreate() | vTaskDelay() | xSemaphoreTake() ...     │
├─────────────────────────────────────────────────────────────┤
│                     任務管理                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Idle     │ │ Timer    │ │ App Task │ │ App Task │  │
│  │ Task     │ │ Task     │ │ 1        │ │ 2        │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
├─────────────────────────────────────────────────────────────┤
│                     排程器                                 │
│  ┌────────────────────────────────────────────────────┐ │
│  │  vTaskSwitchContext() | portYIELD() | ISR Exit      │ │
│  └────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                     核心                                 │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │ List   │ │ Queue  │ │ Timer  │ │ Heap   │        │
│  │        │ │        │ │        │ │        │        │
│  └────────┘ └────────┘ └────────┘ └────────┘        │
├─────────────────────────────────────────────────────────────┤
│                     Port 層                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │ ARM CM │ │ ARMv8-M│ │ RISC-V │ │ ESP32   │        │
│  └────────┘ └────────┘ └────────┘ └────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**任務建立與管理**

```c
#include "FreeRTOS.h"
#include "task.h"

// 任務函數
void vTaskFunction(void *pvParameters) {
    const char *pcTaskName = (const char *)pvParameters;
    
    for(;;) {
        // 任務邏輯
        printf("%s is running\n", pcTaskName);
        
        // 延遲 100ms
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void app_main(void) {
    TaskHandle_t xTaskHandle = NULL;
    
    // 建立任務
    BaseType_t xResult = xTaskCreate(
        vTaskFunction,                    // 任務函數
        "Task1",                         // 任務名稱
        configMINIMAL_STACK_SIZE * 2,     // 堆疊大小
        "Task1",                         // 參數
        1,                               // 優先級 (1)
        &xTaskHandle                     // 任務控制代柄
    );
    
    if (xResult == pdPASS) {
        printf("Task created successfully\n");
    }
    
    // 任務刪除
    // vTaskDelete(xTaskHandle);
}
```

**訊號量與互斥鎖**

```c
// 二元訊號量
SemaphoreHandle_t xBinarySemaphore;

void ISR_Handler(void) {
    // 給予訊號量（在 ISR 中使用 FromISR 版本）
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    xSemaphoreGiveFromISR(xBinarySemaphore, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

void vTaskFunction(void *pvParameters) {
    for(;;) {
        // 獲取訊號量（阻塞等待）
        if (xSemaphoreTake(xBinarySemaphore, portMAX_DELAY) == pdTRUE) {
            // 處理事件
        }
    }
}
```

### 8.3.2 RT-Thread 架構

RT-Thread 是中國開源的微型即時作業系統，以豐富元件和活躍社群著稱。

**RT-Thread 特色架構**

```
┌─────────────────────────────────────────────────────────────┐
│                      應用程式                              │
├─────────────────────────────────────────────────────────────┤
│                      FinSH Shell                          │
├─────────────────────────────────────────────────────────────┤
│                      元件層                               │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌───────┐ │
│  │ 檔案系統│ │ 網路堆疊│ │  GUI   │ │  TLS   │ │ mbedTLS│ │
│  │ (DFS)  │ │  (SAL)  │ │ (GUI)  │ │        │ │       │ │
│  └────────┘ └────────┘ └────────┘ └────────┘ └───────┘ │
├─────────────────────────────────────────────────────────────┤
│                      軟體元件                            │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │   POSIX │ │ 設備框架│ │ 驅動框架│ │  應用框架│        │
│  └────────┘ └────────┘ └────────┘ └────────┘        │
├─────────────────────────────────────────────────────────────┤
│                      RT-Thread Core                      │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │ 執行緒  │ │ 排程器  │ │  IPC   │ │ 記憶體  │        │
│  └────────┘ └────────┘ └────────┘ └────────┘        │
├─────────────────────────────────────────────────────────────┤
│                      抽象層 (HAL)                        │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │  CPU   │ │ 計時器  │ │  中斷  │ │ 訊號   │        │
│  └────────┘ └────────┘ └────────┘ └────────┘        │
├─────────────────────────────────────────────────────────────┤
│                      BSP / 驅動                           │
└─────────────────────────────────────────────────────────────┘
```

**RT-Thread 元件**

| 元件 | 說明 | 特色 |
|------|------|------|
| 執行緒管理 | 搶占式排程，支援 256 優先級 | 支援時間片 |
| IPC 系統 | 訊號量、互斥鎖、事件、訊息佇列 | 統一的同步介面 |
| 軟體計時器 | 單次/週期計時器 | 硬體計時器卸載 |
| 記憶體堆 | 多種配置策略 | 靜態/動態混合 |
| 裝置框架 | 統一的裝置管理 | PIN、I2C、SPI |
| 檔案系統 | DFS (ext4, FAT,UFFS) | POSIX 介面 |
| 網路框架 | TCP/IP, LwIP, AT 元件 | SAL 抽象層 |

## 8.4 驅動程式開發

### 8.4.1 驅動程式的角色與分類

驅動程式是作業系統與硬體之間的橋樑，負責封裝和控制硬體裝置。

**驅動程式的功能**

| 功能 | 說明 |
|------|------|
| 硬體抽象 | 隱藏硬體細節，提供統一的軟體介面 |
| 資源管理 | 管理 IRQ、DMA、記憶體映射 |
| 資料傳輸 | 負責周邊與記憶體之間的資料傳輸 |
| 狀態管理 | 追蹤和管理裝置狀態 |
| 錯誤處理 | 處理硬體異常和錯誤條件 |

**Linux 驅動程式分類**

| 分類 | 說明 | 範例 |
|------|------|------|
| 字元裝置 | 位元組流，随機存取 | 序列埠、I2C、GPIO |
| 區塊裝置 | 區塊讀寫，緩衝管理 | eMMC、SD 卡、NAND Flash |
| 網路裝置 | 網路資料傳輸 | Ethernet、WiFi |
| 平台裝置 | 非隨插即用裝置 | Platform Device |
| USB 裝置 | USB 協定處理 | 滑鼠、鍵盤 |

### 8.4.2 Linux 字元裝置驅動程式框架

```c
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/device.h>

#define DEVICE_NAME "my_device"
#define CLASS_NAME "my_class"

static dev_t dev_num;
static struct cdev my_cdev;
static struct class* my_class = NULL;
static struct device* my_device = NULL;

/* 檔案操作集合 */
static int mydev_open(struct inode *inode, struct file *file) {
    pr_info("my_device: open\n");
    return 0;
}

static ssize_t mydev_read(struct file *file, char __user *buf,
                          size_t count, loff_t *ppos) {
    char kernel_buf[64];
    int len = sprintf(kernel_buf, "Hello from kernel!\n");
    
    if (*ppos >= len)
        return 0;
    
    if (count > len - *ppos)
        count = len - *ppos;
    
    if (copy_to_user(buf, kernel_buf + *ppos, count))
        return -EFAULT;
    
    *ppos += count;
    return count;
}

static ssize_t mydev_write(struct file *file, const char __user *buf,
                          size_t count, loff_t *ppos) {
    char kernel_buf[64];
    
    if (count > sizeof(kernel_buf) - 1)
        count = sizeof(kernel_buf) - 1;
    
    if (copy_from_user(kernel_buf, buf, count))
        return -EFAULT;
    
    kernel_buf[count] = '\0';
    pr_info("my_device: wrote %s\n", kernel_buf);
    
    return count;
}

static int mydev_release(struct inode *inode, struct file *file) {
    pr_info("my_device: release\n");
    return 0;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = mydev_open,
    .read = mydev_read,
    .write = mydev_write,
    .release = mydev_release,
};

/* 模組初始化 */
static int __init mydev_init(void) {
    int ret;
    
    /* 1. 分配裝置號 */
    ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
    if (ret < 0) {
        pr_err("Failed to alloc device number\n");
        return ret;
    }
    
    /* 2. 初始化並註冊 cdev */
    cdev_init(&my_cdev, &fops);
    my_cdev.owner = THIS_MODULE;
    ret = cdev_add(&my_cdev, dev_num, 1);
    if (ret < 0) {
        unregister_chrdev_region(dev_num, 1);
        return ret;
    }
    
    /* 3. 建立裝置類和節點 */
    my_class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(my_class)) {
        cdev_del(&my_cdev);
        unregister_chrdev_region(dev_num, 1);
        return PTR_ERR(my_class);
    }
    
    my_device = device_create(my_class, NULL, dev_num, NULL, DEVICE_NAME);
    if (IS_ERR(my_device)) {
        class_destroy(my_class);
        cdev_del(&my_cdev);
        unregister_chrdev_region(dev_num, 1);
        return PTR_ERR(my_device);
    }
    
    pr_info("my_device: initialized\n");
    return 0;
}

/* 模組退出 */
static void __exit mydev_exit(void) {
    device_destroy(my_class, dev_num);
    class_destroy(my_class);
    cdev_del(&my_cdev);
    unregister_chrdev_region(dev_num, 1);
    pr_info("my_device: removed\n");
}

module_init(mydev_init);
module_exit(mydev_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Author");
MODULE_DESCRIPTION("Simple Character Device Driver");
```

### 8.4.3 嵌入式 GPIO 驅動程式

```c
#include <linux/gpio.h>
#include <linux/of_gpio.h>
#include <linux/platform_device.h>

struct my_gpio_data {
    int led_gpio;        // LED GPIO 腳位
    int button_gpio;     // 按鍵 GPIO 腳位
    struct timer_list debounce_timer;  // 防跳抖計時器
    struct work_struct button_work;    // 按鍵工作
};

static irqreturn_t button_irq_handler(int irq, void *dev_id) {
    struct my_gpio_data *data = dev_id;
    
    // 排程防跳抖工作
    schedule_work(&data->button_work);
    
    return IRQ_HANDLED;
}

static void button_work_handler(struct work_struct *work) {
    struct my_gpio_data *data = container_of(work, struct my_gpio_data, button_work);
    
    // 讀取按鍵狀態
    int state = gpio_get_value(data->button_gpio);
    
    // 設定 LED 狀態
    gpio_set_value(data->led_gpio, state);
    
    pr_info("Button: %s, LED: %s\n", 
             state ? "pressed" : "released",
             state ? "on" : "off");
}

static int my_probe(struct platform_device *pdev) {
    struct my_gpio_data *data;
    int ret;
    
    data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
    if (!data)
        return -ENOMEM;
    
    /* 從設備樹取得 GPIO */
    data->led_gpio = of_get_named_gpio(pdev->dev.of_node, "led-gpios", 0);
    data->button_gpio = of_get_named_gpio(pdev->dev.of_node, "button-gpios", 0);
    
    /* 請求 GPIO */
    ret = devm_gpio_request_one(&pdev->dev, data->led_gpio, 
                                GPIOF_OUT_INIT_LOW, "LED");
    if (ret)
        return ret;
    
    ret = devm_gpio_request_one(&pdev->dev, data->button_gpio,
                                GPIOF_IN, "Button");
    if (ret)
        return ret;
    
    /* 申請中斷 */
    ret = devm_request_irq(&pdev->dev, 
                          gpio_to_irq(data->button_gpio),
                          button_irq_handler,
                          IRQF_TRIGGER_FALLING | IRQF_TRIGGER_RISING,
                          "Button IRQ", data);
    if (ret)
        return ret;
    
    /* 初始化工作 */
    INIT_WORK(&data->button_work, button_work_handler);
    
    platform_set_drvdata(pdev, data);
    
    return 0;
}
```

## 8.5 嵌入式系統的安全性與可靠性

### 8.5.1 看門狗計時器（WDT）

看門狗確保系統在當機後自動恢復。

**看門狗運作原理**

```
正常運行：
┌────────┐     ┌────────┐     ┌────────┐
│ 應用   │────►│ 看門狗  │────►│ 計時器  │
│ 餵狗   │     │ 重置計時 │     │ 正常    │
└────────┘     └────────┘     └────────┘
     │              │              │
     ▼              ▼              ▼
  正常循環      計時器歸零      無動作

當機：
┌────────┐     ┌────────┐     ┌────────┐
│ 應用   │     │ 看門狗  │────►│ 計時器  │
│ 當機   │     │ 無餵狗  │     │ 溢出    │
└────────┘     └────────┘     └────────┘
                                     │
                                     ▼
                               ┌────────┐
                               │ 系統   │
                               │ 重置   │
                               └────────┘
```

**看門狗驅動範例**

```c
#include <linux/watchdog.h>

static int wdt_timeout = 30;  // 30 秒超時
module_param(wdt_timeout, int, 0644);

static int wdt_start(struct watchdog_device *wdd) {
    watchdog_notify_pretimeout(wdd);  // 可選：超時前通知
    return 0;
}

static int wdt_stop(struct watchdog_device *wdd) {
    return 0;
}

static int wdt_keepalive(struct watchdog_device *wdd) {
    /* 餵狗：重置計時器 */
    return 0;
}

static const struct watchdog_ops wdt_ops = {
    .owner = THIS_MODULE,
    .start = wdt_start,
    .stop = wdt_stop,
    .keepalive = wdt_keepalive,
};

static const struct watchdog_info wdt_info = {
    .options = WDIOF_SETTIMEOUT | WDIOF_KEEPALIVEPING,
    .firmware_version = 1,
    .identity = "My Watchdog",
};

static struct watchdog_device wdd = {
    .info = &wdt_info,
    .ops = &wdt_ops,
    .timeout = 30,
};
```

### 8.5.2 記憶體保護單元（MPU）

MPU 在嵌入式系統中提供記憶體區域保護。

**MPU 保護區域**

| 區域屬性 | 說明 |
|----------|------|
| 讀取 | 允許 CPU 讀取該記憶體 |
| 寫入 | 允許 CPU 寫入該記憶體 |
| 執行 | 允許 CPU 執行該記憶體中的指令 |
| 裝置/普通 | 裝置記憶體 vs 普通記憶體 |
| 可共享/不可共享 | 是否可被其他 Masters 訪問 |

**MPU 設定範例**

```c
void mpu_configure(void) {
    /* 設定記憶體區域 */
    
    /* 區域 0: Flash - 讀取+執行，無寫入 */
    MPU->RBAR = 0x08000000 | MPU_RBAR_VALID_Msk | (0 << MPU_RBAR_REGION_Pos);
    MPU->RASR = (0x3 << MPU_RASR_AP_Pos) |    // 讀取+執行
                (0x6 << MPU_RASR_SIZE_Pos) |     // 128KB
                (0x1 << MPU_RASR_ENABLE_Pos);     // 啟用
    
    /* 區域 1: SRAM - 讀寫，無執行 */
    MPU->RBAR = 0x20000000 | MPU_RBAR_VALID_Msk | (1 << MPU_RBAR_REGION_Pos);
    MPU->RASR = (0x1 << MPU_RASR_AP_Pos) |      // 讀寫
                (0x5 << MPU_RASR_SIZE_Pos) |     // 64KB
                (0x0 << MPU_RASR_XN_Pos) |       // 無執行
                (0x1 << MPU_RASR_ENABLE_Pos);
    
    /* 區域 2: Peripherals - 讀寫，強制的裝置屬性 */
    MPU->RBAR = 0x40000000 | MPU_RBAR_VALID_Msk | (2 << MPU_RBAR_REGION_Pos);
    MPU->RASR = (0x1 << MPU_RASR_AP_Pos) |      // 讀寫
                (0x6 << MPU_RASR_SIZE_Pos) |     // 128MB
                (0x2 << MPU_RASR_ATTRINDX_Pos) | // 裝置屬性
                (0x1 << MPU_RASR_ENABLE_Pos);
    
    /* 啟用 MPU */
    MPU->CTRL = MPU_CTRL_ENABLE_Msk | MPU_CTRL_PRIVDEFENA_Msk;
}
```

### 8.5.3 CRC 校驗

CRC（循環冗餘校驗）用於偵測資料傳輸或儲存中的錯誤。

**CRC 原理**

```
CRC 是一種多項式除法：
1. 將資料視為二進位多項式
2. 選擇一個生成多項式 (Generator Polynomial)
3. 將資料多項式左移 r 位 (r = 生成多項式位元數 - 1)
4. 除以生成多項式
5. 餘數就是 CRC 值
```

**常見 CRC 多項式**

| CRC 類型 | 多項式 | 位元數 | 應用 |
|----------|--------|--------|------|
| CRC-8 | 0x07 | 8 | ATM、SMBus |
| CRC-16 | 0x8005 | 16 | Modbus、USB |
| CRC-32 | 0x04C11DB7 | 32 | 乙太網、ZIP |
| CRC-32C | 0x1EDC6F41 | 32 | SSE4.2、儲存 |

**CRC-32 實作**

```c
#include <stdint.h>
#include <stddef.h>

// CRC-32 查找表
static const uint32_t crc32_table[256] = { /* ... */ };

uint32_t crc32(const uint8_t *data, size_t length) {
    uint32_t crc = 0xFFFFFFFF;  // 初始值
    
    while (length--) {
        uint8_t index = (crc ^ *data++) & 0xFF;
        crc = (crc >> 8) ^ crc32_table[index];
    }
    
    return crc ^ 0xFFFFFFFF;  // 最終異或值
}

// 使用範例
void crc_example(void) {
    const char *message = "Hello, CRC!";
    uint32_t checksum = crc32((const uint8_t *)message, strlen(message));
    
    printf("CRC-32: 0x%08X\n", checksum);
}
```

### 8.5.4 錯誤更正碼（ECC）

ECC 用於偵測和自動更正記憶體錯誤。

**ECC 類型**

| 類型 | 能力 | 開銷 |
|------|------|------|
| Parity | 單一位元錯誤偵測 | 1 位元/8 位元組 |
| SECDED | 單一錯誤更正 + 雙錯誤偵測 | 5 位元/32 位元組 |
| DECTED | 雙錯誤偵測 | 4 位元/32 位元組 |
| S4ECDED | 單一四位錯誤更正 + 雙錯誤偵測 | 8 位元/32 位元組 |

**SECDED 原理**

```c
// 32 位元資料 + 7 位元 ECC = 39 位元
// 可更正任何單一錯誤，偵測任何雙一錯誤

typedef struct {
    uint32_t data : 32;  // 資料
    uint32_t ecc : 7;      // ECC 校驗位元
} ecc_word_t;

// ECC 產生
uint32_t calculate_ecc(uint32_t data) {
    uint32_t ecc = 0;
    
    // 根據資料位元計算 ECC
    // 使用 Hamming Code 算法
    // 詳細實作略
    
    return ecc;
}

// ECC 檢查和更正
int check_and_correct(ecc_word_t *word) {
    uint32_t calculated_ecc = calculate_ecc(word->data);
    uint32_t syndrome = word->ecc ^ calculated_ecc;
    
    if (syndrome == 0) {
        return 0;  // 無錯誤
    }
    
    // 檢查單一錯誤是否可更正
    if (is_single_bit_error(syndrome)) {
        int bit_pos = get_error_bit_position(syndrome);
        word->data ^= (1 << bit_pos);  // 更正錯誤位元
        return 1;  // 已更正
    }
    
    // 雙一錯誤：只能偵測
    if (syndrome != 0) {
        return -1;  // 不可更正的錯誤
    }
    
    return 0;
}
```

### 8.5.5 系統可靠性設計模式

**看門狗 + 軟體監控**

```c
typedef enum {
    STATE_NORMAL,
    STATE_WARNING,
    STATE_CRITICAL
} system_state_t;

static system_state_t current_state = STATE_NORMAL;
static uint32_t error_count = 0;
static uint32_t recovery_count = 0;

void update_system_state(void) {
    error_count++;
    
    if (error_count > CRITICAL_THRESHOLD) {
        current_state = STATE_CRITICAL;
        trigger_failsafe();  // 觸發安全模式
    } else if (error_count > WARNING_THRESHOLD) {
        current_state = STATE_WARNING;
        reduce_system_load();  // 降低系統負載
    }
}

void watchdog_callback(void) {
    // 餵狗
    wdt_keepalive();
    
    // 檢查系統狀態
    if (current_state == STATE_CRITICAL) {
        // 準備重置
        enter_safe_mode();
    }
    
    // 週期性重置信計數
    if (error_count > 0 && current_state == STATE_NORMAL) {
        error_count--;
    }
}
```

**安全關機序列**

```c
void safe_shutdown_sequence(void) {
    // 1. 停止接收新的請求
    disable_interrupts();
    
    // 2. 將關鍵資料寫入非易失性儲存
    save_critical_data();
    
    // 3. 關閉馬達/致動器
    motor_stop_all();
    actuator_deenergize();
    
    // 4. 等待所有 I/O 完成
    wait_for_io_complete();
    
    // 5. 進入最低功耗模式
    enter_low_power_mode();
    
    // 6. 準備下次啟動
    prepare_for_wakeup();
}
```
