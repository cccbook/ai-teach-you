# 23. 多工系統——任務切換與排程

## 23.1 從單任務到多工

單任務系統只能同時執行一個程式。多工系統可以同時執行多個任務，透過快速切換造成「同時執行」的錯覺。

```
單工：
|----------- task1 -----------|
時間 ─────────────────────────→

多工（協作式）：
|---- task1 ----||---- task2 ----||---- task1 ----|
時間 ─────────────────────────────────────────────→
```

## 23.2 合作式 vs 搶佔式多工

| 類型 | 說明 | 優點 | 缺點 |
|------|------|------|------|
| 合作式 | 任務自願放棄 CPU | 簡單 | 可能被錯誤任務阻塞 |
| 搶佔式 | OS 強制切換 | 公平響應 | 複雜（需要鎖） |

mini-riscv-os 03-MultiTasking 是合作式多工。

## 23.3 任務管理結構

### 23.3.1 任務控制塊 (TCB)

```c
// task.h
#define MAX_TASKS 4
#define STACK_SIZE 1024

struct task {
    reg_t sp;              // 堆疊指標
    reg_t stack[STACK_SIZE];  // 獨立堆疊
};

struct task tasks[MAX_TASKS];
int taskTop = 0;           // 目前任務數量
```

### 23.3.2 任務初始化

```c
// user.c
void user_task0(void) {
    lib_puts("Task0: begin\n");
    while (1) {
        lib_puts("Task0: running...\n");
        for (volatile int i = 0; i < 100000; i++);
    }
}

void user_task1(void) {
    lib_puts("Task1: begin\n");
    while (1) {
        lib_puts("Task1: running...\n");
        for (volatile int i = 0; i < 100000; i++);
    }
}

void user_init(void) {
    tasks[0].sp = (reg_t) &tasks[0].stack[STACK_SIZE-1];
    tasks[0].sp = (reg_t) &tasks[1].stack[STACK_SIZE-1];
    
    taskTop = 2;
    
    tasks[0].sp = (reg_t) &tasks[0].stack[STACK_SIZE-1];
    task[1].sp = (reg_t) &tasks[1].stack[STACK_SIZE-1];
}
```

## 23.4 任務切換

### 23.4.1 任務跳轉

```c
// task.h
extern void task_go(struct context *ctx);

void task_go(struct context *ctx) {
    sys_switch(&ctx_os, ctx);
}
```

### 23.4.2 任務返回（自願讓出 CPU）

```c
// 任務完成後呼叫這個返回 OS
extern void os_kernel(void);

void task_exit(void) {
    sys_switch(&ctx_task, &ctx_os);
}
```

## 23.5 排程器

### 23.5.1 Round-Robin 排程

Round-Robin（時間片輪轉）是最簡單的排程演算法：

```c
int current_task = 0;

while (1) {
    lib_puts("OS: Activate next task\n");
    task_go(&tasks[current_task]);  // 切換到任務
    lib_puts("OS: Back to OS\n");
    
    // 下一個任務（環形）
    current_task = (current_task + 1) % taskTop;
    lib_puts("\n");
}
```

### 23.5.2 Round-Robin 示意圖

```
任務 0 ────────────────── task_go ──────────────────→ 返回
         (執行一段時間後讓出)

任務 1 ────────────────── task_go ──────────────────→ 返回
         (執行一段時間後讓出)

任務 0 ────────────────── task_go ──────────────────→ 返回
         ...
```

## 23.6 合作式多工的問題

### 23.6.1 任務不讓出 CPU

如果任務進入無限迴圈，OS 無法干預：

```c
void bad_task(void) {
    while (1) {  // 永遠不呼叫 task_exit！
        // 做事情
    }
}
```

### 23.6.2 任務可能忘記讓出

即使任務不是惡意的，也可能忘記讓出 CPU：

```c
void task_with_big_loop(void) {
    for (int i = 0; i < 1000000000; i++) {  // 長時間計算
        // 可能忘記讓出
    }
    task_exit();
}
```

## 23.7 完整的任務切換流程

### 23.7.1 OS 啟動

```c
void os_start() {
    lib_puts("OS start\n");
    user_init();  // 初始化任務
}
```

### 23.7.2 OS 主迴圈

```c
int os_main(void) {
    os_start();
    
    int current_task = 0;
    while (1) {
        lib_puts("OS: Activate next task\n");
        task_go(&tasks[current_task]);
        lib_puts("OS: Back to OS\n");
        current_task = (current_task + 1) % taskTop;
        lib_puts("\n");
    }
}
```

### 23.7.3 任務執行

```c
void user_task0(void) {
    lib_puts("Task0: begin\n");
    while (1) {
        lib_puts("Task0: running...\n");
        // 延遲
        for (volatile int i = 0; i < 100000; i++);
        // 任務返回 OS
        task_exit();
    }
}
```

## 23.8 執行流程圖

```
┌─────────────────────────────────────────────────────────┐
│ os_main()                                              │
│   os_start() → user_init()                            │
│                                                         │
│   while (1) {                                          │
│       task_go(&tasks[current_task]);  ─────────┐       │
│       ...                                      │       │
│       current_task = (current_task + 1) % 2;   │       │
│   }                                             │       │
└─────────────────────────────────────────────────┼───────┘
                                                  │
                              ┌───────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│ sys_switch(&ctx_os, &tasks[current_task])              │
│   1. 保存 OS 上下文到 ctx_os                            │
│   2. 載入 tasks[current_task] 上下文                   │
│   3. ret → 跳到任務                                     │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│ user_task0()                                           │
│   lib_puts("Task0: running...")                        │
│   延遲                                                │
│   task_exit() → sys_switch(&ctx_task, &ctx_os)        │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│ sys_switch(&ctx_task, &ctx_os)                         │
│   1. 保存任務上下文到 ctx_task                         │
│   2. 載入 ctx_os 上下文                               │
│   3. ret → 回到 os_main 的 while 迴圈                 │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
                         返回 OS
```

## 23.9 延遲函式的重要性

```c
for (volatile int i = 0; i < 100000; i++);
```

`volatile` 是必要的，因為：
- 防止編譯器優化掉整個迴圈
- 確保迴圈真的執行

## 23.10 執行結果

```bash
cd _code/mini-riscv-os/03-MultiTasking
make
make qemu
```

輸出：
```
OS start
OS: Activate next task
Task0: begin
Task0: running...
OS: Back to OS

OS: Activate next task
Task1: begin
Task1: running...
OS: Back to OS

OS: Activate next task
Task0: running...
OS: Back to OS
...
```

## 23.11 小結

本章節我們學習了：
- 單工到多工的轉變
- 合作式 vs 搶佔式多工
- 任務控制塊 (TCB) 的結構
- Round-Robin 排程演算法
- 任務切換的完整流程
- 合作式多工的問題

## 23.12 習題

1. 實現優先級排程（高優先級任務先執行）
2. 為什麼需要獨立的任務堆疊？
3. 實現任務讓出 CPU 的延遲測量
4. 如果任務從不呼叫 task_exit，會發生什麼？
5. 研究作業系統中的「飢餓」問題
