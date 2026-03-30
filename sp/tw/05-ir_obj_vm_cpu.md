# 5. 執行環境：中間碼與目的檔，虛擬機與真實處理器

## 5.1 中間表示（IR）形式

### 5.1.1 中間表示的理論基礎

中間表示（Intermediate Representation, IR）是編譯器前端和後端之間的橋樑。

**IR 的設計原則**

| 原則 | 說明 |
|------|------|
| 與語言無關 | 適用於多種原始語言 |
| 與硬體無關 | 適用於多種目標架構 |
| 便於最佳化 | 便於進行各種程式轉換 |
| 明確語意 | 清晰表達程式行為 |

**IR 的抽象層次**

```
高層 IR（接近原始碼）
    │
    ▼
┌────────────────────────────────────────────┐
│  語法樹 (AST)                             │
│  - 忠實反映原始碼結構                      │
│  - 保留所有語法資訊                       │
└────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────┐
│  三地址碼 (TAC)                           │
│  - 線性化指令序列                         │
│  - 每指令最多三個運算元                    │
└────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────┐
│  低層 IR (接近機器碼)                      │
│  - 具體的暫存器/記憶體操作                │
│  - 接近目標機器的表示                      │
└────────────────────────────────────────────┘
    │
    ▼
低層 IR（接近機器碼）
```

### 5.1.2 三地址碼（TAC）

三地址碼是使用最廣泛的 IR 形式。

**TAC 的特點**

1. 每條指令最多包含三個位址（運算元）
2. 形式：`x = y op z` 或 `x = op y`
3. 使用臨時變數儲存中間結果

**基本指令類型**

| 類型 | 格式 | 說明 |
|------|------|------|
| 算術指令 | `t = x + y` | 雙運算元指令 |
| 單目指令 | `t = -x` | 單運算元指令 |
| 載入指令 | `t = *x` | 記憶體讀取 |
| 儲存指令 | `*x = t` | 記憶體寫入 |
| 無條件跳轉 | `goto L` | 無條件跳轉 |
| 條件跳轉 | `if x goto L` | 條件跳轉 |
| 函數呼叫 | `call f, n` | 呼叫函數 |
| 返回指令 | `return x` | 函數返回 |

**TAC 生成器實作**

