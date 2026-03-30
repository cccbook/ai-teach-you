# 第 9 章：史瓦西解與黑洞

## 9.1 史瓦西度規

1916年，卡爾·史瓦西求得愛因斯坦場方程式的第一個精確解：

$$ds^2 = -(1-\frac{2GM}{rc^2})c^2dt^2 + (1-\frac{2GM}{rc^2})^{-1}dr^2 + r^2d\Omega^2$$

[程式檔案：09-1-schwarzschild.py](../_code/09/09-1-schwarzschild.py)

```python
t, r, theta, phi = symbols('t r theta phi')
M, G, c = symbols('M G c', positive=True)

Rs = 2 * M * G / c**2
g_tt = -(1 - Rs/r)
g_rr = 1 / (1 - Rs/r)
g_thth = r**2
g_phiph = r**2 * sin(theta)**2
```

## 9.2 克里斯多費符號

[程式檔案：09-1-schwarzschild.py](../_code/09/09-1-schwarzschild.py)

```python
Gamma = christoffel_symbols(metric, coords)
print(f"Γ^t_{{tr}} = {Gamma[0][1][0]}")
print(f"Γ^r_{{tt}} = {Gamma[1][0][0]}")
```

## 9.3 事件視界

事件視界 (Event Horizon) 是黑洞的「表面」：

$$r_s = \frac{2GM}{c^2}$$

## 9.4 奇點

史瓦西度規的兩個奇點：
1. $r = r_s$：坐標奇點（可消除）
2. $r = 0$：真實的時空奇點

## 9.5 黑洞週期表

| 類型         | 質量     | 旋轉     | 電荷    |
|--------------|----------|----------|---------|
| 史瓦西       | 有       | 無       | 無      |
| 萊斯納-諾德斯特朗 | 有   | 無       | 有      |
| 克爾         | 有       | 有       | 無      |
| 克爾-紐曼    | 有       | 有       | 有      |

## 習題

1. 計算光子球 (photon sphere) 的半徑。
