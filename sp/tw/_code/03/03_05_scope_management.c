#include <stdio.h>
#include <string.h>

typedef enum { GLOBAL, LOCAL, INNER } ScopeType;

typedef struct {
    char name[32];
    int value;
    ScopeType type;
} Variable;

Variable globals[10];
Variable locals[10];
int global_count = 0;
int local_count = 0;

void demonstrate_scope() {
    printf("=== Scope Management ===\n\n");
    
    printf("x = 10  (global scope)\n\n");
    printf("void outer() {\n");
    printf("    y = 20  (outer's scope)\n\n");
    printf("    void inner() {\n");
    printf("        z = 30  (inner's scope)\n");
    printf("        print(x, y, z)  // Visible: x, y, z\n");
    printf("    }\n");
    printf("    inner();\n");
    printf("    // print(z)  // ERROR: z not visible\n");
    printf("}\n\n");
    
    printf("Variable lookup order (lexical scope):\n");
    printf("  1. Current scope\n");
    printf("  2. Parent scope\n");
    printf("  3. Grandparent scope\n");
    printf("  ... (continues until global scope)\n\n");
    
    printf("Scope Implementation Strategies:\n");
    printf("  1. Lexical Scope: Determined by source structure (static)\n");
    printf("  2. Dynamic Scope: Determined by call stack (runtime)\n");
    
    printf("\nC Scope Example:\n");
    
    int x = 10;
    printf("  Global x = %d\n", x);
    
    {
        int y = 20;
        printf("  Outer scope y = %d\n", y);
        printf("  x from outer = %d\n", x);
        
        {
            int z = 30;
            printf("  Inner scope z = %d\n", z);
            printf("  x, y from outer = %d, %d\n", x, y);
        }
    }
}

int main() {
    demonstrate_scope();
    return 0;
}
