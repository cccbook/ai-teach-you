# 13. 迴圈優化與向量化

## 13.1 迴圈優化概述

迴圈是程式效能優化的重要目標，常見的優化技術包括：
- 迴圈展開
- 迴圈融合
- 迴圈切分
- 向量化

## 13.2 迴圈展開

迴圈展開（Loop Unrolling）減少迴圈控制開銷：

[程式檔案：13-1-loop.c](../_code/13/13-1-loop.c)
```c
void vector_add(int n, double* a, double* b, double* c) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}
```

### 展開後

```c
for (int i = 0; i < n; i += 4) {
    c[i] = a[i] + b[i];
    c[i+1] = a[i+1] + b[i+1];
    c[i+2] = a[i+2] + b[i+2];
    c[i+3] = a[i+3] + b[i+3];
}
```

## 13.3 向量化

向量化（Vectorization）使用 SIMD 指令同時處理多個資料：

### SIMD 指令集

| 指令集 | 資料寬度 |
|-------|---------|
| SSE | 128 位元 |
| AVX | 256 位元 |
| AVX-512 | 512 位元 |

### 向量化範例

使用 AVX2 進行向量加法：

```c
#include <immintrin.h>

void vector_add_avx(double* a, double* b, double* c, int n) {
    for (int i = 0; i < n; i += 4) {
        __m256d va = _mm256_load_pd(&a[i]);
        __m256d vb = _mm256_load_pd(&b[i]);
        __m256d vc = _mm256_add_pd(va, vb);
        _mm256_store_pd(&c[i], vc);
    }
}
```

## 13.4 LLVM 向量化 Pass

LLVM 自動向量化：

```bash
# 啟動向量化
clang -O3 -march=native -vectorize-loops example.c -o example

# 查看向量化報告
clang -O3 -Rpass=loop-vectorize -Rpass-missed=loop-vectorize example.c
```

### 向量化前後比較

原始程式碼：
```c
for (int i = 0; i < n; i++) {
    c[i] = a[i] + b[i];
}
```

向量化後（使用 SSE）：
```asm
vmovapd  ymm0, [rdi]
vaddpd   ymm0, ymm0, [rsi]
vmovapd  [rdx], ymm0
```

## 13.5 迴圈熔合

迴圈熔合（Loop Fusion）將多個相鄰迴圈合併：

```c
// 熔合前
for (int i = 0; i < n; i++) {
    a[i] = b[i] + c[i];
}
for (int i = 0; i < n; i++) {
    d[i] = a[i] * 2;
}

// 熔合後
for (int i = 0; i < n; i++) {
    a[i] = b[i] + c[i];
    d[i] = a[i] * 2;
}
```

## 13.6 迴圈分塊

迴圈分塊（Loop Tiling）優化快取使用：

```c
// 分塊前
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        c[i][j] = a[i][j] + b[i][j];
    }
}

// 分塊後
for (int ii = 0; ii < n; ii += BLOCK) {
    for (int jj = 0; jj < n; jj += BLOCK) {
        for (int i = ii; i < min(ii+BLOCK, n); i++) {
            for (int j = jj; j < min(jj+BLOCK, n); j++) {
                c[i][j] = a[i][j] + b[i][j];
            }
        }
    }
}
```

## 13.7 本章小結

本章介紹了迴圈優化與向量化的核心概念：
- 迴圈展開
- SIMD 向量化
- LLVM 向量化 Pass
- 迴圈熔合
- 迴圈分塊

## 練習題

1. 手動優化一個矩陣乘法程式。
2. 比較不同優化等級的向量化結果。
3. 使用 Intrinsics 實作 SIMD 程式碼。
4. 分析向量化對效能的影響。
