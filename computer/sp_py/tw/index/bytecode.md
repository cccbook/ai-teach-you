# 位元組碼 (Bytecode)

## 概述

位元組碼是一種中介程式表示，由直譯器或 JIT 編譯器執行，而非直接由 CPU 執行。每條位元組碼指令通常佔用 1-2 位元組，形成與硬體無關的中間碼，便於跨平台執行。

## 歷史

- **1960s**：IBM 開發 p-code for PL/I
- **1970s**：Pascal p-code 直譯器
- **1990s**：Java 位元組碼席捲業界
- **1999**：.NET CIL/CLR
- **現在**：Python、Ruby、Bridge.NET

## 位元組碼格式

```
[操作碼] [操作數1] [操作數2] ...
 1 byte   1-8 bytes
```

### 1. Java 位元組碼範例

```java
// Java 原始碼
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

```
// javap -c Hello 反編譯結果
public static void main(java.lang.String[]);
  Code:
   0: getstatic     #2
   3: ldc           #3
   5: invokevirtual #4
   8: return
```

### 2. 虛擬機指令集

```python
# 簡化位元組碼指令集
OPCODES = {
    'LOAD': 0x01,    # 載入變數
    'STORE': 0x02,   # 儲存變數
    'CONST': 0x03,   # 常數
    'ADD': 0x10,     # 加法
    'SUB': 0x11,     # 減法
    'MUL': 0x12,     # 乘法
    'DIV': 0x13,     # 除法
    'JUMP': 0x20,    # 跳轉
    'JUMP_IF': 0x21, # 條件跳轉
    'CALL': 0x30,    # 函數調用
    'RET': 0x31,     # 返回
    'PRINT': 0x40,   # 列印
}
```

### 3. 自訂位元組碼直譯器

```python
class BytecodeVM:
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.ip = 0  # 指令指標
    
    def execute(self, bytecode):
        while self.ip < len(bytecode):
            op = bytecode[self.ip]
            
            if op == 0x01:  # LOAD
                self.ip += 1
                var = bytecode[self.ip]
                self.stack.append(self.variables.get(var, 0))
            
            elif op == 0x02:  # STORE
                self.ip += 1
                var = bytecode[self.ip]
                value = self.stack.pop()
                self.variables[var] = value
            
            elif op == 0x03:  # CONST
                self.ip += 1
                value = bytecode[self.ip]
                self.stack.append(value)
            
            elif op == 0x10:  # ADD
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            
            elif op == 0x40:  # PRINT
                value = self.stack.pop()
                print(value)
            
            elif op == 0xFF:  # HALT
                break
            
            self.ip += 1

# 執行範例: x = 5 + 3; print x
bytecode = [
    0x03, 5,       # CONST 5
    0x03, 3,       # CONST 3
    0x10,          # ADD
    0x02, ord('x'), # STORE x
    0x01, ord('x'), # LOAD x
    0x40,          # PRINT
    0xFF,          # HALT
]

vm = BytecodeVM()
vm.execute(bytecode)
```

### 4. Python 位元組碼

```python
import dis

def example():
    x = 1 + 2
    y = x * 3
    return y

# 查看位元組碼
dis.dis(example)
```

輸出：
```
  1           0 LOAD_CONST               1 (3)
              3 STORE_FAST               0 (x)
  2           6 LOAD_FAST                0 (x)
              9 LOAD_CONST               2 (3)
             12 BINARY_MULTIPLY
             13 STORE_FAST               1 (y)
  3          16 LOAD_FAST                1 (y)
             19 RETURN_VALUE
```

### 5. .NET CIL

```csharp
// C# 原始碼
public static void Main() {
    int x = 5;
    int y = 10;
    Console.WriteLine(x + y);
}
```

```
// IL 反編譯
.method private hidebysig static void Main() cil managed
{
  .entrypoint
  .maxstack  2
  .locals init (int32 x, int32 y)
  IL_0000:  ldc.i4.5
  IL_0001:  stloc.0
  IL_0002:  ldc.i4.s  10
  IL_0004:  stloc.1
  IL_0005:  ldloc.0
  IL_0006:  ldloc.1
  IL_0007:  add
  IL_0008:  call      void [System.Console]System.Console::WriteLine(int32)
  IL_000d:  ret
}
```

## 位元組碼優勢

1. **跨平台**：同一份位元組碼可任何 JVM/CLR 執行
2. **安全**：可限制危險操作
3. **壓縮**：比原始碼更緊湊
4. **快速啟動**：比 AOT 編譯快

## 為什麼學習位元組碼？

1. **理解虛擬機**：了解語言執行環境
2. **除錯**：分析位元組碼問題
3. **優化**：針對性優化熱點
4. **語言設計**：實現自己的虛擬機

## 參考資源

- JVM 規範
- "Java Bytecode in Action"
- "Understanding the .NET CLR"
