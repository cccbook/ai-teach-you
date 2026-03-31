"""
貪心演算法範例 (Greedy Algorithm Examples)
==========================================
展示各種貪心演算法（Greedy Algorithm）的實作方式。
貪心演算法在每一步選擇當前最佳解，希望最終得到全域最佳解。
"""

from typing import List, Tuple, Any, Callable, Dict
import heapq


def greedy_coin_change(amount: int, coins: List[int]) -> List[int]:
    """
    貪心找零錢問題
    
    參數:
        amount: 金額
        coins: 硬幣面額（需為已排序的遞減序列）
    
    返回:
        使用的硬幣列表
    """
    result = []
    remaining = amount
    
    for coin in sorted(coins, reverse=True):
        count = remaining // coin
        result.extend([coin] * count)
        remaining -= coin * count
    
    return result


def greedy_activity_selection(
    activities: List[Tuple[int, int]]
) -> List[int]:
    """
    貪心活動選擇問題
    
    參數:
        activities: 活動列表 (start_time, end_time)
    
    返回:
        選擇的活動索引列表
    """
    sorted_activities = sorted(activities, key=lambda x: x[1])
    
    selected = [0]
    last_end_time = sorted_activities[0][1]
    
    for i in range(1, len(sorted_activities)):
        if sorted_activities[i][0] >= last_end_time:
            selected.append(i)
            last_end_time = sorted_activities[i][1]
    
    return selected


