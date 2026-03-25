# SIMD (Single Instruction Multiple Data)

## 概述

SIMD（單一指令多資料）是一種平行運算技術，允許一條指令同時處理多筆資料。SIMD 廣泛用於多媒體處理、科學計算和機器學習，可大幅提升效能。

## 歷史

- **1960s**：早期 SIMD 概念
- **1996**：Intel MMX
- **1999**：SSE
- **2001**：AMD 3DNow!
- **2008**：AVX
- **2013**：AVX-512
- **現在**：Arm NEON

## SIMD 指令集

### 1. x86 SIMD

```c
// SSE: 128-bit = 4 x 32-bit floats
#include <emmintrin.h>

__m128 a, b, result;
result = _mm_add_ps(a, b);  // 4 個浮點數同時相加
```

### 2. AVX

```c
// AVX: 256-bit = 8 x 32-bit floats
#include <immintrin.h>

__m256 a, b, result;
result = _mm256_add_ps(a, b);

// AVX-512: 512-bit = 16 x 32-bit floats
__m512 c, d, result512;
result512 = _mm512_add_ps(c, d);
```

### 3. Arm NEON

```asm
; Arm NEON: 128-bit
vldr q0, [r0]      ; 載入 4 x 32-bit floats
vldr q1, [r1]
vadd.f32 q2, q0, q1 ; 相加
vstr q2, [r2]
```

### 4. C 內建函數

```c
#include <stdio.h>
#include <immintrin.h>

void simd_add(float *a, float *b, float *c, int n) {
    for (int i = 0; i < n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(&c[i], vc);
    }
}

int main() {
    float a[8] = {1,2,3,4,5,6,7,8};
    float b[8] = {8,7,6,5,4,3,2,1};
    float c[8];
    
    simd_add(a, b, c, 8);
    
    for (int i = 0; i < 8; i++)
        printf("%f ", c[i]);
    return 0;
}
```

### 5. 矩陣乘法 SIMD

```c
void matmul_simd(float *A, float *B, float *C, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            __m256 sum = _mm256_setzero_ps();
            for (int k = 0; k < n; k += 8) {
                __m256 a = _mm256_loadu_ps(&A[i*n + k]);
                __m256 b = _mm256_loadu_ps(&B[k*n + j]);
                sum = _mm256_add_ps(sum, _mm256_mul_ps(a, b));
            }
            float s[8];
            _mm256_storeu_ps(s, sum);
            C[i*n + j] = s[0] + s[1] + s[2] + s[3] + 
                        s[4] + s[5] + s[6] + s[7];
        }
    }
}
```

### 6. 自動向量化

```c
// 編譯器自動向量化
// gcc -O3 -march=native -ffast-math

void vector_add(float *a, float *b, float *c, int n) {
    #pragma omp simd
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}
```

## 為什麼學習 SIMD？

1. **效能提升**：數倍加速
2. **多媒體**：圖形/影片處理
3. **科學計算**：數值運算
4. **深度學習**：矩陣運算加速

## 參考資源

- Intel Intrinsics Guide
- Arm NEON 程式設計指南
- "Computer Systems: A Programmer's Perspective"
