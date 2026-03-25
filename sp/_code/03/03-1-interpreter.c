#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKENS 100
#define MAX_VARS 100

typedef enum { 
    TOKEN_NUM, TOKEN_IDENT, TOKEN_PLUS, TOKEN_MINUS, 
    TOKEN_MULT, TOKEN_DIV, TOKEN_ASSIGN, TOKEN_LPAREN, 
    TOKEN_RPAREN, TOKEN_SEMI, TOKEN_PRINT, TOKEN_LET, TOKEN_EOF 
} TokenType;

typedef struct { TokenType type; int value; char name[32]; } Token;
typedef struct ASTNode { 
    char type; int value; char name[32];
    struct ASTNode *left, *right; 
} ASTNode;

Token tokens[MAX_TOKENS];
int token_pos = 0;
int var_count = 0;
int variables[MAX_VARS];
char var_names[MAX_VARS][32];

int var_lookup(const char* name) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(var_names[i], name) == 0) return variables[i];
    }
    return 0;
}

void var_assign(const char* name, int value) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(var_names[i], name) == 0) {
            variables[i] = value;
            return;
        }
    }
    strcpy(var_names[var_count], name);
    variables[var_count] = value;
    var_count++;
}

void tokenize(const char* input) {
    int i = 0, t = 0;
    while (input[i]) {
        if (isspace(input[i])) { i++; continue; }
        if (isdigit(input[i])) {
            int v = 0;
            while (isdigit(input[i])) v = v * 10 + (input[i++] - '0');
            tokens[t++] = (Token){TOKEN_NUM, v, ""};
        } else if (isalpha(input[i]) || input[i] == '_') {
            char name[32] = {0}; int j = 0;
            while (isalnum(input[i]) || input[i] == '_') name[j++] = input[i++];
            if (strcmp(name, "print") == 0) tokens[t++] = (Token){TOKEN_PRINT, 0, ""};
            else if (strcmp(name, "let") == 0) tokens[t++] = (Token){TOKEN_LET, 0, ""};
            else { tokens[t++] = (Token){TOKEN_IDENT, 0, ""}; strcpy(tokens[t-1].name, name); }
        } else {
            switch(input[i++]) {
                case '+': tokens[t++] = (Token){TOKEN_PLUS, 0, ""}; break;
                case '-': tokens[t++] = (Token){TOKEN_MINUS, 0, ""}; break;
                case '*': tokens[t++] = (Token){TOKEN_MULT, 0, ""}; break;
                case '/': tokens[t++] = (Token){TOKEN_DIV, 0, ""}; break;
                case '=': tokens[t++] = (Token){TOKEN_ASSIGN, 0, ""}; break;
                case '(': tokens[t++] = (Token){TOKEN_LPAREN, 0, ""}; break;
                case ')': tokens[t++] = (Token){TOKEN_RPAREN, 0, ""}; break;
                case ';': tokens[t++] = (Token){TOKEN_SEMI, 0, ""}; break;
            }
        }
    }
    tokens[t] = (Token){TOKEN_EOF, 0, ""};
}

ASTNode* parse_expr();

ASTNode* make_num(int v) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = 'N'; n->value = v; n->left = n->right = NULL;
    return n;
}

ASTNode* make_var(const char* name) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = 'V'; n->value = 0; strcpy(n->name, name);
    n->left = n->right = NULL;
    return n;
}

ASTNode* make_binop(char op, ASTNode* left, ASTNode* right) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = op; n->left = left; n->right = right;
    return n;
}

void free_ast(ASTNode* n) {
    if (!n) return;
    free_ast(n->left);
    free_ast(n->right);
    free(n);
}

ASTNode* parse_factor() {
    Token t = tokens[token_pos++];
    if (t.type == TOKEN_NUM) return make_num(t.value);
    if (t.type == TOKEN_IDENT) return make_var(t.name);
    if (t.type == TOKEN_LPAREN) {
        ASTNode* e = parse_expr();
        token_pos++;
        return e;
    }
    return NULL;
}

ASTNode* parse_term() {
    ASTNode* n = parse_factor();
    while (tokens[token_pos].type == TOKEN_MULT || tokens[token_pos].type == TOKEN_DIV) {
        char op = tokens[token_pos++].type == TOKEN_MULT ? '*' : '/';
        n = make_binop(op, n, parse_factor());
    }
    return n;
}

ASTNode* parse_expr() {
    ASTNode* n = parse_term();
    while (tokens[token_pos].type == TOKEN_PLUS || tokens[token_pos].type == TOKEN_MINUS) {
        char op = tokens[token_pos++].type == TOKEN_PLUS ? '+' : '-';
        n = make_binop(op, n, parse_term());
    }
    return n;
}

int eval_expr(ASTNode* n) {
    if (n->type == 'N') return n->value;
    if (n->type == 'V') return var_lookup(n->name);
    int l = eval_expr(n->left), r = eval_expr(n->right);
    switch(n->type) { 
        case '+': return l + r; 
        case '-': return l - r; 
        case '*': return l * r; 
        case '/': return l / r; 
    }
    return 0;
}

void run(const char* input) {
    tokenize(input);
    token_pos = 0;
    ASTNode* ast = parse_expr();
    printf("結果: %d\n", eval_expr(ast));
    free_ast(ast);
}

int main() {
    var_assign("x", 10);
    var_assign("y", 20);
    printf("x = %d\n", var_lookup("x"));
    printf("y = %d\n", var_lookup("y"));
    printf("x + y = %d\n", var_lookup("x") + var_lookup("y"));
    return 0;
}
