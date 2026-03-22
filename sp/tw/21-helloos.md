# 21. 第一個 OS——UART 與 Hello World

## 21.1 從零開始打造 OS

作業系統是管理硬體資源、提供服務給應用程式的軟體。本書使用 mini-riscv-os 專案，從零開始打造一個 RISC-V 上的微型作業系統。

程式碼位置：[_code/mini-riscv-os/](../_code/mini-riscv-os/)

## 21.2 階段總覽

mini-riscv-os 分為 10 個階段：

| 階段 | 目錄 | 內容 |
|------|------|------|
| 01 | HelloOs | 第一個 OS，UART 輸出 |
| 02 | ContextSwitch | 從 OS 切換到任務 |
| 03 | MultiTasking | 合作式多工 |
| 04 | TimerInterrupt | 計時器中斷 |
| 05 | Preemptive | 搶佔式排程 |
| 06 | Spinlock | 自旋鎖 |
| 07 | ExternalInterrupt | 外部中斷 |
| 08 | BlockDeviceDriver | 區塊設備驅動 |
| 09 | MemoryAllocator | 記憶體配置 |
| 10 | SystemCall | 系統呼叫 |

## 21.3 第一個 OS 的結構

### 21.3.1 啟動檔案 start.s

```asm
.equ STACK_SIZE, 8192

.global _start

_start:
    csrr a0, mhartid        # 讀取核心代號 (Hart ID)
    bnez a0, park           # 若不是 0 號核心，跳到 park
    
    la   sp, stacks + STACK_SIZE  # 設定堆疊指標
    j    os_main             # 跳到 OS 主函式

park:
    wfi                      # 等待中斷 (Wait for Interrupt)
    j park

stacks:
    .skip STACK_SIZE         # 分配堆疊空間
```

關鍵點：
- `csrr a0, mhartid`：讀取目前 CPU 核心的 ID
- 多核心系統中，只有 0 號核心執行 OS
- 其他核心進入 park 迴圈等待
- `wfi`：等待計時器中斷以節省電量

### 21.3.2 主程式 os.c

```c
#include <stdint.h>

#define UART        0x10000000
#define UART_THR    (uint8_t*)(UART+0x00)  // 傳送保持暫存器
#define UART_LSR    (uint8_t*)(UART+0x05)  // 線路狀態暫存器
#define UART_LSR_EMPTY_MASK 0x40           // 傳送器空的標誌

int lib_putc(char ch) {
    // 等待 UART 準備好
    while ((*UART_LSR & UART_LSR_EMPTY_MASK) == 0);
    return *UART_THR = ch;
}

void lib_puts(char *s) {
    while (*s) lib_putc(*s++);
}

int os_main(void) {
    lib_puts("Hello OS!\n");
    while (1) {}  // 無限迴圈
    return 0;
}
```

## 21.4 RISC-V 特權模式

RISC-V 有三個特權模式（由高到低）：

| 模式 | 名稱 | 用途 |
|------|------|------|
| M Mode | Machine | 最高權限，Bootloader、BIOS |
| S Mode | Supervisor | 作業系統核心 |
| U Mode | User | 使用者程式 |

mini-riscv-os 運行在 Machine Mode，因為它是一個裸機系統。

### 21.4.1 控制狀態暫存器 (CSR)

M Mode 的重要 CSR：

| CSR | 名稱 | 用途 |
|-----|------|------|
| mhartid | Hart ID | CPU 核心 ID |
| mstatus | Machine Status | 中斷狀態 |
| mtvec | Machine Trap Vector | 中斷處理向量 |
| mie | Machine Interrupt Enable | 中斷使能 |
| mip | Machine Interrupt Pending | 待處理中斷 |
| mepc | Machine Exception PC | 例外發生的 PC |
| mcause | Machine Cause | 例外/中斷原因 |

## 21.5 UART 設備

### 21.5.1 什麼是 UART？

UART（Universal Asynchronous Receiver-Transmitter）是一種序列通訊協定。

