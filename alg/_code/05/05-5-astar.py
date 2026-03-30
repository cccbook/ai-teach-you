"""
A* 搜尋演算法範例 (A* Search Algorithm)
======================================
展示 A* 搜尋演算法的實作方式。
A* 是一種啟發式搜尋演算法，结合了代價估計和貪心最佳化的優點。
"""

from typing import List, Dict, Tuple, Set, Callable, Optional
from collections import defaultdict
import heapq


def astar_search(
    graph: Dict[int, List[Tuple[int, float]]],
    heuristics: Dict[int, float],
    start: int,
    goal: int
) -> Tuple[Optional[List[int]], float]:
    """
    基本 A* 搜尋
    
    參數:
        graph: 圖的鄰接表 {節點: [(鄰居, 代價), ...]}
        heuristics: 啟發式估計 {節點: 到目標的估計代價}
        start: 起始節點
        goal: 目標節點
    
    返回:
        (路徑, 總代價)
    """
    open_set = [(heuristics[start], 0, start, [start])]
    visited = set()
    
    while open_set:
        _, cost, current, path = heapq.heappop(open_set)
        
        if current == goal:
            return path, cost
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for neighbor, edge_cost in graph.get(current, []):
            if neighbor not in visited:
                new_cost = cost + edge_cost
                f_score = new_cost + heuristics.get(neighbor, 0)
                heapq.heappush(open_set, (f_score, new_cost, neighbor, path + [neighbor]))
    
    return None, float('inf')


def astar_maze_solver(
    maze: List[List[int]],
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> Optional[List[Tuple[int, int]]]:
    """
    A* 解決迷宮問題
    
    參數:
        maze: 迷宮（0=路, 1=牆）
        start: 起始位置
        end: 結束位置
    
    返回:
        路徑列表
    """
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    def heuristic(r, c):
        return abs(r - end[0]) + abs(c - end[1])
    
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0
    
    open_set = [(heuristic(start[0], start[1]), 0, start[0], start[1], [(start[0], start[1])])]
    visited = set()
    
    while open_set:
        _, cost, r, c, path = heapq.heappop(open_set)
        
        if (r, c) == end:
            return path
        
        if (r, c) in visited:
            continue
        
        visited.add((r, c))
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if is_valid(nr, nc) and (nr, nc) not in visited:
                move_cost = 1.414 if dr != 0 and dc != 0 else 1
                new_cost = cost + move_cost
                f_score = new_cost + heuristic(nr, nc)
                heapq.heappush(open_set, (f_score, new_cost, nr, nc, path + [(nr, nc)]))
    
    return None


def astar_with_weight(
    graph: Dict[int, List[Tuple[int, float]]],
    heuristics: Dict[int, float],
    start: int,
    goal: int,
    weight: float = 1.0
) -> Tuple[Optional[List[int]], float]:
    """
    加權 A* 搜尋
    
    參數:
        graph: 圖的鄰接表
        heuristics: 啟發式估計
        start: 起始節點
        goal: 目標節點
        weight: 權重因子（>1 更快但可能非最優）
    
    返回:
        (路徑, 總代價)
    """
    open_set = [(heuristics[start] * weight, 0, start, [start])]
    visited = set()
    
    while open_set:
        _, cost, current, path = heapq.heappop(open_set)
        
        if current == goal:
            return path, cost
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for neighbor, edge_cost in graph.get(current, []):
            if neighbor not in visited:
                new_cost = cost + edge_cost
                f_score = new_cost + heuristics.get(neighbor, 0) * weight
                heapq.heappush(open_set, (f_score, new_cost, neighbor, path + [neighbor]))
    
    return None, float('inf')


def astar_8_puzzle(
    state: Tuple[int, ...],
    goal: Tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 0)
) -> Optional[List[Tuple[int, ...]]]:
    """
    A* 解決 8 數字推盤遊戲
    
    參數:
        state: 初始狀態（9個數字，0表示空格）
        goal: 目標狀態
    
    返回:
        求解步驟列表
    """
    def heuristic(state):
        distance = 0
        for i, val in enumerate(state):
            if val != 0:
                goal_pos = (val - 1) // 3, (val - 1) % 3
                current_pos = i // 3, i % 3
                distance += abs(goal_pos[0] - current_pos[0]) + abs(goal_pos[1] - current_pos[1])
        return distance
    
    def get_neighbors(state):
        neighbors = []
        pos = state.index(0)
        row, col = pos // 3, pos % 3
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_pos = nr * 3 + nc
                new_state = list(state)
                new_state[pos], new_state[new_pos] = new_state[new_pos], new_state[pos]
                neighbors.append(tuple(new_state))
        
        return neighbors
    
    open_set = [(heuristic(state), 0, state, [state])]
    visited = {}
    
    while open_set:
        _, cost, current, path = heapq.heappop(open_set)
        
        if current == goal:
            return path
        
        if current in visited and visited[current] <= cost:
            continue
        
        visited[current] = cost
        
        for neighbor in get_neighbors(current):
            new_cost = cost + 1
            if neighbor not in visited or visited[neighbor] > new_cost:
                f_score = new_cost + heuristic(neighbor)
                heapq.heappush(open_set, (f_score, new_cost, neighbor, path + [neighbor]))
    
    return None


