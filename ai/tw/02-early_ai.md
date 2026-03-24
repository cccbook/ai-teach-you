# 第 2 章：傳統 AI 技術 (1950-2010) 簡介

## 2.1 爬山演算法：f(x) = (x-1)² 找最低點

在進入複雜的 AI 技術之前，讓我們從最簡單的最優化問題開始。爬山演算法（Hill Climbing）是解決最優化問題的基本方法，其核心思想非常直觀：從一個起始點出發，每次朝著能讓目標函數值變小的方向移動，直到找不到更好的鄰居為止。

讓我們以一個簡單的一維函數 f(x) = (x-1)² 為例。這個函數的最小值出現在 x = 1 處，此時 f(x) = 0。

[程式檔案：02-1-hill-climbing.py](../_code/02/02-1-hill-climbing.py)

```python
#!/usr/bin/env python3
"""
爬山演算法：f(x) = (x-1)² 找最低點
最優化問題的基本方法
"""

import random
import math

def f(x):
    """目標函數: f(x) = (x-1)^2"""
    return (x - 1) ** 2

def hill_climbing(func, start, step_size=0.1, max_iterations=1000):
    """
    爬山演算法
    
    參數:
        func: 目標函數
        start: 起始點
        step_size: 每次移動的步長
        max_iterations: 最大迭代次數
    
    返回:
        (最佳位置, 最小值, 歷史記錄)
    """
    current = start
    current_value = func(current)
    history = [(current, current_value)]
    
    for i in range(max_iterations):
        neighbors = [
            current + step_size,
            current - step_size
        ]
        
        best_neighbor = current
        best_value = current_value
        
        for neighbor in neighbors:
            value = func(neighbor)
            if value < best_value:
                best_neighbor = neighbor
                best_value = value
        
        if best_value < current_value:
            current = best_neighbor
            current_value = best_value
            history.append((current, current_value))
        else:
            break
    
    return current, current_value, history

def hill_climbing_stochastic(func, start, step_size=0.5, max_iterations=1000):
    """
    隨機爬山演算法 - 加入隨機性避免局部極小值
    """
    current = start
    current_value = func(current)
    history = [(current, current_value)]
    
    for i in range(max_iterations):
        delta = random.uniform(-step_size, step_size)
        neighbor = current + delta
        neighbor_value = func(neighbor)
        
        if neighbor_value < current_value:
            current = neighbor
            current_value = neighbor_value
            history.append((current, current_value))
        
        step_size *= 0.995
    
    return current, current_value, history

def visualize_search(history):
    print("迭代過程:")
    print("-" * 50)
    for i, (x, y) in enumerate(history):
        print(f"迭代 {i:3d}: x = {x:8.4f}, f(x) = {y:8.4f}")

def example_2d():
    """二維例子: f(x,y) = (x-1)^2 + (y-2)^2"""
    def f2d(point):
        x, y = point
        return (x - 1) ** 2 + (y - 2) ** 2
    
    def hill_climb_2d(start, steps=0.1, iterations=1000):
        current = start
        current_value = f2d(current)
        
        for _ in range(iterations):
            best = current
            best_value = current_value
            
            for dx, dy in [(steps, 0), (-steps, 0), (0, steps), (0, -steps)]:
                neighbor = (current[0] + dx, current[1] + dy)
                value = f2d(neighbor)
                if value < best_value:
                    best = neighbor
                    best_value = value
            
            if best_value < current_value:
                current = best
                current_value = best_value
            else:
                break
        
        return current, current_value
    
    print("\n=== 二維爬山演算法 ===")
    print("目標: minimize f(x,y) = (x-1)² + (y-2)²")
    print("理論最優解: (1, 2), f = 0")
    print()
    
    start = (0.0, 0.0)
    result, value = hill_climb_2d(start)
    print(f"起始點: {start}")
    print(f"結果: x = {result[0]:.4f}, y = {result[1]:.4f}")
    print(f"最小值: {value:.4f}")

if __name__ == "__main__":
    print("=== 爬山演算法：f(x) = (x-1)² 找最低點 ===\n")
    print("目標函數: f(x) = (x-1)²")
    print("理論最優解: x = 1, f(x) = 0")
    print()
    
    print("--- 標準爬山演算法 ---")
    start = 0.0
    best_x, min_value, history = hill_climbing(f, start)
    visualize_search(history)
    print(f"\n最終結果: x = {best_x:.4f}, f(x) = {min_value:.4f}")
    
    print("\n" + "=" * 50)
    print("\n--- 隨機爬山演算法 (多次執行) ---")
    results = []
    for _ in range(5):
        start = random.uniform(-5, 5)
        best_x, min_value, _ = hill_climbing_stochastic(f, start, step_size=0.5)
        results.append((best_x, min_value))
        print(f"起始 {start:.2f} -> x = {best_x:.4f}, f(x) = {min_value:.4f}")
    
    best = min(results, key=lambda x: x[1])
    print(f"\n最佳結果: x = {best[0]:.4f}, f(x) = {best[1]:.4f}")
    
    example_2d()
```

