// C 程式：無 SIMD
void add_arrays(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

// 使用 SIMD (SSE/AVX)
void add_arrays_simd(float* a, float* b, float* c, int n) {
    // 每次處理 4 個 float (SSE) 或 8 個 float (AVX)
    int i = 0;
    
    // AVX: 一次處理 8 個 float
    for (; i + 7 < n; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_store_ps(&c[i], vc);
    }
    
    // 處理剩餘元素
    for (; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

// 使用編譯器向量化
// gcc -O3 -march=native -ftree-vectorize