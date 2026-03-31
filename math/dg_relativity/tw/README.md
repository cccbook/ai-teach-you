# 從微分幾何到廣義相對論

> 從基礎數學到時空幾何的完整指南

---

## 目錄

### 第一部分：預備數學知識

| 章節 | 主題 | 說明 |
|------|------|------|
| [01-向量與向量空間](01-vector-spaces.md) | 向量與線性代數 | 向量、向量空間、線性組合、基底與維度 |
| [02-矩陣與線性映射](02-matrices-linear-maps.md) | 矩陣運算 | 矩陣乘法、行列式、秩、特徵值與特徵向量 |
| [03-張量初步](03-tensors-intro.md) | 張量基礎 | 張量定義、指標記號、愛因斯坦求公約 |
| [04-多變數微積分](04-multivariable-calculus.md) | 多變數微分與積分 | 偏導數、梯度、散度、旋度、多重積分 |

### 第二部分：微分幾何基礎

| 章節 | 主題 | 說明 |
|------|------|------|
| [05-流形概述](05-manifolds.md) | 流形概念 | 拓撲流形、圖冊座標系、維度 |
| [06-切空間與餘切空間](06-tangent-cotangent.md) | 切向量與餘切向量 | 切空間、餘切空間、切映射 |
| [07-向量場與張量場](07-vector-tensor-fields.md) | 場的運算 | 向量場、李導數、流 |
| [08-微分形式](08-differential-forms.md) | 外微分形式 | 1-形式、2-形式、外積、霍奇星算子 |
| [09-李群與李代數](09-lie-groups-algebras.md) | 對稱性 | 李群定義、李代數、伴隨表示 |

### 第三部分：微分幾何核心

| 章節 | 主題 | 說明 |
|------|------|------|
| [10-黎曼度量](10-riemannian-metric.md) | 度量張量 | 度量定義、距離、角度、測地線 |
| [11-協變導數與連絡](11-covariant-derivative.md) | 平行移動 | 列維-奇維塔聯絡、協變導數、測地線方程 |
| [12-曲率](12-curvature.md) | 曲率張量 | 黎曼曲率張量、里奇曲率、標量曲率 |
| [13-測地線](13-geodesics.md) | 最短路徑 | 測地線方程、指數映射測地線座標 |
| [14-黎曼幾何專題](14-riemannian-geometry.md) | 深入主題 | 雅可比場、第二變分、比較定理 |

### 第四部分：狹義相對論

| 章節 | 主題 | 說明 |
|------|------|------|
| [15-時空幾何](15-spacetime-geometry.md) | Minkowski 時空 | 光錐、固有时、世界線 |
| [16-洛倫茲變換](16-lorentz-transform.md) | 時空變換 | 洛倫茲矩陣、速度加成 |
| [17-相對論運動學](17-relativistic-kinematics.md) | 運動效應 | 時間膨脹、長度收縮、雙生子悖論 |
| [18-相對論動力學](18-relativistic-dynamics.md) | 能量與動量 | 質能等價、四動量、能量-動量張量 |
| [19-電磁場的相對論形式](19-relativistic-em.md) | Maxwell 方程 | 四維電磁勢、場張量、洛倫茲力 |

### 第五部分：廣義相對論基礎

| 章節 | 主題 | 說明 |
|------|------|------|
| [20-等效原理](20-equivalence-principle.md) | 引力與幾何 | 局域慣性系、強弱等效原理 |
| [21-愛因斯坦場方程](21-einstein-equations.md) | 引力場方程 | 愛因斯坦-希爾伯特作用量、場方程推導 |
| [22-Schwarzschild 解](22-schwarzschild.md) | 球對稱時空 | Schwarzschild 度量、事件視界 |
| [23-測地線偏折](23-geodesic-equation.md) | 時空中的運動 | 測地線方程、引力紅移、光線偏折 |
| [24-黑洞物理](24-black-holes.md) | 黑洞基礎 | 黑洞分類、奇點、視界熱力學 |

### 第六部分：廣義相對論進階

