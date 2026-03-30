# 第 14 章：相對論性動力學模擬

## 14.1 洛倫茲因子

[程式檔案：14-1-relativistic-simulation.py](../_code/14/14-1-relativistic-simulation.py)

```python
import numpy as np

def lorentz_factor(beta):
    return 1.0 / np.sqrt(1 - beta**2)

for v in [0.0, 0.5, 0.8, 0.9, 0.99, 0.999]:
    gamma = lorentz_factor(v)
    print(f"v = {v:.3f}c → γ = {gamma:.4f}")
```

## 14.2 時間膨脹

$$\Delta t = \gamma \Delta \tau$$

## 14.3 粒子加速模擬

[程式檔案：14-1-relativistic-simulation.py](../_code/14/14-1-relativistic-simulation.py)

```python
def relativistic_momentum(mass, velocity, c=1.0):
    beta = velocity / c
    gamma = lorentz_factor(beta)
    return gamma * mass * velocity

def kinetic_energy(mass, velocity, c=1.0):
    beta = velocity / c
    gamma = lorentz_factor(beta)
    return (gamma - 1) * mass * c**2
```

## 14.4 雙生子悖論

[程式檔案：14-1-relativistic-simulation.py](../_code/14/14-1-relativistic-simulation.py)

```python
v = 0.8
gamma = lorentz_factor(v)
tau = 1  # 年
t = gamma * tau
print(f"太空人時間: {tau:.1f} 年")
print(f"地球時間: {t:.4f} 年")
```

## 14.5 LHC 中的相對論效應

[程式檔案：14-1-relativistic-simulation.py](../_code/14/14-1-relativistic-simulation.py)

```python
m_p = 1.67e-27  # kg
gamma_LHC = 7000
E_LHC = gamma_LHC * m_p * c**2 / eV_to_J / 1e12
print(f"LHC 質子能量: {E_LHC:.1f} TeV")
```
