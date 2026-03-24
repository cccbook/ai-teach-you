# 8. 嵌入式作業系統

## 8.1 嵌入式系統特性與限制

[程式檔案：08-2-embedded-system.py](../_code/08/08-2-embedded-system.py)
```c
// 嵌入式系統範例：Arduino 控制 LED
// 硬體: ATmega328P, 16MHz, 2KB RAM, 32KB Flash

#define LED_PIN 13

void setup() {
    pinMode(LED_PIN, OUTPUT);  // 設定腳位為輸出
}

void loop() {
    digitalWrite(LED_PIN, HIGH);  // LED 亮
    delay(1000);                   // 延遲 1 秒
    digitalWrite(LED_PIN, LOW);   // LED 滅
    delay(1000);                   // 延遲 1 秒
}

// 嵌入式系統特性：
// 1. 資源受限 - RAM/ROM 有限
// 2. 即時性 - 需要確定性的回應時間
// 3. 低功耗 - 电池供电设备
// 4. 無人值守 - 长时间运行
// 5. 專用性 - 单个功能或有限功能
```

[程式檔案：08-2-embedded-system.py](../_code/08/08-2-embedded-system.py)
```python
"""
嵌入式系統資源估算
"""

class EmbeddedSystem:
    """嵌入式系統資源評估"""
    
    def __init__(self):
        self.cpu = None          # CPU 型號
        self.ram = 0             # RAM 大小 (KB)
        self.flash = 0           # Flash 大小 (KB)
        self.clock = 0           # 時脈 (MHz)
        self.power_consumption = 0  # 功耗 (mW)
    
    def estimate_resources(self, application):
        """估算應用所需資源"""
        
        # 記憶體估算
        code_size = application.get('code_lines', 0) * 4  # 每行約 4 bytes
        data_size = application.get('variables', 0) * 4   # 每個變數約 4 bytes
        stack_size = application.get('max_stack', 256)    # 堆疊深度
        
        total_ram = code_size + data_size + stack_size
        
        # 檢查是否適合目標平台
        if total_ram > self.ram:
            print(f"警告: 需要 {total_ram}KB RAM，超過 {self.ram}KB")
        else:
            print(f"記憶體足夠: 需要 {total_ram}KB")
        
        # 執行時間估算
        cycles = application.get('operations', 0) * 10  # 假設每操作 10 時脈
        execution_time = cycles / (self.clock * 1000000)  # 秒
        print(f"執行時間: {execution_time*1000:.2f} ms")
        
        return {
            'ram': total_ram,
            'execution_time': execution_time,
            'power_estimate': execution_time * self.power_consumption
        }

# 測試
system = EmbeddedSystem()
system.cpu = "ATmega328P"
system.ram = 2 * 1024      # 2KB
system.flash = 32 * 1024   # 32KB
system.clock = 16          # 16MHz
system.power_consumption = 50  # 50mW @ 5V

app = {
    'code_lines': 500,
    'variables': 50,
    'max_stack': 128,
    'operations': 10000
}

system.estimate_resources(app)
```

## 8.2 即時作業系統（RTOS）概念

[程式檔案：08-3-rtos.c](../_code/08/08-3-rtos.c)
```c
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
```

```python
"""
RTOS 任務排程模擬
"""

import time
from enum import Enum

class TaskState(Enum):
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    SUSPENDED = "suspended"

class Task:
    """RTOS 任務"""
    
    def __init__(self, name, priority, period, function):
        self.name = name
        self.priority = priority  # 數字越小優先級越高
        self.period = period     # 執行週期 (秒)
        self.function = function
        self.state = TaskState.READY
        self.next_run = 0
        self.worst_case_execution = 0
    
    def run(self):
        """執行任務"""
        self.state = TaskState.RUNNING
        print(f"[{self.name}] 開始執行 (優先級: {self.priority})")
        
        # 執行任務工作
        try:
            self.function()
        except Exception as e:
            print(f"任務執行錯誤: {e}")
        
        self.state = TaskState.READY
        print(f"[{self.name}] 執行完成")
    
    def wait(self, delay):
        """任務延遲"""
        self.state = TaskState.BLOCKED
        time.sleep(delay)
        self.state = TaskState.READY

# RTOS 排程器
class RTOSScheduler:
    """即時排程器"""
    
    def __init__(self, scheduler_type="fixed_priority"):
        self.tasks = []
        self.scheduler_type = scheduler_type
    
    def add_task(self, task):
        """加入任務"""
        self.tasks.append(task)
    
    def schedule(self):
        """排程任務"""
        # 固定優先級排程
        if self.scheduler_type == "fixed_priority":
            self.tasks.sort(key=lambda t: t.priority)
        
        # Rate Monotonic Scheduling (RMS)
        elif self.scheduler_type == "rms":
            self.tasks.sort(key=lambda t: t.period)
        
        # Earliest Deadline First (EDF)
        elif self.scheduler_type == "edf":
            self.tasks.sort(key=lambda t: t.next_run)
    
    def run(self, duration):
        """執行排程器"""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            self.schedule()
            
            # 執行就緒任務
            for task in self.tasks:
                if task.state == TaskState.READY:
                    task.run()
                    break
            
            time.sleep(0.1)

# 測試
def sensor_task():
    """感測器任務"""
    print("  -> 讀取感測器資料")

def control_task():
    """控制任務"""
    print("  -> 執行控制邏輯")

def display_task():
    """顯示任務"""
    print("  -> 更新顯示")

rtos = RTOSScheduler(scheduler_type="fixed_priority")
rtos.add_task(Task("Sensor", priority=1, period=0.1, function=sensor_task))
rtos.add_task(Task("Control", priority=2, period=0.2, function=control_task))
rtos.add_task(Task("Display", priority=3, period=0.5, function=display_task))

print("=== RTOS 排程模擬 ===")
rtos.run(duration=1.0)

# 即時性分析
print("\n=== 即時性分析 ===")
print("固定優先級:")
print("  - 高優先級任務會搶占低優先級任務")
print("  - 可能產生優先級反轉")

print("\nRMS (Rate Monotonic):")
print("  - 週期越短，優先級越高")
print("  - 可行性條件: U <= n(2^(1/n) - 1)")
```

