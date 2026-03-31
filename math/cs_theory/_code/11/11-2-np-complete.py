"""
經典NP-完全問題實現
"""

from typing import List, Set, Tuple, Optional

class ThreeSAT:
    def __init__(self):
        self.variables = set()
        self.clauses = []
    
    def add_clause(self, x: int, y: int, z: int):
        self.variables.add(abs(x))
        self.variables.add(abs(y))
        self.variables.add(abs(z))
        self.clauses.append((x, y, z))
    
    def is_satisfied(self, assignment: dict) -> bool:
        for x, y, z in self.clauses:
            val = (assignment.get(x, False) or 
                   assignment.get(y, False) or 
                   assignment.get(z, False))
            if not val:
                return False
        return True
    
    def solve_greedy(self) -> Optional[dict]:
        assignment = {}
        
        for var in range(1, max(self.variables) + 1):
            assignment[var] = True
        
        return assignment if self.is_satisfied(assignment) else None


class TravelingSalesman:
    def __init__(self, n: int):
        self.n = n
        self.distances = [[0 if i == j else float('inf') 
                         for j in range(n)] for i in range(n)]
    
    def add_edge(self, i: int, j: int, weight: float):
        self.distances[i][j] = weight
        self.distances[j][i] = weight
    
    def nearest_neighbor(self, start: int = 0) -> Tuple[float, List[int]]:
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
        
        cost += self.distances[current][start]
        path.append(start)
        
        return cost, path


def demo_np_complete():
    print("=== NP-完全問題演示 ===\n")
    
    # 3-SAT
    print("1. 3-SAT 問題：")
    sat = ThreeSAT()
    sat.add_clause(1, 2, 3)
    sat.add_clause(-1, 2, -3)
    sat.add_clause(1, -2, 3)
    
    result = sat.solve_greedy()
    if result:
        print(f"   候選解：x₁={result[1]}, x₂={result[2]}, x₃={result[3]}")
        print(f"   滿足所有子句：{sat.is_satisfied(result)}")
    
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
    
    cost, path = tsp.nearest_neighbor(0)
    print(f"   最近鄰居：路徑 {path}，成本 {cost}")


if __name__ == "__main__":
    demo_np_complete()
