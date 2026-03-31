"""
Church 編碼：用λ演算表示數據結構
展示如何用純函數表示數字、布爾值和列表
"""

from typing import Callable, Any
from functools import reduce

ChurchNum = Callable[[Callable[[Any], Any]], Callable[[Any], Any]]

def church_zero() -> ChurchNum:
    return lambda f: lambda x: x

def church_one() -> ChurchNum:
    return lambda f: lambda x: f(x)

def church_two() -> ChurchNum:
    return lambda f: lambda x: f(f(x))

def church_three() -> ChurchNum:
    return lambda f: lambda x: f(f(f(x)))

def church_n(n: int) -> ChurchNum:
    return lambda f: lambda x: reduce(lambda acc, _: f(acc), range(n), x)

def church_to_int(cn: ChurchNum) -> int:
    return cn(lambda x: x + 1)(0)

def int_to_church(n: int) -> ChurchNum:
    return church_n(n)

ChurchBool = Callable[[Any], Callable[[Any], Any]]

TRUE = lambda a: lambda b: a
FALSE = lambda a: lambda b: b

IF = lambda p: lambda a: lambda b: p(a)(b)

def church_not(c: ChurchBool) -> ChurchBool:
    return lambda a: lambda b: c(b)(a)

# 測試用的布林值
TRUE_BOOL = TRUE
FALSE_BOOL = FALSE

def not_bool(b):
    return FALSE_BOOL if b else TRUE_BOOL

def church_and(a: ChurchBool) -> Callable[[ChurchBool], ChurchBool]:
    return lambda q: a(q)(a)

def church_or(a: ChurchBool) -> Callable[[ChurchBool], ChurchBool]:
    return lambda q: a(a)(q)

ChurchPair = Callable[[Callable[[Any, Any], Any]], Any]

PAIR = lambda x: lambda y: lambda f: f(x)(y)
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)

ChurchList = Callable[[Callable[[Any], Callable[[Any], Any]], Any], Any]

NIL = PAIR(TRUE)(TRUE)
NULL = FIRST

def CONS(hd: Any) -> Callable[[ChurchList], ChurchList]:
    return lambda tl: PAIR(FALSE)(PAIR(hd)(tl))

def HEAD(xs: ChurchList) -> Any:
    return FIRST(SECOND(xs))

def TAIL(xs: ChurchList) -> ChurchList:
    return SECOND(SECOND(xs))

def list_to_church(items: list) -> ChurchList:
    result = NIL
    for item in reversed(items):
        result = CONS(item)(result)
    return result

def church_to_list(cl: ChurchList) -> list:
    def _to_list(lst):
        is_null = lst(TRUE)(FALSE)
        if is_null:
            return []
        return [HEAD(lst)] + _to_list(TAIL(lst))
    return _to_list(cl)

def demo():
    print("=== Church 編碼演示 ===\n")
    
    print("Church 數：")
    nums = [church_zero(), church_one(), church_two(), church_three(), church_n(5)]
    for n in nums:
        print(f"  {church_to_int(n)}", end=" ")
    print("\n")
    
    print("Church 數運算（2 + 3）：")
    add = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
    result = add(church_two())(church_three())
    print(f"  {church_to_int(result)}\n")
    
    print("Church 布林值：")
    print(f"  TRUE  = IF TRUE 'yes' 'no' = {IF(TRUE)('yes')('no')}")
    print(f"  FALSE = IF FALSE 'yes' 'no' = {IF(FALSE)('yes')('no')}")
    print(f"  NOT TRUE = {not_bool(True)}")
    print(f"  NOT FALSE = {not_bool(False)}")
    print(f"  AND TRUE FALSE = {IF(church_and(TRUE)(FALSE))('yes')('no')}")
    print()
    
    print("Church 列表 [1, 2, 3]：")
    cl = list_to_church([1, 2, 3])
    print(f"  轉換為 Python：{church_to_list(cl)}")
    print(f"  HEAD = {HEAD(cl)}")
    print(f"  HEAD(TAIL) = {HEAD(TAIL(cl))}")


if __name__ == "__main__":
    demo()