爬山演算法的關鍵問題是「局部極小值」。想像你站在一座山上想找到最低點，如果每次只往更低的方向走，你可能會被困在一個小山谷裡，而不是找到真正的最低點（全球極小值）。

## 2.2 爬山演算法解決 TSP 旅行推銷員問題

旅行推銷員問題（Traveling Salesman Problem, TSP）是一個經典的組合優化問題：給定一系列城市和每對城市之間的距離，要求找出拜訪所有城市並返回出發城市的最短路徑。

[程式檔案：02-2-hill-climbing-tsp.py](../_code/02/02-2-hill-climbing-tsp.py)

```python
#!/usr/bin/env python3
"""
爬山演算法解決 TSP 旅行推銷員問題
展示抽象化的爬山演算法如何應用於組合優化
"""

import random
import math
import copy

class TSP:
    def __init__(self, num_cities=10):
        self.num_cities = num_cities
        self.cities = self._generate_cities()
        self.distance_matrix = self._compute_distance_matrix()
    
    def _generate_cities(self):
        return [(random.uniform(0, 100), random.uniform(0, 100)) 
                for _ in range(self.num_cities)]
    
    def _compute_distance_matrix(self):
        n = self.num_cities
        dist = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                x1, y1 = self.cities[i]
                x2, y2 = self.cities[j]
                dist[i][j] = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return dist
    
    def total_distance(self, route):
        """計算路徑總距離"""
        dist = 0
        for i in range(len(route) - 1):
            dist += self.distance_matrix[route[i]][route[i+1]]
        dist += self.distance_matrix[route[-1]][route[0]]
        return dist
    
    def generate_neighbor(self, route):
        """產生相鄰解：交換兩個城市的位置"""
        new_route = route.copy()
        i, j = random.sample(range(len(new_route)), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route
    
    def two_opt_neighbor(self, route):
        """2-opt 相鄰解：反轉一段路徑"""
        new_route = route.copy()
        i, j = sorted(random.sample(range(len(new_route)), 2))
        new_route[i:j+1] = reversed(new_route[i:j+1])
        return new_route
    
    def hill_climbing(self, max_iterations=10000, use_2opt=True):
        """爬山演算法"""
        current_route = list(range(self.num_cities))
        random.shuffle(current_route)
        current_distance = self.total_distance(current_route)
        
        history = [current_distance]
        
        for i in range(max_iterations):
            if use_2opt:
                neighbor = self.two_opt_neighbor(current_route)
            else:
                neighbor = self.generate_neighbor(current_route)
            
            neighbor_distance = self.total_distance(neighbor)
            
            if neighbor_distance < current_distance:
                current_route = neighbor
                current_distance = neighbor_distance
                history.append(current_distance)
        
        return current_route, current_distance, history
    
    def simulated_annealing(self, initial_temp=10000, cooling_rate=0.9999, min_temp=0.01):
        """模擬退火演算法 - 加入隨機性避免局部極小"""
        current_route = list(range(self.num_cities))
        random.shuffle(current_route)
        current_distance = self.total_distance(current_route)
        
        best_route = current_route.copy()
        best_distance = current_distance
        
        temp = initial_temp
        history = [current_distance]
        
        while temp > min_temp:
            neighbor = self.two_opt_neighbor(current_route)
            neighbor_distance = self.total_distance(neighbor)
            
            delta = neighbor_distance - current_distance
            
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current_route = neighbor
                current_distance = neighbor_distance
                
                if current_distance < best_distance:
                    best_route = current_route.copy()
                    best_distance = current_distance
            
            temp *= cooling_rate
            history.append(best_distance)
        
        return best_route, best_distance, history

def visualize_route(cities, route, distance):
    print(f"\n城市數量: {len(cities)}")
    print(f"最佳路徑: {' -> '.join(map(str, route))} -> {route[0]}")
    print(f"總距離: {distance:.2f}")

def example_tsp():
    print("=== 爬山演算法解決 TSP ===\n")
    
    random.seed(42)
    tsp = TSP(num_cities=10)
    
    print("城市位置:")
    for i, (x, y) in enumerate(tsp.cities):
        print(f"  城市 {i}: ({x:.1f}, {y:.1f})")
    
    print("\n--- 爬山演算法 ---")
    route, distance, history = tsp.hill_climbing(max_iterations=5000)
    visualize_route(tsp.cities, route, distance)
    print(f"收斂過程: {len(history)} 次改進")
    
    print("\n--- 模擬退火 ---")
    route2, distance2, history2 = tsp.simulated_annealing()
    visualize_route(tsp.cities, route2, distance2)
    print(f"收斂過程: {len(history2)} 次改進")
    
    print("\n--- 比較 ---")
    print(f"爬山演算法: {distance:.2f}")
    print(f"模擬退火:    {distance2:.2f}")

if __name__ == "__main__":
    example_tsp()
```

