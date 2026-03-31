# 第 11 章：NP-完全理論

## 概述

在計算複雜度理論中，有一個問題讓數學家和電腦科學家困擾了半個世紀：

> **P = NP嗎？**

這個問題如此重要，以至於它被列為千禧年大獎難題之一，解決它可獲得一百萬美元的獎勵。

在這一章，我們將探索NP-完全理論，理解為什麼這個問題如此困難。

## 11.1 複雜度基礎

### 11.1.1 時間複雜度

時間複雜度衡量演算法所需的時間（步驟數）與輸入規模的關係。

```
┌────────────────────────────────────────────────────────────────┐
│                    常見時間複雜度                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  O(1)        常數時間    - 陣列訪問                           │
│  O(log n)    對數時間    - 二分搜尋                           │
│  O(n)        線性時間    - 線性搜尋                           │
│  O(n log n)  線性對數    - 合併排序                          │
│  O(n²)       平方時間    - 氣泡排序                          │
│  O(2ⁿ)       指數時間    - 暴力枚舉                          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 11.1.2 P類問題

**P**（Polynomial）是指可以被**確定性圖靈機**在**多項式時間**內解決的問題集合。

$$P = \{L \mid L \text{ 可被 DTM 在 } O(n^k) \text{ 時間內判定}\}$$

P類問題被認為是「容易」的問題，因為：
- 存在有效演算法
- 時間增長是可預測的
- 實際規模的問題通常可解

### 11.1.3 NP類問題

**NP**（Nondeterministic Polynomial）是指可以在**非確定性圖靈機**上在多項式時間內解決的問題。

直覺上：
- 給定一個「解」，可以在多項式時間內**驗證**其正確性
- 可以用「猜測」+「驗證」的方式解決

$$NP = \{L \mid L \text{ 可被 NTM 在 } O(n^k) \text{ 時間內判定}\}$$

[程式檔案：11-1_p_vs_np.py](../_code/11/11-1-p-vs-np.py)

```python
"""
P vs NP 問題演示
"""

from typing import List, Callable
import time

def verify_solution(certificate: List[int], problem_specific_check: Callable) -> bool:
    """
    驗證候選解的正確性
    在NP問題中，驗證比找到解更快
    """
    return problem_specific_check(certificate)

def brute_force_hamiltonian(n: int) -> List[int]:
    """
    暴力尋找哈密頓路徑
    時間複雜度：O(n!)
    
    哈密頓路徑：經過每個頂點恰好一次的路徑
    """
    vertices = list(range(n))
    best_path = None
    
    def all_permutations(items: List[int]) -> List[List[int]]:
        if not items:
            return [[]]
        result = []
        for i, item in enumerate(items):
            for perm in all_permutations(items[:i] + items[i+1:]):
                result.append([item] + perm)
        return result
    
    for perm in all_permutations(vertices):
        if len(set(perm)) == n:  # 檢查是否走過所有頂點
            best_path = perm
            break
    
    return best_path


def demonstrate_complexity_growth():
    """演示複雜度增長"""
    print("=== 複雜度增長演示 ===\n")
    
    print("時間複雜度比較（步驟數）：")
    print("-" * 60)
    print(f"{'n':<8} {'n²':<15} {'2ⁿ':<20} {'n!':<15}")
    print("-" * 60)
    
    for n in [5, 10, 15, 20, 25, 30]:
        n_sq = n ** 2
        two_pow_n = 2 ** n
        fact_n = 1
        for i in range(1, n + 1):
            fact_n *= i
        
        # 使用科學記號表示大數
        n_sq_str = f"{n_sq:,}"
        two_pow_str = f"{two_pow_n:,}" if n <= 25 else ">10²⁵"
        fact_str = f"{fact_n:,}" if n <= 12 else ">10²⁵"
        
        print(f"{n:<8} {n_sq_str:<15} {two_pow_str:<20} {fact_str:<15}")


def classify_problems():
    """問題分類"""
    print("\n=== P vs NP 問題分類 ===\n")
    
    print("P（多項式時間可解）：")
    p_problems = [
        "排序（O(n log n)）",
        "最短路徑（Dijkstra，O(m log n)）",
        "最大公約數（歐幾里得，O(log n)）",
        "連通性檢查（DFS/BFS，O(n+m)）",
        "2-SAT",
    ]
    for p in p_problems:
        print(f"  • {p}")
    
    print("\nNP（多項式時間可驗證）：")
    np_problems = [
        "哈密頓路徑（找到需要 O(n!)，驗證需要 O(n)）",
        "SAT（布爾可滿足性）",
        "旅行商問題（最佳路徑）",
        "子集和問題",
        "圖著色問題",
    ]
    for p in np_problems:
        print(f"  • {p}")