def astar_admissible_heuristic(
    graph: Dict[int, List[Tuple[int, float]]],
    goal: int
) -> Dict[int, float]:
    """
    為圖生成 admissable 啟發式
    
    參數:
        graph: 圖的鄰接表
        goal: 目標節點
    
    返回:
        啟發式字典
    """
    def bfs(target):
        distances = {target: 0}
        queue = [(target, 0)]
        
        while queue:
            node, dist = queue.pop(0)
            
            for neighbor in graph.get(node, []):
                if neighbor[0] not in distances:
                    distances[neighbor[0]] = dist + neighbor[1]
                    queue.append((neighbor[0], dist + neighbor[1]))
        
        return distances
    
    return bfs(goal)


def astar_iterative_deepening(
    graph: Dict[int, List[Tuple[int, float]]],
    heuristics: Dict[int, float],
    start: int,
    goal: int
) -> Optional[List[int]]:
    """
    A* 迭代加深搜尋
    
    參數:
        graph: 圖的鄰接表
        heuristics: 啟發式估計
        start: 起始節點
        goal: 目標節點
    
    返回:
        路徑
    """
    threshold = heuristics[start]
    
    while True:
        path, cost, found = astar_recursive(graph, heuristics, start, goal, threshold, {}, set())
        
        if found:
            return path
        
        if cost == float('inf'):
            return None
        
        threshold = cost


def astar_recursive(
    graph: Dict[int, List[Tuple[int, float]]],
    heuristics: Dict[int, float],
    current: int,
    goal: int,
    threshold: float,
    g_scores: Dict[int, float],
    visited: Set[int]
) -> Tuple[Optional[List[int]], float, bool]:
    """遞迴 A*"""
    f = g_scores.get(current, 0) + heuristics.get(current, 0)
    
    if f > threshold:
        return None, f, False
    
    if current == goal:
        return [current], g_scores[current], True
    
    visited.add(current)
    
    min_next = float('inf')
    found_path = None
    
    for neighbor, cost in graph.get(current, []):
        if neighbor not in visited:
            new_g = g_scores.get(current, 0) + cost
            
            if neighbor not in g_scores or new_g < g_scores[neighbor]:
                g_scores[neighbor] = new_g
            
            path, next_threshold, found = astar_recursive(
                graph, heuristics, neighbor, goal, threshold, g_scores, visited
            )
            
            if found:
                return [current] + path, next_threshold, True
            
            min_next = min(min_next, next_threshold)
    
    visited.remove(current)
    return found_path, min_next, False


def astar_best_first_search(
    graph: Dict[int, List[Tuple[int, float]]],
    heuristics: Dict[int, float],
    start: int,
    goal: int
) -> Optional[List[int]]:
    """
    最佳優先搜尋（貪心 A*）
    
    參數:
        graph: 圖的鄰接表
        heuristics: 啟發式估計
        start: 起始節點
        goal: 目標節點
    
    返回:
        路徑
    """
    open_set = [(heuristics[start], start, [start])]
    visited = set()
    
    while open_set:
        _, current, path = heapq.heappop(open_set)
        
        if current == goal:
            return path
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for neighbor, cost in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(open_set, (heuristics.get(neighbor, 0), neighbor, path + [neighbor]))
    
    return None


class AStarSolver:
    """A* 求解器類別"""
    
    def __init__(self, graph: Dict[int, List[Tuple[int, float]]], heuristics: Dict[int, float]):
        self.graph = graph
        self.heuristics = heuristics
    
    def solve(self, start: int, goal: int, weighted: bool = False) -> Dict:
        """求解"""
        if weighted:
            path, cost = astar_with_weight(self.graph, self.heuristics, start, goal, 1.5)
        else:
            path, cost = astar_search(self.graph, self.heuristics, start, goal)
        
        return {
            "path": path,
            "cost": cost,
            "found": path is not None
        }


def demo_astar():
    """演示 A*"""
    print("=== A* 搜尋演算法範例演示 ===")
    print()
    
    print("1. 基本 A* 搜尋:")
    graph = {
        0: [(1, 1), (2, 4)],
        1: [(0, 1), (2, 2), (3, 5)],
        2: [(0, 4), (1, 2), (3, 1)],
        3: [(1, 5), (2, 1)]
    }
    heuristics = {0: 3, 1: 2, 2: 1, 3: 0}
    
    path, cost = astar_search(graph, heuristics, 0, 3)
    print(f"   圖: {graph}")
    print(f"   從 0 到 3: 路徑={path}, 代價={cost}")
    print()
    
    print("2. 最佳優先搜尋:")
    path = astar_best_first_search(graph, heuristics, 0, 3)
    print(f"   路徑: {path}")
    print()
    
    print("3. 加權 A* 搜尋:")
    path, cost = astar_with_weight(graph, heuristics, 0, 3, 1.5)
    print(f"   路徑: {path}, 代價: {cost}")
    print()
    
    print("4. 8 數字推盤:")
    initial = (1, 2, 3, 4, 0, 5, 6, 7, 8)
    solution = astar_8_puzzle(initial)
    if solution:
        print(f"   求解步數: {len(solution) - 1}")


if __name__ == "__main__":
    demo_astar()
