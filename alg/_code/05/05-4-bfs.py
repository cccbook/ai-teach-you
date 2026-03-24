"""
廣度優先搜尋範例 (Breadth-First Search - BFS)
=========================================
展示廣度優先搜尋（BFS）的各種實作方式。
BFS 是一種圖形遍訪演算法，從根節點開始逐層向外擴展搜尋。
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, deque


def bfs_basic(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    基本廣度優先搜尋
    
    參數:
        graph: 圖的鄰接表
        start: 起始節點
    
    返回:
        遍歷順序
    """
    visited = {start}
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result


def bfs_levels(graph: Dict[int, List[int]], start: int) -> List[List[int]]:
    """
    BFS 分層遍歷
    
    參數:
        graph: 圖的鄰接表
        start: 起始節點
    
    返回:
        每層的節點列表
    """
    visited = {start}
    queue = deque([start])
    levels = []
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        levels.append(current_level)
    
    return levels


def bfs_shortest_path(
    graph: Dict[int, List[int]],
    start: int,
    target: int
) -> Optional[List[int]]:
    """
    BFS 找最短路徑
    
    參數:
        graph: 圖的鄰接表
        start: 起始節點
        target: 目標節點
    
    返回:
        最短路徑列表
    """
    if start == target:
        return [start]
    
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor == target:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None


def bfs_shortest_distance(
    graph: Dict[int, List[int]],
    start: int
) -> Dict[int, int]:
    """
    BFS 計算最短距離
    
    参數:
        graph: 圖的鄰接表
        start: 起始節點
    
    返回:
        各節點到起始點的最短距離
    """
    distances = {start: 0}
    visited = {start}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)
    
    return distances


def bfs_all_paths(
    graph: Dict[int, List[int]],
    start: int,
    target: int
) -> List[List[int]]:
    """
    BFS 找出所有最短路徑
    
    參數:
        graph: 圖的鄰接表
        start: 起始節點
        target: 目標節點
    
    返回:
        所有最短路徑列表
    """
    paths = []
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor not in path:
                new_path = path + [neighbor]
                
                if neighbor == target:
                    paths.append(new_path)
                else:
                    queue.append((neighbor, new_path))
    
    return paths


def bfs_maze_shortest_path(
    maze: List[List[int]],
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> Optional[List[Tuple[int, int]]]:
    """
    BFS 找迷宮最短路徑
    
    參數:
        maze: 迷宮（0=路, 1=牆）
        start: 起始位置
        end: 結束位置
    
    返回:
        最短路徑列表
    """
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0
    
    if maze[start[0]][start[1]] == 1 or maze[end[0]][end[1]] == 1:
        return None
    
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        (r, c), path = queue.popleft()
        
        if (r, c) == end:
            return path
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if is_valid(nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    
    return None


def bfs_detect_cycle(graph: Dict[int, List[int]]) -> bool:
    """
    BFS 檢測循環
    
    參數:
        graph: 圖的鄰接表
    
    返回:
        是否有循環
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    
    for node in graph:
        if color[node] != WHITE:
            continue
        
        queue = deque([node])
        color[node] = GRAY
        
        while queue:
            current = queue.popleft()
            
            for neighbor in graph[current]:
                if color[neighbor] == GRAY:
                    return True
                
                if color[neighbor] == WHITE:
                    color[neighbor] = GRAY
                    queue.append(neighbor)
            
            color[current] = BLACK
    
    return False


def bfs_tree_level_order(root: 'TreeNode') -> List[List[Any]]:
    """
    二元樹層級遍歷（BFS）
    
    參數:
        root: 樹根節點
    
    返回:
        每層的節點列表
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result


def bfs_find_minimum_depth(root: 'TreeNode') -> int:
    """
    BFS 找二元樹最小深度
    
    參數:
        root: 樹根節點
    
    返回:
        最小深度
    """
    if not root:
        return 0
    
    queue = deque([root])
    depth = 0
    
    while queue:
        depth += 1
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            
            if not node.left and not node.right:
                return depth
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return depth


def bfs_connect_all_nodes(graph: Dict[int, List[int]], n: int) -> int:
    """
    BFS 檢查並計算連通分量數量
    
    參數:
        graph: 圖的鄰接表
        n: 節點總數
    
    返回:
        連通分量數量
    """
    if n == 0:
        return 0
    
    visited = set()
    components = 0
    
    for node in range(n):
        if node not in visited:
            components += 1
            queue = deque([node])
            
            while queue:
                current = queue.popleft()
                
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
    
    return components


class TreeNode:
    """二元樹節點"""
    def __init__(self, val: Any, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right


def demo_bfs():
    """演示 BFS"""
    print("=== 廣度優先搜尋範例演示 ===")
    print()
    
    print("1. 基本 BFS:")
    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1],
        5: [2]
    }
    result = bfs_basic(graph, 0)
    print(f"   圖: {graph}")
    print(f"   遍歷順序: {result}")
    print()
    
    print("2. 分層遍歷:")
    levels = bfs_levels(graph, 0)
    print(f"   分層結果: {levels}")
    print()
    
    print("3. 最短路徑:")
    path = bfs_shortest_path(graph, 0, 5)
    print(f"   從 0 到 5 的最短路徑: {path}")
    print()
    
    print("4. 最短距離:")
    distances = bfs_shortest_distance(graph, 0)
    print(f"   各節點到 0 的距離: {distances}")
    print()
    
    print("5. 樹層級遍歷:")
    tree = TreeNode(1,
                   TreeNode(2, TreeNode(4), TreeNode(5)),
                   TreeNode(3, TreeNode(6), TreeNode(7)))
    levels = bfs_tree_level_order(tree)
    print(f"   層級遍歷: {levels}")
    print()
    
    print("6. 最小深度:")
    depth = bfs_find_minimum_depth(tree)
    print(f"   樹的最小深度: {depth}")


if __name__ == "__main__":
    demo_bfs()
