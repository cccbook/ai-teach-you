# 第 15 章：重力波簡介

## 15.1 什麼是重力波？

重力波是時空曲率的波動，由加速質量產生，以光速傳播。

2015年9月14日，LIGO 首次直接探測到重力波！

## 15.2 愛因斯坦預言

1916年，愛因斯坦從廣義相對論預言了重力波的存在。

在 transverse-traceless (TT) 規範：

$$h_{\mu\nu} = \begin{pmatrix}
0 & 0 & 0 & 0 \\
0 & h_+ & h_\times & 0 \\
0 & h_\times & -h_+ & 0 \\
0 & 0 & 0 & 0
\end{pmatrix}$$

兩種偏振：+ (plus) 和 × (cross)

## 15.3 重力波效應

- 在一個方向拉伸
- 在垂直方向壓縮

典型量級：$h \approx 10^{-21}$

## 15.4 重力波源

[程式檔案：15-1-gravitational-waves.py](../_code/15/15-1-gravitational-waves.py)

```python
print("""
1. 雙星黑洞合併 - LIGO 主要探測源
2. 雙星中子星合併 - 2017年 GW170817
3. 超新星爆發
4. 早期宇宙漲落
""")
```

## 15.5 探測器

[程式檔案：15-1-gravitational-waves.py](../_code/15/15-1-gravitational-waves.py)

```python
print("""
地面探測器：
- LIGO (美國): 4 km 臂長
- Virgo (義大利): 3 km
- KAGRA (日本): 3 km

太空探測器：
- LISA (計畫中): 250萬公里臂長
""")
```

## 15.6 重力波天文學

重力波的探測開啟了新的天文學時代！

2017年諾貝爾物理學獎頒給 LIGO 的三位創始人。