TSP 問題的挑戰在於：隨著城市數量增加，可能的路徑數量呈現階乘級別成長。對於 10 個城市，有 10! / 2 = 1,814,400 種可能的路徑；而對於 20 個城市，數量會暴增到 6 × 10^16 種。傳統的暴力搜尋在實際應用中是完全不可行的。

## 2.3 搜尋演算法：A*、DFS、BFS

搜尋是 AI 中最基本也最重要的技術之一。無論是走迷宮、規劃路徑，還是解決各種邏輯問題，搜尋演算法都是核心工具。

### 2.3.1 網格搜尋

讓我們先從最簡單的網格搜尋開始，這種方法透過系統性地遍歷整個搜尋空間來找到最優解。

[程式檔案：02-3-grid-search.py](../_code/02/02-3-grid-search.py)

```python
#!/usr/bin/env python3
"""
網格搜尋演算法
暴力搜尋找最低點
"""

def grid_search(func, ranges, step=0.1):
    """
    網格搜尋
    
    參數:
        func: 目標函數
        ranges: 每個維度的搜尋範圍 [(min, max), ...]
        step: 搜尋步長
    
    返回:
        (最佳點, 最小值)
    """
    best_x = None
    best_value = float('inf')
    
    grids = []
    for min_val, max_val in ranges:
        grid = []
        x = min_val
        while x <= max_val:
            grid.append(x)
            x += step
        grids.append(grid)
    
    import itertools
    for values in itertools.product(*grids):
        value = func(*values)
        if value < best_value:
            best_value = value
            best_x = values
    
    return best_x, best_value

def f1(x):
    """一維函數"""
    return (x - 3) ** 2

def f2(x, y):
    """二維函數"""
    return (x - 1) ** 2 + (y - 2) ** 2

def f3(x, y):
    """有區域極小的函數"""
    return (x ** 2 - 4) ** 2 + (y ** 2 - 4) ** 2

if __name__ == "__main__":
    print("=== 網格搜尋演算法 ===\n")
    
    print("--- 一維範例: f(x) = (x-3)² ---")
    best_x, best_value = grid_search(f1, [(-5, 10)], step=0.5)
    print(f"網格搜尋: x = {best_x[0]:.1f}, f(x) = {best_value:.1f}")
    print(f"理論最優: x = 3, f(x) = 0")
    
    print("\n--- 二維範例: f(x,y) = (x-1)² + (y-2)² ---")
    best_x, best_value = grid_search(f2, [(-5, 5), (-5, 5)], step=1.0)
    print(f"網格搜尋: x = {best_x[0]}, y = {best_x[1]}, f(x,y) = {best_value}")
    print(f"理論最優: x = 1, y = 2, f(x,y) = 0")
    
    print("\n--- 多區域極小範例 ---")
    best_x, best_value = grid_search(f3, [(-3, 3), (-3, 3)], step=0.5)
    print(f"網格搜尋: x = {best_x[0]:.1f}, y = {best_x[1]:.1f}, f(x,y) = {best_value:.1f}")
```

