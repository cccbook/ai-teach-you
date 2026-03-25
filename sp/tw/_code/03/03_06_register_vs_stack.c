#include <stdio.h>

void print_stack_based_vm() {
    printf("=== Stack-based VM ===\n\n");
    
    printf("Computing 1 + 2:\n\n");
    printf("Stack Operations:\n");
    printf("  iconst 1    // Push 1 onto stack\n");
    printf("                Stack: [1]\n");
    printf("  iconst 2    // Push 2 onto stack\n");
    printf("                Stack: [1, 2]\n");
    printf("  iadd        // Pop 2, Pop 1, Push 1+2\n");
    printf("                Stack: [3]\n");
    printf("  print        // Pop and print 3\n");
    printf("  halt\n\n");
    
    printf("Stack-based bytecode:\n");
    int bytecode1[] = {1, 1, 1, 2, 3, 5, 6};
    const char* ops[] = {"", "iconst", "iadd", "print", "halt"};
    printf("  [");
    for (int i = 0; i < 7; i++) {
        if (bytecode1[i] == 1 || bytecode1[i] == 2) {
            printf("%s %d", ops[bytecode1[i]], bytecode1[i+1]);
            i++;
        } else {
            printf("%s", ops[bytecode1[i]]);
        }
        if (i < 6) printf(", ");
    }
    printf("]\n\n");
}

void print_register_based_vm() {
    printf("=== Register-based VM ===\n\n");
    
    printf("Computing 1 + 2:\n\n");
    printf("Register Operations:\n");
    printf("  LOADK R0, 1    // R0 = 1\n");
    printf("  LOADK R1, 2    // R1 = 2\n");
    printf("  ADD R2, R0, R1 // R2 = R0 + R1\n");
    printf("  PRINT R2        // Print R2\n");
    printf("  HALT\n\n");
    
    printf("Register bytecode:\n");
    printf("  LOADK  0, 1    // R0 = 1\n");
    printf("  LOADK  1, 2    // R1 = 2\n");
    printf("  ADD    2, 0, 1 // R2 = R0 + R1\n");
    printf("  PRINT  2\n");
    printf("  HALT\n\n");
}

int main() {
    printf("=== Stack-based vs Register-based VM ===\n\n");
    
    print_stack_based_vm();
    print_register_based_vm();
    
    printf("Comparison:\n");
    printf("+------------------+------------------+\n");
    printf("|    Stack VM      |   Register VM    |\n");
    printf("+------------------+------------------+\n");
    printf("| Compact bytecode  | Larger bytecode  |\n");
    printf("| Implicit operands | Explicit operands |\n");
    printf("| More stack ops   | Fewer ops        |\n");
    printf("| Simple impl      | Complex impl     |\n");
    printf("| Lua 5.0+        | JavaScript V8    |\n");
    printf("| Python VM       | Dalvik VM        |\n");
    printf("+------------------+------------------+\n");
    
    return 0;
}
