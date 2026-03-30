#include <stdio.h>

int constant_fold(int left, int right, char op) {
    switch (op) {
        case '+': return left + right;
        case '*': return left * right;
        case '-': return left - right;
        case '/': return right != 0 ? left / right : 0;
    }
    return 0;
}

int algebraic_simplify(int x, char op, int y) {
    switch (op) {
        case '+': 
            if (y == 0) return x;
            break;
        case '*':
            if (y == 1) return x;
            if (y == 0) return 0;
            if (y == 2) return x << 1;
            break;
        case '-':
            if (y == 0) return x;
            break;
        case '/':
            if (y == 1) return x;
            break;
    }
    return -1;
}

int main() {
    printf("=== Constant Folding Demo ===\n");
    
    int result = constant_fold(5, 0, '+');
    printf("5 + 0 = %d (optimized to 5)\n", result);
    
    result = constant_fold(5, 1, '*');
    printf("5 * 1 = %d (optimized to 5)\n", result);
    
    result = constant_fold(3, 4, '*');
    printf("3 * 4 = %d (computed at compile time)\n", result);
    
    printf("\n=== Algebraic Simplification Demo ===\n");
    
    result = algebraic_simplify(10, '+', 0);
    printf("x + 0 = %d (simplified)\n", result);
    
    result = algebraic_simplify(7, '*', 1);
    printf("x * 1 = %d (simplified)\n", result);
    
    result = algebraic_simplify(9, '*', 0);
    printf("x * 0 = %d (simplified)\n", result);
    
    result = algebraic_simplify(5, '*', 2);
    printf("x * 2 = %d (simplified to x << 1)\n", result);
    
    return 0;
}