## 8.3 FreeRTOS、RT-Thread 介紹

[程式檔案：08-4-freertos.c](../_code/08/08-4-freertos.c)
```c
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
```

```python
"""
RT-Thread 模擬
"""

class RTThread:
    """RT-Thread 任務類比"""
    
    def __init__(self, name, stack_size, priority):
        self.name = name
        self.stack_size = stack_size
        self.priority = priority
        self.state = 'ready'
        self.mailbox = []  # 郵箱
        self.semaphore = 0
    
    def send(self, message):
        """發送訊息"""
        if len(self.mailbox) < 10:
            self.mailbox.append(message)
            return True
        return False
    
    def receive(self):
        """接收訊息"""
        if self.mailbox:
            return self.mailbox.pop(0)
        return None

# RT-Thread 特性
print("""
=== RT-Thread 特性 ===

1. 微型核心
   - 核心精簡，約 3KB
   - 模組化設計

2. 命名管道（Named Pipe）
   - 建立點對點通訊

3. 訊息佇列
   - 記憶體池管理

4. 訊號
   - 同步與訊號處理

5. 事件
   - 多事件等待

6. 線程同步
   - 互斥鎖、訊號量、臨界區
""")

# RT-Thread 與 FreeRTOS 比較
print("""
=== RT-Thread vs FreeRTOS ===

| 特性       | RT-Thread     | FreeRTOS     |
|------------|--------------|--------------|
| 起源       | 中國         | 美國/英國    |
| 核心大小   | ~3KB         | ~5KB         |
| 任務數量   | 255          | 取決於 RAM   |
| 優先級     | 256          | 可配置       |
| 中文社群   | 強大         | 一般         |
| 檔系統    | 有           | 可選         |
| 網路堆疊   | 有           | 可選         |
""")
```

## 8.4 驅動程式開發

[程式檔案：08-5-driver.c](../_code/08/08-5-driver.c)
```c
// Linux 核心模組範例

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Author");
MODULE_DESCRIPTION("Simple Character Driver");

// 裝置結構
struct my_device {
    dev_t dev_num;
    struct cdev cdev;
};

// 開啟裝置
static int mydev_open(struct inode *inode, struct file *file) {
    printk(KERN_INFO "裝置已開啟\n");
    return 0;
}

// 讀取裝置
static ssize_t mydev_read(struct file *file, char __user *buf, 
                           size_t len, loff_t *offset) {
    printk(KERN_INFO "讀取資料\n");
    return 0;
}

// 寫入裝置
static ssize_t mydev_write(struct file *file, const char __user *buf,
                           size_t len, loff_t *offset) {
    printk(KERN_INFO "寫入資料\n");
    return len;
}

// 檔案操作
static struct file_operations fops = {
    .owner   = THIS_MODULE,
    .open    = mydev_open,
    .read    = mydev_read,
    .write   = mydev_write,
};

// 初始化模組
static int __init mydev_init(void) {
    printk(KERN_INFO "模組載入\n");
    // 註冊字元裝置
    register_chrdev(255, "mydev", &fops);
    return 0;
}

// 移除模組
static void __exit mydev_exit(void) {
    printk(KERN_INFO "模組卸載\n");
    unregister_chrdev(255, "mydev");
}

module_init(mydev_init);
module_exit(mydev_exit);
```