### 2.3.2 深度優先搜尋 (DFS)

深度優先搜尋（Depth-First Search, DFS）沿著一條路徑一直走下去，直到走不通為止，然後回溯（backtrack）到上一個分叉點，嘗試其他路徑。DFS 的特點是佔用記憶體少，但可能會找到一條很長的路徑而非最短路徑。

[程式檔案：02-4-dfs.py](../_code/02/02-4-dfs.py)

```python
"""
Depth-First Search (DFS) Implementation
Uses a stack-based approach to explore the maze
"""

class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def is_empty(self):
        return len(self.items) == 0


def dfs_maze(maze, start, goal):
    """
    Find path from start to goal using DFS
    Returns path as list of coordinates
    """
    rows, cols = len(maze), len(maze[0])
    stack = Stack()
    stack.push([start])
    visited = set()
    visited.add(start)
    
    while not stack.is_empty():
        path = stack.pop()
        current = path[-1]
        
        if current == goal:
            return path
        
        row, col = current
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] == 0 and (nr, nc) not in visited):
                visited.add((nr, nc))
                new_path = path + [(nr, nc)]
                stack.push(new_path)
    
    return None


def print_maze(maze, path=None):
    """Display maze with path marked"""
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if path and (r, c) in path:
                line += " * "
            elif cell == 1:
                line += " ###"
            else:
                line += " . "
        print(line)
    print()


if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)
    goal = (4, 4)
    
    print("=== DFS Maze Solver ===")
    print(f"Start: {start}, Goal: {goal}\n")
    print("Maze (### = wall, . = path):")
    print_maze(maze)
    
    path = dfs_maze(maze, start, goal)
    
    if path:
        print("Solution path found:")
        print_maze(maze, path)
        print(f"Path: {path}")
        print(f"Steps: {len(path)}")
    else:
        print("No path found")
```

### 2.3.3 廣度優先搜尋 (BFS)

廣度優先搜尋（Breadth-First Search, BFS）按照「由近及遠」的順序探索所有可能的狀態。BFS 的特點是**保證找到最短路徑**，但需要較多的記憶體來儲存所有已訪問的節點。

[程式檔案：02-5-bfs.py](../_code/02/02-5-bfs.py)

```python
"""
Breadth-First Search (BFS) Implementation
Uses queue for level-order exploration, guarantees shortest path
"""

from collections import deque


def bfs_shortest_path(maze, start, goal):
    """
    Find shortest path from start to goal using BFS
    Returns path and distance
    """
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            return path, len(path) - 1
        
        row, col = current
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] == 0 and (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    
    return None, float('inf')


def print_maze(maze, path=None):
    """Display maze with path marked"""
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if path and (r, c) in path:
                line += " * "
            elif cell == 1:
                line += " ###"
            else:
                line += " . "
        print(line)
    print()


if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)
    goal = (4, 4)
    
    print("=== BFS Shortest Path ===")
    print(f"Start: {start}, Goal: {goal}\n")
    print("Maze (### = wall, . = path):")
    print_maze(maze)
    
    path, distance = bfs_shortest_path(maze, start, goal)
    
    if path:
        print("Shortest path found:")
        print_maze(maze, path)
        print(f"Path: {path}")
        print(f"Shortest distance: {distance} steps")
    else:
        print("No path found")
```

