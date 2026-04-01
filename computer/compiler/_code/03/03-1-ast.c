#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "03-1-ast.h"

static int indentLevel = 0;

ASTNode* createNode(ASTNodeType type) {
    ASTNode* node = (ASTNode*)malloc(sizeof(ASTNode));
    node->type = type;
    node->name = NULL;
    node->value = 0;
    node->left = NULL;
    node->right = NULL;
    node->third = NULL;
    node->next = NULL;
    return node;
}

ASTNode* createNumber(int value) {
    ASTNode* node = createNode(AST_NUMBER);
    node->value = value;
    return node;
}

ASTNode* createVariable(char* name) {
    ASTNode* node = createNode(AST_VARIABLE);
    node->name = strdup(name);
    return node;
}

ASTNode* createBinaryOp(ASTNodeType op, ASTNode* left, ASTNode* right) {
    ASTNode* node = createNode(op);
    node->left = left;
    node->right = right;
    return node;
}

ASTNode* createFunction(char* name, ASTNode* params, ASTNode* body) {
    ASTNode* node = createNode(AST_FUNCTION);
    node->name = strdup(name);
    node->left = params;
    node->right = body;
    return node;
}

ASTNode* createCall(char* name, ASTNode* args) {
    ASTNode* node = createNode(AST_CALL);
    node->name = strdup(name);
    node->left = args;
    return node;
}

ASTNode* createReturn(ASTNode* value) {
    ASTNode* node = createNode(AST_RETURN);
    node->left = value;
    return node;
}

ASTNode* createIf(ASTNode* condition, ASTNode* thenBranch, ASTNode* elseBranch) {
    ASTNode* node = createNode(AST_IF);
    node->left = condition;
    node->right = thenBranch;
    node->third = elseBranch;
    return node;
}

ASTNode* createWhile(ASTNode* condition, ASTNode* body) {
    ASTNode* node = createNode(AST_WHILE);
    node->left = condition;
    node->right = body;
    return node;
}

ASTNode* createAssign(char* name, ASTNode* value) {
    ASTNode* node = createNode(AST_ASSIGN);
    node->name = strdup(name);
    node->left = value;
    return node;
}

ASTNode* createDeclaration(char* name) {
    ASTNode* node = createNode(AST_DECL);
    node->name = strdup(name);
    return node;
}

static const char* nodeTypeToString(ASTNodeType type) {
    switch (type) {
        case AST_PROGRAM: return "PROGRAM";
        case AST_FUNCTION: return "FUNCTION";
        case AST_CALL: return "CALL";
        case AST_RETURN: return "RETURN";
        case AST_IF: return "IF";
        case AST_WHILE: return "WHILE";
        case AST_FOR: return "FOR";
        case AST_ASSIGN: return "ASSIGN";
        case AST_BINARY_OP: return "BINARY_OP";
        case AST_UNARY_OP: return "UNARY_OP";
        case AST_VARIABLE: return "VARIABLE";
        case AST_NUMBER: return "NUMBER";
        case AST_DECL: return "DECL";
        case AST_PARAM_LIST: return "PARAM_LIST";
        case AST_ARG_LIST: return "ARG_LIST";
        case AST_BLOCK: return "BLOCK";
        case AST_BINOP_ADD: return "ADD";
        case AST_BINOP_SUB: return "SUB";
        case AST_BINOP_MUL: return "MUL";
        case AST_BINOP_DIV: return "DIV";
        case AST_BINOP_LT: return "LT";
        case AST_BINOP_GT: return "GT";
        case AST_BINOP_EQ: return "EQ";
        default: return "UNKNOWN";
    }
}

void printAST(ASTNode* node, int indent) {
    if (node == NULL) return;
    
    for (int i = 0; i < indent; i++) printf("  ");
    printf("%s", nodeTypeToString(node->type));
    
    if (node->name) {
        printf(" (%s)", node->name);
    }
    if (node->type == AST_NUMBER) {
        printf(" = %d", node->value);
    }
    printf("\n");
    
    printAST(node->left, indent + 1);
    printAST(node->right, indent + 1);
    printAST(node->third, indent + 1);
    printAST(node->next, indent);
}

int main() {
    ASTNode* body = createReturn(
        createBinaryOp(AST_BINOP_ADD,
            createVariable("a"),
            createVariable("b")
        )
    );
    
    ASTNode* ast = createFunction("add", 
        createNode(AST_PARAM_LIST),
        body
    );
    
    ASTNode* program = createNode(AST_PROGRAM);
    program->left = ast;
    
    printf("AST for add function:\n");
    printAST(program, 0);
    
    return 0;
}
