#include <stdio.h>

void vector_add(int n, double* a, double* b, double* c) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

int main() {
    double a[4] = {1.0, 2.0, 3.0, 4.0};
    double b[4] = {5.0, 6.0, 7.0, 8.0};
    double c[4];
    
    vector_add(4, a, b, c);
    
    for (int i = 0; i < 4; i++) {
        printf("%f ", c[i]);
    }
    printf("\n");
    
    return 0;
}
