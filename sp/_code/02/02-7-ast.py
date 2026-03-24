# 語法樹與抽象語法樹的比較

# 完整語法樹（Parse Tree）- 忠實反映文法結構
#          *
#         / \
#        +   4
#       / \
#      2   3

# 抽象語法樹（AST）- 只保留必要資訊
#      *
#     / \
#    +   4
#   / \
#  2   3

class ASTNode:
    def __init__(self, node_type, value=None):
        self.type = node_type
        self.value = value
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __repr__(self):
        if self.value:
            return f"({self.type}: {self.value})"
        return f"({self.type})"

# 將 Parser 輸出的元組轉換為 AST
def build_ast(parse_tree):
    """將簡化的 parse tree 轉換為 AST"""
    if not isinstance(parse_tree, tuple):
        return ASTNode('number', parse_tree)
    
    op, left, right = parse_tree
    node = ASTNode('binary_op', op)
    node.add_child(build_ast(left))
    node.add_child(build_ast(right))
    return node

def print_ast(node, indent=0):
    print("  " * indent + str(node))
    for child in node.children:
        print_ast(child, indent + 1)

# 測試
parse_tree = ('+', ('num', '2'), ('*', ('num', '3'), ('num', '4')))
ast = build_ast(parse_tree)
print_ast(ast)
# 輸出：
# (+)
#   (num: 2)
#   (*)
#     (num: 3)
#     (num: 4)