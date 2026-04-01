#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "02-1-token.h"

typedef struct {
    const char* source;
    size_t position;
    size_t length;
    int line;
} Lexer;

static void initLexer(Lexer* lexer, const char* source) {
    lexer->source = source;
    lexer->position = 0;
    lexer->length = strlen(source);
    lexer->line = 1;
}

static char peek(Lexer* lexer) {
    if (lexer->position >= lexer->length) {
        return '\0';
    }
    return lexer->source[lexer->position];
}

static char advance(Lexer* lexer) {
    char c = peek(lexer);
    lexer->position++;
    return c;
}

static void skipWhitespace(Lexer* lexer) {
    while (peek(lexer) == ' ' || peek(lexer) == '\t' || 
           peek(lexer) == '\n' || peek(lexer) == '\r') {
        if (peek(lexer) == '\n') {
            lexer->line++;
        }
        advance(lexer);
    }
}

static void skipComment(Lexer* lexer) {
    if (peek(lexer) == '/') {
        if (lexer->position + 1 < lexer->length) {
            if (lexer->source[lexer->position + 1] == '/') {
                while (peek(lexer) != '\n' && peek(lexer) != '\0') {
                    advance(lexer);
                }
            } else if (lexer->source[lexer->position + 1] == '*') {
                advance(lexer);
                advance(lexer);
                while (1) {
                    if (peek(lexer) == '\0') break;
                    if (peek(lexer) == '*' && lexer->position + 1 < lexer->length && 
                        lexer->source[lexer->position + 1] == '/') {
                        advance(lexer);
                        advance(lexer);
                        break;
                    }
                    if (peek(lexer) == '\n') lexer->line++;
                    advance(lexer);
                }
            }
        }
    }
}

static Token makeToken(Lexer* lexer, TokenType type, char* lexeme) {
    Token token;
    token.type = type;
    token.lexeme = lexeme;
    token.line = lexer->line;
    return token;
}

static Token scanNumber(Lexer* lexer) {
    size_t start = lexer->position;
    while (isdigit(peek(lexer))) {
        advance(lexer);
    }
    size_t len = lexer->position - start;
    char* lexeme = malloc(len + 1);
    strncpy(lexeme, lexer->source + start, len);
    lexeme[len] = '\0';
    
    Token token;
    token.type = TOKEN_NUMBER;
    token.value = atoi(lexeme);
    token.lexeme = lexeme;
    token.line = lexer->line;
    free(lexeme);
    return token;
}

static Token scanIdentifier(Lexer* lexer) {
    size_t start = lexer->position;
    while (isalnum(peek(lexer)) || peek(lexer) == '_') {
        advance(lexer);
    }
    size_t len = lexer->position - start;
    char* lexeme = malloc(len + 1);
    strncpy(lexeme, lexer->source + start, len);
    lexeme[len] = '\0';
    
    Token token;
    if (strcmp(lexeme, "int") == 0) {
        token.type = TOKEN_INT;
    } else if (strcmp(lexeme, "return") == 0) {
        token.type = TOKEN_RETURN;
    } else if (strcmp(lexeme, "if") == 0) {
        token.type = TOKEN_IF;
    } else if (strcmp(lexeme, "else") == 0) {
        token.type = TOKEN_ELSE;
    } else if (strcmp(lexeme, "for") == 0) {
        token.type = TOKEN_FOR;
    } else if (strcmp(lexeme, "while") == 0) {
        token.type = TOKEN_WHILE;
    } else {
        token.type = TOKEN_IDENT;
    }
    token.lexeme = lexeme;
    token.line = lexer->line;
    free(lexeme);
    return token;
}

static const char* tokenTypeToString(TokenType type) {
    switch (type) {
        case TOKEN_INT: return "INT";
        case TOKEN_RETURN: return "RETURN";
        case TOKEN_IF: return "IF";
        case TOKEN_ELSE: return "ELSE";
        case TOKEN_FOR: return "FOR";
        case TOKEN_WHILE: return "WHILE";
        case TOKEN_IDENT: return "IDENT";
        case TOKEN_NUMBER: return "NUMBER";
        case TOKEN_PLUS: return "PLUS";
        case TOKEN_MINUS: return "MINUS";
        case TOKEN_MUL: return "MUL";
        case TOKEN_DIV: return "DIV";
        case TOKEN_LPAREN: return "LPAREN";
        case TOKEN_RPAREN: return "RPAREN";
        case TOKEN_LBRACE: return "LBRACE";
        case TOKEN_RBRACE: return "RBRACE";
        case TOKEN_SEMICOLON: return "SEMICOLON";
        case TOKEN_ASSIGN: return "ASSIGN";
        case TOKEN_LT: return "LT";
        case TOKEN_GT: return "GT";
        case TOKEN_EQ: return "EQ";
        case TOKEN_EOF: return "EOF";
        case TOKEN_ERROR: return "ERROR";
        default: return "UNKNOWN";
    }
}

Token scanToken(Lexer* lexer) {
    skipWhitespace(lexer);
    skipComment(lexer);
    
    if (peek(lexer) == '\0') {
        return makeToken(lexer, TOKEN_EOF, NULL);
    }
    
    char c = advance(lexer);
    
    if (isdigit(c)) {
        lexer->position--;
        return scanNumber(lexer);
    }
    
    if (isalpha(c) || c == '_') {
        lexer->position--;
        return scanIdentifier(lexer);
    }
    
    switch (c) {
        case '(': return makeToken(lexer, TOKEN_LPAREN, "(");
        case ')': return makeToken(lexer, TOKEN_RPAREN, ")");
        case '{': return makeToken(lexer, TOKEN_LBRACE, "{");
        case '}': return makeToken(lexer, TOKEN_RBRACE, "}");
        case ';': return makeToken(lexer, TOKEN_SEMICOLON, ";");
        case '+': return makeToken(lexer, TOKEN_PLUS, "+");
        case '-': return makeToken(lexer, TOKEN_MINUS, "-");
        case '*': return makeToken(lexer, TOKEN_MUL, "*");
        case '/': return makeToken(lexer, TOKEN_DIV, "/");
        case '<': return makeToken(lexer, TOKEN_LT, "<");
        case '>': return makeToken(lexer, TOKEN_GT, ">");
        case '=': return makeToken(lexer, TOKEN_ASSIGN, "=");
    }
    
    return makeToken(lexer, TOKEN_ERROR, "Unknown token");
}

int main() {
    const char* source = "int main() { return 42; }";
    Lexer lexer;
    initLexer(&lexer, source);
    
    printf("Source: %s\n\n", source);
    printf("Tokens:\n");
    
    Token token;
    do {
        token = scanToken(&lexer);
        printf("  %s", tokenTypeToString(token.type));
        if (token.lexeme) {
            printf(" ('%s')", token.lexeme);
        }
        if (token.type == TOKEN_NUMBER) {
            printf(" value=%d", token.value);
        }
        printf(" at line %d\n", token.line);
    } while (token.type != TOKEN_EOF && token.type != TOKEN_ERROR);
    
    return 0;
}
