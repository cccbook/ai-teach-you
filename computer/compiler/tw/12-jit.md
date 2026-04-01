# 12. JIT 編譯與虛擬機

## 12.1 JIT 編譯概述

JIT（Just-In-Time）編譯器在執行時期將程式碼即時編譯為機器碼，結合了解譯器和提前編譯器的優點。

## 12.2 虛擬機實作

[程式檔案：12-1-simple-vm.c](../_code/12/12-1-simple-vm.c)
```c
typedef enum {
    OP_LOAD,
    OP_STORE,
    OP_ADD,
    OP_SUB,
    OP_MUL,
    OP_DIV,
    OP_JMP,
    OP_JZ,
    OP_HALT
} OpCode;

typedef struct {
    OpCode opcode;
    int operand;
} Instruction;

typedef struct {
    int* stack;
    int sp;
    int ip;
    int* memory;
} VM;

void execute(VM* vm, Instruction* program, int program_size) {
    while (vm->ip < program_size) {
        Instruction* instr = &program[vm->ip++];
        
        switch (instr->opcode) {
            case OP_LOAD:
                push(vm, vm->memory[instr->operand]);
                break;
            case OP_ADD: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a + b);
                break;
            }
            case OP_HALT:
                return;
        }
    }
}
```

## 12.3 JIT 編譯原理

### 基本流程

```
原始程式碼
    │
    ▼
┌─────────────┐
│   解譯器    │  (解釋執行)
└─────────────┘
    │
    ▼
┌─────────────┐
│ 熱點偵測   │  (識別頻繁執行的程式碼)
└─────────────┘
    │
    ▼
┌─────────────┐
│  JIT 編譯  │  (編譯為機器碼)
└─────────────┘
    │
    ▼
  機器碼執行
```

## 12.4 LLVM JIT

LLVM 提供了強大的 JIT 編譯功能：

```c
#include <llvm-c/Target.h>
#include <llvm-c/ExecutionEngine.h>

LLVMExecutionEngineRef engine;
LLVMModuleRef module;

LLVMInitializeNativeTarget();
LLVMInitializeNativeAsmPrinter();

LLVMModuleRef module = LLVMModuleCreateWithName("my_module");

// 建立函數
LLVMBuilderRef builder = LLVMCreateBuilder();
LLVMPositionBuilderAtEnd(builder, entry);

// 執行 JIT
LLVMBuildRet(builder, LLVMConstInt(LLVMInt32Type(), 42, 0));

// 建立執行引擎
LLVMCreateExecutionEngineForModule(&engine, module, &error);
```

## 12.5 ORC JIT API

LLVM 12+ 的新 JIT API：

```c
#include <llvm/Executioner/Orc/OrcLLJIT.h>

using namespace llvm::orc;

Expected<std::unique_ptr<OrcLLJIT>> jit = OrcLLJIT::Builder().build();

auto& jd = jit->getDynamicInstance();
cantFail(jd.getDefinitions().define(
    llvm::orc::absoluteSymbols({{
        Mangle("printf"),
        JITEAddressSymbol((uint64_t)&printf)
    }})
));

cantFail(jit->addIRModule(
    ThreadSafeModule(std::move(module), std::move(ctx))
));

auto entry = jit->lookup("main");
```

## 12.6 JIT 優化

### 內聯快取

```c
void* inlineCache[256];
void* lookupAndCompile(void* key) {
    void* addr = inlineCache[(uintptr_t)key % 256];
    if (addr && validate(key, addr)) {
        return addr;
    }
    addr = compile(key);
    inlineCache[(uintptr_t)key % 256] = addr;
    return addr;
}
```

### 熱度追蹤

```c
typedef struct {
    void* code_addr;
    int call_count;
} ProfileEntry;

void recordCall(ProfileEntry* entry) {
    entry->call_count++;
    if (entry->call_count > THRESHOLD) {
        compile(entry->code_addr);
    }
}
```

## 12.7 本章小結

本章介紹了 JIT 編譯與虛擬機的核心概念：
- 虛擬機的基本實現
- JIT 編譯原理
- LLVM JIT API
- JIT 優化技術

## 練習題

1. 實作一個簡單的位元碼虛擬機。
2. 為虛擬機加入函數呼叫支援。
3. 使用 LLVM 實作一個 JIT 編譯器。
4. 研究 JIT 編譯器的熱度追蹤演算法。