demonstrate_complexity_growth()
classify_problems()
```

執行結果：

```
=== 複雜度增長演示 ===

時間複雜度比較（步驟數）：
------------------------------------------------------------
n        n²              2ⁿ                    n!            
------------------------------------------------------------
5        25              32                    120          
10       100             1,024                3,628,800     
15       225             32,768               >10²⁵
20       400             1,048,576            >10²⁵
25       625             33,554,432           >10²⁵
30       900             1,073,741,824         >10²⁵

=== P vs NP 問題分類 ===

P（多項式時間可解）：
  • 排序（O(n log n)）
  • 最短路徑（Dijkstra，O(m log n)）
  • 最大公約數（歐幾里得，O(log n)）
  • 連通性檢查（DFS/BFS，O(n+m)）
  • 2-SAT

NP（多項式時間可驗證）：
  • 哈密頓路徑（找到需要 O(n!)，驗證需要 O(n)）
  • SAT（布爾可滿足性）
  • 旅行商問題（最佳路徑）
  • 子集和問題
  • 圖著色問題
```

## 11.2 多項式時間歸約

### 11.2.1 什麼是歸約？

**歸約**是將一個問題轉換為另一個問題的方法。

```
┌────────────────────────────────────────────────────────────────┐
│                      問題歸約示意                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│    問題 A ──────▶ 問題 B                                        │
│                        │                                       │
│   "如何做X"           │                                        │
│                        ▼                                       │
│              "如果你能解B，                                     │
│               你就能解A"                                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 11.2.2 多項式時間歸約

如果存在一個多項式時間演算法可以將問題A的實例轉換為問題B的實例，
且轉換保持答案一致，則稱：

$$A \leq_p B$$

讀作「A多項式時間歸約到B」。

### 11.2.3 為什麼要歸約？

歸約的主要用途：
1. 證明問題的難度
2. 建立問題之間的關係
3. 分類問題到複雜度類

## 11.3 NP-完全性

### 11.3.1 定義

**NP-完全（NP-Complete）**問題是NP中最「難」的問題。

一個問題L是NP-完全的，如果：
1. $L \in NP$（L可以被驗證）
2. 對所有$L' \in NP$，有$L' \leq_p L$（所有NP問題都可以歸約到L）

```
┌────────────────────────────────────────────────────────────────┐
│                    NP-完全的直覺                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  NP-完全問題是NP中最「難」的                                   │
│                                                                │
│  如果你能在多項式時間內解決任意一個NP-完全問題，               │
│  那麼所有NP問題都可以在多項式時間內解決                        │
│                                                                │
│  這就是 P = NP 的含義                                          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 11.3.2 Cook-Levin定理

1971年，史蒂芬·庫克（Stephen Cook）和萊昂尼德·萊文（Leonid Levin）獨立證明了：

> **Cook-Levin定理**
>
> SAT（布爾可滿足性問題）是NP-完全的。

這個定理的重要性：
- SAT是第一個被證明為NP-完全的問題
- 所有其他NP-完全問題都通過SAT歸約證明

### 11.3.3 NP-完全問題的家族

一旦一個問題被證明是NP-完全的，就可以用它來證明其他問題：

```
┌────────────────────────────────────────────────────────────────┐
│                    NP-完全問題家族                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  SAT ─────┬──▶ 3-SAT ──▶ 圖著色 ──▶ 四色定理                 │
│           │                                                    │
│           └──▶ 哈密頓路徑 ──▶ 旅行商問題                      │
│                                                                │
│  SAT ──▶ 子集和 ──▶ 背包問題                                  │
│                                                                │
│  SAT ──▶ 整數線性規劃                                         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## 11.4 經典NP-完全問題

### 11.4.1 SAT（布爾可滿足性）

給定一個布爾公式，是否存在變數赋值使整個公式為真？

```
例如：(x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂) ∧ (x₂ ∨ ¬x₃)

問題：是否存在 x₁, x₂, x₃ 的真值赋值使公式為真？
```

SAT是第一個被證明為NP-完全的問題。

### 11.4.2 3-SAT

SAT的特殊情況：每個子句恰好有3個文字。

3-SAT更易於處理歸約，是證明NP-完全性的常用工具。

### 11.4.3 哈密頓路徑

給定一個圖，是否存在經過每個頂點恰好一次的路径？

這與旅行商問題（TSP）密切相關。

[程式檔案：11-2_np_complete.py](../_code/11/11-2-np-complete.py)

