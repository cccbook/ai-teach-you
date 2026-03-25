"""
符號表實作 - 追蹤變數、函數的資訊
"""

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # 作用域堆疊
    
    def enter_scope(self):
        """進入新作用域"""
        self.scopes.append({})
    
    def exit_scope(self):
        """離開作用域"""
        self.scopes.pop()
    
    def define(self, name, symbol):
        """定義符號"""
        self.scopes[-1][name] = symbol
    
    def lookup(self, name):
        """查詢符號（由內而外）"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def lookup_current(self, name):
        """只在當前作用域查詢"""
        return self.scopes[-1].get(name)

# 測試符號表
symbols = SymbolTable()

# 全域作用域
symbols.define('x', {'type': 'int', 'kind': 'variable', 'address': 0})
symbols.define('main', {'type': 'function', 'kind': 'function', 'params': []})

# 進入區塊作用域
symbols.enter_scope()
symbols.define('x', {'type': 'int', 'kind': 'parameter', 'address': 8})
symbols.define('y', {'type': 'double', 'kind': 'variable', 'address': 16})

print("lookup('x'):", symbols.lookup('x'))  # 找到區塊作用域的 x
print("lookup('y'):", symbols.lookup('y'))
print("lookup('main'):", symbols.lookup('main'))

symbols.exit_scope()
print("離開區塊後 lookup('x'):", symbols.lookup('x'))  # 回到全域作用域的 x
