#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "../02/02-1-token.h"

typedef struct {
    Token* tokens;
    size_t position;
    size_t count;
} Parser;

static void initParser(Parser* parser, Token* tokens, size_t count) {
    parser->tokens = tokens;
    parser->position = 0;
    parser->count = count;
}

static Token* peek(Parser* parser) {
    if (parser->position >= parser->count) {
        return NULL;
    }
    return &parser->tokens[parser->position];
}

static Token* advance(Parser* parser) {
    Token* token = peek(parser);
    if (token) {
        parser->position++;
    }
    return token;
}

static int check(Parser* parser, TokenType type) {
    Token* token = peek(parser);
    return token && token->type == type;
}

static Token* match(Parser* parser, TokenType type) {
    if (check(parser, type)) {
        return advance(parser);
    }
    return NULL;
}

typedef struct ASTNode {
    int type;
    char* name;
    int value;
    struct ASTNode* left;
    struct ASTNode* right;
} ASTNode;

#define AST_NUMBER 1
#define AST_VARIABLE 2
#define AST_BINARY_OP 3
#define AST_FUNCTION 4
#define AST_CALL 5
#define AST_RETURN 6
#define AST_DECL 7
#define AST_ASSIGN 8

ASTNode* createNode(int type) {
    ASTNode* node = (ASTNode*)malloc(sizeof(ASTNode));
    node->type = type;
    node->name = NULL;
    node->value = 0;
    node->left = NULL;
    node->right = NULL;
    return node;
}

ASTNode* expression(Parser* parser);
ASTNode* term(Parser* parser);
ASTNode* factor(Parser* parser);

ASTNode* factor(Parser* parser) {
    Token* token = peek(parser);
    
    if (!token) return NULL;
    
    if (token->type == TOKEN_NUMBER) {
        advance(parser);
        ASTNode* node = createNode(AST_NUMBER);
        node->value = token->value;
        return node;
    }
    
    if (token->type == TOKEN_IDENT) {
        advance(parser);
        ASTNode* node = createNode(AST_VARIABLE);
        node->name = strdup(token->lexeme);
        
        if (check(parser, TOKEN_LPAREN)) {
            advance(parser);
            node->type = AST_CALL;
            node->left = expression(parser);
            match(parser, TOKEN_RPAREN);
        }
        return node;
    }
    
    if (token->type == TOKEN_LPAREN) {
        advance(parser);
        ASTNode* node = expression(parser);
        match(parser, TOKEN_RPAREN);
        return node;
    }
    
    return NULL;
}

ASTNode* term(Parser* parser) {
    ASTNode* node = factor(parser);
    
    while (check(parser, TOKEN_MUL) || check(parser, TOKEN_DIV)) {
        Token* op = advance(parser);
        ASTNode* right = factor(parser);
        ASTNode* newNode = createNode(AST_BINARY_OP);
        newNode->name = strdup(op->lexeme);
        newNode->left = node;
        newNode->right = right;
        node = newNode;
    }
    
    return node;
}

ASTNode* expression(Parser* parser) {
    ASTNode* node = term(parser);
    
    while (check(parser, TOKEN_PLUS) || check(parser, TOKEN_MINUS)) {
        Token* op = advance(parser);
        ASTNode* right = term(parser);
        ASTNode* newNode = createNode(AST_BINARY_OP);
        newNode->name = strdup(op->lexeme);
        newNode->left = node;
        newNode->right = right;
        node = newNode;
    }
    
    return node;
}

ASTNode* statement(Parser* parser);
ASTNode* block(Parser* parser);

ASTNode* statement(Parser* parser) {
    if (check(parser, TOKEN_RETURN)) {
        advance(parser);
        ASTNode* expr = expression(parser);
        match(parser, TOKEN_SEMICOLON);
        ASTNode* node = createNode(AST_RETURN);
        node->left = expr;
        return node;
    }
    
    if (check(parser, TOKEN_INT)) {
        advance(parser);
        Token* ident = match(parser, TOKEN_IDENT);
        if (check(parser, TOKEN_ASSIGN)) {
            advance(parser);
            ASTNode* expr = expression(parser);
            match(parser, TOKEN_SEMICOLON);
            ASTNode* node = createNode(AST_ASSIGN);
            node->name = strdup(ident->lexeme);
            node->left = expr;
            return node;
        }
        match(parser, TOKEN_SEMICOLON);
        ASTNode* node = createNode(AST_DECL);
        node->name = strdup(ident->lexeme);
        return node;
    }
    
    if (check(parser, TOKEN_LBRACE)) {
        return block(parser);
    }
    
    return expression(parser);
}

ASTNode* block(Parser* parser) {
    match(parser, TOKEN_LBRACE);
    ASTNode* head = NULL;
    ASTNode* tail = NULL;
    
    while (!check(parser, TOKEN_RBRACE) && peek(parser)) {
        ASTNode* stmt = statement(parser);
        if (!head) {
            head = stmt;
            tail = stmt;
        } else {
            tail->right = stmt;
            tail = stmt;
        }
    }
    
    match(parser, TOKEN_RBRACE);
    return head;
}

ASTNode* function(Parser* parser) {
    match(parser, TOKEN_INT);
    Token* name = match(parser, TOKEN_IDENT);
    match(parser, TOKEN_LPAREN);
    match(parser, TOKEN_RPAREN);
    ASTNode* body = block(parser);
    
    ASTNode* node = createNode(AST_FUNCTION);
    node->name = strdup(name->lexeme);
    node->left = body;
    return node;
}

ASTNode* parse(Parser* parser) {
    return function(parser);
}

void printTree(ASTNode* node, int indent) {
    if (!node) return;
    for (int i = 0; i < indent; i++) printf("  ");
    
    switch (node->type) {
        case AST_NUMBER: printf("NUMBER(%d)\n", node->value); break;
        case AST_VARIABLE: printf("VAR(%s)\n", node->name); break;
        case AST_BINARY_OP: printf("BINOP(%s)\n", node->name); break;
        case AST_FUNCTION: printf("FUNCTION(%s)\n", node->name); break;
        case AST_CALL: printf("CALL(%s)\n", node->name); break;
        case AST_RETURN: printf("RETURN\n"); break;
        case AST_DECL: printf("DECL(%s)\n", node->name); break;
        case AST_ASSIGN: printf("ASSIGN(%s)\n", node->name); break;
    }
    
    printTree(node->left, indent + 1);
    printTree(node->right, indent + 1);
}

int main() {
    const char* source = "int add(int a, int b) { return a + b; }";
    printf("Parsing: %s\n\n", source);
    printf("Abstract Syntax Tree:\n");
    
    return 0;
}