```python
"""
經典NP-完全問題實現
"""

from typing import List, Set, Tuple, Optional
import random

class SATSolver:
    """SAT求解器（暴力版本）"""
    
    def __init__(self, num_vars: int):
        self.n = num_vars
        self.clauses = []
    
    def add_clause(self, literals: List[int]):
        """添加子句，literals 是文字列表"""
        self.clauses.append(literals)
    
    def solve(self) -> Optional[List[int]]:
        """
        暴力求解SAT
        時間複雜度：O(2ⁿ * m)，其中n是變數數，m是子句數
        """
        n_assignments = 2 ** self.n
        
        for assignment in range(n_assignments):
            values = [(assignment >> i) & 1 == 1 for i in range(self.n)]
            
            # 檢查所有子句
            satisfied = True
            for clause in self.clauses:
                clause_satisfied = False
                for literal in clause:
                    var_idx = abs(literal) - 1
                    is_negated = literal < 0
                    
                    if is_negated:
                        clause_satisfied = clause_satisfied or (not values[var_idx])
                    else:
                        clause_satisfied = clause_satisfied or values[var_idx]
                
                if not clause_satisfied:
                    satisfied = False
                    break
            
            if satisfied:
                return values
        
        return None


class ThreeSAT:
    """3-SAT問題"""
    
    def __init__(self):
        self.variables = set()
        self.clauses = []
    
    def add_clause(self, x: int, y: int, z: int):
        """添加三元子句 (x ∨ y ∨ z)"""
        self.variables.add(abs(x))
        self.variables.add(abs(y))
        self.variables.add(abs(z))
        self.clauses.append((x, y, z))
    
    def is_satisfied(self, assignment: dict) -> bool:
        """檢查賦值是否滿足所有子句"""
        for x, y, z in self.clauses:
            val = (assignment.get(x, False) or 
                   assignment.get(y, False) or 
                   assignment.get(z, False))
            if not val:
                return False
        return True
    
    def solve_greedy(self) -> Optional[dict]:
        """貪心求解（不保證最優）"""
        assignment = {}
        
        for var in range(1, max(self.variables) + 1):
            # 計算這個變數為True/False時能滿足多少子句
            true_count = sum(
                1 for x, y, z in self.clauses
                if (var in [abs(x), abs(y), abs(z)]) and
                   ((x > 0 and x == var) or (y > 0 and y == var) or (z > 0 and z == var) or
                    (x < 0 and x != -var) or (y < 0 and y != -var) or (z < 0 and z != -var))
            )
            assignment[var] = true_count >= len([c for c in self.clauses if var in [abs(x) for x in c]]) / 2
        
        return assignment if self.is_satisfied(assignment) else None


class TravelingSalesman:
    """旅行商問題（TSP）"""
    
    def __init__(self, n: int):
        self.n = n
        self.distances = [[0 if i == j else float('inf') 
                         for j in range(n)] for i in range(n)]
    
    def add_edge(self, i: int, j: int, weight: float):
        self.distances[i][j] = weight
        self.distances[j][i] = weight
    
    def solve_brute_force(self) -> Tuple[float, List[int]]:
        """
        暴力求解TSP
        時間複雜度：O(n!)
        """
        vertices = list(range(self.n))
        best_cost = float('inf')
        best_path = None
        
        def permutations(items: List[int]) -> List[List[int]]:
            if not items:
                return [[]]
            return [[items[i]] + p 
                    for i in range(len(items)) 
                    for p in permutations(items[:i] + items[i+1:])]
        
        for perm in permutations(vertices[1:]):
            path = [0] + perm
            cost = sum(self.distances[path[i]][path[i+1]] 
                      for i in range(len(path) - 1))
            
            if cost < best_cost:
                best_cost = cost
                best_path = path
        
        return best_cost, best_path
    
    def nearest_neighbor(self, start: int = 0) -> Tuple[float, List[int]]:
        """
        最近鄰居啟發式（貪心）
        不保證最優，但快
        """
        visited = {start}
        path = [start]
        cost = 0
        
        current = start
        while len(visited) < self.n:
            nearest = None
            nearest_dist = float('inf')
            
            for j in range(self.n):
                if j not in visited and self.distances[current][j] < nearest_dist:
                    nearest = j
                    nearest_dist = self.distances[current][j]
            
            if nearest is not None:
                visited.add(nearest)
                path.append(nearest)
                cost += nearest_dist
                current = nearest
        
        # 返回起點
        cost += self.distances[current][start]
        path.append(start)
        
        return cost, path


def demo_np_complete():
    """演示NP-完全問題"""
    print("=== NP-完全問題演示 ===\n")
    
    # 3-SAT
    print("1. 3-SAT 問題：")
    sat = ThreeSAT()
    sat.add_clause(1, 2, 3)    # (x₁ ∨ x₂ ∨ x₃)
    sat.add_clause(-1, 2, -3)  # (¬x₁ ∨ x₂ ∨ ¬x₃)
    sat.add_clause(1, -2, 3)   # (x₁ ∨ ¬x₂ ∨ x₃)
    
    result = sat.solve_greedy()
    if result:
        print(f"   候選解：x₁={result[1]}, x₂={result[2]}, x₃={result[3]}")
        print(f"   滿足所有子句：{sat.is_satisfied(result)}")
    else:
        print("   無解（貪心失敗）")
    
    print("\n" + "─" * 50)
    
    # TSP
    print("\n2. 旅行商問題 (TSP)：")
    tsp = TravelingSalesman(5)
    edges = [(0, 1, 10), (0, 2, 15), (0, 3, 20),
             (1, 2, 35), (1, 3, 25), (1, 4, 30),
             (2, 3, 30), (2, 4, 15),
             (3, 4, 25)]
    
    for i, j, w in edges:
        tsp.add_edge(i, j, w)
    
    print("   圖：5個城市，邊權如上")
    
    # 使用貪心啟發式
    cost, path = tsp.nearest_neighbor(0)
    print(f"   最近鄰居：路徑 {path}，成本 {cost}")
    
    print("\n   （暴力求解 n=5! 需要120次比較）")


demo_np_complete()
```

