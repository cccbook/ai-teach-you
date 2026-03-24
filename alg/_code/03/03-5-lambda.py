"""
Lambda 運算範例 (Lambda Calculus Examples)
==========================================
展示 Lambda 運算（Lambda Calculus）的基本概念與應用。
Lambda 運算是函數式程式設計的理論基礎，包含變數、抽象化和應用三個核心概念。
"""

from typing import Callable, Any, List, Dict
import functools


TRUE = lambda x: lambda y: x
FALSE = lambda x: lambda y: y


defchurch_boolean():
    """Church 布林值"""
    return {
        "TRUE": TRUE,
        "FALSE": FALSE,
        "NOT": lambda b: b(FALSE)(TRUE),
        "AND": lambda a: lambda b: a(b)(FALSE),
        "OR": lambda a: lambda b: a(TRUE)(b),
        "XOR": lambda a: lambda b: a(b)(TRUE)(b)(FALSE),
        "IF": lambda b: lambda then_: lambda else_: b(then_)(else_),
    }


def church_natural():
    """Church 自然數"""
    
    zero = lambda f: lambda x: x
    one = lambda f: lambda x: f(x)
    two = lambda f: lambda x: f(f(x))
    three = lambda f: lambda x: f(f(f(x)))
    four = lambda f: lambda x: f(f(f(f(x))))
    five = lambda f: lambda x: f(f(f(f(f(x)))))
    
    def succ(n):
        return lambda f: lambda x: f(n(f)(x))
    
    def plus(m, n):
        return lambda f: lambda x: m(f)(n(f)(x))
    
    def mult(m, n):
        return lambda f: m(n(f))
    
    def power(m, n):
        return n(m)
    
    def pred(n):
        return lambda f: lambda x: n(lambda g: lambda h: h(g(f)))(lambda _: x)(lambda u: u)
    
    def subtract(m, n):
        return n(pred)(m)
    
    def is_zero(n):
        return n(lambda _: FALSE)(TRUE)
    
    def less_or_equal(m, n):
        return is_zero(subtract(m, n))
    
    return {
        "zero": zero,
        "one": one,
        "two": two,
        "three": three,
        "four": four,
        "five": five,
        "succ": succ,
        "plus": plus,
        "mult": mult,
        "power": power,
        "pred": pred,
        "subtract": subtract,
        "is_zero": is_zero,
        "less_or_equal": less_or_equal,
    }


def church_pair():
    """Church 序對"""
    
    cons = lambda a: lambda b: lambda f: f(a)(b)
    car = lambda p: p(TRUE)
    cdr = lambda p: p(FALSE)
    
    return {"cons": cons, "car": car, "cdr": cdr}


def church_list():
    """Church 列表"""
    
    nil = FALSE
    
    def isnil(p):
        return p(lambda a: lambda b: FALSE)
    
    def cons(x, xs):
        return lambda f: f(x)(xs)
    
    def head(xs):
        return xs(TRUE)
    
    def tail(xs):
        return xs(FALSE)
    
    return {
        "nil": nil,
        "isnil": isnil,
        "cons": cons,
        "head": head,
        "tail": tail,
    }


def church_natural_to_int(cn):
    """將 Church 自然數轉換為 Python 整數"""
    return cn(lambda x: x + 1)(0)


def church_int_to_natural(n: int) -> Callable:
    """將 Python 整數轉換為 Church 自然數"""
    return lambda f: lambda x: functools.reduce(lambda acc, _: f(acc), range(n), x)


def church_boolean_to_python(cb: Callable) -> bool:
    """將 Church 布林值轉換為 Python 布林值"""
    return cb(True)(False)


def lambda_calculus_examples():
    """Lambda 運算範例"""
    
    identity = lambda x: x
    
    constant = lambda x: lambda y: x
    
    apply = lambda f: lambda x: f(x)
    
    compose = lambda f: lambda g: lambda x: f(g(x))
    
    swap = lambda f: lambda y: lambda x: f(x)(y)
    
    return {
        "identity": identity,
        "constant": constant,
        "apply": apply,
        "compose": compose,
        "swap": swap,
    }


def y_combinator():
    """Y  combinator（不動點 combinator）"""
    
    Y = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))
    
    factorial = Y(lambda f: lambda n: 1 if n == 0 else n * f(n - 1))
    
    fibonacci = Y(lambda f: lambda n: n if n <= 1 else f(n - 1) + f(n - 2))
    
    return {"Y": Y, "factorial": factorial, "fibonacci": fibonacci}


def z_combinator():
    """Z  combinator（用於嚴格語言）"""
    
    Z = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))
    
    factorial = Z(lambda f: lambda n: 1 if n == 0 else n * f(n - 1))
    
    return {"Z": Z, "factorial": factorial}


def church_numerals():
    """Church 數字與運算"""
    
    cb = church_boolean()
    
    zero = lambda f: lambda x: x
    one = lambda f: lambda x: f(x)
    
    def add1(n):
        return lambda f: lambda x: f(n(f)(x))
    
    def to_church(n):
        if n == 0:
            return zero
        return add1(to_church(n - 1))
    
    def from_church(cn):
        return cn(lambda x: x + 1)(0)
    
    return {"to_church": to_church, "from_church": from_church}


def demo_lambda():
    """演示 Lambda 運算"""
    print("=== Lambda 運算範例演示 ===")
    print()
    
    print("1. Church 布林值:")
    cb = church_boolean()
    print(f"   TRUE = {cb['TRUE'](1)(2)}")
    print(f"   FALSE = {cb['FALSE'](1)(2)}")
    print(f"   NOT TRUE = {cb['NOT'](cb['TRUE'])(1)(2)}")
    print(f"   AND TRUE FALSE = {cb['AND'](cb['TRUE'])(cb['FALSE'])(1)(2)}")
    print(f"   OR TRUE FALSE = {cb['OR'](cb['TRUE'])(cb['FALSE'])(1)(2)}")
    print()
    
    print("2. Church 自然數:")
    cn = church_natural()
    two = cn["two"]
    three = cn["three"]
    print(f"   2 = {church_natural_to_int(two)}")
    print(f"   3 = {church_natural_to_int(three)}")
    print(f"   succ(2) = {church_natural_to_int(cn['succ'](two))}")
    print(f"   plus(2, 3) = {church_natural_to_int(cn['plus'](two)(three))}")
    print(f"   mult(2, 3) = {church_natural_to_int(cn['mult'](two)(three))}")
    print(f"   power(2, 3) = {church_natural_to_int(cn['power'](two)(three))}")
    print()
    
    print("3. Church 序對:")
    cp = church_pair()
    pair = cp["cons"](1)(2)
    print(f"   cons(1, 2)")
    print(f"   car = {cp['car'](pair)}")
    print(f"   cdr = {cp['cdr'](pair)}")
    print()
    
    print("4. Y Combinator:")
    yc = y_combinator()
    print(f"   factorial(5) = {yc['factorial'](5)}")
    print(f"   fibonacci(10) = {yc['fibonacci'](10)}")
    print()
    
    print("5. Lambda 運算:")
    lc = lambda_calculus_examples()
    print(f"   identity(5) = {lc['identity'](5)}")
    print(f"   constant(5)(3) = {lc['constant'](5)(3)}")
    print(f"   compose(lambda x: x*2)(lambda x: x+1)(3) = {lc['compose'](lambda x: x*2)(lambda x: x+1)(3)}")


if __name__ == "__main__":
    demo_lambda()