### 2.3.4 A* 搜尋演算法

A* 演算法結合了 BFS 的最優性保證和貪心搜尋的效率。A* 的核心思想是使用啟發式函數（heuristic）來估計每個節點到目標的距離，從而優先探索更有希望的節點。

[程式檔案：02-6-astar.py](../_code/02/02-6-astar.py)

```python
"""
A* Search Algorithm Implementation
Uses heuristic to guide search toward goal efficiently
"""

import heapq


def heuristic(a, b):
    """Manhattan distance heuristic for grid"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_search(maze, start, goal):
    """
    Find shortest path using A* algorithm
    f(n) = g(n) + h(n) where g=cost from start, h=heuristic to goal
    """
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1], g_score[goal]
        
        row, col = current
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            neighbor = (nr, nc)
            
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] == 0):
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
    
    return None, float('inf')


def print_maze(maze, path=None):
    """Display maze with path marked"""
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if path and (r, c) in path:
                line += " * "
            elif cell == 1:
                line += " ###"
            else:
                line += " . "
        print(line)
    print()


if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)
    goal = (4, 4)
    
    print("=== A* Search Algorithm ===")
    print(f"Start: {start}, Goal: {goal}")
    print("Using Manhattan distance heuristic\n")
    print("Maze (### = wall, . = path):")
    print_maze(maze)
    
    path, cost = astar_search(maze, start, goal)
    
    if path:
        print("Optimal path found:")
        print_maze(maze, path)
        print(f"Path: {path}")
        print(f"Total cost: {cost}")
    else:
        print("No path found")
```

## 2.4 邏輯與推論：命題邏輯、一階邏輯

邏輯推論是早期 AI 研究的核心。邏輯提供了一種形式化的方法來表示知識和進行推理。

### 2.4.1 命題邏輯

命題邏輯是最簡單的邏輯系統，它只處理真（True）或假（False）的命題。透過邏輯聯結詞（AND、OR、NOT、IMPLIES），我們可以組合出複雜的邏輯表達式。

### 2.4.2 一階邏輯

一階邏輯（First-Order Logic, FOL）比命題邏輯更強大，它允許使用：
- **個體變數**：如 x、y、z
- **謂詞**：如 Father(x, y)、Loves(x, y)
- **量詞**：全稱量詞 ∀ 和存在量詞 ∃

一階邏輯使得我們可以用更自然的方式表達「所有人的母親也是人」這樣的知識。

## 2.5 專家系統 MYCIN

MYCIN 是我們在第 1 章已經介紹過的專家系統。作為回顧，MYCIN 的核心特點包括：
- 使用可信度因子（Certainty Factor）處理不確定知識
- 知識庫與推理引擎分離
- 推論過程可解釋

## 2.6 知識表示與本體論

知識表示（Knowledge Representation）是 AI 的核心問題之一。我們如何讓電腦夠表示「鳥會飛」、「蘇格拉底是人」、「所有人類都會死」這樣的知識？

常見的知識表示方法包括：
1. **語意網路 (Semantic Networks)**：用圖結構表示概念之間的關係
2. **框架 (Frames)**：用結構化的資料槽位表示概念
3. **本體論 (Ontology)**：形式化的概念體系，如 WordNet

## 2.7 早期機器學習：決策樹、貝葉斯分類器、SVM

在深度學習興起之前，機器學習領域主要依賴於傳統的統計方法。讓我們介紹三個經典的機器學習演算法。

### 2.7.1 決策樹

決策樹是一種直觀且易於解釋的分類方法。它透過不斷地問問題來分類資料，直到達到葉節點。

[程式檔案：02-7-decision-tree.py](../_code/02/02-7-decision-tree.py)

