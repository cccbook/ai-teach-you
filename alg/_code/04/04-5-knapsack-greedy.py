"""
分數背包問題（貪心）範例 (Fractional Knapsack - Greedy)
=====================================================
展示分數背包問題（Fractional Knapsack）的貪心解法。
在分數背包問題中，我們可以取物品的一部分，目標是最大化總價值。
"""

from typing import List, Tuple, Dict, Any
import heapq


def fractional_knapsack_greedy(
    weights: List[float],
    values: List[float],
    capacity: float
) -> Tuple[float, List[float]]:
    """
    貪心分數背包問題解法
    
    參數:
        weights: 物品重量列表
        values: 物品價值列表
        capacity: 背包容量
    
    返回:
        (最大總價值, 各物品取得比例)
    """
    n = len(weights)
    
    items = [(values[i] / weights[i], weights[i], values[i], i) for i in range(n)]
    items.sort(reverse=True)
    
    total_value = 0.0
    fractions = [0.0] * n
    
    for ratio, weight, value, i in items:
        if capacity >= weight:
            fractions[i] = 1.0
            total_value += value
            capacity -= weight
        else:
            fractions[i] = capacity / weight
            total_value += value * fractions[i]
            capacity = 0
            break
    
    return total_value, fractions


def fractional_knapsack_with_items(
    items: List[Tuple[str, float, float]],
    capacity: float
) -> Dict[str, Any]:
    """
    帶有物品名稱的分數背包
    
    參數:
        items: 物品列表 (名稱, 重量, 價值)
        capacity: 背包容量
    
    返回:
        結果字典
    """
    item_ratios = []
    for name, weight, value in items:
        if weight > 0:
            ratio = value / weight
            item_ratios.append((ratio, weight, value, name))
    
    item_ratios.sort(reverse=True, key=lambda x: x[0])
    
    total_value = 0.0
    selected = []
    remaining_capacity = capacity
    
    for ratio, weight, value, name in item_ratios:
        if remaining_capacity <= 0:
            break
        
        if weight <= remaining_capacity:
            fraction = 1.0
            selected.append({
                "name": name,
                "fraction": fraction,
                "weight": weight,
                "value": value
            })
            total_value += value
            remaining_capacity -= weight
        else:
            fraction = remaining_capacity / weight
            selected.append({
                "name": name,
                "fraction": fraction,
                "weight": remaining_capacity,
                "value": value * fraction
            })
            total_value += value * fraction
            remaining_capacity = 0
    
    return {
        "total_value": total_value,
        "selected_items": selected,
        "remaining_capacity": remaining_capacity
    }


def fractional_knapsack_heap(
    weights: List[float],
    values: List[float],
    capacity: float
) -> Tuple[float, List[float]]:
    """
    使用堆積的分數背包
    
    參數:
        weights: 重量列表
        values: 價值列表
        capacity: 容量
    
    返回:
        (最大價值, 取得比例)
    """
    n = len(weights)
    
    heap = [(-values[i] / weights[i], i) for i in range(n) if weights[i] > 0]
    heapq.heapify(heap)
    
    total_value = 0.0
    fractions = [0.0] * n
    remaining = capacity
    
    while heap and remaining > 0:
        ratio_neg, i = heapq.heappop(heap)
        ratio = -ratio_neg
        
        if remaining >= weights[i]:
            fractions[i] = 1.0
            total_value += values[i]
            remaining -= weights[i]
        else:
            fractions[i] = remaining / weights[i]
            total_value += values[i] * fractions[i]
            remaining = 0
    
    return total_value, fractions


