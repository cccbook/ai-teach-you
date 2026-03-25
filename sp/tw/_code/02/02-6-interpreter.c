#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKENS 100

typedef enum { TOKEN_NUM, TOKEN_PLUS, TOKEN_MINUS, TOKEN_MULT, 
               TOKEN_DIV, TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_EOF } TokenType;

typedef struct {
    TokenType type;
    int value;
} Token;

typedef struct ASTNode {
    char type;  // 'N' for number, otherwise operator
    int value;
    struct ASTNode* left;
    struct ASTNode* right;
} ASTNode;

Token tokens[MAX_TOKENS];
int token_count = 0;
int token_pos = 0;

// ============== 詞法分析 ==============
int is_op(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/' || c == '(' || c == ')';
}

void tokenize(const char* input) {
    token_count = 0;
    int i = 0;
    while (input[i]) {
        if (isspace(input[i])) { i++; continue; }
        if (isdigit(input[i])) {
            int v = 0;
            while (isdigit(input[i])) {
                v = v * 10 + (input[i] - '0');
                i++;
            }
            tokens[token_count++] = (Token){TOKEN_NUM, v};
        } else {
            TokenType t;
            switch(input[i]) {
                case '+': t = TOKEN_PLUS; break;
                case '-': t = TOKEN_MINUS; break;
                case '*': t = TOKEN_MULT; break;
                case '/': t = TOKEN_DIV; break;
                case '(': t = TOKEN_LPAREN; break;
                case ')': t = TOKEN_RPAREN; break;
                default: i++; continue;
            }
            tokens[token_count++] = (Token){t, 0};
            i++;
        }
    }
    tokens[token_count] = (Token){TOKEN_EOF, 0};
}

Token next_token() {
    return tokens[token_pos++];
}

void backup_token() {
    token_pos--;
}

// ============== 語法分析 ==============
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
        next_token();  // consume ')'
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
    backup_token();
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
    backup_token();
    return node;
}

// ============== 執行 ==============
int evaluate(ASTNode* n) {
    if (n->type == 'N') return n->value;
    int l = evaluate(n->left);
    int r = evaluate(n->right);
    switch(n->type) {
        case '+': return l + r;
        case '-': return l - r;
        case '*': return l * r;
        case '/': return l / r;
    }
    return 0;
}

void free_ast(ASTNode* n) {
    if (!n) return;
    free_ast(n->left);
    free_ast(n->right);
    free(n);
}

const char* token_name(TokenType t) {
    switch(t) {
        case TOKEN_NUM: return "NUM";
        case TOKEN_PLUS: return "PLUS";
        case TOKEN_MINUS: return "MINUS";
        case TOKEN_MULT: return "MULT";
        case TOKEN_DIV: return "DIV";
        case TOKEN_LPAREN: return "LPAREN";
        case TOKEN_RPAREN: return "RPAREN";
        case TOKEN_EOF: return "EOF";
    }
    return "?";
}

void print_tokens() {
    printf("Tokens: [");
    for (int i = 0; tokens[i].type != TOKEN_EOF; i++) {
        if (tokens[i].type == TOKEN_NUM)
            printf("(NUM, %d)", tokens[i].value);
        else
            printf("(%s, %c)", token_name(tokens[i].type), 
                   "+-*/()"[tokens[i].type - TOKEN_PLUS]);
        if (tokens[i+1].type != TOKEN_EOF) printf(", ");
    }
    printf("]\n");
}

// ============== 主程式 ==============
int main() {
    const char* tests[] = {"2+3", "10-4*2", "(10-4)*2", "100/10/2", NULL};
    
    for (int i = 0; tests[i]; i++) {
        printf("原始碼: %s\n", tests[i]);
        
        tokenize(tests[i]);
        print_tokens();
        
        token_pos = 0;
        ASTNode* ast = parse_expr();
        
        int result = evaluate(ast);
        printf("結果: %d\n\n", result);
        
        free_ast(ast);
    }
    
    return 0;
}
