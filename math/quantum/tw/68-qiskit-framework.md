# 第六十八章：Qiskit 框架

## 68.1 Qiskit 概述

Qiskit 是 IBM 開發的開源量子計算軟體框架，提供了一個全面的工具集用於量子計算研究、教育和應用開發。

Qiskit 的目標是：
- 使量子計算易於訪問
- 提供高效的量子電路設計工具
- 支持量子演算法的研究和實現
- 教育量子計算基礎

Qiskit 包含多個主要模組：
- **Terra**：基礎框架和量子電路
- **Aer**：量子模擬器
- **Ignis**：量子錯誤和噪聲處理
- **Aqua**：量子應用（現在整合到其他模組）

## 68.2 安裝和設置

Qiskit 可以通過 pip 安裝：
```bash
pip install qiskit
```

基本使用：
```python
from qiskit import QuantumCircuit, execute, Aer
```

Qiskit 需要較新版本的 Python（3.8+）。

## 68.3 量子電路設計

Qiskit 的核心是 QuantumCircuit 類。

```python
qc = QuantumCircuit(2, 2)  # 2 量子位元, 2 經典位元

qc.h(0)      # Hadamard 閘
qc.cx(0, 1)  # CNOT 閘
qc.measure([0, 1], [0, 1])  # 測量

qc.draw()  # 繪製電路圖
```

Qiskit 提供了直觀的 API 來設計量子電路。

## 68.4 單量子位元閘

Qiskit 支援所有標準單量子位元閘。

```python
from qiskit.circuit.library import *

qc.h(0)    # Hadamard
qc.x(0)    # Pauli-X
qc.y(0)    # Pauli-Y
qc.z(0)    # Pauli-Z
qc.s(0)    # Phase
qc.t(0)    # T 閘
qc.rz(pi/4, 0)  # Rz 旋轉
qc.rx(pi/2, 0)  # Rx 旋轉
qc.ry(pi/2, 0)  # Ry 旋轉
```

## 68.5 雙量子位元閘

Qiskit 支援標準雙量子位元閘。

```python
qc.cx(0, 1)   # CNOT，控制=0，目標=1
qc.cz(0, 1)   # CZ
qc.swap(0, 1) # SWAP
qc.iSwap(0, 1)  # iSWAP
qc.crz(pi/4, 0, 1)  # 受控 Rz
```

也可以使用自訂閘分解。

## 68.6 量子模擬器

Qiskit Aer 提供了高效的量子模擬器。

```python
from qiskit import execute
from qiskit.providers.aer import AerSimulator

simulator = AerSimulator()

job = execute(qc, simulator, shots=1024)
result = job.result()
counts = result.get_counts(qc)
```

可以模擬理想和噪聲量子電路。

## 68.7 實際硬體執行

Qiskit 可以直接執行到 IBM Quantum 硬體。

```python
from qiskit import IBMQ

IBMQ.save_account('YOUR_TOKEN')
provider = IBMQ.load_account()

backend = provider.get_backend('ibmq_lima')
job = execute(qc, backend, shots=1024)
```

Qiskit 提供了訪問真實量子處理器的功能。

## 68.8 量子位元映射

將邏輯電路映射到物理硬體時需要處理連接性。

```python
from qiskit.transpiler import PassManager, BasicSwap
from qiskit.transpiler.passes import BasicSwap

pm = PassManager([BasicSwap()])
mapped_circuit = pm.run(qc)
```

Qiskit 提供了自動映射和優化工具。

## 68.9 量子錯誤處理

Qiskit Ignis 模組用於處理量子錯誤。

```python
from qiskit.ignis.characterization import Calibrations

# 測量錯誤緩解
from qiskit.ignis.mitigation.measurement import CompleteMeasFitter

meas_fitter = CompleteMeasFitter(result, ["00", "01", "10", "11"])
mitigated_counts = meas_fitter.filter.apply(result)
```

Qiskit 提供了測量錯誤緩解工具。

## 68.10 量子機器學習

Qiskit 整合了量子機器學習功能。

```python
from qiskit_machine_learning.circuit_library import QNNCircuit

# 量子神經網路
qnn = QNNCircuit(num_qubits=4)
```

Qiskit ML 支援變分量子分類器等模型。

## 68.11 教育和可視化

Qiskit 提供了豐富的教育資源和可視化工具。

```python
qc.draw(output='mpl')  # 繪製電路圖
plot_bloch_multivector(state)  # 布洛赫球
plot_histogram(counts)  # 直方圖
plot_state_city(state)  # 密度矩陣
```

Qiskit 提供了強大的可視化功能。

## 68.12 本章小結

本章我們介紹了 Qiskit 量子計算框架。

Qiskit 提供了設計、模擬和執行量子電路的完整工具集。其核心是 QuantumCircuit 類，支持所有標準量子閘。

Qiskit Aer 提供了高效的模擬器，AerSimulator 可以模擬理想和噪聲電路。通過 IBM Quantum 雲服務，可以直接執行到真實量子硬體。

Qiskit 還提供了錯誤處理、量子機器學習和豐富的可視化工具，是學習和應用量子計算的優秀平台。
