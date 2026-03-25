#include <stdio.h>
#include <string.h>

void simulate_dynamic_graph() {
    printf("=== Dynamic Computation Graph (Concept) ===\n\n");
    
    printf("PyTorch-style dynamic graph:\n\n");
    
    float x = 1.0f;
    printf("  x = %.2f (requires_grad=True)\n\n", x);
    
    printf("  Loop iteration 0:\n");
    float y;
    if (0 % 2 == 0) {
        y = x * 2;
        printf("    y = x * 2 = %.2f\n", y);
    }
    x = y;
    
    printf("  Loop iteration 1:\n");
    if (1 % 2 == 0) {
        y = x * 2;
    } else {
        y = x + 1;
        printf("    y = x + 1 = %.2f\n", y);
    }
    x = y;
    
    printf("  ... (continues for 10 iterations)\n\n");
    
    printf("Key difference from static graph:\n");
    printf("  + Graph is rebuilt each forward pass\n");
    printf("  + Control flow can depend on data\n");
    printf("  + Easier debugging and prototyping\n");
    printf("  - Cannot optimize across runs\n");
}

int main() {
    simulate_dynamic_graph();
    
    printf("C equivalent concept:\n");
    printf("  // Dynamic graph in C (simplified)\n");
    printf("  void forward(float* x, int iterations) {\n");
    printf("      for (int i = 0; i < iterations; i++) {\n");
    printf("          if (i %% 2 == 0) {\n");
    printf("              *x = *x * 2;\n");
    printf("          } else {\n");
    printf("              *x = *x + 1;\n");
    printf("          }\n");
    printf("      }\n");
    printf("  }\n");
    
    return 0;
}
