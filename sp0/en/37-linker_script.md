# 37. Linker Scripts——Controlling Memory Layout

## 37.1 Role of Linker Scripts

Linkers use linker scripts to control:
- Order of section arrangement
- Memory region definitions
- Symbol address allocation

## 37.2 Default Behavior

If there's no linker script, the linker uses default configuration.

## 37.3 Basic Linker Scripts

### 37.3.1 Simple Example

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

### 37.3.2 Memory Regions

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

## 37.4 Symbol Definitions

### 37.4.1 Define Symbols

```ld
_start = 0x80000000;
end = .;
```

### 37.4.2 Use Symbols

```c
extern char _start;
extern char end;

void *heap_start = &end;
```

## 37.5 mini-riscv-os Linker Script

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

## 37.6 Summary

In this chapter we learned:
- Basic linker script syntax
- Memory region definitions
- Section arrangement

## 37.7 Exercises

1. Write a linker script for an embedded system
2. Research .got and .plt sections
3. Implement custom sections
