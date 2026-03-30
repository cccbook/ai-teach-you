#include <stdio.h>
#include <stdlib.h>

typedef enum {EXPR_NUMBER, EXPR_BINARY} ExprType;

typedef struct Expr {
    ExprType type;
    char op;
    union {
        int value;
        struct {
            struct Expr *left;
            struct Expr *right;
        } binary;
    } u;
} Expr;

int eval_expr(Expr *expr) {
    if (expr->type == EXPR_NUMBER) {
        return expr->u.value;
    }
    if (expr->type == EXPR_BINARY) {
        int left = eval_expr(expr->u.binary.left);
        int right = eval_expr(expr->u.binary.right);
        switch (expr->op) {
            case '+': return left + right;
            case '*': return left * right;
            case '-': return left - right;
            case '/': return left / right;
        }
    }
    return 0;
}

int constant_folding(Expr *expr) {
    if (expr->type == EXPR_BINARY) {
        int l = eval_expr(expr->u.binary.left);
        int r = eval_expr(expr->u.binary.right);
        
        if (expr->op == '*' && r == 1) {
            expr->type = EXPR_NUMBER;
            expr->u.value = l;
            return 1;
        }
        if (expr->op == '*' && l == 1) {
            expr->type = EXPR_NUMBER;
            expr->u.value = r;
            return 1;
        }
        if (expr->op == '+' && r == 0) {
            expr->type = EXPR_NUMBER;
            expr->u.value = l;
            return 1;
        }
    }
    return 0;
}

int main() {
    Expr e = {
        .type = EXPR_BINARY,
        .op = '*',
        .u.binary.left = &(Expr){.type = EXPR_NUMBER, .u.value = 5},
        .u.binary.right = &(Expr){.type = EXPR_NUMBER, .u.value = 1}
    };
    
    printf("Before folding: %d * 1\n", eval_expr(&e));
    constant_folding(&e);
    printf("After folding: %d\n", eval_expr(&e));
    
    return 0;
}
