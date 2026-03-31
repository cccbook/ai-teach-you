#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKENS 100
#define MAX_VARS 100

typedef enum { 
    TOKEN_NUM, TOKEN_IDENT, TOKEN_PLUS, TOKEN_MINUS, 
    TOKEN_MULT, TOKEN_DIV, TOKEN_ASSIGN, TOKEN_LPAREN, 
    TOKEN_RPAREN, TOKEN_SEMI, TOKEN_PRINT, TOKEN_LET,
    TOKEN_EOF 
} TokenType;

typedef struct {
    TokenType type;
    int value;
    char name[32];
} Token;

typedef struct ASTNode {
    char type;
    int value;
    char name[32];
    struct ASTNode *left, *right;
} ASTNode;

Token tokens[MAX_TOKENS];
int token_pos = 0;

// 變數儲存 - 獨立的變數表
char var_names[MAX_VARS][32];
int var_values[MAX_VARS];
int var_count = 0;

// ========== 詞法分析 ==========
void tokenize(const char* input) {
    int i = 0, t = 0;
    while (input[i]) {
        if (isspace(input[i])) { i++; continue; }
        if (isdigit(input[i])) {
            int v = 0;
            while (isdigit(input[i])) v = v * 10 + (input[i++] - '0');
            tokens[t++] = (Token){TOKEN_NUM, v, ""};
        } else if (isalpha(input[i]) || input[i] == '_') {
            char name[32] = {0};
            int j = 0;
            while (isalnum(input[i]) || input[i] == '_') 
                name[j++] = input[i++];
            if (strcmp(name, "print") == 0) 
                tokens[t++] = (Token){TOKEN_PRINT, 0, ""};
            else if (strcmp(name, "let") == 0) 
                tokens[t++] = (Token){TOKEN_LET, 0, ""};
            else {
                tokens[t++] = (Token){TOKEN_IDENT, 0, ""};
                strcpy(tokens[t-1].name, name);
            }
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

// ========== 語法分析 ==========
ASTNode* parse_expr();

ASTNode* make_num(int v) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = 'N'; n->value = v; n->name[0] = '\0';
    n->left = n->right = NULL;
    return n;
}

ASTNode* make_var(const char* name) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = 'V'; n->value = 0;
    strcpy(n->name, name);
    n->left = n->right = NULL;
    return n;
}

ASTNode* make_binop(char op, ASTNode* l, ASTNode* r) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = op; n->left = l; n->right = r; n->name[0] = '\0';
    return n;
}

ASTNode* parse_factor() {
    Token t = tokens[token_pos++];
    if (t.type == TOKEN_NUM) return make_num(t.value);
    if (t.type == TOKEN_IDENT) return make_var(t.name);
    if (t.type == TOKEN_LPAREN) {
        ASTNode* e = parse_expr();
        token_pos++; // skip ')'
        return e;
    }
    return NULL;
}

ASTNode* parse_term() {
    ASTNode* n = parse_factor();
    while (tokens[token_pos].type == TOKEN_MULT || 
           tokens[token_pos].type == TOKEN_DIV) {
        char op = tokens[token_pos++].type == TOKEN_MULT ? '*' : '/';
        n = make_binop(op, n, parse_factor());
    }
    return n;
}

ASTNode* parse_expr() {
    ASTNode* n = parse_term();
    while (tokens[token_pos].type == TOKEN_PLUS || 
           tokens[token_pos].type == TOKEN_MINUS) {
        char op = tokens[token_pos++].type == TOKEN_PLUS ? '+' : '-';
        n = make_binop(op, n, parse_term());
    }
    return n;
}

// ========== 執行 ==========
int get_var(const char* name) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(var_names[i], name) == 0) return var_values[i];
    }
    return 0;
}

void set_var(const char* name, int value) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(var_names[i], name) == 0) { 
            var_values[i] = value; 
            return; 
        }
    }
    strcpy(var_names[var_count], name);
    var_values[var_count++] = value;
}

int eval_expr(ASTNode* n) {
    if (!n) return 0;
    if (n->type == 'N') return n->value;
    if (n->type == 'V') return get_var(n->name);
    int l = eval_expr(n->left), r = eval_expr(n->right);
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

void run(const char* input) {
    printf(">>> %s\n", input);
    tokenize(input);
    token_pos = 0;
    
    while (tokens[token_pos].type != TOKEN_EOF) {
        Token t = tokens[token_pos];
        
        if (t.type == TOKEN_LET) {
            token_pos++; // skip 'let'
            char name[32];
            strcpy(name, tokens[token_pos].name);
            token_pos++; // skip IDENT
            token_pos++; // skip '='
            ASTNode* e = parse_expr();
            int val = eval_expr(e);
            set_var(name, val);
            free_ast(e);
            token_pos++; // skip ';'
        } 
        else if (t.type == TOKEN_PRINT) {
            token_pos++; // skip 'print'
            token_pos++; // skip '('
            ASTNode* e = parse_expr();
            int val = eval_expr(e);
            printf("%d\n", val);
            free_ast(e);
            token_pos++; // skip ')'
            token_pos++; // skip ';'
        }
        else if (t.type == TOKEN_IDENT) {
            char name[32];
            strcpy(name, t.name);
            token_pos++; // skip IDENT
            token_pos++; // skip '='
            ASTNode* e = parse_expr();
            int val = eval_expr(e);
            set_var(name, val);
            free_ast(e);
            token_pos++; // skip ';'
        }
        else {
            // 可能是沒有分號的表達式
            ASTNode* e = parse_expr();
            if (e) printf("%d\n", eval_expr(e));
            free_ast(e);
            break;
        }
    }
}

int main() {
    run("let x = 10;");
    run("let y = 20;");
    run("print(x + y);");
    run("let z = (x + y) * 2;");
    run("print(z);");
    return 0;
}
