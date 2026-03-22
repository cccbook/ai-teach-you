# 37. 連結腳本——控制記憶體佈局

## 37.1 連結腳本的角色

連結器使用連結腳本來控制：
- 各 section 的排列順序
- 記憶體區域的定義
- 符號的位址分配

## 37.2 預設行為

如果沒有連結腳本，連結器使用預設配置。

## 37.3 基本連結腳本

### 37.3.1 簡單範例

```ld
OUTPUT_ARCH(riscv)
ENTRY(_start)

SECTIONS
{
    . = 0x80000000;
    .text : { *(.text) }
    .data : { *(.data) }
    .bss  : { *(.bss) }
}
```

### 37.3.2 記憶體區域

```ld
MEMORY
{
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 256K
    RAM (rwx)  : ORIGIN = 0x20000000, LENGTH = 64K
}

SECTIONS
{
    .text : {
        *(.text)
    } > FLASH
    
    .data : {
        *(.data)
    } > RAM AT> FLASH
}
```

## 37.4 符號定義

### 37.4.1 定義符號

```ld
_start = 0x80000000;
end = .;
```

### 37.4.2 使用符號

```c
extern char _start;
extern char end;

void *heap_start = &end;
```

## 37.5 mini-riscv-os 的連結腳本

```ld
OUTPUT_ARCH(riscv)
OUTPUT_FORMAT("elf32-littleriscv", "elf32-littleriscv", "elf32-littleriscv")

ENTRY(_start)

SECTIONS
{
    . = 0x80000000;
    
    .text : {
        *(.text)
    }
    
    .data : {
        *(.data)
    }
    
    .bss : {
        *(.bss)
    }
}
```

## 37.6 小結

本章節我們學習了：
- 連結腳本的基本語法
- 記憶體區域定義
- section 排列

## 37.7 習題

1. 為嵌入式系統編寫連結腳本
2. 研究 .got 和 .plt section
3. 實現自訂 section
