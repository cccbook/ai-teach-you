# Python - 函數式風格
from functools import reduce

result = reduce(lambda x, y: x + y, range(1, 11))
print(result)  # 輸出 55
