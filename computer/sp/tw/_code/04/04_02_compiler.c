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
    struct ASTNode **statements;
    int stmt_count;
} ASTNode;

typedef struct {
    Token tokens[MAX_TOKENS];
    int count;
    int pos;
    char ir[MAX_IR][128];
    int ir_count;
} Compiler;

void lex(Compiler *c, const char *source) {
    c->count = 0;
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
                strcmp(word, "if") == 0 || strcmp(word, "else") == 0 ||
                strcmp(word, "while") == 0 || strcmp(word, "print") == 0) {
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
            case '(': c->tokens[c->count].type = TOKEN_LPAREN; strcpy(c->tokens[c->count].value, "("); break;
            case ')': c->tokens[c->count].type = TOKEN_RPAREN; strcpy(c->tokens[c->count].value, ")"); break;
            case '{': c->tokens[c->count].type = TOKEN_LBRACE; strcpy(c->tokens[c->count].value, "{"); break;
            case '}': c->tokens[c->count].type = TOKEN_RBRACE; strcpy(c->tokens[c->count].value, "}"); break;
            case ';': c->tokens[c->count].type = TOKEN_SEMI; strcpy(c->tokens[c->count].value, ";"); break;
            case '+': c->tokens[c->count].type = TOKEN_PLUS; strcpy(c->tokens[c->count].value, "+"); break;
            case '-': c->tokens[c->count].type = TOKEN_MINUS; strcpy(c->tokens[c->count].value, "-"); break;
            case '*': c->tokens[c->count].type = TOKEN_MULT; strcpy(c->tokens[c->count].value, "*"); break;
            case '=': c->tokens[c->count].type = TOKEN_ASSIGN; strcpy(c->tokens[c->count].value, "="); break;
            case '<': c->tokens[c->count].type = TOKEN_LT; strcpy(c->tokens[c->count].value, "<"); break;
            case '>': c->tokens[c->count].type = TOKEN_GT; strcpy(c->tokens[c->count].value, ">"); break;
            default: i++; continue;
        }
        i++;
        c->count++;
    }
    c->tokens[c->count].type = TOKEN_EOF;
    c->count++;
}

Token *peek(Compiler *c) {
    if (c->pos < c->count) return &c->tokens[c->pos];
    return NULL;
}

Token *consume(Compiler *c) {
    Token *t = peek(c);
    if (t) c->pos++;
    return t;
}

ASTNode *primary(Compiler *c) {
    Token *t = peek(c);
    ASTNode *node = malloc(sizeof(ASTNode));
    if (!node) return NULL;
    memset(node, 0, sizeof(ASTNode));
    
    if (t->type == TOKEN_NUMBER) {
        strcpy(node->type, "number");
        node->value = atoi(t->value);
        consume(c);
    } else if (t->type == TOKEN_IDENT) {
        strcpy(node->type, "identifier");
        strcpy(node->name, t->value);
        consume(c);
    } else if (t->type == TOKEN_LPAREN) {
        consume(c);
        node = primary(c);
        if (peek(c)->type == TOKEN_RPAREN) consume(c);
    }
    return node;
}

ASTNode *multiplicative(Compiler *c) {
    ASTNode *result = primary(c);
    while (peek(c) && peek(c)->type == TOKEN_MULT) {
        consume(c);
        ASTNode *right = primary(c);
        ASTNode *op = malloc(sizeof(ASTNode));
        memset(op, 0, sizeof(ASTNode));
        strcpy(op->type, "binary");
        strcpy(op->op, "*");
        op->left = result;
        op->right = right;
        result = op;
    }
    return result;
}

ASTNode *additive(Compiler *c) {
    ASTNode *result = multiplicative(c);
    while (peek(c) && (peek(c)->type == TOKEN_PLUS || peek(c)->type == TOKEN_MINUS)) {
        Token *op_tok = consume(c);
        ASTNode *right = multiplicative(c);
        ASTNode *op = malloc(sizeof(ASTNode));
        memset(op, 0, sizeof(ASTNode));
        strcpy(op->type, "binary");
        strcpy(op->op, op_tok->value);
        op->left = result;
        op->right = right;
        result = op;
    }
    return result;
}

ASTNode *expr(Compiler *c) {
    return additive(c);
}

void generate_ir_expr(Compiler *c, ASTNode *node, char *out) {
    if (!node) return;
    if (strcmp(node->type, "number") == 0) {
        sprintf(out, "%d", node->value);
    } else if (strcmp(node->type, "identifier") == 0) {
        strcpy(out, node->name);
    } else if (strcmp(node->type, "binary") == 0) {
        char left[64], right[64];
        generate_ir_expr(c, node->left, left);
        generate_ir_expr(c, node->right, right);
        sprintf(out, "(%s %s %s)", left, node->op, right);
    }
}

void generate_ir_stmt(Compiler *c, ASTNode *stmt) {
    if (!stmt) return;
    if (strcmp(stmt->type, "return") == 0) {
        char val[64];
        generate_ir_expr(c, stmt->left, val);
        sprintf(c->ir[c->ir_count++], "  return %s", val);
    } else if (strcmp(stmt->type, "print") == 0) {
        char val[64];
        generate_ir_expr(c, stmt->left, val);
        sprintf(c->ir[c->ir_count++], "  print %s", val);
    } else if (strcmp(stmt->type, "expr") == 0) {
        char val[64];
        generate_ir_expr(c, stmt->left, val);
        sprintf(c->ir[c->ir_count++], "  %s", val);
    }
}

void generate_ir(Compiler *c, ASTNode *ast) {
    c->ir_count = 0;
    if (ast && ast->statements) {
        for (int i = 0; i < ast->stmt_count; i++) {
            generate_ir_stmt(c, ast->statements[i]);
        }
    }
}

void generate_asm(Compiler *c) {
    printf("\n=== x86 Assembly ===\n");
    printf("    .global main\n");
    printf("main:\n");
    for (int i = 0; i < c->ir_count; i++) {
        char *line = c->ir[i];
        if (strstr(line, "return")) {
            int val = 0;
            char *p = strchr(line, ' ');
            if (p) {
                while (*p == ' ') p++;
                if (isdigit(*p)) val = atoi(p);
            }
            printf("    movl $%d, %%eax\n", val);
            printf("    ret\n");
        } else if (strstr(line, "print")) {
            char *p = strchr(line, ' ');
            while (p && *p == ' ') p++;
            if (isdigit(*p)) {
                printf("    movl $%d, %%edi\n", atoi(p));
            } else {
                printf("    movl %s, %%edi\n", p);
            }
            printf("    call print_int\n");
        }
    }
}

void compile(Compiler *c, const char *source) {
    printf("=== Source Code ===\n%s\n", source);
    
    lex(c, source);
    printf("\n=== Tokens ===\n");
    for (int i = 0; i < c->count; i++) {
        printf("(%d, \"%s\") ", c->tokens[i].type, c->tokens[i].value);
    }
    printf("\n");
    
    c->pos = 0;
    ASTNode *ast = expr(c);
    
    printf("\n=== AST ===\n");
    printf("expr: ");
    char buf[128];
    generate_ir_expr(c, ast, buf);
    printf("%s\n", buf);
    
    generate_ir(c, ast);
    printf("\n=== IR ===\n");
    for (int i = 0; i < c->ir_count; i++) {
        printf("%s\n", c->ir[i]);
    }
    
    generate_asm(c);
}

int main() {
    Compiler c;
    memset(&c, 0, sizeof(Compiler));
    
    const char *source = "10 + 20";
    compile(&c, source);
    
    return 0;
}
