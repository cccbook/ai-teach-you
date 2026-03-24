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