def greedy_huffman_coding(text: str) -> Dict[str, str]:
    """
    霍夫曼編碼
    
    參數:
        text: 輸入文字
    
    返回:
        字元到編碼的映射
    """
    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1
    
    heap = [[weight, [char, ""]] for char, weight in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        for pair in left[1:]:
            pair[1] = "0" + pair[1]
        for pair in right[1:]:
            pair[1] = "1" + pair[1]
        
        heapq.heappush(heap, [left[0] + right[0]] + left[1:] + right[1:])
    
    codes = {}
    for pair in heap[0][1:]:
        codes[pair[0]] = pair[1]
    
    return codes


def greedy_fractional_knapsack(
    weights: List[float],
    values: List[float],
    capacity: float
) -> Tuple[float, List[float]]:
    """
    貪心分數背包問題
    
    參數:
        weights: 物品重量列表
        values: 物品價值列表
        capacity: 背包容量
    
    返回:
        (最大價值, 各物品取得比例)
    """
    n = len(weights)
    
    ratios = [(values[i] / weights[i], i) for i in range(n)]
    ratios.sort(reverse=True, key=lambda x: x[0])
    
    total_value = 0.0
    fractions = [0.0] * n
    
    for ratio, i in ratios:
        if capacity >= weights[i]:
            fractions[i] = 1.0
            total_value += values[i]
            capacity -= weights[i]
        else:
            fractions[i] = capacity / weights[i]
            total_value += values[i] * fractions[i]
            break
    
    return total_value, fractions


def greedy_minimum_spanning_tree(
    edges: List[Tuple[int, int, float]]
) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Prim 演算法求最小生成樹
    
    參數:
        edges: 邊列表 (u, v, weight)
    
    返回:
        (最小權重和, 邊列表)
    """
    if not edges:
        return 0, []
    
    vertices = set()
    for u, v, _ in edges:
        vertices.add(u)
        vertices.add(v)
    
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    mst_edges = []
    visited = {min(vertices)}
    min_heap = [(w, u, v) for u, v, w in adj[min(vertices)]]
    heapq.heapify(min_heap)
    
    total_weight = 0
    
    while min_heap and len(visited) < len(vertices):
        weight, u, v = heapq.heappop(min_heap)
        
        if v in visited:
            continue
        
        visited.add(v)
        mst_edges.append((u, v, weight))
        total_weight += weight
        
        for neighbor, w in adj[v]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (w, v, neighbor))
    
    return total_weight, mst_edges


def greedy_dijkstra(
    graph: Dict[int, List[Tuple[int, float]]],
    source: int
) -> Dict[int, float]:
    """
    Dijkstra 最短路徑演算法
    
    參數:
        graph: 圖的鄰接表表示 {節點: [(鄰居, 權重), ...]}
        source: 起始節點
    
    返回:
        從 source 到各節點的最短距離
    """
    distances = {source: 0}
    heap = [(0, source)]
    visited = set()
    
    while heap:
        dist, node = heapq.heappop(heap)
        
        if node in visited:
            continue
        
        visited.add(node)
        
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                new_dist = dist + weight
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor))
    
    return distances


def greedy_job_sequencing(
    jobs: List[Tuple[str, int, int]]
) -> List[str]:
    """
    貪心工作排序
    
    參數:
        jobs: 工作列表 (name, deadline, profit)
    
    返回:
        選擇的工作名稱列表
    """
    sorted_jobs = sorted(jobs, key=lambda x: x[2], reverse=True)
    
    max_deadline = max(job[1] for job in jobs)
    time_slots = [False] * (max_deadline + 1)
    
    selected = []
    
    for name, deadline, profit in sorted_jobs:
        for t in range(deadline, 0, -1):
            if not time_slots[t]:
                time_slots[t] = True
                selected.append(name)
                break
    
    return selected


def greedy_set_cover(
    universe: List[Any],
    sets: Dict[str, List[Any]]
) -> Tuple[List[str], List[Any]]:
    """
    集合覆蓋問題（近似演算法）
    
    參數:
        universe: 宇宙集合
        sets: 集合字典
    
    返回:
        (選擇的集合鍵列表, 覆蓋的元素)
    """
    covered = set()
    selected = []
    
    while covered != set(universe):
        best_set = None
        best_coverage = set()
        
        for key, elements in sets.items():
            if key in selected:
                continue
            
            new_coverage = set(elements) - covered
            if len(new_coverage) > len(best_coverage):
                best_set = key
                best_coverage = new_coverage
        
        if best_set is None:
            break
        
        selected.append(best_set)
        covered.update(best_coverage)
    
    return selected, list(covered)


def greedy_fractional_change(
    amount: int,
    coins: List[int]
) -> float:
    """
    貪心分數找零問題（最佳比率）
    
    參數:
        amount: 金額
        coins: 硬幣面額
    
    返回:
        最小硬幣數量
    """
    sorted_coins = sorted(coins, reverse=True)
    
    count = 0
    remaining = amount
    
    for coin in sorted_coins:
        count += remaining // coin
        remaining = remaining % coin
    
    return count


def demo_greedy():
    """演示貪心演算法"""
    print("=== 貪心演算法範例演示 ===")
    print()
    
    print("1. 找零錢問題:")
    coins = [25, 10, 5, 1]
    result = greedy_coin_change(63, coins)
    print(f"   找63元: 使用 {result}")
    print(f"   硬幣數: {len(result)}")
    print()
    
    print("2. 活動選擇:")
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)]
    selected = greedy_activity_selection(activities)
    print(f"   活動: {activities}")
    print(f"   選擇索引: {selected}")
    print()
    
    print("3. 分數背包:")
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    total, fractions = greedy_fractional_knapsack(weights, values, capacity)
    print(f"   重量: {weights}, 價值: {values}, 容量: {capacity}")
    print(f"   最大價值: {total:.2f}")
    print(f"   取得比例: {fractions}")
    print()
    
    print("4. 工作排序:")
    jobs = [("A", 2, 100), ("B", 1, 19), ("C", 2, 27), ("D", 1, 25), ("E", 3, 15)]
    selected = greedy_job_sequencing(jobs)
    print(f"   工作: {jobs}")
    print(f"   選擇: {selected}")
    print()
    
    print("5. Dijkstra 最短路徑:")
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(0, 4), (2, 2), (3, 5)],
        2: [(0, 1), (1, 2), (3, 8)],
        3: [(1, 5), (2, 8)]
    }
    distances = greedy_dijkstra(graph, 0)
    print(f"   最短距離: {distances}")


if __name__ == "__main__":
    demo_greedy()