QEMU 的 Virt 平台將 UART 映射到記憶體位址 `0x10000000`。

### 21.5.2 UART 暫存器

| 位址 | 名稱 | 說明 |
|------|------|------|
| 0x00 | THR | 傳送保持暫存器（寫入要發送的字元）|
| 0x05 | LSR | 線路狀態暫存器（讀取狀態）|

LSR 位元 6 (UART_LSR_EMPTY_MASK)：當為 1 時，表示傳送器空，可以發送下一個字元。

### 21.5.3 字元輸出流程

```
CPU                    UART                    終端
  |                      |                      |
  |─── 寫入 THR ────────→|                      |
  |                      |─── 序列位元 ────────→|
  |                      |                      |
  |←── 輪詢 LSR ─────────|                      |
  |                      |                      |
```

## 21.6 連結腳本 os.ld

```ld
OUTPUT_ARCH(riscv)
OUTPUT_FORMAT("elf32-littleriscv", "elf32-littleriscv", "elf32-littleriscv")

ENTRY(_start)

SECTIONS {
    . = 0x80000000;
    .text : { *(.text) }
    .data : { *(.data) }
    .bss  : { *(.bss) }
}
```

關鍵點：
- `ENTRY(_start)`：程式的進入點
- `. = 0x80000000`：程式碼從這個位址開始（QEMU 期望的位置）
- 所有 section 從這個位址開始排列

## 21.7 Makefile

```makefile
CC = riscv64-unknown-elf-gcc
CFLAGS = -nostdlib -fno-builtin -mcmodel=medany -march=rv32ima -mabi=ilp32

QEMU = qemu-system-riscv32
QFLAGS = -nographic -smp 4 -machine virt -bios none

all: os.elf

os.elf: start.s os.c
    $(CC) $(CFLAGS) -T os.ld -o os.elf $^

qemu:
    $(QEMU) $(QFLAGS) -kernel os.elf

clean:
    rm -f *.elf
```

關鍵編譯選項：
- `-nostdlib`：不連結標準函式庫（我們是 OS，沒有標準庫）
- `-fno-builtin`：不使用內建函式
- `-mcmodel=medany`：使用任意位址的程式碼模型
- `-march=rv32ima`：目標架構（32 位元，支援 M、A、I 擴展）
- `-mabi=ilp32`：32 位元 ABI（整數/指標為 32 位元）

## 21.8 執行與測試

### 21.8.1 建置

```bash
cd _code/mini-riscv-os/01-HelloOs
make
```

### 21.8.2 在 QEMU 中執行

```bash
make qemu
```

會看到輸出：
```
Hello OS!
```

### 21.8.3 退出 QEMU

按 `Ctrl-A` 然後按 `X`。

## 21.9 開機流程

```
┌─────────────────────────────────────────────────────────┐
│  QEMU 載入 os.elf                                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  _start (start.s)                                       │
│    1. 讀取 mhartid                                      │
│    2. 非 0 號核心進入 park                              │
│    3. 0 號核心設定 sp 並跳到 os_main                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  os_main (os.c)                                        │
│    1. 呼叫 lib_puts("Hello OS!\n")                      │
│    2. 無限迴圈                                          │
└─────────────────────────────────────────────────────────┘
```

## 21.10 小結

本章節我們學習了：
- mini-riscv-os 的階段結構
- RISC-V 特權模式（M/S/U Mode）
- 控制狀態暫存器（CSR）
- UART 設備和序列通訊
- 連結腳本的基本結構
- Makefile 編譯選項
- 從零開始的第一個 OS

## 21.11 習題

1. 修改 `os.c`，讓它輸出自己的名字
2. 添加一個 `lib_puti` 函式，輸出數字
3. 實現 `printf` 函式（支援 %d、%x、%s）
4. 為什麼需要輪詢 LSR？如何改用中斷？
5. 研究 QEMU 的 `-machine virt` 平台的記憶體佈局
