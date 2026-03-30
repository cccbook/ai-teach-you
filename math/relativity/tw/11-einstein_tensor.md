# 第 11 章：使用 SymPy 計算愛因斯坦張量

## 11.1 愛因斯坦張量定義

$$G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}g_{\mu\nu}R$$

[程式檔案：11-1-einstein-tensor.py](../_code/11/11-1-einstein-tensor.py)

```python
def einstein_tensor(Ricci, R_scalar, metric, coords):
    """計算愛因斯坦張量"""
    n = len(coords)
    G = [[0]*n for _ in range(n)]
    for mu in range(n):
        for nu in range(n):
            g_elem = metric[mu][nu]
            G[mu][nu] = sp.simplify(Ricci[mu][nu] - R_scalar * g_elem / 2)
    return G
```

## 11.2 Minkowski 時空

[程式檔案：11-1-einstein-tensor.py](../_code/11/11-1-einstein-tensor.py)

```python
eta = [[-1, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 1, 0],
       [0, 0, 0, 1]]

G = einstein_tensor(Ricci, R_scalar, eta, coords)
print(f"G_μν = 0: {all_zero}")
```

## 11.3 真空場方程式

真空: $T_{\mu\nu} = 0 \Rightarrow G_{\mu\nu} = 0 \Rightarrow R_{\mu\nu} = 0$
