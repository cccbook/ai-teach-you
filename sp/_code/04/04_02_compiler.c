#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKENS 1000
#define MAX_IR 100

typedef enum {TOKEN_NUMBER, TOKEN_IDENT, TOKEN_KEYWORD, TOKEN_LPAREN, TOKEN_RPAREN, 
              TOKEN_LBRACE, TOKEN_RBRACE, TOKEN_SEMI, TOKEN_PLUS, TOKEN_MINUS, 
              TOKEN_MULT, TOKEN_ASSIGN, TOKEN_LT, TOKEN_GT, TOKEN_EOF} TokenType;

typedef struct {
    TokenType type;
    char value[64];
} Token;

typedef struct ASTNode {
    char type[32];
    char op[8];
    int value;
    char name[64];
    struct ASTNode *left;
    struct ASTNode *right;
} ASTNode;

typedef struct {
    Token tokens[MAX_TOKENS];
    int count;
    int pos;
    char ir[MAX_IR][128];
    int ir_count;
} Compiler;

ASTNode* parse_expr(Compiler *c);

void next_token(Compiler *c) {
    if (c->pos < c->count) c->pos++;
}

Token peek(Compiler *c) {
    if (c->pos < c->count) return c->tokens[c->pos];
    return (Token){TOKEN_EOF, ""};
}

ASTNode* make_num(int v) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    strcpy(n->type, "NUMBER");
    n->value = v;
    n->left = n->right = NULL;
    return n;
}

ASTNode* make_var(const char* name) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    strcpy(n->type, "VAR");
    strcpy(n->name, name);
    n->left = n->right = NULL;
    return n;
}

ASTNode* make_binop(const char* op, ASTNode* left, ASTNode* right) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    strcpy(n->type, "BINOP");
    strcpy(n->op, op);
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

ASTNode* parse_factor(Compiler *c) {
    Token t = peek(c);
    if (t.type == TOKEN_NUMBER) {
        next_token(c);
        return make_num(atoi(t.value));
    }
    if (t.type == TOKEN_IDENT) {
        next_token(c);
        return make_var(t.value);
    }
    if (t.type == TOKEN_LPAREN) {
        next_token(c);
        ASTNode* e = parse_expr(c);
        if (peek(c).type == TOKEN_RPAREN) next_token(c);
        return e;
    }
    return NULL;
}

ASTNode* parse_term(Compiler *c) {
    ASTNode* n = parse_factor(c);
    while (peek(c).type == TOKEN_MULT) {
        next_token(c);
        n = make_binop("*", n, parse_factor(c));
    }
    return n;
}

ASTNode* parse_expr(Compiler *c) {
    ASTNode* n = parse_term(c);
    while (peek(c).type == TOKEN_PLUS || peek(c).type == TOKEN_MINUS) {
        char op[2] = {peek(c).type == TOKEN_PLUS ? '+' : '-', 0};
        next_token(c);
        n = make_binop(op, n, parse_term(c));
    }
    return n;
}

int eval(ASTNode* n) {
    if (!n) return 0;
    if (strcmp(n->type, "NUMBER") == 0) return n->value;
    if (strcmp(n->type, "VAR") == 0) return 42;
    if (strcmp(n->type, "BINOP") == 0) {
        int l = eval(n->left), r = eval(n->right);
        if (strcmp(n->op, "+") == 0) return l + r;
        if (strcmp(n->op, "-") == 0) return l - r;
        if (strcmp(n->op, "*") == 0) return l * r;
    }
    return 0;
}

void lex(Compiler *c, const char *source) {
    c->count = 0;
    c->pos = 0;
    c->ir_count = 0;
    int i = 0;
    while (source[i] != '\0') {
        if (isspace(source[i])) { i++; continue; }
        if (isdigit(source[i])) {
            int j = i;
            while (isdigit(source[j])) j++;
            c->tokens[c->count].type = TOKEN_NUMBER;
            int len = j - i;
            if (len > 63) len = 63;
            strncpy(c->tokens[c->count].value, source + i, len);
            c->tokens[c->count].value[len] = '\0';
            i = j;
            c->count++;
            continue;
        }
        if (isalpha(source[i]) || source[i] == '_') {
            int j = i;
            while (isalnum(source[j]) || source[j] == '_') j++;
            char word[64];
            int len = j - i;
            if (len > 63) len = 63;
            strncpy(word, source + i, len);
            word[len] = '\0';
            if (strcmp(word, "int") == 0 || strcmp(word, "return") == 0 || 
                strcmp(word, "print") == 0) {
                c->tokens[c->count].type = TOKEN_KEYWORD;
            } else {
                c->tokens[c->count].type = TOKEN_IDENT;
            }
            strcpy(c->tokens[c->count].value, word);
            i = j;
            c->count++;
            continue;
        }
        switch (source[i]) {
            case '+': c->tokens[c->count].type = TOKEN_PLUS; strcpy(c->tokens[c->count].value, "+"); break;
            case '-': c->tokens[c->count].type = TOKEN_MINUS; strcpy(c->tokens[c->count].value, "-"); break;
            case '*': c->tokens[c->count].type = TOKEN_MULT; strcpy(c->tokens[c->count].value, "*"); break;
            default: i++; continue;
        }
        i++;
        c->count++;
    }
    c->tokens[c->count].type = TOKEN_EOF;
    strcpy(c->tokens[c->count].value, "");
    c->count++;
}

int main() {
    Compiler c;
    const char* source = "3 + 4 * 2";
    
    printf("原始碼: %s\n", source);
    
    lex(&c, source);
    printf("詞法分析: ");
    for (int i = 0; i < c.count; i++) {
        printf("[%s:%s] ", 
               c.tokens[i].type == TOKEN_NUMBER ? "NUM" : 
               c.tokens[i].type == TOKEN_PLUS ? "PLUS" : 
               c.tokens[i].type == TOKEN_MULT ? "MULT" : "EOF",
               c.tokens[i].value);
    }
    printf("\n");
    
    c.pos = 0;
    ASTNode* ast = parse_expr(&c);
    printf("語法樹評估: %d\n", eval(ast));
    
    free_ast(ast);
    return 0;
}