[_code/05/05_01_tac_generator.c](_code/05/05_01_tac_generator.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INSTRUCTIONS 100

typedef struct {
    char instructions[MAX_INSTRUCTIONS][128];
    int count;
    int temp_counter;
} TACGenerator;

char* new_temp(TACGenerator *g) {
    static char temp[16];
    sprintf(temp, "t%d", g->temp_counter++);
    return temp;
}

void emit_add(TACGenerator *g, char *result, char *left, char *right) {
    sprintf(g->instructions[g->count++], "%s = %s + %s", result, left, right);
}

void emit_mul(TACGenerator *g, char *result, char *left, char *right) {
    sprintf(g->instructions[g->count++], "%s = %s * %s", result, left, right);
}

int main() {
    TACGenerator g;
    memset(&g, 0, sizeof(TACGenerator));
    
    char *t0 = new_temp(&g);
    char *t1 = new_temp(&g);
    
    emit_mul(&g, t0, "2", "3");
    emit_add(&g, t1, t0, "4");
    
    printf("t0 = 2 * 3\n");
    printf("t1 = t0 + 4\n");
    
    return 0;
}
```

### 5.1.3 靜態單一形式（SSA）

SSA 是 TAC 的一種延伸，其中每個變數只被賦值一次。

**SSA 的特性**

```assembly
# 非 SSA
x = 1
x = x + 1
x = x * 2

# SSA（使用 φ 函數合併不同路徑的值）
x1 = 1
x2 = x1 + 1
x3 = φ(x2, x4)  # 如果從左分支來，選 x2；從右分支來，選 x4
x3 = x3 * 2
```

**φ 函數（Phi Function）**

φ 函數根據控制流選擇正確的版本值：
- 從不同分支匯合時使用
- 需要知道執行的前驅路徑

### 5.1.4 控制流程圖（CFG）

CFG 是表示程式控制流的基本工具。

**基本區塊（Basic Block）**

基本區塊是滿足以下條件的最大連續指令序列：
1. 所有指令按序執行，無跳轉進入
2. 區塊最後一條指令可能是跳轉或分支

**CFG 構建演算法**

```
輸入：三地址碼指令序列
輸出：基本區塊序列

演算法：
1. 找出所有區塊 leader：
   - 第一條指令是 leader
   - 跳轉目標指令是 leader
   - 跳轉後下一條指令是 leader

2. 將指令分配到區塊：
   - 從 leader 到下一個 leader 之前（或指令序列結束）為一個區塊
```

**CFG 範例**

```python
# 原始程式
if (x > 0)
    y = x + 1;
else
    y = 0;
z = y * 2;

# 控制流程圖
   ┌─────────────┐
   │  B1:       │
   │  if x > 0  │
   └──────┬──────┘
          │
    ┌─────┴─────┐
    ▼           ▼
┌────────┐   ┌────────┐
│ B2:   │   │ B3:   │
│ y=x+1 │   │ y=0   │
└───┬────┘   └───┬────┘
    │            │
    └─────┬──────┘
          ▼
    ┌─────────────┐
    │ B4:        │
    │ z = y * 2  │
    └─────────────┘
```

## 5.2 目的檔格式

### 5.2.1 目的檔的結構

目的檔（Object File）包含編譯後的程式碼和資料，以及用於連結的元資料。

**目的檔的組成**

```
┌─────────────────────────────────────────────┐
│  Header (檔頭)                             │
│  - 魔數 (Magic Number)                     │
│  - 架構類型                               │
│  - 段表偏移                               │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  Section Headers (段頭表)                  │
│  - .text (程式碼)                          │
│  - .data (已初始化資料)                    │
│  - .bss (未初始化資料)                     │
│  - .symtab (符號表)                        │
│  - .strtab (字串表)                        │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  Section Data (段資料)                      │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  Relocation Info (重定位資訊)                │
└─────────────────────────────────────────────┘
```

### 5.2.2 ELF 格式（Linux）

ELF（Executable and Linkable Format）是 Linux 系統使用的目的檔和執行檔格式。

**ELF 檔案類型**

| 類型 | 說明 |
|------|------|
| ET_REL | 可重定位檔（.o 檔） |
| ET_EXEC | 可執行檔 |
| ET_DYN | 共享目標檔（.so） |
| ET_CORE | Core dump |

**ELF 檔頭結構**

[_code/05/05_02_elf_parser.c](_code/05/05_02_elf_parser.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct {
    uint8_t magic[4];
    uint16_t type;
    uint16_t machine;
    uint64_t entry;
} ELFHeader;

int parse_elf_header(ELFHeader *header, const uint8_t *data) {
    if (data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
        printf("Not a valid ELF file\n");
        return -1;
    }
    
    header->type = (data[16]) | (data[17] << 8);
    header->machine = (data[18]) | (data[19] << 8);
    
    printf("ELF Type: %d\n", header->type);
    printf("Target Machine: %d\n", header->machine);
    printf("Entry Point: 0x%lx\n", header->entry);
    
    return 0;
}

int main() {
    uint8_t dummy_elf[64] = {0};
    ELFHeader header;
    return parse_elf_header(&header, dummy_elf);
}
```

### 5.2.3 PE 格式（Windows）

PE（Portable Executable）是 Windows 系統使用的執行檔格式。

**PE 檔案結構**

```
┌─────────────────────────────────────────────┐
│  DOS Header (MZ)                           │
│  - DOS 向下相容                             │
│  - 指向 PE Header                          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  PE Signature                               │
│  - "PE\0\0"                               │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  COFF File Header                          │
│  - 機器類型、區段數                        │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  Optional Header                           │
│  - 入口點、影像基址                        │
│  - 資料目錄                               │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  Section Headers                           │
│  - .text, .data, .rdata, .bss            │
└─────────────────────────────────────────────┘
```

```python
class PEParser:
    """PE (Portable Executable) 解析器"""
    
    DOS_HEADER_SIGNATURE = b'MZ'
    PE_SIGNATURE = b'PE\x00\x00'
    
    def parse(self, data):
        # DOS Header
        if data[:2] != self.DOS_HEADER_SIGNATURE:
            raise ValueError("不是有效的 PE 檔")
        
        # PE 簽名位置
        e_lfanew = struct.unpack('<I', data[60:64])[0]
        
        # PE 簽名
        if data[e_lfanew:e_lfanew+4] != self.PE_SIGNATURE:
            raise ValueError("PE 簽名無效")
        
        print(f"有效的 PE 檔，PE 頭位於: {e_lfanew}")
```

[_code/05/05_03_pe_parser.c](_code/05/05_03_pe_parser.c)

```c
#include <stdio.h>
#include <stdint.h>

#define DOS_SIGNATURE 0x5A4D
#define PE_SIGNATURE 0x00004550

int parse_pe_header(const uint8_t *data) {
    uint16_t dos_sig = data[0] | (data[1] << 8);
    if (dos_sig != DOS_SIGNATURE) {
        printf("Not a valid PE file\n");
        return -1;
    }
    
    uint32_t e_lfanew = data[60] | (data[61] << 8) | (data[62] << 16) | (data[63] << 24);
    uint32_t pe_sig = data[e_lfanew] | (data[e_lfanew+1] << 8) | 
                      (data[e_lfanew+2] << 16) | (data[e_lfanew+3] << 24);
    
    if (pe_sig != PE_SIGNATURE) {
        printf("Invalid PE signature\n");
        return -1;
    }
    
    printf("Valid PE file, PE header at: %u\n", e_lfanew);
    return 0;
}

int main() {
    return 0;
}
```

### 5.2.4 Mach-O 格式（macOS）

Mach-O 是 macOS 系統使用的目的檔和執行檔格式。

**Mach-O 特色**

| 特性 | 說明 |
|------|------|
| Fat Binary | 單一檔案含多架構碼 |
| Universal Binary | Apple 的 Fat Binary 品牌名 |
| Code Signing | 執行階段驗證 |

```python
class MachOParser:
    """Apple Mach-O 解析器"""
    
    FAT_MAGIC = 0xcafebabe
    MH_MAGIC = 0xfeedface
    
    def parse(self, data):
        magic = struct.unpack('>I', data[:4])[0]
        
        if magic == self.FAT_MAGIC:
            print("Fat Binary (通用二進制)")
        elif magic == self.MH_MAGIC:
            print("32-bit Mach-O")
        else:
            print("64-bit Mach-O")
```

[_code/05/05_04_macho_parser.c](_code/05/05_04_macho_parser.c)

```c
#include <stdio.h>
#include <stdint.h>

#define FAT_MAGIC 0xcafebabe
#define MH_MAGIC 0xfeedface
#define MH_MAGIC_64 0xfeedfacf

int parse_macho(uint32_t magic) {
    if (magic == FAT_MAGIC) {
        printf("Fat Binary\n");
    } else if (magic == MH_MAGIC) {
        printf("32-bit Mach-O\n");
    } else if (magic == MH_MAGIC_64) {
        printf("64-bit Mach-O\n");
    } else {
        printf("Unknown format\n");
        return -1;
    }
    return 0;
}

int main() {
    parse_macho(MH_MAGIC_64);
    return 0;
}
```

## 5.3 虛擬機架構

### 5.3.1 堆疊式 VM vs 暫存器式 VM

**堆疊式 VM（Stack-based VM）**

特點：
- 使用運算元堆疊儲存運算元
- 指令緊湊（無需指定運算元位置）
- 所有運算元隱含存取

代表：
- JVM (Java)
- .NET CLR
- Python VM

**堆疊式 VM（Stack-based VM）**

[_code/05/05_05_stack_vm.c](_code/05/05_05_stack_vm.c)

```c
#include <stdio.h>
#include <stdlib.h>

#define MAX_STACK 256

typedef enum {OP_ICONST, OP_IADD, OP_PRINT, OP_HALT} OpCode;

typedef struct {
    int stack[MAX_STACK];
    int sp;
} StackVM;

void push(StackVM *vm, int val) { vm->stack[vm->sp++] = val; }
int pop(StackVM *vm) { return vm->stack[--vm->sp]; }

void run(StackVM *vm, OpCode *bc, int len) {
    for (int pc = 0; pc < len; pc++) {
        switch (bc[pc]) {
            case OP_ICONST: push(vm, bc[++pc]); break;
            case OP_IADD: { int b = pop(vm), a = pop(vm); push(vm, a + b); break; }
            case OP_PRINT: printf("%d\n", pop(vm)); break;
            case OP_HALT: return;
        }
    }
}

int main() {
    StackVM vm = {0};
    OpCode bc[] = {OP_ICONST, 1, OP_ICONST, 2, OP_IADD, OP_PRINT, OP_HALT};
    run(&vm, bc, 7);
    return 0;
}
```

**暫存器式 VM（Register-based VM）**

特點：
- 使用虛擬暫存器集合
- 指令需指定運算元位置
- 較少指令數量

代表：
- Lua VM
- Dalvik VM (Android)

**暫存器式 VM（Register-based VM）**

[_code/05/05_06_register_vm.c](_code/05/05_06_register_vm.c)

```c
#include <stdio.h>

#define NUM_REGS 256

typedef enum {OP_LOADK, OP_ADD, OP_PRINT, OP_HALT} OpCode;

typedef struct {
    int regs[NUM_REGS];
    int pc;
} RegisterVM;

void run(RegisterVM *vm, int *bc, int len) {
    while (vm->pc < len) {
        switch (bc[vm->pc++]) {
            case OP_LOADK:
                vm->regs[bc[vm->pc++]] = bc[vm->pc++];
                break;
            case OP_ADD: {
                int d = bc[vm->pc++], l = bc[vm->pc++], r = bc[vm->pc++];
                vm->regs[d] = vm->regs[l] + vm->regs[r];
                break;
            }
            case OP_PRINT:
                printf("%d\n", vm->regs[bc[vm->pc++]]);
                break;
            case OP_HALT:
                return;
        }
    }
}

int main() {
    RegisterVM vm = {0};
    int bc[] = {OP_LOADK, 0, 1, OP_LOADK, 1, 2, OP_ADD, 2, 0, 1, OP_PRINT, 2, OP_HALT};
    run(&vm, bc, 13);
    return 0;
}
```

### 5.3.2 兩種 VM 的比較

| 特性 | 堆疊式 VM | 暫存器式 VM |
|------|------------|--------------|
| 指令大小 | 較小 | 較大 |
| 指令數量 | 較多 | 較少 |
| 執行速度 | 需頻繁堆疊存取 | 減少存取次數 |
| 實作複雜度 | 簡單 | 較複雜 |
| 省電效率 | 較差 | 較好 |

**比較：同一段程式碼的位元組碼差異**

[_code/05/05_05_stack_vm.c](_code/05/05_05_stack_vm.c) (Stack VM)
[_code/05/05_06_register_vm.c](_code/05/05_06_register_vm.c) (Register VM)

```c
#include <stdio.h>

int main() {
    printf("=== Stack-based VM ===\n");
    printf("bytecode: [ICONST, 1, ICONST, 2, IADD, PRINT, HALT]\n");
    
    printf("\n=== Register-based VM ===\n");
    printf("bytecode: [LOADK, R0, 1, LOADR, R1, 2, ADD, R2, R0, R1, PRINT, R2, HALT]\n");
    
    return 0;
}
```

## 5.4 x86/x64、ARM、RISC-V 架構介紹

### 5.4.1 指令集架構（ISA）的分類

**複雜指令集電腦（CISC）**

- x86/x64 是典型 CISC
- 指令長度可變
- 指令功能強大但複雜
- 記憶體對記憶體指令

**精簡指令集電腦（RISC）**

- ARM、RISC-V 是典型 RISC
- 指令長度固定（32 位元）
- 載入/儲存架構（記憶體僅透過特定指令存取）
- 大量暫存器

### 5.4.2 x86-64 架構

x86-64（也稱 AMD64）是 Intel 64 位元擴展，廣泛用於 PC 和伺服器。

**x86-64 特色**

| 特性 | 說明 |
|------|------|
| 位址空間 | 64 位元（實際使用 48 位元虛擬位址） |
| 通用暫存器 | 16 個 64 位元暫存器 |
| 呼叫約定 | System V AMD64 ABI |
| 資料模型 | LP64 |

**通用暫存器**

```
rax, rbx, rcx, rdx
rsi, rdi, rbp, rsp
r8, r9, r10, r11
r12, r13, r14, r15
```

**x86-64 組合語言範例**

```asm
# add 函數
add:
    lea    (%rdi,%rsi,1), %rax   # rax = rdi + rsi
    ret

# main 函數
main:
    push   %rbp
    mov    %rsp, %rbp
    mov    $2, %esi               # 第二個參數
    mov    $1, %edi               # 第一個參數
    call   add
    pop    %rbp
    ret
```

### 5.4.3 ARM64（AArch64）架構

ARM64 是 64 位元 ARM 架構，廣泛用於行動裝置和嵌入式系統。

**ARM64 特色**

| 特性 | 說明 |
|------|------|
| 固定指令長度 | 32 位元 |
| 大量暫存器 | 31 個通用暫存器 |
| 簡化指令 | 指令功能較單一 |
| 條件執行 | 部分指令支援條件執行 |

**通用暫存器**

```
x0-x30 (64 位元) / w0-w30 (32 位元)
x29 (fp - Frame Pointer)
x30 (lr - Link Register)
sp (Stack Pointer)
xzr (Zero Register)
```

**ARM64 組合語言範例**

```asm
# add 函數
add:
    add    w0, w0, w1            # w0 = w0 + w1
    ret

# main 函數
main:
    stp    x29, x30, [sp, -16]!  # 保存 frame pointer
    mov    w1, 2                 # 第二個參數
    mov    w0, 1                 # 第一個參數
    bl     add                   # 呼叫 add
    ldp    x29, x30, [sp], 16    # 恢復
    ret
```

### 5.4.4 RISC-V 架構

RISC-V 是開源的 RISC 指令集架構，設計簡潔靈活。

**RISC-V 特色**

| 特性 | 說明 |
|------|------|
| 模組化設計 | 基本整數指令 + 擴展 |
| 開放標準 | 無專利授權限制 |
| 暫存器 | 32 個通用暫存器 (x0-x31) |
| 簡潔設計 | 基礎指令少於 50 條 |

**RISC-V 組合語言範例**

```asm
# add 函數
add:
    add    a0, a0, a1            # a0 = a0 + a1
    ret

# main 函數
    addi   a1, zero, 2           # a1 = 2
    addi   a0, zero, 1           # a0 = 1
    jal    ra, add               # 呼叫 add
    # a0 現在是結果
```

## 5.5 系統呼叫與 ABI

### 5.5.1 系統呼叫的原理

系統呼叫（System Call）是使用者程式請求作業系統核心服務的機制。

**使用者模式 vs 核心模式**

```
┌─────────────────────────────────────────────┐
│              使用者模式                       │
│         (User Mode / Ring 3)                 │
│  - 應用程式執行                            │
│  - 無法直接存取硬體                        │
│  - 受記憶體保護限制                        │
└─────────────────────────────────────────────┘
                    │ 系統呼叫
                    ▼
┌─────────────────────────────────────────────┐
│              核心模式                        │
│         (Kernel Mode / Ring 0)              │
│  - 作業系統核心執行                        │
│  - 可存取所有硬體                          │
│  - 可執行特殊指令                          │
└─────────────────────────────────────────────┘
```

**系統呼叫機制（x86-64）**

1. 將系統呼叫號放入 `rax`
2. 將參數放入 `rdi, rsi, rdx, r10, r8, r9`
3. 執行 `syscall` 指令
4. 核心處理後，返回值放入 `rax`

```c
/* Linux 系統呼叫範例 */
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    // write(1, "Hello\n", 6)
    // 系統呼叫號: 1 (write)
    // fd=1, buf="Hello\n", count=6
    char msg[] = "Hello, World!\n";
    syscall(SYS_write, 1, msg, 14);
    
    // exit(0)
    syscall(SYS_exit, 0);
    return 0;
}
```

### 5.5.2 ABI（應用程式二進位介面）

ABI 定義了程式二進位介面的低層細節。

**ABI 的組成部分**

| 部分 | 說明 |
|------|------|
| 呼叫約定 | 參數傳遞、返回值、暫存器保存 |
| 記憶體布局 | 堆疊框架、資料對齊 |
| 符號修飾 | 函數名稱的編碼方式 |
| 目的檔格式 | 目標平台的執行檔格式 |

**x86-64 System V ABI**

呼叫約定：
- 參數傳遞：`rdi, rsi, rdx, rcx, r8, r9`
- 返回值：`rax`（整數）、`xmm0`（浮點數）
- 被呼叫者保存：`rbx, rbp, r12, r13, r14, r15`
- 呼叫者保存：`rax, rcx, rdx, rsi, rdi, r8, r9, r10, r11`

```c
// 呼叫約定示意圖
void function(int a, int b) {
    // a -> rdi, b -> rsi
    int local = a + b;  // local 在堆疊上
    // 返回值在 rax
}
```

### 5.5.3 作業系統 API vs 語言 API

**作業系統 API**

- 直接提供給應用程式的系統呼叫介面
- 例如：POSIX API、Win32 API

**語言標準庫**

- 程式語言提供的標準功能
- 對作業系統 API 的封裝
- 提供跨平台抽象

```
應用程式 → 語言標準庫 → 作業系統 API → 核心
           (libc, STL)   (syscall)      ↓
                                    硬體
```

**C socket 範例**

[_code/05/05_06_socket.c](_code/05/05_06_socket.c)

```c
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main() {
    printf("=== POSIX Socket API ===\n\n");
    
    printf("C socket example:\n");
    printf("  int sock = socket(AF_INET, SOCK_STREAM, 0);\n");
    printf("  struct sockaddr_in addr = {\n");
    printf("      .sin_family = AF_INET,\n");
    printf("      .sin_port = htons(8080),\n");
    printf("      .sin_addr.s_addr = inet_addr(\"127.0.0.1\")\n");
    printf("  };\n");
    printf("  connect(sock, (struct sockaddr*)&addr, sizeof(addr));\n\n");
    
    printf("Call hierarchy:\n");
    printf("  Python: socket.connect()\n");
    printf("     |  (wraps)\n");
    printf("  C:     connect()\n");
    printf("     |  (syscall)\n");
    printf("  Kernel: sys_connect\n\n");
    
    printf("Language runtime provides:\n");
    printf("  - Memory management\n");
    printf("  - Type system\n");
    printf("  - Standard library\n");
    printf("  - System call abstraction\n");
    
    return 0;
}
```
