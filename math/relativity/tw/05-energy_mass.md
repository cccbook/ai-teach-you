# 第 5 章：質能方程式與四維向量

## 5.1 質能等價 (E = mc²)

愛因斯坦最著名的方程式揭示了質量與能量的關係。

[程式檔案：05-1-energy-mass.py](../_code/05/05-1-energy-mass.py)

```python
m, c = symbols('m c', positive=True)
E = m * c**2
print(f"E = mc² = {E}")

m_kg = 1  # kg
c_val = 3e8  # m/s
E_joules = m_kg * c_val**2
print(f"1 kg 物質蘊含的能量: {E_joules:.2e} 焦耳")
print(f"約等於 {E_joules/4.18e9:.2f} 噸 TNT 當量")
```

## 5.2 相對論動量

[程式檔案：05-1-energy-mass.py](../_code/05/05-1-energy-mass.py)

```python
v = symbols('v', positive=True)
gamma = 1 / sqrt(1 - v**2/c**2)
p = gamma * m * v
print(f"相對論動量: p = γmv")
print(f"p = {p}")
```

## 5.3 相對論能量

[程式檔案：05-1-energy-mass.py](../_code/05/05-1-energy-mass.py)

```python
E_total = gamma * m * c**2
E_kin = (gamma - 1) * m * c**2
print(f"總能量: E = γmc² = {E_total}")
print(f"動能: K = (γ-1)mc² = {E_kin}")
```

## 5.4 四維動量向量

[程式檔案：05-1-energy-mass.py](../_code/05/05-1-energy-mass.py)

```python
p_mu = Matrix([E/c, p, 0, 0])
print(f"四維動量 p^μ = (E/c, p^x, p^y, p^z) = ")
print(p_mu)

p_sq = p_mu[0]**2 - p_mu[1]**2 - p_mu[2]**2 - p_mu[3]**2
print(f"p·p = {sp.simplify(p_sq)} = (mc)²")
```

## 5.5 四維速度

[程式檔案：05-1-energy-mass.py](../_code/05/05-1-energy-mass.py)

```python
tau = symbols('tau')
U_mu = Matrix([gamma*c, gamma*v, 0, 0])
print(f"四維速度 U^μ = γ(c, v) = ")
print(U_mu)

U_sq = U_mu[0]**2 - U_mu[1]**2 - U_mu[2]**2 - U_mu[3]**2
print(f"U^μ U_μ = {sp.simplify(U_sq)} = -c²")
```

## 5.6 能量-動量關係

$$E^2 = (mc^2)^2 + (pc)^2$$

[程式檔案：05-1-energy-mass.py](../_code/05/05-1-energy-mass.py)

```python
E, p, m, c = symbols('E p m c')
E_sq = (m*c**2)**2 + (p*c)**2
print(f"E² = (mc²)² + (pc)²")
```

## 習題

1. 計算電子加速到 0.99c 時的動能和動量。
2. 證明四維動量的內積是不變量。
3. 討論光子 ($m=0$) 的能量-動量關係。