```python
"""
Simple Decision Tree Implementation
Uses information gain (entropy) to select splitting features
"""

from collections import Counter
import math


def entropy(labels):
    """Calculate entropy of a label distribution"""
    total = len(labels)
    if total == 0:
        return 0
    counts = Counter(labels)
    probs = [count / total for count in counts.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)


def information_gain(data, feature_idx, threshold):
    """Calculate information gain from splitting on a feature"""
    labels = [row[-1] for row in data]
    parent_entropy = entropy(labels)
    
    left_data = [row for row in data if row[feature_idx] <= threshold]
    right_data = [row for row in data if row[feature_idx] > threshold]
    
    if not left_data or not right_data:
        return 0
    
    left_labels = [row[-1] for row in left_data]
    right_labels = [row[-1] for row in right_data]
    
    left_weight = len(left_data) / len(data)
    right_weight = len(right_data) / len(data)
    
    child_entropy = (left_weight * entropy(left_labels) + 
                     right_weight * entropy(right_labels))
    
    return parent_entropy - child_entropy


def build_tree(data, depth=0, max_depth=3):
    """Build decision tree recursively"""
    labels = [row[-1] for row in data]
    
    if len(set(labels)) == 1:
        return labels[0]
    
    if len(data[0]) == 1 or depth >= max_depth:
        return Counter(labels).most_common(1)[0][0]
    
    best_gain = -1
    best_split = None
    
    for feature_idx in range(len(data[0]) - 1):
        values = [row[feature_idx] for row in data]
        thresholds = set(values)
        for threshold in thresholds:
            gain = information_gain(data, feature_idx, threshold)
            if gain > best_gain:
                best_gain = gain
                best_split = (feature_idx, threshold)
    
    if best_gain <= 0:
        return Counter(labels).most_common(1)[0][0]
    
    feature_idx, threshold = best_split
    left = [row for row in data if row[feature_idx] <= threshold]
    right = [row for row in data if row[feature_idx] > threshold]
    
    return {
        'feature': feature_idx,
        'threshold': threshold,
        'left': build_tree(left, depth + 1, max_depth),
        'right': build_tree(right, depth + 1, max_depth)
    }


def predict(tree, sample):
    """Predict class label for a sample"""
    if isinstance(tree, dict):
        if sample[tree['feature']] <= tree['threshold']:
            return predict(tree['left'], sample)
        else:
            return predict(tree['right'], sample)
    return tree


if __name__ == "__main__":
    # Data: [humidity, temperature, play]
    # humidity <= 80: normal, > 80: high
    # temperature: numeric
    # play: 1=yes, 0=no
    training_data = [
        [70, 25, 1],
        [85, 30, 0],
        [75, 20, 1],
        [90, 28, 0],
        [65, 22, 1],
        [80, 32, 0],
        [60, 18, 1],
        [95, 35, 0],
    ]
    
    print("=== Simple Decision Tree ===")
    print("Features: Humidity, Temperature")
    print("Target: Play (1=Yes, 0=No)\n")
    print("Training data:")
    for row in training_data:
        print(f"  Humidity: {row[0]}, Temp: {row[1]}, Play: {row[2]}")
    
    tree = build_tree(training_data, max_depth=3)
    print(f"\nDecision Tree: {tree}")
    
    test_samples = [
        [70, 26],  # normal humidity, moderate temp
        [88, 30],  # high humidity
    ]
    
    print("\nPredictions:")
    for sample in test_samples:
        prediction = predict(tree, sample)
        print(f"  Humidity: {sample[0]}, Temp: {sample[1]} -> Play: {prediction}")
```

決策樹的核心思想是：每次選擇一個特徵和閾值來分割資料，使得分割後的子集合比原集合更「純」（homogeneous）。我們用**信息增益（Information Gain）**來衡量這個純度。

信息增益 = 父節點的熵 - 子節點加權平均的熵

### 2.7.2 貝葉斯分類器

