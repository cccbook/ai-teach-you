"""
查詢表範例 (Lookup Table Example)
===============================
使用查詢表（Lookup Table）技術來優化計算效能。
查詢表是一種預先計算並儲存結果的資料結構，可快速查詢而無需即時計算。
"""

from typing import Dict, List, Any
import math


class LookupTable:
    """查詢表類別 - 用於儲存和查詢預先計算的結果"""
    
    def __init__(self):
        self._table: Dict[Any, Any] = {}
    
    def insert(self, key: Any, value: Any) -> None:
        """插入鍵值對"""
        self._table[key] = value
    
    def lookup(self, key: Any, default: Any = None) -> Any:
        """查詢鍵對應的值"""
        return self._table.get(key, default)
    
    def contains(self, key: Any) -> bool:
        """檢查鍵是否存在"""
        return key in self._table


def factorial_lookup_table(n: int, max_n: int = 20) -> int:
    """
    使用查詢表計算階乘
    
    參數:
        n: 要計算的階乘數
        max_n: 查詢表的最大預先計算範圍
    
    返回:
        n! 的值
    """
    if n < 0:
        raise ValueError("階乘不能為負數")
    if n > max_n:
        return math.factorial(n)
    
    table = {
        0: 1, 1: 1, 2: 2, 3: 6, 4: 24, 5: 120,
        6: 720, 7: 5040, 8: 40320, 9: 362880,
        10: 3628800, 11: 39916800, 12: 479001600,
        13: 6227020800, 14: 87178291200, 15: 1307674368000,
        16: 20922789888000, 17: 355687428096000,
        18: 6402373705728000, 19: 121645100408832000,
        20: 2432902008176640000
    }
    
    return table[n]


def trig_lookup_table(angle_degrees: float, precision: float = 1.0) -> float:
    """
    使用查詢表計算正弦值
    
    參數:
        angle_degrees: 角度（度）
        precision: 精度（度），查詢表的離散化程度
    
    返回:
        sin(angle) 的近似值
    """
    angle = angle_degrees % 360
    if angle < 0:
        angle += 360
    
    table = {}
    for deg in range(0, 360, int(precision)):
        table[deg] = math.sin(math.radians(deg))
    
    nearest = int(round(angle / precision) * precision)
    return table.get(nearest, math.sin(math.radians(angle)))


def days_in_month_lookup(year: int, month: int) -> int:
    """
    使用查詢表取得每月天數
    
    參數:
        year: 年份
        month: 月份（1-12）
    
    返回:
        該月的天數
    """
    days_table = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    
    if month == 2 and ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
        return 29
    
    return days_table[month]


def color_conversion_lookup() -> Dict[str, Dict[str, float]]:
    """
    顏色轉換查詢表
    RGB 到 HSV 的預先計算轉換值
    """
    table = {}
    
    for r in range(0, 256, 16):
        for g in range(0, 256, 16):
            for b in range(0, 256, 16):
                r_norm, g_norm, b_norm = r / 255, g / 255, b / 255
                
                max_val = max(r_norm, g_norm, b_norm)
                min_val = min(r_norm, g_norm, b_norm)
                diff = max_val - min_val
                
                if diff == 0:
                    h = 0
                elif max_val == r_norm:
                    h = (60 * ((g_norm - b_norm) / diff) + 360) % 360
                elif max_val == g_norm:
                    h = (60 * ((b_norm - r_norm) / diff) + 120) % 360
                else:
                    h = (60 * ((r_norm - g_norm) / diff) + 240) % 360
                
                s = 0 if max_val == 0 else (diff / max_val) * 100
                v = max_val * 100
                
                key = f"{r},{g},{b}"
                table[key] = {"h": h, "s": s, "v": v}
    
    return table


class CacheLookupTable:
    """帶有快取功能的查詢表"""
    
    def __init__(self, size: int = 1000):
        self._table: Dict[int, int] = {}
        self._size = size
        self._hits = 0
        self._misses = 0
    
    def get(self, key: int) -> int:
        """取得值，若不存在則返回 None"""
        if key in self._table:
            self._hits += 1
            return self._table[key]
        self._misses += 1
        return None
    
    def put(self, key: int, value: int) -> None:
        """插入值，若已滿則清除最舊的項目"""
        if len(self._table) >= self._size:
            first_key = next(iter(self._table))
            del self._table[first_key]
        self._table[key] = value
    
    def compute(self, key: int, compute_func) -> int:
        """
        計算並快取結果
        
        參數:
            key: 鍵
            compute_func: 計算函數
        """
        result = self.get(key)
        if result is None:
            result = compute_func(key)
            self.put(key, result)
        return result
    
    def stats(self) -> Dict[str, int]:
        """返回快取統計資訊"""
        return {
            "size": len(self._table),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self._hits / (self._hits + self._misses) if self._hits + self._misses > 0 else 0
        }


def demo_lookup_table():
    """演示查詢表的使用"""
    print("=== 查詢表範例演示 ===")
    print()
    
    print("1. 階乘查詢表:")
    for n in [5, 10, 15, 20]:
        result = factorial_lookup_table(n)
        print(f"   {n}! = {result}")
    print()
    
    print("2. 三角函數查詢表:")
    for angle in [0, 30, 45, 60, 90]:
        result = trig_lookup_table(angle)
        print(f"   sin({angle}°) ≈ {result:.4f}")
    print()
    
    print("3. 月份天數查詢表:")
    for month in [1, 2, 12]:
        days = days_in_month_lookup(2024, month)
        print(f"   2024年{month}月 = {days}天")
    print()
    
    print("4. 快取查詢表:")
    cache = CacheLookupTable(size=100)
    for i in range(200):
        cache.compute(i, lambda x: x ** 2)
    print(f"   快取統計: {cache.stats()}")


if __name__ == "__main__":
    demo_lookup_table()