def fractional_knapsack_iterative(
    weights: List[float],
    values: List[float],
    capacity: float
) -> Dict[str, Any]:
    """
    分數背包問題 - 迭代版本
    
    參數:
        weights: 重量列表
        values: 價值列表
        capacity: 容量
    
    返回:
        詳細結果
    """
    n = len(weights)
    
    item_data = []
    for i in range(n):
        if weights[i] > 0:
            item_data.append({
                "index": i,
                "weight": weights[i],
                "value": values[i],
                "ratio": values[i] / weights[i]
            })
    
    item_data.sort(key=lambda x: x["ratio"], reverse=True)
    
    result = {
        "total_value": 0.0,
        "selected": [],
        "total_weight": 0.0
    }
    
    remaining = capacity
    
    for item in item_data:
        if remaining <= 0:
            break
        
        if item["weight"] <= remaining:
            fraction = 1.0
            result["selected"].append({
                "index": item["index"],
                "fraction": fraction,
                "value_taken": item["value"],
                "weight_taken": item["weight"]
            })
            result["total_value"] += item["value"]
            result["total_weight"] += item["weight"]
            remaining -= item["weight"]
        else:
            fraction = remaining / item["weight"]
            value_taken = item["value"] * fraction
            result["selected"].append({
                "index": item["index"],
                "fraction": fraction,
                "value_taken": value_taken,
                "weight_taken": remaining
            })
            result["total_value"] += value_taken
            result["total_weight"] += remaining
            remaining = 0
    
    return result


def fractional_knapsack_multiple(
    weights: List[float],
    values: List[float],
    capacities: List[float]
) -> List[Tuple[float, List[float]]]:
    """
    多背包分數背包問題
    
    參數:
        weights: 重量列表
        values: 價值列表
        capacities: 各背包容量
    
    返回:
        各背包的結果列表
    """
    results = []
    
    sorted_items = sorted(
        range(len(weights)),
        key=lambda i: values[i] / weights[i] if weights[i] > 0 else 0,
        reverse=True
    )
    
    for capacity in capacities:
        fractions = [0.0] * len(weights)
        total = 0.0
        remaining = capacity
        
        for i in sorted_items:
            if remaining <= 0:
                break
            if weights[i] <= remaining:
                fractions[i] = 1.0
                total += values[i]
                remaining -= weights[i]
            else:
                fractions[i] = remaining / weights[i]
                total += values[i] * fractions[i]
                remaining = 0
        
        results.append((total, fractions))
    
    return results


class FractionalKnapsack:
    """分數背包求解器類別"""
    
    def __init__(self, weights: List[float], values: List[float]):
        self.weights = weights
        self.values = values
        self.n = len(weights)
    
    def solve(self, capacity: float) -> Dict[str, Any]:
        """求解"""
        return fractional_knapsack_iterative(self.weights, self.values, capacity)
    
    def get_value_density(self) -> List[Tuple[float, int]]:
        """取得價值密度排序"""
        densities = []
        for i in range(self.n):
            if self.weights[i] > 0:
                densities.append((self.values[i] / self.weights[i], i))
        
        return sorted(densities, reverse=True)


def demo_fractional_knapsack():
    """演示分數背包"""
    print("=== 分數背包問題（貪心）範例演示 ===")
    print()
    
    print("1. 基本分數背包:")
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    
    total, fractions = fractional_knapsack_greedy(weights, values, capacity)
    print(f"   物品: weights={weights}, values={values}")
    print(f"   容量: {capacity}")
    print(f"   最大價值: {total}")
    print(f"   取得比例: {fractions}")
    print()
    
    print("2. 帶物品名稱:")
    items = [
        ("黃金", 10, 60),
        ("白銀", 20, 100),
        ("青銅", 30, 120)
    ]
    capacity = 50
    result = fractional_knapsack_with_items(items, capacity)
    print(f"   物品: {items}")
    print(f"   容量: {capacity}")
    print(f"   總價值: {result['total_value']}")
    print(f"   選擇:")
    for item in result['selected_items']:
        print(f"     - {item['name']}: {item['fraction']*100:.1f}%")
    print()
    
    print("3. 迭代版本:")
    result = fractional_knapsack_iterative(weights, values, capacity)
    print(f"   總價值: {result['total_value']:.2f}")
    print(f"   總重量: {result['total_weight']:.2f}")
    print()
    
    print("4. 多背包:")
    capacities = [30, 40, 50]
    results = fractional_knapsack_multiple(weights, values, capacities)
    for i, (total, fractions) in enumerate(results):
        print(f"   背包 {i+1} (容量{capacities[i]}): 價值={total:.2f}")


if __name__ == "__main__":
    demo_fractional_knapsack()