貝葉斯分類器基於貝氏定理，計算每個類別的後驗機率，選擇具有最高後驗機率的類別作為預測結果。

[程式檔案：02-8-naive-bayes.py](../_code/02/02-8-naive-bayes.py)

```python
"""
Naive Bayes Classifier Implementation
Uses Bayes theorem with independence assumption
"""

from collections import defaultdict
import math


class NaiveBayesClassifier:
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # Laplace smoothing
        self.class_probs = {}
        self.feature_probs = defaultdict(dict)
        self.classes = []
    
    def fit(self, X, y):
        """Train the classifier on feature matrix X and labels y"""
        self.classes = list(set(y))
        n_samples = len(y)
        
        for cls in self.classes:
            self.class_probs[cls] = (y.count(cls) + self.alpha) / (n_samples + self.alpha * len(self.classes))
        
        n_features = len(X[0])
        for cls in self.classes:
            class_samples = [X[i] for i in range(len(y)) if y[i] == cls]
            for feature_idx in range(n_features):
                feature_values = [sample[feature_idx] for sample in class_samples]
                value_counts = defaultdict(int)
                for val in feature_values:
                    value_counts[val] += 1
                
                unique_values = len(set(feature_values))
                self.feature_probs[(cls, feature_idx)] = {
                    val: (count + self.alpha) / (len(class_samples) + self.alpha * unique_values)
                    for val, count in value_counts.items()
                }
    
    def predict_single(self, sample):
        """Predict class for a single sample"""
        best_class = None
        best_prob = -1
        
        for cls in self.classes:
            prob = math.log(self.class_probs[cls])
            for feature_idx, value in enumerate(sample):
                probs = self.feature_probs.get((cls, feature_idx), {})
                prob += math.log(probs.get(value, self.alpha))
            
            if prob > best_prob or best_class is None:
                best_prob = prob
                best_class = cls
        
        return best_class
    
    def predict(self, X):
        """Predict classes for multiple samples"""
        return [self.predict_single(sample) for sample in X]


if __name__ == "__main__":
    # Weather dataset: [Outlook, Temperature, Humidity, Windy, Play]
    training_data = [
        ['sunny', 'hot', 'high', 'weak', 'no'],
        ['sunny', 'hot', 'high', 'strong', 'no'],
        ['overcast', 'hot', 'high', 'weak', 'yes'],
        ['rainy', 'mild', 'high', 'weak', 'yes'],
        ['rainy', 'cool', 'normal', 'weak', 'yes'],
        ['rainy', 'cool', 'normal', 'strong', 'no'],
        ['overcast', 'cool', 'normal', 'strong', 'yes'],
        ['sunny', 'mild', 'high', 'weak', 'no'],
        ['sunny', 'cool', 'normal', 'weak', 'yes'],
        ['rainy', 'mild', 'normal', 'weak', 'yes'],
        ['sunny', 'mild', 'normal', 'strong', 'yes'],
        ['overcast', 'mild', 'high', 'strong', 'yes'],
        ['overcast', 'hot', 'normal', 'weak', 'yes'],
        ['rainy', 'mild', 'high', 'strong', 'no'],
    ]
    
    X = [row[:-1] for row in training_data]
    y = [row[-1] for row in training_data]
    
    print("=== Naive Bayes Classifier ===")
    print("Features: Outlook, Temperature, Humidity, Windy")
    print("Target: Play (yes/no)\n")
    print("Training samples:", len(training_data))
    
    clf = NaiveBayesClassifier()
    clf.fit(X, y)
    
    test_samples = [
        ['sunny', 'cool', 'high', 'weak'],
        ['rainy', 'hot', 'normal', 'strong'],
        ['overcast', 'mild', 'normal', 'weak'],
    ]
    
    predictions = clf.predict(test_samples)
    
    print("\nPredictions:")
    for sample, pred in zip(test_samples, predictions):
        print(f"  {sample} -> Play: {pred}")
    
    print(f"\nClass priors: {clf.class_probs}")
```

