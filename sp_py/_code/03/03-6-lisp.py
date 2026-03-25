"""簡化的 LISP 直譯器"""

def eval_expr(expr, env):
    if isinstance(expr, str):  # 符號
        return env.get(expr, expr)
    if isinstance(expr, (int, float)):  # 數字
        return expr
    
    # 表達式 (op args...)
    op = expr[0]
    args = expr[1:]
    
    if op == 'quote':
        return args[0]
    
    if op == 'if':
        condition = eval_expr(args[0], env)
        if condition:
            return eval_expr(args[1], env)
        return eval_expr(args[2], env) if len(args) > 2 else None
    
    if op == 'define':
        env[args[0]] = eval_expr(args[1], env)
        return None
    
    if op == 'lambda':
        return {'type': 'function', 'params': args[0], 'body': args[1], 'env': env.copy()}
    
    # 函數呼叫
    func = eval_expr(op, env)
    if isinstance(func, dict) and func['type'] == 'function':
        new_env = func['env'].copy()
        for param, arg in zip(func['params'], args):
            new_env[param] = eval_expr(arg, env)
        return eval_expr(func['body'], new_env)
    
    # 內建函數
    evaled_args = [eval_expr(arg, env) for arg in args]
    if op == '+': return sum(evaled_args)
    if op == '-': return evaled_args[0] - sum(evaled_args[1:])
    if op == '*': return eval_expr(args[0], env) * eval_expr(args[1], env)
    if op == '=': return evaled_args[0] == evaled_args[1]
    if op == 'car': return evaled_args[0][0]
    if op == 'cdr': return evaled_args[0][1:]
    if op == 'cons': return [evaled_args[0]] + evaled_args[1]

# 測試
env = {}
print(eval_expr(['+', 2, 3], env))  # 5
print(eval_expr(['if', ['=', 1, 1], 'yes', 'no'], env))  # yes
print(eval_expr(['define', 'x', 10], env))
print(eval_expr('x', env))  # 10

# 遞迴範例：階乘
factorial = ['define', 'fact', ['lambda', ['n'],
    ['if', ['=', 'n', 1], 1, ['*', 'n', ['fact', ['-', 'n', 1]]]]]]
eval_expr(factorial, env)
print(eval_expr(['fact', 5], env))  # 120
