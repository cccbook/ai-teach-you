#!/bin/bash
# 測試腳本 - 第5章：λ演算Python實作

cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "=== 第5章測試 ==="
echo ""

echo "1. 測試AST..."
python3 -c "
from lambda_interpreter.ast import Var, Abs, App
identity = Abs('x', Var('x'))
print(f'恆等函數：{identity}')
app = App(identity, Var('y'))
print(f'應用 (λx. x) y：{app}')
result = app.substitute('y', Var('z'))
print(f'替換後：{result}')
"
echo ""

echo "2. 測試詞法分析器..."
python3 -c "
from lambda_interpreter.lexer import Lexer
text = 'λx. x'
lexer = Lexer(text)
tokens = lexer.tokenize()
print(f'輸入：{text}')
print(f'Token：{[(t.type.name, t.value) for t in tokens]}')
"
echo ""

echo "3. 測試解析器..."
python3 -c "
from lambda_interpreter.parser import Parser
text = 'λx. x'
parser = Parser(text)
ast = parser.parse()
print(f'輸入：{text}')
print(f'AST：{ast}')
"
echo ""

echo "4. 測試歸約引擎..."
python3 -c "
from lambda_interpreter.parser import Parser
from lambda_interpreter.reducer import Normalizer
text = '(λx. x) y'
parser = Parser(text)
ast = parser.parse()
normalizer = Normalizer()
result, steps, _ = normalizer.normalize(ast)
print(f'輸入：{text}')
print(f'結果：{result}')
print(f'步數：{steps}')
"
echo ""

echo "5. 測試λ演算直接演示..."
python3 lambda_interpreter/lexer.py 2>/dev/null || python3 -c "
from lambda_interpreter.lexer import Lexer
text = 'λx. x y'
lexer = Lexer(text)
tokens = lexer.tokenize()
print('=== λ演算演示 ===')
print(f'輸入：{text}')
print(f'Token：{[(t.type.name, t.value) for t in tokens]}')
"
echo ""

echo "=== 第5章測試完成 ==="