貝葉斯分類器的「天真」（naive）假設是：所有特徵在條件下互相獨立。儘管這個假設在現實中很少成立，貝葉斯分類器在很多實際應用中仍然表現良好。

### 2.7.3 支持向量機 (SVM)

支持向量機（Support Vector Machine, SVM）是一種強大的分類演算法，它的核心思想是找到一個能夠最大化類別間隔（margin）的超平面。

[程式檔案：02-9-svm.py](../_code/02/02-9-svm.py)

```python
"""
Support Vector Machine (SVM) Implementation
Simple linear SVM using gradient descent
"""

import numpy as np


class SimpleSVM:
    def __init__(self, learning_rate=0.01, lambda_param=0.01, n_iters=1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.weights = None
        self.bias = None
    
    def fit(self, X, y):
        """Train SVM using gradient descent"""
        n_samples, n_features = X.shape
        y_ = np.where(y <= 0, -1, 1)
        
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.weights) + self.bias) >= 1
                
                if condition:
                    self.weights -= self.lr * (2 * self.lambda_param * self.weights)
                else:
                    self.weights -= self.lr * (
                        2 * self.lambda_param * self.weights -
                        np.dot(x_i, y_[idx])
                    )
                    self.bias -= self.lr * y_[idx]
    
    def predict(self, X):
        """Predict class labels for samples"""
        linear_output = np.dot(X, self.weights) + self.bias
        return np.sign(linear_output)


def accuracy(y_true, y_pred):
    """Calculate classification accuracy"""
    return np.mean(y_true == y_pred)


if __name__ == "__main__":
    np.random.seed(42)
    
    X1 = np.random.randn(50, 2) + np.array([2, 2])
    X2 = np.random.randn(50, 2) + np.array([-2, -2])
    X = np.vstack((X1, X2))
    y = np.hstack((np.ones(50), -np.ones(50)))
    
    print("=== Support Vector Machine (Linear) ===")
    print(f"Training samples: {len(X)}")
    print(f"Features: 2D points")
    print(f"Classes: +1 (blue), -1 (red)\n")
    
    svm = SimpleSVM(learning_rate=0.01, lambda_param=0.01, n_iters=1000)
    svm.fit(X, y)
    
    predictions = svm.predict(X)
    acc = accuracy(y, predictions)
    print(f"Training accuracy: {acc * 100:.2f}%")
    
    test_points = [
        [3, 3],    # should be +1
        [-3, -3],  # should be -1
        [0, 0],    # near boundary
        [2, -2],   # should be -1
    ]
    
    print("\nTest predictions:")
    for point in test_points:
        pred = svm.predict(np.array([point]))[0]
        label = "+1" if pred == 1 else "-1"
        print(f"  Point {point} -> Class {label}")
    
    print(f"\nLearned weights: {svm.weights}")
    print(f"Learned bias: {svm.bias:.4f}")
```

SVM 的最大優點是：
1. **大間隔原則**：最大化分類間隔使得模型具有較好的泛化能力
2. **核技巧**：透過核函數（kernel function），SVM 可以處理非線性可分的資料

## 2.8 總結

本章介紹了傳統 AI 技術的核心概念和演算法：

| 類別 | 技術 | 特點 |
|------|------|------|
| 最優化 | 爬山演算法、模擬退火 | 簡單但容易陷入局部極小 |
| 搜尋 | DFS、BFS、A* | 圖搜尋的基本工具 |
| 專家系統 | 規則式系統、MYCIN | 知識編碼與推理 |
| 機器學習 | 決策樹、貝葉斯、SVM | 統計學習的代表 |

這些技術為現代深度學習奠定了基礎。雖然深度學習在很多任務上已經超越了這些傳統方法，但理解它們仍然非常重要：
1. 傳統方法在小型資料集上表現良好
2. 傳統方法具有更好的可解釋性
3. 很多現代方法的核心思想源自這些傳統技術

在接下來的章節中，我們將開始探討現代 AI 技術的核心——神經網路與深度學習。
