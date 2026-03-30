# PE (Portable Executable)

## 概述

PE（Portable Executable）是 Windows 系統的可執行檔格式，用於 EXE、DLL、SYS 等檔案。PE 是 COFF（Common Object File Format）的擴展，繼承自早期的 DOS MZ executable。

## 歷史

- **1987**：DOS 引入 MZ executable
- **1993**：Windows NT 引入 PE
- **1995**：Windows 95 採用 PE
- **現在**：所有 Windows 版本標準

## PE 結構

```
┌──────────────────────────────┐
│ DOS Header (MZ)              │
│ DOS Stub                     │
├──────────────────────────────┤
│ PE Signature                 │
├──────────────────────────────┤
│ COFF Header (File Header)   │
├──────────────────────────────┤
│ Optional Header              │
├──────────────────────────────┤
│ Section Headers              │
├──────────────────────────────┤
│ Section 1: .text             │
│ Section 2: .data             │
│ Section 3: .rdata            │
│ ...                         │
└──────────────────────────────┘
```

### 1. DOS Header

```c
typedef struct _IMAGE_DOS_HEADER {
    uint16_t e_magic;      // 0x5A4D ("MZ")
    uint16_t e_cblp;
    uint16_t e_cp;
    uint16_t e_crlc;
    uint16_t e_cparhdr;
    uint16_t e_minalloc;
    uint16_t e_maxalloc;
    uint16_t e_ss;
    uint16_t e_sp;
    uint16_t e_csum;
    uint16_t e_ip;
    uint16_t e_cs;
    uint16_t e_lfarlc;
    uint16_t e_ovno;
    uint16_t e_res[4];
    uint16_t e_oemid;
    uint16_t e_oeminfo;
    uint32_t e_res2[10];
    uint32_t e_lfanew;     // PE Header 偏移
} IMAGE_DOS_HEADER;
```

### 2. PE Header

```c
typedef struct _IMAGE_FILE_HEADER {
    uint16_t Machine;
    uint16_t NumberOfSections;
    uint32_t TimeDateStamp;
    uint32_t PointerToSymbolTable;
    uint32_t NumberOfSymbols;
    uint16_t SizeOfOptionalHeader;
    uint16_t Characteristics;
} IMAGE_FILE_HEADER;

// Machine 類型
IMAGE_FILE_MACHINE_I386 = 0x014c  // x86
IMAGE_FILE_MACHINE_AMD64 = 0x8664 // x64
IMAGE_FILE_MACHINE_ARM = 0x01c0   // ARM
IMAGE_FILE_MACHINE_ARM64 = 0xaa64 // ARM64
```

### 3. Optional Header

```c
typedef struct _IMAGE_OPTIONAL_HEADER64 {
    uint16_t Magic;                    // 0x20b (64-bit)
    uint8_t  MajorLinkerVersion;
    uint8_t  MinorLinkerVersion;
    uint32_t SizeOfCode;
    uint32_t SizeOfInitializedData;
    uint32_t SizeOfUninitializedData;
    uint32_t AddressOfEntryPoint;     // 入口點 RVA
    uint32_t BaseOfCode;
    uint64_t ImageBase;               // 載入位址
    uint32_t SectionAlignment;
    uint32_t FileAlignment;
    uint16_t MajorOperatingSystemVersion;
    uint16_t MinorOperatingSystemVersion;
    // ...
} IMAGE_OPTIONAL_HEADER64;
```

### 4. 解析 PE 檔案

```python
import struct

class PE:
    def __init__(self, data):
        self.data = data
        self.parse()
    
    def parse(self):
        # DOS Header
        if self.data[:2] != b'MZ':
            raise ValueError("不是有效的 PE 檔案")
        
        # PE Header 偏移
        dos_header = struct.unpack('<H', self.data[60:62])[0]
        
        # PE Signature
        if self.data[dos_header:dos_header+4] != b'PE\x00\x00':
            raise ValueError("無效的 PE 簽名")
        
        # COFF Header
        coff = self.data[dos_header+4:]
        self.machine = struct.unpack('<H', coff[:2])[0]
        self.num_sections = struct.unpack('<H', coff[2:4])[0]
        self.size_optional = struct.unpack('<H', coff[16:18])[0]
        
        # Optional Header
        opt = coff[20:20+self.size_optional]
        self.entry_point = struct.unpack('<I', opt[16:20])[0]
        self.image_base = struct.unpack('<Q', opt[24:32])[0]
```

### 5. Sections

```python
# 標準 sections
SECTIONS = {
    '.text': '可執行代碼',
    '.data': '已初始化資料',
    '.rdata': '唯讀資料',
    '.bss': '未初始化資料',
    '.rsrc': '資源',
    '.reloc': '重定位',
    '.edata': '匯出表',
    '.idata': '匯入表',
}

# 解析 section headers
def parse_sections(pe):
    sections = []
    offset = pe.dos_header + 4 + 20 + pe.size_optional
    
    for i in range(pe.num_sections):
        name = pe.data[offset:offset+8].decode().strip('\x00')
        vsize = struct.unpack('<I', pe.data[offset+8:offset+12])[0]
        vaddr = struct.unpack('<I', pe.data[offset+12:offset+16])[0]
        raw_size = struct.unpack('<I', pe.data[offset+16:offset+20])[0]
        raw_offset = struct.unpack('<I', pe.data[offset+20:offset+24])[0]
        
        sections.append({
            'name': name,
            'vsize': vsize,
            'vaddr': vaddr,
            'size': raw_size,
            'offset': raw_offset,
        })
        offset += 40
    
    return sections
```

### 6. 匯入表

```python
def parse_imports(pe):
    # 找到 .idata section
    # 解析 IMAGE_IMPORT_DESCRIPTOR
    pass
```

## PE 工具

```bash
# 查看 PE 資訊
dumpbin /headers program.exe

# PE Explorer
peview program.exe

# CFF Explorer
cff-explorer program.exe

# objdump
objdump -f program.exe
```

## 為什麼學習 PE？

1. **Windows 逆向**：分析 Windows 程式
2. **軟體開發**：理解程式載入
3. **安全分析**：病毒分析、漏洞挖掘
4. **殼與保護**：加殼技術

## 參考資源

- Microsoft PE/COFF Specification
- "Reversing: Secrets of Reverse Engineering"
- "Windows Internals"
