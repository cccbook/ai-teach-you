#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    char name[32];
    int body_size;
    int is_leaf;
    int is_recursive;
    int execution_freq;
} Function;

int has_static_vars(Function* func) {
    return 0;
}

int should_inline(Function* call_site, Function* callee) {
    if (callee->is_recursive) {
        printf("  NOT inlining: %s is recursive\n", callee->name);
        return 0;
    }
    
    if (callee->body_size > 100) {
        printf("  NOT inlining: %s body too large (%d statements)\n",
               callee->name, callee->body_size);
        return 0;
    }
    
    if (has_static_vars(callee)) {
        printf("  NOT inlining: %s has static variables\n", callee->name);
        return 0;
    }
    
    if (callee->is_leaf && callee->body_size < 20) {
        printf("  Inlining: %s is small leaf function\n", callee->name);
        return 1;
    }
    
    if (call_site->execution_freq > 1000) {
        printf("  Inlining: %s is called frequently (%d times)\n",
               callee->name, call_site->execution_freq);
        return 1;
    }
    
    return 0;
}

void inline_function(char* result, Function* call_site, Function* callee) {
    printf("Inlining %s at call site %s:\n", callee->name, call_site->name);
    printf("  1. Copy function body\n");
    printf("  2. Substitute parameters with arguments\n");
    printf("  3. Handle return statements\n");
    printf("  4. Insert inlined code\n");
    
    sprintf(result, "// Inlined %s\n%s", callee->name,
            callee->is_leaf ? "// Leaf function - efficient\n" : "// Non-leaf function\n");
}

int main() {
    Function square = {"square", 3, 1, 0, 0};
    Function big_func = {"big_func", 150, 0, 0, 100};
    Function hot_loop = {"hot_loop", 15, 1, 0, 5000};
    Function recursive = {"factorial", 20, 1, 1, 0};
    
    Function caller = {"caller", 50, 0, 0, 2000};
    
    printf("=== Function Inlining Analysis ===\n\n");
    
    char result[256];
    
    printf("Test 1: Small leaf function\n");
    inline_function(result, &caller, &square);
    printf("  should_inline: %s\n\n", should_inline(&caller, &square) ? "YES" : "NO");
    
    printf("Test 2: Large function\n");
    inline_function(result, &caller, &big_func);
    printf("  should_inline: %s\n\n", should_inline(&caller, &big_func) ? "YES" : "NO");
    
    printf("Test 3: Hot path function\n");
    inline_function(result, &caller, &hot_loop);
    printf("  should_inline: %s\n\n", should_inline(&caller, &hot_loop) ? "YES" : "NO");
    
    printf("Test 4: Recursive function\n");
    inline_function(result, &caller, &recursive);
    printf("  should_inline: %s\n\n", should_inline(&caller, &recursive) ? "YES" : "NO");
    
    printf("Inlining Benefits:\n");
    printf("  - Eliminates call overhead\n");
    printf("  - Enables cross-function optimizations\n");
    printf("  - Improves cache locality\n\n");
    
    printf("Inlining Costs:\n");
    printf("  - Code bloat\n");
    printf("  - Increased register pressure\n");
    printf("  - Compile time increase\n");
    
    return 0;
}
