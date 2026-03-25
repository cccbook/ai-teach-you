#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef enum {
    TOKEN_NUM,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_MULT,
    TOKEN_DIV,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_EOF
} TokenType;

typedef struct {
    TokenType type;
    int value;
} Token;

typedef struct {
    Token* tokens;
    int pos;
    int size;
} Parser;

Token* tokens;
int token_pos = 0;

Token next_token() {
    if (token_pos >= 10) {
        return (Token){TOKEN_EOF, 0};
    }
    return tokens[token_pos++];
}

void unget_token() {
    token_pos--;
}

typedef struct ASTNode {
    char type;
    int value;
    struct ASTNode* left;
    struct ASTNode* right;
} ASTNode;

ASTNode* make_num(int v) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = 'N';
    n->value = v;
    n->left = n->right = NULL;
    return n;
}

ASTNode* make_binop(char op, ASTNode* left, ASTNode* right) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = op;
    n->left = left;
    n->right = right;
    return n;
}

ASTNode* parse_expr();
ASTNode* parse_term();
ASTNode* parse_factor();

ASTNode* parse_factor() {
    Token t = next_token();
    if (t.type == TOKEN_NUM) {
        return make_num(t.value);
    } else if (t.type == TOKEN_LPAREN) {
        ASTNode* e = parse_expr();
        t = next_token();
        return e;
    }
    return NULL;
}

ASTNode* parse_term() {
    ASTNode* node = parse_factor();
    Token t = next_token();
    
    while (t.type == TOKEN_MULT || t.type == TOKEN_DIV) {
        ASTNode* right = parse_factor();
        node = make_binop(t.type == TOKEN_MULT ? '*' : '/', node, right);
        t = next_token();
    }
    unget_token();
    return node;
}

ASTNode* parse_expr() {
    ASTNode* node = parse_term();
    Token t = next_token();
    
    while (t.type == TOKEN_PLUS || t.type == TOKEN_MINUS) {
        ASTNode* right = parse_term();
        node = make_binop(t.type == TOKEN_PLUS ? '+' : '-', node, right);
        t = next_token();
    }
    unget_token();
    return node;
}

int eval(ASTNode* n) {
    if (n->type == 'N') return n->value;
    int left = eval(n->left);
    int right = eval(n->right);
    switch(n->type) {
        case '+': return left + right;
        case '-': return left - right;
        case '*': return left * right;
        case '/': return left / right;
    }
    return 0;
}

void tokenize(const char* input) {
    int n = strlen(input);
    tokens = (Token*)malloc(10 * sizeof(Token));
    int tidx = 0;
    
    for (int i = 0; i < n; i++) {
        if (isspace(input[i])) continue;
        if (isdigit(input[i])) {
            int v = 0;
            while (i < n && isdigit(input[i])) {
                v = v * 10 + (input[i] - '0');
                i++;
            }
            tokens[tidx++] = (Token){TOKEN_NUM, v};
            i--;
        } else {
            switch(input[i]) {
                case '+': tokens[tidx++] = (Token){TOKEN_PLUS, 0}; break;
                case '-': tokens[tidx++] = (Token){TOKEN_MINUS, 0}; break;
                case '*': tokens[tidx++] = (Token){TOKEN_MULT, 0}; break;
                case '/': tokens[tidx++] = (Token){TOKEN_DIV, 0}; break;
                case '(': tokens[tidx++] = (Token){TOKEN_LPAREN, 0}; break;
                case ')': tokens[tidx++] = (Token){TOKEN_RPAREN, 0}; break;
            }
        }
    }
    tokens[tidx] = (Token){TOKEN_EOF, 0};
}

int main() {
    const char* tests[] = {"2+3", "2+3*4", "(2+3)*4", "10-4*2", NULL};
    
    for (int i = 0; tests[i]; i++) {
        printf("原始碼: %s\n", tests[i]);
        tokenize(tests[i]);
        token_pos = 0;
        ASTNode* ast = parse_expr();
        int result = eval(ast);
        printf("結果: %d\n\n", result);
        free(tokens);
    }
    
    return 0;
}
