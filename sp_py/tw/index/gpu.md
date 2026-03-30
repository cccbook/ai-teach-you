# GPU (Graphics Processing Unit)

## 概述

GPU（圖形處理單元）是專門設計用於處理圖形和平行運算的處理器。GPU 擁有大量核心，可以同時執行大量簡單計算，是深度學習和高效能運算的核心硬體。

## 歷史

- **1993**：NVIDIA 成立
- **1999**：GPU 術語出現
- **2006**：CUDA 發布
- **現在**：AI 時代 GPU 需求暴增

## GPU 架構

### 1. GPU vs CPU

```
CPU:                       GPU:
┌─────────────┐           ┌─────────────┐
│   核心      │           │  數千核心   │
│   少量      │           │   大量     │
│ 最佳化     │           │  平行     │
│  串行任務  │           │  資料流   │
└─────────────┘           └─────────────┘
```

### 2. CUDA 程式設計

```c
#include <stdio.h>

// CUDA 核心函數
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    const int N = 1000000;
    float *a, *b, *c;
    float *d_a, *d_b, *d_c;
    
    // 配置記憶體
    cudaMalloc(&d_a, N * sizeof(float));
    cudaMalloc(&d_b, N * sizeof(float));
    cudaMalloc(&d_c, N * sizeof(float));
    
    // 複製資料到 GPU
    cudaMemcpy(d_a, a, N * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, b, N * sizeof(float), cudaMemcpyHostToDevice);
    
    // 啟動核心
    int threads = 256;
    int blocks = (N + threads - 1) / threads;
    vectorAdd<<<blocks, threads>>>(d_a, d_b, d_c, N);
    
    // 複製結果回主機
    cudaMemcpy(c, d_c, N * sizeof(float), cudaMemcpyDeviceToHost);
    
    // 釋放記憶體
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    
    return 0;
}
```

### 3. 深度學習框架

```python
# PyTorch GPU 使用
import torch

# 檢查 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 移動模型和資料到 GPU
model = model.to(device)
x = x.to(device)
y = y.to(device)

# 訓練
output = model(x)
loss = criterion(output, y)
loss.backward()
optimizer.step()

# 多 GPU
model = torch.nn.DataParallel(model)
```

```python
# TensorFlow GPU 使用
import tensorflow as tf

# 列出 GPU
gpus = tf.config.list_physical_devices('GPU')
print(f"GPUs: {gpus}")

# 指定 GPU
tf.config.set_visible_devices(gpus[0], 'GPU')

# 檢查記憶體
for gpu in gpus:
    print(f"{gpu}: Memory Allocated")
```

### 4. NVIDIA 工具

```bash
# 查看 GPU 狀態
nvidia-smi

# GPU 監控
nvidia-smi -l 1
nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used --format=csv
```

## 為什麼學習 GPU？

1. **深度學習**：模型訓練必需
2. **高效能運算**：科學計算
3. **平行處理**：大量資料
4. **效能優化**：加速運算

## 參考資源

- NVIDIA CUDA 官方文檔
- "Programming Massively Parallel Processors"
- PyTorch/TensorFlow 文件