```python
"""
模擬 Linux 驅動程式框架
"""

class LinuxDriver:
    """Linux 驅動程式模擬"""
    
    def __init__(self, name):
        self.name = name
        self.loaded = False
    
    def init(self):
        """初始化"""
        print(f"[{self.name}] 驅動程式初始化")
        self.register_device()
        self.loaded = True
    
    def register_device(self):
        """註冊裝置"""
        print(f"[{self.name}] 註冊裝置到核心")
    
    def open(self):
        """開啟"""
        print(f"[{self.name}] 開啟裝置")
    
    def read(self, size):
        """讀取"""
        print(f"[{self.name}] 讀取 {size} bytes")
        return b"data from device"
    
    def write(self, data):
        """寫入"""
        print(f"[{self.name}] 寫入 {len(data)} bytes")
    
    def close(self):
        """關閉"""
        print(f"[{self.name}] 關閉裝置")
    
    def exit(self):
        """移除"""
        print(f"[{self.name}] 驅動程式移除")
        self.loaded = False

# 測試
driver = LinuxDriver("my_device")
driver.init()
driver.open()
data = driver.read(512)
driver.write(b"hello")
driver.close()
driver.exit()

# GPIO 驅動範例
class GPIODriver:
    """GPIO 驅動"""
    
    def __init__(self):
        self.pins = {}  # pin -> direction
    
    def export(self, pin):
        """匯出 GPIO"""
        self.pins[pin] = 'in'
        print(f"GPIO {pin} 已匯出")
    
    def set_direction(self, pin, direction):
        """設定方向"""
        if pin in self.pins:
            self.pins[pin] = direction
            print(f"GPIO {pin} 設為 {direction}")
    
    def write(self, pin, value):
        """寫入"""
        print(f"GPIO {pin} 設為 {value}")
    
    def read(self, pin):
        """讀取"""
        return 0

gpio = GPIODriver()
gpio.export(17)
gpio.set_direction(17, 'out')
gpio.write(17, 1)
```

## 8.5 嵌入式系統的安全性與可靠性

[程式檔案：08-9-security.c](../_code/08/08-9-security.c)
```c
// 嵌入式系統安全性範例

// 1. 看門狗定時器
void init_watchdog() {
    // 設定看門狗，1秒後重置
    WDTCTL = WDTPW + WDTTMSEL + WDTIS_2;  // 1秒
}

// 2. 記憶體保護單元 (MPU)
void configure_mpu() {
    // 設定記憶體區域權限
    MPU->RNR = 0;              // Region 0
    MPU->RBAR = 0x20000000;    // SRAM 起始
    MPU->RASR = MPU_REGION_SIZE_64KB | 
                MPU_REGION_READ_WRITE |
                MPU_REGION_NOT_EXECUTE;
}

// 3. CRC 校驗
uint32_t crc32(uint8_t *data, size_t len) {
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            crc = (crc >> 1) ^ (0xEDB88320 & -(crc & 1));
        }
    }
    return ~crc;
}

// 4. 錯誤更正碼 (ECC)
void enable_ecc() {
    // 啟用 ECC 用於 SRAM/Flash
    FMC->ECCCTL |= FMC_ECC_EN;
}
```

```python
"""
嵌入式系統可靠性模式
"""

# 1. 看門狗監控
class Watchdog:
    """看門狗定時器"""
    
    def __init__(self, timeout=1.0):
        self.timeout = timeout
        self.last_pet = time.time()
        self.enabled = True
    
    def pet(self):
        """餵狗"""
        self.last_pet = time.time()
        print("看門狗已重置")
    
    def check(self):
        """檢查"""
        if not self.enabled:
            return True
        
        elapsed = time.time() - self.last_pet
        if elapsed > self.timeout:
            print("看門狗超時！系統將重置")
            return False
        return True

# 2. 錯誤復原
class ErrorRecovery:
    """錯誤復原策略"""
    
    @staticmethod
    def retry(operation, max_retries=3):
        """重試"""
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                print(f"嘗試 {attempt+1} 失敗: {e}")
                time.sleep(0.1)
        return None
    
    @staticmethod
    def fallback(primary, fallback_func):
        """降級"""
        try:
            return primary()
        except:
            return fallback_func()

# 3. 資料完整性
class DataIntegrity:
    """資料完整性檢查"""
    
    @staticmethod
    def checksum(data):
        """簡單校驗和"""
        return sum(data) % 256
    
    @staticmethod
    def crc32(data):
        """CRC32"""
        import zlib
        return zlib.crc32(data)
    
    @staticmethod
    def verify(data, expected):
        """驗證"""
        return DataIntegrity.checksum(data) == expected

# 測試
wd = Watchdog(timeout=0.5)
wd.pet()
time.sleep(0.3)
wd.pet()
time.sleep(0.6)  # 將觸發重置
wd.check()

# 錯誤復原
result = ErrorRecovery.retry(
    lambda: 1/0,  # 會失敗的操作
    max_retries=3
)
print(f"重試結果: {result}")

# 資料完整性
data = b"Hello, World!"
checksum = DataIntegrity.checksum(data)
print(f"資料校驗: {DataIntegrity.verify(data, checksum)}")
```