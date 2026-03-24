"""
深度優先搜尋範例 (Depth-First Search - DFS)
=========================================
展示深度優先搜尋（DFS）的各種實作方式。
DFS 是一種圖形遍歷演算法，沿著分支尽可能深入搜尋，然後回溯。
"""

from typing import List, Dict, Set, Tuple, Any, Callable, Optional
from collections import defaultdict


def dfs_recursive(
    graph: Dict[int, List[int]],
    start: int,
    visited: Set[int] = None
) -> List[int]:
    """
    遞迴深度優先搜尋
    
    參數:
        graph: 圖的鄰接表
        start: 起始節點
        visited: 已訪問節點集合
    
    返回:
        遍歷順序
    """
    if visited is None:
        visited = set()
    
    visited.add(start)
    result = [start]
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))
    
    return result


def dfs_iterative(
    graph: Dict[int, List[int]],
    start: int
) -> List[int]:
    """
    迭代深度優先搜尋（使用堆疊）
    
    參數:
        graph: 圖的鄰接表
        start: 起始節點
    
    返回:
        遍歷順序
    """
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        
        if node not in visited:
            visited.add(node)
            result.append(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result


def dfs_with_prepost_order(
    graph: Dict[int, List[int]],
    start: int
) -> Dict[str, List[int]]:
    """
    DFS 記錄前序和後序
    
    參數:
        graph: 圖的鄰接表
        start: 起始節點
    
    返回:
        前序、後序列表
    """
    visited = set()
    pre_order = []
    post_order = []
    
    def dfs(node):
        visited.add(node)
        pre_order.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        
        post_order.append(node)
    
    dfs(start)
    
    return {
        "pre_order": pre_order,
        "post_order": post_order
    }


def dfs_path_finding(
    graph: Dict[int, List[int]],
    start: int,
    target: int
) -> Optional[List[int]]:
    """
    DFS 找路徑
    
    參數:
        graph: 圖的鄰接表
        start: 起始節點
        target: 目標節點
    
    返回:
        路徑列表，若不存在則返回 None
    """
    visited = set()
    path = []
    
    def dfs(node):
        if node == target:
            path.append(node)
            return True
        
        visited.add(node)
        path.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
        
        path.pop()
        return False
    
    dfs(start)
    return path if path else None


def dfs_all_paths(
    graph: Dict[int, List[int]],
    start: int,
    target: int
) -> List[List[int]]:
    """
    DFS 找出所有路徑
    
    參數:
        graph: 圖的鄰接表
        start: 起始節點
        target: 目標節點
    
    返回:
        所有路徑列表
    """
    paths = []
    visited = set()
    
    def dfs(node, current_path):
        if node == target:
            paths.append(current_path + [node])
            return
        
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, current_path + [node])
        
        visited.remove(node)
    
    dfs(start, [])
    return paths


