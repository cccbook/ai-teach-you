"""
P vs NP 問題演示
"""

def demonstrate_complexity_growth():
    print("=== 複雜度增長演示 ===\n")
    
    print("時間複雜度比較（步驟數）：")
    print("-" * 60)
    print(f"{'n':<8} {'n²':<15} {'2ⁿ':<20}")
    print("-" * 60)
    
    for n in [5, 10, 15, 20, 25]:
        n_sq = n ** 2
        two_pow_n = 2 ** n
        
        n_sq_str = f"{n_sq:,}"
        two_pow_str = f"{two_pow_n:,}" if n <= 25 else ">10²⁵"
        
        print(f"{n:<8} {n_sq_str:<15} {two_pow_str:<20}")


def classify_problems():
    print("\n=== P vs NP 問題分類 ===\n")
    
    print("P（多項式時間可解）：")
    p_problems = [
        "排序（O(n log n)）",
        "最短路徑（Dijkstra，O(m log n)）",
        "最大公約數（歐幾里得，O(log n)）",
        "連通性檢查（DFS/BFS，O(n+m)）",
    ]
    for p in p_problems:
        print(f"  • {p}")
    
    print("\nNP（多項式時間可驗證）：")
    np_problems = [
        "哈密頓路徑",
        "SAT（布爾可滿足性）",
        "旅行商問題",
        "子集和問題",
    ]
    for p in np_problems:
        print(f"  • {p}")


if __name__ == "__main__":
    demonstrate_complexity_growth()
    classify_problems()
