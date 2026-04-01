# 6. 中間碼生成

## 6.1 什麼是中間碼生成

中間碼生成（IR Generation）是編譯器將抽象語法樹轉換為中間表示（IR）的過程。在 LLVM 架構中，這就是生成 LLVM IR 的階段。

## 6.2 AST 到 IR 的轉換

### 基本原則

1. 每個 AST 節點對應一個或多個 IR 指令
2. 變數需要配置記憶體空間（alloca）
3. 運算式需要計算並產生結果
4. 控制流需要使用分支指令

## 6.3 代碼生成器框架

[程式檔案：06-1-codegen.h](../_code/06/06-1-codegen.h)
```c
typedef struct {
    FILE* output;
    int tempCount;
    int labelCount;
} CodeGen;

CodeGen* createCodeGen(FILE* output);
char* generateTemp(CodeGen* gen);
char* generateLabel(CodeGen* gen);
void generate(ASTNode* node, CodeGen* gen);
```

## 6.4 運算式生成

運算式生成需要遞迴地處理每個子節點：

[程式檔案：06-1-codegen.c](../_code/06/06-1-codegen.c)
```c
void generateExpression(ASTNode* node, CodeGen* gen) {
    if (!node) return;
    
    switch (node->type) {
        case AST_NUMBER: {
            char* temp = generateTemp(gen);
            fprintf(gen->output, "  %s = add i32 0, %d\n", temp, node->value);
            break;
        }
        case AST_VARIABLE: {
            char* temp = generateTemp(gen);
            fprintf(gen->output, "  %s = load i32, i32* @%s\n", temp, node->name);
            break;
        }
        case AST_BINOP_ADD: {
            char* leftTemp = generateTemp(gen);
            char* rightTemp = generateTemp(gen);
            generateExpression(node->left, gen);
            generateExpression(node->right, gen);
            fprintf(gen->output, "  %s = add i32 %s, %s\n", 
                leftTemp, leftTemp, rightTemp);
            break;
        }
    }
}
```

## 6.5 語句生成

### 變數宣告

```llvm
%x = alloca i32, align 4
store i32 10, i32* %x
```

### 賦值語句

```llvm
%value = add i32 0, 20
store i32 %value, i32* %x
```

### 返回語句

```llvm
%result = add i32 %a, %b
ret i32 %result
```

## 6.6 控制流生成

### 條件分支

```llvm
%cmp = icmp slt i32 %a, %b
br i1 %cmp, label %then, label %else

then:
  ; then 分支的程式碼
  br label %end

else:
  ; else 分支的程式碼
  br label %end

end:
  ; 合併控制流
```

### 迴圈

```llvm
br label %loop

loop:
  %cmp = icmp slt i32 %i, %n
  br i1 %cmp, label %body, label %end

body:
  ; 迴圈主體
  br label %inc

inc:
  %i_next = add i32 %i, 1
  br label %loop

end:
  ; 迴圈結束
```

## 6.7 函數生成

```llvm
define i32 @add(i32 %a, i32 %b) {
entry:
  %result = add i32 %a, %b
  ret i32 %result
}
```

## 6.8 使用 clang 驗證生成結果

```bash
# 產生 IR
clang -S -emit-llvm -O0 example.c -o example.ll

# 查看 IR
cat example.ll
```

## 6.9 本章小結

本章介紹了中間碼生成的核心概念：
- AST 到 IR 的轉換原則
- 代碼生成器的基本框架
- 運算式和語句的生成
- 控制流的生成
- 使用 LLVM 工具驗證結果

## 練習題

1. 擴充代碼生成器支援浮點數類型。
2. 為代碼生成器加入陣列支援。
3. 實作指標類型的代碼生成。
4. 為函數呼叫生成正確的呼叫約定。
