import numpy as np

# 純 Python（慢）
def add_arrays_python(a, b):
    c = []
    for i in range(len(a)):
        c.append(a[i] + b[i])
    return c

# NumPy 向量化（快）
def add_arrays_numpy(a, b):
    return a + b

# 效能測試
import time

n = 10000000
a = np.random.rand(n)
b = np.random.rand(n)

start = time.time()
for _ in range(10):
    c = a + b
numpy_time = time.time() - start

print(f"NumPy 時間: {numpy_time:.3f}s")
print(f"處理 {n} 個元素，吞吐量: {n * 10 / numpy_time:.0f} ops/s")

# 自動向量化範例
# 使用 Numba JIT
from numba import jit

@jit(nopython=True)
def add_arrays_numba(a, b):
    n = len(a)
    c = np.empty(n)
    for i in range(n):
        c[i] = a[i] + b[i]
    return c

# 第一次呼叫會編譯，後續呼叫會使用編譯後的程式碼
result = add_arrays_numba(a, b)

import numpy as np

def grayscale_naive(image):
    """逐像素處理（慢）"""
    h, w, c = image.shape
    result = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            result[i, j] = 0.299 * image[i, j, 0] + 0.587 * image[i, j, 1] + 0.114 * image[i, j, 2]
    return result

def grayscale_vectorized(image):
    """向量化處理（快）"""
    # 使用 NumPy 廣播
    return np.dot(image, [0.299, 0.587, 0.114])

# 測試
image = np.random.randint(0, 255, (1000, 1000, 3), dtype=np.uint8)

start = time.time()
g1 = grayscale_naive(image)
t1 = time.time() - start

start = time.time()
g2 = grayscale_vectorized(image)
t2 = time.time() - start

print(f"逐像素: {t1:.3f}s")
print(f"向量化: {t2:.3f}s")
print(f"加速比: {t1/t2:.1f}x")