# 14. LLVM Pass 開發

## 14.1 LLVM Pass 概述

LLVM Pass 是 LLVM 編譯器架構的核心擴展機制，用於實現各種優化和分析功能。

## 14.2 Pass 結構

[程式檔案：14-1-hello-pass.cpp](../_code/14/14-1-hello-pass.cpp)
```cpp
#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {
    struct HelloPass : public FunctionPass {
        static char ID;
        HelloPass() : FunctionPass(ID) {}
        
        bool runOnFunction(Function &F) override {
            errs() << "Hello: ";
            errs().write_escaped(F.getName()) << '\n';
            return false;
        }
    };
}

char HelloPass::ID = 0;
static RegisterPass<HelloPass> X("hello", "Hello World Pass");
```

## 14.3 Pass 類型

### 1. FunctionPass

在每個函數上執行：

```cpp
struct MyFunctionPass : public FunctionPass {
    bool runOnFunction(Function &F) override;
};
```

### 2. LoopPass

在每個迴圈上執行：

```cpp
struct MyLoopPass : public LoopPass {
    bool runOnLoop(Loop *L, LPPassManager &LPM) override;
};
```

### 3. BasicBlockPass

在每個基本區塊上執行：

```cpp
struct MyBasicBlockPass : public BasicBlockPass {
    bool runOnBasicBlock(BasicBlock &BB) override;
};
```

### 4. ModulePass

在整個模組上執行：

```cpp
struct MyModulePass : public ModulePass {
    bool runOnModule(Module &M) override;
};
```

## 14.4 分析 Pass

### 產生分析結果

```cpp
struct MyAnalysis : public FunctionPass {
    void getAnalysisUsage(AnalysisUsage &AU) const override {
        AU.addRequired<DominatorTreeWrapperPass>();
    }
    
    bool runOnFunction(Function &F) override {
        auto &DT = getAnalysis<DominatorTreeWrapperPass>().getDomTree();
        // 使用 Dominator Tree 分析
        return false;
    }
};
```

### 常見分析

| 分析 Pass | 描述 |
|----------|------|
| DominatorTree | 支配樹 |
| LoopInfo | 迴圈資訊 |
| ScalarEvolution | 標量演化 |
| AliasAnalysis | 別名分析 |
| CallGraph | 呼叫圖 |

## 14.5 最佳化 Pass 範例

### 常數折疊

```cpp
struct ConstantFoldPass : public FunctionPass {
    bool runOnFunction(Function &F) override {
        bool changed = false;
        for (auto &BB : F) {
            for (auto &I : BB) {
                if (auto *binop = dyn_cast<BinaryOperator>(&I)) {
                    if (isa<Constant>(binop->getOperand(0)) &&
                        isa<Constant>(binop->getOperand(1))) {
                        if (Constant *c = ConstantExpr::get(binop->getOpcode(),
                            cast<Constant>(binop->getOperand(0)),
                            cast<Constant>(binop->getOperand(1)))) {
                            I.replaceAllUsesWith(c);
                            changed = true;
                        }
                    }
                }
            }
        }
        return changed;
    }
};
```

## 14.6 建置 Pass

```bash
# 建立 CMakeLists.txt
add_library(HelloPass MODULE 14-1-hello-pass.cpp)

# 編譯
mkdir build && cd build
cmake -G Ninja -DLLVM_DIR=/path/to/llvm/build/lib/cmake/llvm ..
ninja

# 使用 Pass
opt -load ./libHelloPass.so -hello input.ll
```

## 14.7 使用 opt 工具

```bash
# 執行自訂 Pass
opt -load ./MyPass.so -mypass input.ll -o output.ll

# 執行多個 Pass
opt -load ./Pass1.so -load ./Pass2.so -pass1 -pass2 input.ll

# 分析 Pass
opt -analyze -load ./MyPass.so -myanalysis input.ll
```

## 14.8 本章小結

本章介紹了 LLVM Pass 開發的核心概念：
- Pass 結構與類型
- 分析 Pass 與最佳化 Pass
- Pass 的建置與使用
- 常見的分析工具

## 練習題

1. 實作一個簡單的 Hello World Pass。
2. 建立一個分析 Pass 來計算函數的基本區塊數量。
3. 實作一個簡單的最佳化 Pass。
4. 研究 LLVM Pass Manager 的運作原理。
