#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    TOKEN_IDENT,
    TOKEN_NUMBER,
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
    char value[64];
    int position;
    int line;
    int column;
} Token;

Token* token_create(TokenType type, const char* value, int pos) {
    Token* t = (Token*)malloc(sizeof(Token));
    t->type = type;
    strncpy(t->value, value, 63);
    t->position = pos;
    t->line = 1;
    t->column = 1;
    return t;
}

const char* token_type_name(TokenType type) {
    switch(type) {
        case TOKEN_IDENT: return "IDENT";
        case TOKEN_NUMBER: return "NUMBER";
        case TOKEN_PLUS: return "PLUS";
        case TOKEN_MINUS: return "MINUS";
        case TOKEN_MULT: return "MULT";
        case TOKEN_DIV: return "DIV";
        case TOKEN_LPAREN: return "LPAREN";
        case TOKEN_RPAREN: return "RPAREN";
        case TOKEN_EOF: return "EOF";
        default: return "UNKNOWN";
    }
}

void token_print(Token* t) {
    printf("Token(%s, \"%s\", pos=%d)\n", 
           token_type_name(t->type), t->value, t->position);
}

void token_destroy(Token* t) {
    free(t);
}

int main() {
    Token* t1 = token_create(TOKEN_IDENT, "x", 0);
    Token* t2 = token_create(TOKEN_PLUS, "+", 2);
    Token* t3 = token_create(TOKEN_NUMBER, "42", 4);
    
    token_print(t1);
    token_print(t2);
    token_print(t3);
    
    token_destroy(t1);
    token_destroy(t2);
    token_destroy(t3);
    
    return 0;
}
