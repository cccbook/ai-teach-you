#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { NODE_NUM, NODE_BINOP, NODE_IDENT, NODE_IF } NodeType;

typedef struct ASTNode {
    NodeType type;
    union {
        int num_value;
        char op;
        char ident[32];
        struct {
            struct ASTNode* condition;
            struct ASTNode* then_branch;
            struct ASTNode* else_branch;
        } if_data;
        struct {
            char op;
            struct ASTNode* left;
            struct ASTNode* right;
        } binop_data;
    } data;
} ASTNode;

ASTNode* make_number(int v) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = NODE_NUM;
    n->data.num_value = v;
    return n;
}

ASTNode* make_binary(char op, ASTNode* left, ASTNode* right) {
    ASTNode* n = (ASTNode*)malloc(sizeof(ASTNode));
    n->type = NODE_BINOP;
    n->data.binop_data.op = op;
    n->data.binop_data.left = left;
    n->data.binop_data.right = right;
    return n;
}

void ast_print(ASTNode* node, int indent) {
    for (int i = 0; i < indent; i++) printf("  ");
    if (!node) { printf("(null)\n"); return; }
    
    switch(node->type) {
        case NODE_NUM:
            printf("Number: %d\n", node->data.num_value);
            break;
        case NODE_BINOP:
            printf("BinOp: %c\n", node->data.binop_data.op);
            ast_print(node->data.binop_data.left, indent + 1);
            ast_print(node->data.binop_data.right, indent + 1);
            break;
        case NODE_IDENT:
            printf("Ident: %s\n", node->data.ident);
            break;
        case NODE_IF:
            printf("If\n");
            ast_print(node->data.if_data.condition, indent + 1);
            ast_print(node->data.if_data.then_branch, indent + 1);
            ast_print(node->data.if_data.else_branch, indent + 1);
            break;
    }
}

int ast_evaluate(ASTNode* node) {
    if (!node) return 0;
    switch(node->type) {
        case NODE_NUM:
            return node->data.num_value;
        case NODE_BINOP: {
            int l = ast_evaluate(node->data.binop_data.left);
            int r = ast_evaluate(node->data.binop_data.right);
            switch(node->data.binop_data.op) {
                case '+': return l + r;
                case '-': return l - r;
                case '*': return l * r;
                case '/': return l / r;
            }
        }
    }
    return 0;
}

void ast_destroy(ASTNode* node) {
    if (!node) return;
    if (node->type == NODE_BINOP) {
        ast_destroy(node->data.binop_data.left);
        ast_destroy(node->data.binop_data.right);
    }
    if (node->type == NODE_IF) {
        ast_destroy(node->data.if_data.condition);
        ast_destroy(node->data.if_data.then_branch);
        ast_destroy(node->data.if_data.else_branch);
    }
    free(node);
}

int main() {
    // 建立 AST: 2 + 3 * 4
    ASTNode* ast = make_binary('+',
        make_number(2),
        make_binary('*', make_number(3), make_number(4))
    );
    
    printf("AST for 2 + 3 * 4:\n");
    ast_print(ast, 0);
    
    printf("\nEvaluation result: %d\n", ast_evaluate(ast));
    
    ast_destroy(ast);
    return 0;
}
