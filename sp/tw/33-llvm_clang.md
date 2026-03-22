# 33. LLVM/Clang——模組化編譯器框架

## 33.1 LLVM 專案

LLVM 不只是一個編譯器，是一個**模組化的編譯器框架**：

```
        ┌─────────────────────────┐
        │     應用程式            │
        └───────────┬─────────────┘
                    │
        ┌───────────▼───────────────┐
        │        Clang              │ ← C/C++/Objective-C 前端
        │     (語法分析, 語意分析)  │
        └───────────┬───────────────┘
                    │
        ┌───────────▼───────────────┐
        │      LLVM Core            │ ← 中間表示 (IR)
        │  (最佳化, CodeGen)        │
        └───────────┬───────────────┘
                    │
        ┌───────────┼───────────────┐
        │           │               │
   ┌────▼────┐ ┌───▼───┐    ┌─────▼─────┐
   │  x86    │ │ ARM   │    │  RISC-V  │
   │ 後端    │ │ 後端  │    │  後端     │
   └─────────┘ └───────┘    └───────────┘
```

## 33.2 Clang 特色

### 33.2.1 快速編譯

```bash
clang -O2 hello.c -o hello
```

### 33.2.2 清晰的錯誤訊息

```c
// error.c
int main() {
    int* p = 0;
    return *p;  // 空指標解引用
}
```

```bash
clang error.c -o error
# 輸出：
# error.c:3:12: warning: null pointer returned from function returning non-null 'int' [-Wreturn-stack-address]
#     return *p;
#            ^
# error.c:3:12: error: indirection requires pointer operand ('int' invalid)
```

## 33.3 LLVM IR

### 33.3.1 生成 IR

```bash
clang -S -emit-llvm hello.c -o hello.ll
```

### 33.3.2 IR 查看

```llvm
; hello.ll
@.str = private constant [12 x i8] c"Hello World\00"

define i32 @main() {
entry:
    %call = call i32 @puts(i8* getelementptr inbounds ([12 x i8], [12 x i8]* @.str, i64 0, i64 0))
    ret i32 0
}

declare i32 @puts(i8*)
```

## 33.4 工具鏈

### 33.4.1 opt - 最佳化

```bash
opt -S -O2 hello.ll -o hello_opt.ll
```

### 33.4.2 llc - 編譯到組語

```bash
llc hello.ll -o hello.s
llc -march=riscv64 hello.ll -o hello_rv.s
```

### 33.4.3 lli - 直譯執行

```bash
lli hello.ll
```

### 33.4.4 llvm-dis - 反組譯

```bash
llvm-dis hello.bc -o hello.ll
```

## 33.5 靜態分析

### 33.5.1 scan-build

```bash
scan-build clang hello.c -o hello
```

### 33.5.2 clang --analyze

```bash
clang --analyze hello.c
```

## 33.6 語法樹查看

```bash
# 顯示抽象語法樹
clang -Xclang -ast-dump hello.c

# 顯示語意差異視圖
clang -Xclang -ast-view hello.c
```

## 33.7 小結

本章節我們學習了：
- LLVM 專案的架構
- Clang 的特色
- LLVM IR 的使用
- opt、llc、lli 工具
- 靜態分析工具

## 33.8 習題

1. 使用 `clang -ast-dump` 查看 AST
2. 比較 GCC 和 Clang 的錯誤訊息
3. 使用 `opt` 實驗不同最佳化 passes
4. 研究 LLVM 的 pass 管理器
5. 實現一個簡單的 LLVM pass
