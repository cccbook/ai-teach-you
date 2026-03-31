#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKENS 100

typedef enum { TOKEN_NUM, TOKEN_PLUS, TOKEN_MINUS, TOKEN_MULT, 
               TOKEN_DIV, TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_EOF } TokenType;

typedef struct { TokenType type; int value; } Token;

typedef struct ASTNode {
    char type;
    int value;
    struct ASTNode *left, *right;
} ASTNode;

Token tokens[MAX_TOKENS];
int token_pos = 0;

ASTNode* parse_expr();
ASTNode* parse_term();
ASTNode* parse_factor();

Token make_token(TokenType type, int value) {
    Token t;
    t.type = type;
    t.value = value;
    return t;
}

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

void free_ast(ASTNode* n) {
    if (!n) return;
    free_ast(n->left);
    free_ast(n->right);
    free(n);
}

void tokenize(const char* input) {
    int i = 0, count = 0;
    while (input[i]) {
        if (isspace(input[i])) { i++; continue; }
        if (isdigit(input[i])) {
            int v = 0;
            while (isdigit(input[i])) v = v * 10 + (input[i++] - '0');
            tokens[count++] = make_token(TOKEN_NUM, v);
        } else {
            TokenType t;
            switch(input[i++]) {
                case '+': t = TOKEN_PLUS; break;
                case '-': t = TOKEN_MINUS; break;
                case '*': t = TOKEN_MULT; break;
                case '/': t = TOKEN_DIV; break;
                case '(': t = TOKEN_LPAREN; break;
                case ')': t = TOKEN_RPAREN; break;
                default: continue;
            }
            tokens[count++] = make_token(t, 0);
        }
    }
    tokens[count] = make_token(TOKEN_EOF, 0);
}

ASTNode* parse_factor() {
    Token t = tokens[token_pos++];
    if (t.type == TOKEN_NUM) return make_num(t.value);
    if (t.type == TOKEN_LPAREN) {
        ASTNode* e = parse_expr();
        token_pos++;
        return e;
    }
    return NULL;
}

ASTNode* parse_term() {
    ASTNode* node = parse_factor();
    while (tokens[token_pos].type == TOKEN_MULT || 
           tokens[token_pos].type == TOKEN_DIV) {
        char op = tokens[token_pos++].type == TOKEN_MULT ? '*' : '/';
        node = make_binop(op, node, parse_factor());
    }
    return node;
}

ASTNode* parse_expr() {
    ASTNode* node = parse_term();
    while (tokens[token_pos].type == TOKEN_PLUS || 
           tokens[token_pos].type == TOKEN_MINUS) {
        char op = tokens[token_pos++].type == TOKEN_PLUS ? '+' : '-';
        node = make_binop(op, node, parse_term());
    }
    return node;
}

int evaluate(ASTNode* n) {
    if (n->type == 'N') return n->value;
    int l = evaluate(n->left), r = evaluate(n->right);
    switch(n->type) {
        case '+': return l + r;
        case '-': return l - r;
        case '*': return l * r;
        case '/': return l / r;
    }
    return 0;
}

int main() {
    const char* tests[] = {"2+3", "10-4*2", "(10-4)*2", NULL};
    for (int i = 0; tests[i]; i++) {
        tokenize(tests[i]);
        token_pos = 0;
        ASTNode* ast = parse_expr();
        printf("原始碼: %s => 結果: %d\n", tests[i], evaluate(ast));
        free_ast(ast);
    }
    return 0;
}