| 章節 | 主題 | 說明 |
|------|------|------|
| [25-Reissner-Nordström 度規](25-reissner-nordstrom.md) | 帶電黑洞 | 帶電球對稱時空、事件視界 |
| [26-Kerr 度規](26-kerr-metric.md) | 旋轉黑洞 | Kerr 度量、拖曳效應、ERG |
| [27-廣義相對論實驗驗證](27-experimental-tests.md) | 實驗證據 | 水星近日點進動、雷射測月、GPS |
| [28-宇宙學基礎](28-cosmology.md) | 宇宙學原理 | Robertson-Walker 度規、弗里德曼方程 |
| [29-引力波](29-gravitational-waves.md) | 引力波理論 | 線性化引力波、能量傳輸、波源 |

### 第七部分：廣義相對論專題

| 章節 | 主題 | 說明 |
|------|------|------|
| [30-黑洞資訊悖論](30-information-paradox.md) | 量子引力前沿 | 霍金輻射、黑洞蒸發、Entanglement |
| [31-蟲洞與時間機器](31-wormholes.md) | 時空拓撲 | 蟲洞、閉合類時曲線、因果性 |
| [32-黑洞吸積盤](32-accretion-disks.md) | 天體物理 | 黑洞吸積、噴流、Johns-Mitteltown |
| [33-數值相對論入門](33-numerical-relativity.md) | 計算方法 | 數值模擬、3+1 分解、Chicago 格式 |

---

## 程式碼目錄

```
_code/
├── 01/          # 第1章 向量與向量空間
├── 02/          # 第2章 矩陣與線性映射
├── 03/          # 第3章 張量初步
├── 04/          # 第4章 多變數微積分
├── 05/          # 第5章 流形概述
├── 06/          # 第6章 切空間與餘切空間
├── 07/          # 第7章 向量場與張量場
├── 08/          # 第8章 微分形式
├── 09/          # 第9章 李群與李代數
├── 10/          # 第10章 黎曼度量
├── 11/          # 第11章 協變導數與連絡
├── 12/          # 第12章 曲率
├── 13/          # 第13章 測地線
├── 14/          # 第14章 黎曼幾何專題
├── 15/          # 第15章 時空幾何
├── 16/          # 第16章 洛倫茲變換
├── 17/          # 第17章 相對論運動學
├── 18/          # 第18章 相對論動力學
├── 19/          # 第19章 電磁場的相對論形式
├── 20/          # 第20章 等效原理
├── 21/          # 第21章 愛因斯坦場方程
├── 22/          # 第22章 Schwarzschild 解
├── 23/          # 第23章 測地線偏折
├── 24/          # 第24章 黑洞物理
├── 25/          # 第25章 Reissner-Nordström 度規
├── 26/          # 第26章 Kerr 度規
├── 27/          # 第27章 廣義相對論實驗驗證
├── 28/          # 第28章 宇宙學基礎
├── 29/          # 第29章 引力波
├── 30/          # 第30章 黑洞資訊悖論
├── 31/          # 第31章 蟲洞與時間機器
├── 32/          # 第32章 黑洞吸積盤
└── 33/          # 第33章 數值相對論入門
```

---

## 專有名詞索引

* [流形](index/manifolds.md) - 局部類似歐氏空間的拓撲空間
* [張量](index/tensors.md) - 多重線性幾何量
* [黎曼度量](index/riemannian-metric.md) - 定義流形上距離與角度的對稱二形式
* [曲率](index/curvature.md) - 描述幾何體彎曲程度的量
* [Minkowski 時空](index/minkowski.md) - 狹義相對論的平直時空
* [愛因斯坦場方程](index/einstein-equations.md) - 描述時空幾何與物質關係的方程
* [黑洞](index/black-holes.md) - 連光都無法逃脫的時空區域
* [測地線](index/geodesics.md) - 彎曲空間中的「直線」
* [引力波](index/gravitational-waves.md) - 時空曲率的擾動傳播

---

## 參考資源

* [Sean Carroll, Spacetime and Geometry](https://www.amazon.com/Spacetime-Geometry-Introduction-General-Relativity/dp/0805387323)
* [Riemann,iemann, A Short Course in General Relativity](https://www.amazon.com/Short-Course-General-Relativity-Sciences/dp/0387260785)
* [Misner, Thorne, Wheeler, Gravitation](https://www.amazon.com/Gravitation-Misner-Thorne-Wheeler/dp/0691179331)
* [Wald, General Relativity](https://www.amazon.com/General-Relativity-Science-Publications/dp/0226870335)
* [Hartle, Gravity: An Introduction to Einstein's General Relativity](https://www.amazon.com/Gravity-Introduction-Einsteins-General-Relativity/dp/0805386629)

---

*最後更新：2026-03-31*
