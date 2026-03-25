# Mach-O (Mach Object)

## 概述

Mach-O 是 macOS、iOS、tvOS 等 Apple 系統的原生可執行檔格式。作為 Mach 核心的延伸，Mach-O 支援 Universal Binaries（通用二進制），可包含多種架構的程式碼。

## 歷史

- **1988**：NeXTSTEP 引入 Mach-O
- **2001**：macOS X 採用 Mach-O
- **現在**：macOS 和 iOS 標準格式

## Mach-O 結構

```
┌──────────────────────────────┐
│ Mach Header                  │
├──────────────────────────────┤
│ Load Commands                │
│ (segment commands)           │
├──────────────────────────────┤
│ Segment 1: __TEXT           │
│ (代碼)                      │
├──────────────────────────────┤
│ Segment 2: __DATA           │
│ (資料)                      │
├──────────────────────────────┤
│ ...                         │
└──────────────────────────────┘
```

### 1. Mach Header

```c
#define MH_MAGIC_64 0xfeedfacf
#define MH_CIGAM_64 0xcffaedfe  // Big endian

struct mach_header_64 {
    uint32_t    magic;      // 魔數
    cpu_type_t  cputype;    // CPU 類型
    cpu_subtype_t cpusubtype; // CPU 子類型
    uint32_t    filetype;   // 檔案類型
    uint32_t    ncmds;      // load commands 數量
    uint32_t    sizeofcmds; // commands 總大小
    uint32_t    flags;      // 標誌
};
```

### 2. CPU 類型

```c
#define CPU_TYPE_X86           (CPU_ARCH_MASK | 7)
#define CPU_TYPE_X86_64        (CPU_ARCH_MASK | 0x01000007)
#define CPU_TYPE_ARM           (CPU_ARCH_MASK | 12)
#define CPU_TYPE_ARM64         (CPU_ARCH_MASK | 0x0200000c)
#define CPU_TYPE_ARM64_32      (CPU_ARCH_MASK | 0x0200000d)
```

### 3. 檔案類型

```c
#define MH_OBJECT        0x1     // 目標檔 .o
#define MH_EXECUTE       0x2     // 可執行檔
#define MH_FVMLIB        0x3     // FVM 函式庫
#define MH_CORE          0x4     // Core 檔案
#define MH_PRELOAD       0x5     // 預先載入
#define MH_DYLIB        0x6     // 動態庫 .dylib
#define MH_DYLINKER      0x7     // 動態連結器
#define MH_BUNDLE        0x8     // Bundle
```

### 4. 解析 Mach-O

```python
import struct

class MachO:
    def __init__(self, data):
        self.data = data
        self.parse_header()
    
    def parse_header(self):
        magic = struct.unpack('<I', self.data[:4])[0]
        
        if magic == 0xfeedface:  # 32-bit
            self.is_64 = False
            self.parse_32()
        elif magic == 0xfeedfacf:  # 64-bit
            self.is_64 = True
            self.parse_64()
        elif magic == 0xcefaedfe:  # 32-bit BE
            self.is_64 = False
            self.swap_endian()
            self.parse_32()
        elif magic == 0xcffaedfe:  # 64-bit BE
            self.is_64 = True
            self.swap_endian()
            self.parse_64()
    
    def parse_64(self):
        self.cputype = struct.unpack('<i', self.data[4:8])[0]
        self.cpusubtype = struct.unpack('<i', self.data[8:12])[0]
        self.filetype = struct.unpack('<I', self.data[12:16])[0]
        self.ncmds = struct.unpack('<I', self.data[16:20])[0]
        self.sizeofcmds = struct.unpack('<I', self.data[20:24])[0]
        self.flags = struct.unpack('<I', self.data[24:28])[0]
```

### 5. Load Commands

```c
#define LC_SEGMENT_64      0x19    // 64-bit segment
#define LC_SEGMENT         0x1    // 32-bit segment
#define LC_SYMTAB          0x2    // 符號表
#define LC_DYSYMTAB        0x0b    // 動態符號表
#define LC_LOAD_DYLIB      0xc    // 匯入動態庫
#define LC_MAIN            0x80000028 // 入口點
```

### 6. Segment 結構

```c
struct segment_command_64 {
    uint32_t    cmd;        // LC_SEGMENT_64
    uint32_t    cmdsize;   // command 大小
    char        segname[16]; // segment 名稱
    uint64_t    vmaddr;     // 虛擬位址
    uint64_t    vmsize;     // 虛擬大小
    uint64_t    fileoff;    // 檔案偏移
    uint64_t    filesize;   // 檔案大小
    uint32_t    maxprot;    // 最大保護
    uint32_t    initprot;  // 初始保護
    uint32_t    nsects;     // section 數量
    uint32_t    flags;      // 標誌
};
```

### 7. Sections

```c
// 標準 segments 和 sections
__TEXT:
  __text          // 可執行指令
  __stubs         // 連結器 stubs
  __stub_helper  // 輔助程式
  __cstring       // C 字串

__DATA:
  __data          // 初始化資料
  __bss           // 未初始化資料
  __la_symbol_ptr // Lazy 符號指標
  __nl_symbol_ptr // Non-lazy 符號指標

__LINKEDIT:
  __symbol_stub   // 符號 stubs
  __nl_symbol_ptr // NL 符號指標
```

### 8. Universal Binaries

```python
# 查看 Universal Binary 架構
def parse_fat_header(data):
    magic = struct.unpack('>I', data[:4])[0]
    if magic != 0xcafebabe:
        return None
    
    nfat_arch = struct.unpack('>I', data[4:8])[0]
    
    archs = []
    offset = 8
    for _ in range(nfat_arch):
        cputype = struct.unpack('>i', data[offset:offset+4])[0]
        cpusubtype = struct.unpack('>i', data[offset+4:offset+8])[0]
        offset_addr = struct.unpack('>I', data[offset+8:offset+12])[0]
        size = struct.unpack('>I', data[offset+12:offset+16])[0]
        align = struct.unpack('>I', data[offset+16:offset+20])[0]
        
        archs.append({
            'cputype': cputype,
            'offset': offset_addr,
            'size': size,
            'align': align,
        })
        offset += 20
    
    return archs
```

## Mach-O 工具

```bash
# 查看檔案架構
lipo -info program

# 查看內容
otool -hv program
otool -t program  # text section
otool -L program  # 動態庫依賴

# otool 範例
otool -L /usr/lib/libSystem.B.dylib
otool -l program  # load commands
```

## 為什麼學習 Mach-O？

1. **macOS/iOS 開發**：理解 Apple 平台
2. **逆向分析**：分析 Apple 應用
3. **安全研究**：iOS 越獄、安全研究
4. **跨平台**： Universal Binaries 概念

## 參考資源

- Apple Mach-O Format Reference
- "Mac OS X Internals"
- otool man page
