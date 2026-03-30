# TPU (Tensor Processing Unit)

## 概述

TPU 是 Google 專門為機器學習設計的 ASIC（特殊應用積體電路）。TPU 針對深度學習的神經網路運算進行最佳化，提供比 GPU 更高的效能和能源效率，廣泛用於 Google 雲端和產品中。

## 歷史

- **2015**：Google 首次部署 TPU
- **2017**：TPU v2 發布
- **2018**：TPU v3
- **2021**：TPU v4
- **現在**：Google Cloud TPU 服務

## TPU 架構

### 1. TPU 核心元件

```
┌─────────────────────────────────────┐
│           MXU (Matrix Multiply Unit) │
│     128x128 乘法累加器陣�列           │
├─────────────────────────────────────┤
│           VPU (Vector Processing Unit) │
│         向量處理單元                 │
├─────────────────────────────────────┤
│           UFC (Unified Buffer)      │
│         28MB 統一緩衝記憶體           │
├─────────────────────────────────────┤
│           HBM (High Bandwidth Memory) │
│         高頻寬記憶體                  │
└─────────────────────────────────────┘
```

### 2. TensorFlow 使用 TPU

```python
import tensorflow as tf

# 解析 TPU
resolver = tf.distribute.cluster_resolver.TPUClusterResolver(
    tpu='grpc://' + os.environ.get('COLAB_TPU_ADDR')
)
tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)

# 建立分散式策略
strategy = tf.distribute.TPUStrategy(resolver)

# 使用 TPU 訓練
with strategy.scope():
    model = build_model()
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

model.fit(train_dataset, epochs=10)
```

### 3. PyTorch 使用 TPU

```python
import torch
import torch_xla
import torch_xla.core.xla_model as xm
import torch_xla.distributed.xla_multiprocessing as xmp

def train_fn(index, flags):
    device = xm.xla_device()
    model = MyModel().to(device)
    
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    loss_fn = torch.nn.CrossEntropyLoss()
    
    for data, target in dataloader:
        optimizer.zero_grad()
        output = model(data.to(device))
        loss = loss_fn(output, target.to(device))
        loss.backward()
        xm.optimizer_step(optimizer)

xmp.spawn(train_fn, args=(flags,), nprocs=flags.num_cores)
```

### 4. JAX 使用 TPU

```python
import jax
import jax.numpy as jnp
from jax.tools import pmap

devices = jax.devices('tpu')
print(f"TPU devices: {devices}")

# pmap 到所有 TPU
pmapped_fn = pmap(fn, axis_name='batch')

# JIT 編譯
compiled_fn = jax.jit(fn)
```

### 5. Cloud TPU

```bash
# gcloud 命令建立 TPU
gcloud compute tpus create my-tpu \
    --zone=us-central1-a \
    --accelerator-type=v2-8 \
    --software-version=tpu-vm-base
```

## TPU vs GPU

| 特性 | TPU | GPU |
|------|-----|-----|
| 設計 | ASIC | 通用 GPU |
| 矩陣乘法 | 硬體最佳化 | 可程式化 |
| 精度 | INT8, BF16 | FP32, FP16, BF16 |
| 能耗比 | 更高 | 中等 |
| 靈活性 | 較低 | 較高 |

## 為什麼使用 TPU？

1. **深度學習效能**：矩陣運算硬體加速
2. **能源效率**：每瓦效能更高
3. **大規模訓練**：Google 雲端支援
4. **成本**：大批量訓練成本較低

## 參考資源

- Google Cloud TPU 文檔
- TPU 論文
- "TPU v4: Accelerating Deep Learning at Scale"
