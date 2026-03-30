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

int main() {
    printf("Token types defined:\n");
    printf("  TOKEN_IDENT    = %d\n", TOKEN_IDENT);
    printf("  TOKEN_NUMBER   = %d\n", TOKEN_NUMBER);
    printf("  TOKEN_PLUS     = %d\n", TOKEN_PLUS);
    printf("  TOKEN_MINUS    = %d\n", TOKEN_MINUS);
    printf("  TOKEN_MULT     = %d\n", TOKEN_MULT);
    printf("  TOKEN_DIV      = %d\n", TOKEN_DIV);
    printf("  TOKEN_LPAREN   = %d\n", TOKEN_LPAREN);
    printf("  TOKEN_RPAREN   = %d\n", TOKEN_RPAREN);
    printf("  TOKEN_EOF      = %d\n", TOKEN_EOF);
    
    Token* t = token_create(TOKEN_NUMBER, "42", 0);
    printf("\nSample token: type=%s, value=%s\n", 
           token_type_name(t->type), t->value);
    free(t);
    
    return 0;
}
