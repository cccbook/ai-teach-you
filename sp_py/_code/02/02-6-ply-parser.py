# 安裝: pip install ply
# 檔案: calc.py

from ply import yacc

# 詞法分析
tokens = ['NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAREN', 'RPAREN']

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NUMBER  = r'\d+'

def t_ignore(t):
    r' +'
    pass

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"詞法錯誤: {t.value[0]}")
    t.lexer.skip(1)

lexer = yacc.lex()

# 語法分析
def p_expr(p):
    '''expr : expr PLUS expr
            | expr MINUS expr'''
    p[0] = ('+', p[1], p[3]) if p[2] == '+' else ('-', p[1], p[3])

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term(p):
    '''term : term MULT term
            | term DIV term'''
    p[0] = ('*', p[1], p[3]) if p[2] == '*' else ('/', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = ('num', p[1])

def p_factor_expr(p):
    'factor : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error(p):
    print("語法錯誤!")

parser = yacc.yacc()

# 測試
result = parser.parse("2 + 3 * 4")
print(result)