def dfs_detect_cycle(
    graph: Dict[int, List[int]]
) -> Tuple[bool, Optional[int]]:
    """
    DFS 檢測循環
    
    參數:
        graph: 圖的鄰接表
    
    返回:
        (是否有循環, 循環中的節點)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    
    def dfs(node):
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True
        
        color[node] = BLACK
        return False
    
    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True, None
    
    return False, None


def dfs_topological_sort(graph: Dict[int, List[int]]) -> List[int]:
    """
    DFS 拓撲排序
    
    參數:
        graph: 有向無環圖的鄰接表
    
    返回:
        拓撲排序順序
    """
    visited = set()
    result = []
    
    def dfs(node):
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        
        result.append(node)
    
    for node in graph:
        if node not in visited:
            dfs(node)
    
    return result[::-1]


def dfs_maze_solver(
    maze: List[List[int]],
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> Optional[List[Tuple[int, int]]]:
    """
    DFS 解決迷宮問題
    
    參數:
        maze: 迷宮（0=路, 1=牆）
        start: 起始位置
        end: 結束位置
    
    返回:
        路徑列表
    """
    rows, cols = len(maze), len(maze[0])
    visited = set()
    path = []
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0
    
    def dfs(r, c):
        if (r, c) == end:
            path.append((r, c))
            return True
        
        visited.add((r, c))
        path.append((r, c))
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and (nr, nc) not in visited:
                if dfs(nr, nc):
                    return True
        
        path.pop()
        return False
    
    dfs(start[0], start[1])
    return path if path else None


def dfs_find_connected_components(
    graph: Dict[int, List[int]]
) -> List[Set[int]]:
    """
    DFS 找出連通分量
    
    參數:
        graph: 圖的鄰接表
    
    返回:
        連通分量列表
    """
    visited = set()
    components = []
    
    def dfs(node, component):
        visited.add(node)
        component.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for node in graph:
        if node not in visited:
            component = set()
            dfs(node, component)
            components.append(component)
    
    return components


def dfs_binary_tree_inorder(root: 'TreeNode') -> List[Any]:
    """
    二元樹中序遍歷（DFS）
    
    參數:
        root: 樹根節點
    
    返回:
        中序遍歷結果
    """
    if root is None:
        return []
    
    result = []
    
    result.extend(dfs_binary_tree_inorder(root.left))
    result.append(root.val)
    result.extend(dfs_binary_tree_inorder(root.right))
    
    return result


def dfs_binary_tree_preorder(root: 'TreeNode') -> List[Any]:
    """
    二元樹前序遍歷（DFS）
    
    參數:
        root: 樹根節點
    
    返回:
        前序遍歷結果
    """
    if root is None:
        return []
    
    result = [root.val]
    result.extend(dfs_binary_tree_preorder(root.left))
    result.extend(dfs_binary_tree_preorder(root.right))
    
    return result


def dfs_binary_tree_postorder(root: 'TreeNode') -> List[Any]:
    """
    二元樹後序遍歷（DFS）
    
    參數:
        root: 樹根節點
    
    返回:
        後序遍歷結果
    """
    if root is None:
        return []
    
    result = []
    result.extend(dfs_binary_tree_postorder(root.left))
    result.extend(dfs_binary_tree_postorder(root.right))
    result.append(root.val)
    
    return result


class TreeNode:
    """二元樹節點"""
    def __init__(self, val: Any, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right


def demo_dfs():
    """演示 DFS"""
    print("=== 深度優先搜尋範例演示 ===")
    print()
    
    print("1. 基本 DFS:")
    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1],
        5: [2]
    }
    result = dfs_recursive(graph, 0)
    print(f"   圖: {graph}")
    print(f"   遍歷順序: {result}")
    print()
    
    print("2. 迭代 DFS:")
    result = dfs_iterative(graph, 0)
    print(f"   遍歷順序: {result}")
    print()
    
    print("3. 找路徑:")
    path = dfs_path_finding(graph, 0, 4)
    print(f"   從 0 到 4 的路徑: {path}")
    print()
    
    print("4. 所有路徑:")
    paths = dfs_all_paths(graph, 0, 5)
    print(f"   從 0 到 5 的所有路徑: {paths}")
    print()
    
    print("5. 拓撲排序:")
    dag = {
        0: [1, 2],
        1: [3],
        2: [3],
        3: []
    }
    result = dfs_topological_sort(dag)
    print(f"   DAG: {dag}")
    print(f"   拓撲排序: {result}")
    print()
    
    print("6. 二元樹遍歷:")
    tree = TreeNode(1, 
                   TreeNode(2, TreeNode(4), TreeNode(5)),
                   TreeNode(3, TreeNode(6), TreeNode(7)))
    print(f"   前序: {dfs_binary_tree_preorder(tree)}")
    print(f"   中序: {dfs_binary_tree_inorder(tree)}")
    print(f"   後序: {dfs_binary_tree_postorder(tree)}")


if __name__ == "__main__":
    demo_dfs()
