# 虛擬機 (Virtual Machine)

## 概述

虛擬機（VM）是一種軟體實現的計算機，可以執行位元組碼。虛擬機隔離程式與硬體，提供跨平台執行環境、常數管理、記憶體分配和安全控制。著名虛擬機包括 JVM、.NET CLR、Python VM。

## 歷史

- **1970s**：IBM 推出 VM/370
- **1995**：Sun 發布 Java 和 JVM
- **2000**：Microsoft .NET CLR
- **2010**：WebAssembly VM
- **現在**：容器和沙箱虛擬化

## 虛擬機架構

```
┌─────────────────────────────────────┐
│           虛擬機核心                │
├─────────────────────────────────────┤
│  類別載入器  │  記憶體管理  │  GC   │
├─────────────────────────────────────┤
│  執行引擎    │  JIT 編譯器 │  同步 │
├─────────────────────────────────────┤
│  本地方法介面 │  訊號處理   │
└─────────────────────────────────────┘
              ↓
        [硬體/作業系統]
```

### 1. 簡單堆疊虛擬機

```python
class SimpleVM:
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.ip = 0
    
    def run(self, code):
        while self.ip < len(code):
            op = code[self.ip]
            
            if op == 'CONST':
                self.ip += 1
                self.stack.append(code[self.ip])
            
            elif op == 'LOAD':
                self.ip += 1
                var = code[self.ip]
                self.stack.append(self.variables.get(var))
            
            elif op == 'STORE':
                self.ip += 1
                var = code[self.ip]
                self.variables[var] = self.stack.pop()
            
            elif op == 'ADD':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            
            elif op == 'SUB':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
            
            elif op == 'PRINT':
                print(self.stack.pop())
            
            elif op == 'HALT':
                break
            
            self.ip += 1

# 執行: print 5 + 3
code = ['CONST', 5, 'CONST', 3, 'ADD', 'PRINT', 'HALT']
vm = SimpleVM()
vm.run(code)
```

### 2. 記憶體管理

```python
class MemoryManager:
    def __init__(self, size=1024):
        self.memory = bytearray(size)
        self.alloc_ptr = 0
    
    def allocate(self, size):
        if self.alloc_ptr + size > len(self.memory):
            raise MemoryError("Out of memory")
        
        addr = self.alloc_ptr
        self.alloc_ptr += size
        return addr
    
    def read(self, addr, size):
        return bytes(self.memory[addr:addr+size])
    
    def write(self, addr, data):
        self.memory[addr:addr+len(data)] = data
    
    def free(self, addr, size):
        pass  # 簡化版本，不實際釋放
```

### 3. 類別載入器

```python
class ClassLoader:
    def __init__(self, vm):
        self.vm = vm
        self.classes = {}
    
    def load_class(self, class_data):
        # 解析類別結構
        class_name = class_data['name']
        methods = class_data['methods']
        
        self.classes[class_name] = {
            'name': class_name,
            'methods': methods,
            'fields': {}
        }
        
        return self.classes[class_name]
    
    def resolve_method(self, class_name, method_name):
        cls = self.classes.get(class_name)
        if cls and method_name in cls['methods']:
            return cls['methods'][method_name]
        return None
```

### 4. 垃圾回收器（簡化）

```python
class SimpleGC:
    def __init__(self):
        self.heap = []
        self.roots = []
    
    def mark_and_sweep(self):
        marked = set()
        
        # 標記 root 可達物件
        for root in self.roots:
            self.mark(root, marked)
        
        # 回收未標記物件
        self.heap = [obj for obj in self.heap if obj in marked]
    
    def mark(self, obj, marked):
        marked.add(id(obj))
        # 遞迴標記所有參考
        for ref in obj.get_refs():
            if id(ref) not in marked:
                self.mark(ref, marked)
```

### 5. JVM 結構範例

```java
// JVM 類別檔案結構
public class JVMStructure {
    // u1: 1 byte 無符號整數
    // u2: 2 byte 無符號整數
    // u4: 4 byte 無符號整數
    
    /*
    ClassFile {
        u4 magic;              // 0xCAFEBABE
        u2 minor_version;
        u2 major_version;
        u2 constant_pool_count;
        cp_info constant_pool[constant_pool_count-1];
        u2 access_flags;
        u2 this_class;
        u2 super_class;
        u2 interfaces_count;
        u2 interfaces[interfaces_count];
        u2 fields_count;
        field_info fields[fields_count];
        u2 methods_count;
        method_info methods[methods_count];
        u2 attributes_count;
        attribute_info attributes[attributes_count];
    }
    */
}
```

## 虛擬機類型

### 1. 基於堆疊（Stack-based）

```python
# JVM 是基於堆疊的 VM
# 指令範例: iconst_5, istore_0, iload_0
```

### 2. 基於暫存器（Register-based）

```python
# Lua VM 是基於暫存器的 VM
# 更快，但指令更複雜
```

## 為什麼學習虛擬機？

1. **語言實現**：實現自己的程式語言
2. **效能優化**：優化執行效率
3. **安全隔離**：沙箱執行不受信任程式碼
4. **跨平台**：理解跨平台原理

## 參考資源

- "Inside the Java Virtual Machine"
- "Virtual Machines" by Smith & Nair
- JVM 規範
