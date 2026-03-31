# ELF (Executable and Linkable Format)

## 概述

ELF 是 Unix 和 Linux 系統中標準的可執行檔和目標檔格式。作為 COFF 的 successors，ELF 支援可執行檔、共享庫、目標檔等多種類型。它是 Linux 系統中最重要的二進制格式。

## 歷史

- **1983**：UNIX System V 引入 COFF
- **1989**：UNIX System V Release 4 引入 ELF
- **1995**：Linux 採用 ELF 作為標準
- **現在**：Linux、FreeBSD、Solaris 標準格式

## ELF 結構

```
┌──────────────────────────────┐
│ ELF Header                   │
├──────────────────────────────┤
│ Program Header Table         │
│ (segments)                   │
├──────────────────────────────┤
│ Section 1: .text            │
│ Section 2: .data            │
│ Section 3: .bss             │
│ ...                         │
├──────────────────────────────┤
│ Section Header Table        │
│ (sections)                  │
└──────────────────────────────┘
```

### 1. ELF Header

```c
#define EI_MAG0     0
#define EI_MAG1     1
#define EI_MAG2     2
#define EI_MAG3     3
#define EI_CLASS   4
#define EI_DATA    5

typedef struct {
    unsigned char e_ident[16];  // Magic + info
    uint16_t     e_type;         // 檔案類型
    uint16_t     e_machine;      // 架構
    uint32_t     e_version;     // 版本
    uint64_t     e_entry;       // 入口點
    uint64_t     e_phoff;       // Program Header 偏移
    uint64_t     e_shoff;       // Section Header 偏移
    uint32_t     e_flags;       // 架構標誌
    uint16_t     e_ehsize;      // ELF Header 大小
    uint16_t     e_phentsize;   // Program Header  entry 大小
    uint16_t     e_phnum;       // Program Header 數量
    uint16_t     e_shentsize;   // Section Header entry 大小
    uint16_t     e_shnum;       // Section Header 數量
    uint16_t     e_shstrndx;    // 字串表索引
} Elf64_Ehdr;
```

### 2. 讀取 ELF 資訊

```python
import struct

class ELF:
    def __init__(self, data):
        self.data = data
        self.parse_header()
    
    def parse_header(self):
        # ELF Magic
        self.magic = self.data[:4]
        if self.magic != b'\x7fELF':
            raise ValueError("不是有效的 ELF 檔案")
        
        # Class (32/64 bit)
        self.cls = self.data[4]
        
        # Endianness
        self.endian = self.data[5]
        
        # 解析 header
        if self.cls == 2:  # 64-bit
            fmt = '<16HHIQQQIHHHHHH'
        else:  # 32-bit
            fmt = '<16HHIIIIIHHHHHH'
        
        self.e_type, self.e_machine, self.e_version = struct.unpack(
            fmt, self.data[:16]
        )
```

### 3. Sections

```python
# 常用 sections
SECTIONS = {
    '.text': '可執行指令',
    '.data': '已初始化資料',
    '.bss': '未初始化資料',
    '.rodata': '唯讀資料',
    '.symtab': '符號表',
    '.strtab': '字串表',
    '.rel/.rela': '重定位表',
    '.comment': '版本資訊',
    '.note': '備註資訊',
}
```

### 4. 動態連結

```python
# 動態連結 section
DYNAMIC_SECTIONS = ['.dynamic', '.dynsym', '.dynstr']

# 解析動態依賴
def parse_dependencies(elf_data):
    # 找到 .dynamic section
    dyn_str = b''
    # 解析 DT_NEEDED 條目
    return dependencies
```

### 5. 符號表

```python
class Symbol:
    def __init__(self, name, address, size, type):
        self.name = name
        self.address = address
        self.size = size
        self.type = type  # STT_FUNC, STT_OBJECT, etc.

# 符號類型
STT_NOTYPE = 0
STT_FUNC = 2
STT_OBJECT = 3
STT_FILE = 4
```

## ELF 類型

```c
// e_type 值
ET_NONE = 0        // 無類型
ET_REL = 1         // 可重定位目標檔
ET_EXEC = 2        // 可執行檔
ET_DYN = 3         // 共享物件（.so）
ET_CORE = 4        // Core 檔案
```

## 工具

```bash
# 查看 ELF 資訊
readelf -h program

# 查看 sections
readelf -S program

# 查看符號表
readelf -s program

# 查看程式段
readelf -l program

# 動態依賴
ldd program

# objdump
objdump -d program
```

## 為什麼學習 ELF？

1. **理解二進制**：理解程式如何執行
2. **逆向工程**：分析可執行檔
3. **軟體安全**：漏洞分析
4. **系統程式設計**：連結和載入

## 參考資源

- ELF Specification (Tool Interface Standard)
- "Linkers and Loaders"
- readelf/objdump man pages
