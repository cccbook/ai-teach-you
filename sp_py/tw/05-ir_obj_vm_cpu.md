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

```python
"""
三地址碼（TAC）IR 系統
"""

class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        """產生新的臨時變數"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        """產生新的標籤"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit_add(self, result, left, right):
        self.instructions.append(f"{result} = {left} + {right}")
    
    def emit_sub(self, result, left, right):
        self.instructions.append(f"{result} = {left} - {right}")
    
    def emit_mul(self, result, left, right):
        self.instructions.append(f"{result} = {left} * {right}")
    
    def emit_div(self, result, left, right):
        self.instructions.append(f"{result} = {left} / {right}")
    
    def emit_load(self, dest, address):
        self.instructions.append(f"{dest} = *{address}")
    
    def emit_store(self, source, address):
        self.instructions.append(f"*{address} = {source}")
    
    def emit_branch(self, label):
        self.instructions.append(f"goto {label}")
    
    def emit_cond_branch(self, cond, true_label, false_label):
        self.instructions.append(f"if {cond} goto {true_label}")
        self.instructions.append(f"goto {false_label}")
    
    def emit_label(self, label):
        self.instructions.append(f"{label}:")
    
    def emit_call(self, func, args):
        self.instructions.append(f"call {func}({', '.join(args)})")
    
    def emit_return(self, value):
        self.instructions.append(f"return {value}")
    
    def translate(self, node):
        """翻譯 AST 為 TAC"""
        if node['type'] == 'number':
            return str(node['value'])
        if node['type'] == 'identifier':
            return node['name']
        if node['type'] == 'binary':
            left = self.translate(node['left'])
            right = self.translate(node['right'])
            result = self.new_temp()
            if node['op'] == '+':
                self.emit_add(result, left, right)
            elif node['op'] == '-':
                self.emit_sub(result, left, right)
            elif node['op'] == '*':
                self.emit_mul(result, left, right)
            elif node['op'] == '/':
                self.emit_div(result, left, right)
            return result
        return ""

# 測試 TAC 生成
tac = TACGenerator()
ast = {
    'type': 'binary',
    'op': '+',
    'left': {'type': 'binary', 'op': '*', 'left': {'type': 'number', 'value': 2}, 'right': {'type': 'number', 'value': 3}},
    'right': {'type': 'number', 'value': 4}
}
tac.translate(ast)
print("\n".join(tac.instructions))
# 輸出：
# t0 = 2 * 3
# t1 = t0 + 4
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

```python
class ELFParser:
    def __init__(self, data):
        self.data = data
    
    def parse_header(self):
        """解析 ELF 檔頭"""
        # ELF 魔數
        magic = self.data[:4]
        if magic != b'\x7fELF':
            raise ValueError("不是有效的 ELF 檔")
        
        # 檔頭結構
        e_type = struct.unpack('<H', self.data[16:18])[0]
        e_machine = struct.unpack('<H', self.data[18:20])[0]
        e_entry = struct.unpack('<Q', self.data[24:32])[0]
        e_phoff = struct.unpack('<Q', self.data[32:40])[0]
        e_shoff = struct.unpack('<Q', self.data[40:48])[0]
        
        print(f"ELF 類型: {e_type}")
        print(f"目標架構: {e_machine}")
        print(f"入口點: 0x{e_entry:x}")
        print(f"程式頭偏移: {e_phoff}")
        print(f"區段頭偏移: {e_shoff}")
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

```python
class StackVM:
    def __init__(self):
        self.stack = []      # 操作數堆疊
        self.variables = {}  # 區域變數
        self.pc = 0
    
    def run(self, bytecode):
        while self.pc < len(bytecode):
            op = bytecode[self.pc]
            
            if op == 'iconst':
                self.stack.append(bytecode[self.pc + 1])
                self.pc += 2
            
            elif op == 'iload':
                var_idx = bytecode[self.pc + 1]
                self.stack.append(self.variables.get(var_idx, 0))
                self.pc += 2
            
            elif op == 'istore':
                self.variables[bytecode[self.pc + 1]] = self.stack.pop()
                self.pc += 2
            
            elif op == 'iadd':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
                self.pc += 1
```

**暫存器式 VM（Register-based VM）**

特點：
- 使用虛擬暫存器集合
- 指令需指定運算元位置
- 較少指令數量

代表：
- Lua VM
- Dalvik VM (Android)

```python
class RegisterVM:
    def __init__(self):
        self.registers = [0] * 256  # 256 個暫存器
        self.pc = 0
    
    def run(self, bytecode):
        while self.pc < len(bytecode):
            op = bytecode[self.pc]
            
            if op == 'LOADK':  # 載入常數到暫存器
                reg = bytecode[self.pc + 1]
                const = bytecode[self.pc + 2]
                self.registers[reg] = const
                self.pc += 3
            
            elif op == 'ADD':  # 暫存器相加
                dest = bytecode[self.pc + 1]
                left = bytecode[self.pc + 2]
                right = bytecode[self.pc + 3]
                self.registers[dest] = self.registers[left] + self.registers[right]
                self.pc += 4
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

```python
# 計算 1 + 2:
print("=== 基於堆疊 VM ===")
stack_bytecode = [
    'iconst', 1,    # 推入 1
    'iconst', 2,    # 推入 2
    'iadd',         # 彈出並相加，結果推回
    'print',        # 輸出
    'halt'
]

print("\n=== 基於暫存器 VM ===")
register_bytecode = [
    'LOADK', 0, 1,     # R0 = 1
    'LOADK', 1, 2,     # R1 = 2
    'ADD', 2, 0, 1,    # R2 = R0 + R1
    'PRINT', 2,        # 輸出 R2
    'HALT'
]
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

**Python socket 範例**

```python
import socket

# Python 封裝了 POSIX socket API
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8080))

# 底層可能呼叫：connect() → SYS_connect → 核心
```
