#include <stdio.h>
#include <stdlib.h>

typedef enum { NODE_NUM, NODE_BINOP, NODE_IDENT, NODE_IF } NodeType;

typedef struct ASTNode {
    NodeType type;
    union {
        int num_value;
        char op;
        struct { char op; struct ASTNode *left, *right; } binop;
        struct { struct ASTNode *cond, *then, *else_; } if_data;
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
    n->data.binop.op = op;
    n->data.binop.left = left;
    n->data.binop.right = right;
    return n;
}

void free_ast(ASTNode* n) {
    if (!n) return;
    if (n->type == NODE_BINOP) {
        free_ast(n->data.binop.left);
        free_ast(n->data.binop.right);
    } else if (n->type == NODE_IF) {
        free_ast(n->data.if_data.cond);
        free_ast(n->data.if_data.then);
        free_ast(n->data.if_data.else_);
    }
    free(n);
}

int evaluate(ASTNode* n) {
    if (n->type == NODE_NUM) return n->data.num_value;
    int l = evaluate(n->data.binop.left);
    int r = evaluate(n->data.binop.right);
    switch(n->data.binop.op) {
        case '+': return l + r;
        case '-': return l - r;
        case '*': return l * r;
        case '/': return l / r;
    }
    return 0;
}

void print_ast(ASTNode* n, int depth) {
    if (!n) return;
    for (int i = 0; i < depth; i++) printf("  ");
    if (n->type == NODE_NUM) {
        printf("NUM: %d\n", n->data.num_value);
    } else if (n->type == NODE_BINOP) {
        printf("BINOP: %c\n", n->data.binop.op);
        print_ast(n->data.binop.left, depth + 1);
        print_ast(n->data.binop.right, depth + 1);
    }
}

int main() {
    ASTNode* ast = make_binary('+',
        make_number(2),
        make_binary('*', make_number(3), make_number(4))
    );
    printf("AST structure:\n");
    print_ast(ast, 0);
    printf("\nResult: %d\n", evaluate(ast));
    free_ast(ast);
    return 0;
}
