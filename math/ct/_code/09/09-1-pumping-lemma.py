"""
泵引理驗證工具
"""

def pumping_lemma_regular(w: str, n: int = 10) -> bool:
    """
    對給定的字串，嘗試找到泵引理所要求的分解
    """
    for split in range(1, min(n, len(w) // 2) + 1):
        x = w[:split]
        y = w[split:split+split]
        z = w[split*2:]
        
        if len(x) + len(y) <= n:
            print(f"候選分解：x={x!r}, y={y!r}, z={z!r}")
            print(f"  |xy| = {len(x)+len(y)} <= {n}")
            return True
    
    return False


def prove_not_regular():
    print("=== 證明 L = {0ⁿ1ⁿ | n >= 0} 不是正規語言 ===\n")
    
    print("假設 L 是正規語言，設泵長度為 n")
    print("取 w = 0ⁿ1ⁿ\n")
    
    print("w 可以分解為：")
    print("  x = 0ᵃ")
    print("  y = 0ᵇ (b >= 1)")
    print("  z = 0ⁿ⁻ᵃ⁻ᵇ 1ⁿ")
    print(f"\n其中 |xy| = a+b <= n\n")
    
    print(f"泵送 y：xy²z = 0ⁿ⁺ᵇ1ⁿ")
    print(f"但 n+b ≠ n，所以 xy²z ∉ L")
    print(f"矛盾！因此 L 不是正規語言")


def prove_not_context_free():
    print("\n=== 證明 L = {0ⁿ1ⁿ0ⁿ1ⁿ} 不是上下文無關語言 ===\n")
    
    print("假設 L 是上下文無關的")
    print("使用 Ogden's Lemma：存在泵長度 p")
    print("取 w = 0ᵖ1ᵖ0ᵖ1ᵖ\n")
    
    print("標記所有 0 為「標記」位置")
    print("根據 Ogden's Lemma，存在分解 w = uvxyz")
    print("泵送 v 和 y")
    print("結果將打破兩組 0ⁿ1ⁿ 的對稱性")
    print("矛盾！")


if __name__ == "__main__":
    prove_not_regular()
    print()
    prove_not_context_free()
