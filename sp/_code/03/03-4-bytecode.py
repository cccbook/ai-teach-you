import dis

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# 查看 Python 的位元組碼
dis.dis(factorial)