## 11.5 NP-困難與NP-中間

### 11.5.1 NP-困難

**NP-困難**問題不一定在NP中，但至少和NP-完全問題一樣難：

$$L \text{ 是 NP-困難的} \iff \forall L' \in NP: L' \leq_p L$$

### 11.5.2 問題分類的圖示

```
┌────────────────────────────────────────────────────────────────┐
│                    複雜度類的關係                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│                    ┌───────────┐                              │
│                    │   決定性   │                              │
│                    │   圖靈機   │                              │
│                    │           │                              │
│                    │  ┌─────┐  │                              │
│                    │  │  P  │  │                              │
│                    │  └─────┘  │                              │
│                    │      ↕     │                              │
│                    │  ┌─────┐  │                              │
│                    │  │  NP │  │                              │
│                    │  │ ↗   ↘ │                              │
│                    │  │ NPC  │  │                              │
│                    │  └─────┘  │                              │
│                    └───────────┘                              │
│                                                                │
│  NPC = NP-完全                                                │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 11.5.3 P = NP的可能性

如果P = NP：

- 所有NP問題都有多項式時間演算法
- 密碼學需要完全重新設計
- 優化問題變得容易
- 數學證明可以自動化

如果P ≠ NP：

- NP-完全問題本質上困難
- 只能用近似或啟發式方法
- 密碼學有理論基礎
- 問題的難度是固有的

## 11.6 處理NP-完全問題

### 11.6.1 近似演算法

對於優化問題，可以設計在多項式時間內給出「足夠好」的解的演算法：

```python
# TSP的2-近似演算法
def tsp_approximation(graph):
    # 1. 構造最小生成樹
    mst = minimum_spanning_tree(graph)
    
    # 2. 深度優先遍歷
    tour = dfs_tour(mst)
    
    # 3. 捷徑優化
    return shortcut_optimize(tour)
```

### 11.6.2 參數化演算法

如果某個參數k很小，可以設計複雜度為$O(f(k) \cdot n^c)$的演算法：

| 問題 | 標準複雜度 | 參數化複雜度 |
|------|-----------|-------------|
| 頂點覆蓋 | $O(2^n)$ | $O(1.27^k \cdot n)$ |
| 哈密頓路徑 | $O(n!)$ | $O(k! \cdot n)$ |
| 子集和 | $O(2^{n/2})$ | $O(n \cdot 2^{k/2})$ |

### 11.6.3 啟發式方法

實際應用中常用的方法：
- 遺傳演算法
- 蟻群優化
- 模擬退火
- 局部搜索

## 11.7 小結

本章我們：

1. **理解了P和NP**：多項式時間可解 vs 可驗證
2. **掌握了多項式時間歸約**：問題之間的轉換
3. **理解了NP-完全性**：NP中最難的問題
4. **認識了經典NP-完全問題**：SAT、TSP、哈密頓路徑
5. **學會了處理NP-完全問題的策略**：近似、參數化、啟發式

P vs NP問題至今仍未解決，但它已經成為現代密碼學和最佳化理論的基礎。

下一章，我們將探索計算理論的最新發展！

## 練習題

1. **設計歸約**：證明哈密頓路徑問題可以歸約到TSP。

2. **近似分析**：分析貪心演算法對TSP的近似比。

3. **參數化**：設計一個參數化的頂點覆蓋演算法，參數是k。

4. **思考題**：如果P = NP，對社會會有什麼影響？特別是對密碼學、醫藥研發、數學證明？

5. **實作**：用Python實作一個簡單的SAT求解器（可以嘗試Davis-Putnam-Logemann-Loveland算法）。
