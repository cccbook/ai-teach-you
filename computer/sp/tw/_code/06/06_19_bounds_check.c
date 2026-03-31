#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int lower_bound;
    int upper_bound;
    bool bounds_enforced;
} LoopInfo;

typedef struct {
    int access_min;
    int access_max;
    bool is_bounds_check;
} Statement;

bool bounds_are_enforced(LoopInfo* loop) {
    return loop->bounds_enforced;
}

bool is_bounds_check(Statement* stmt) {
    return stmt->is_bounds_check;
}

bool is_redundant_due_to_loop(LoopInfo* loop, Statement* stmt) {
    if (!bounds_are_enforced(loop)) return false;
    
    if (stmt->access_min >= loop->lower_bound &&
        stmt->access_max <= loop->upper_bound) {
        return true;
    }
    
    return false;
}

void eliminate_bounds_check(Statement* stmt) {
    printf("  ELIMINATED: Bounds check on [%d, %d] (redundant)\n",
           stmt->access_min, stmt->access_max);
}

void process_loop(LoopInfo* loop, Statement stmts[], int n) {
    printf("Loop bounds: [%d, %d], enforced: %s\n",
           loop->lower_bound, loop->upper_bound,
           loop->bounds_enforced ? "YES" : "NO");
    
    if (!bounds_are_enforced(loop)) {
        printf("  Cannot eliminate bounds checks (bounds not enforced)\n");
        return;
    }
    
    for (int i = 0; i < n; i++) {
        if (is_bounds_check(&stmts[i])) {
            if (is_redundant_due_to_loop(loop, &stmts[i])) {
                eliminate_bounds_check(&stmts[i]);
            } else {
                printf("  KEEP: Bounds check [%d, %d] (may exceed loop bounds)\n",
                       stmts[i].access_min, stmts[i].access_max);
            }
        }
    }
}

int main() {
    printf("=== Bounds Check Elimination ===\n\n");
    
    LoopInfo safe_loop = {0, 99, true};
    
    Statement stmts[] = {
        {0, 99, true},
        {-5, 50, true},
        {50, 150, true},
        {10, 20, false}
    };
    int n = 4;
    
    printf("Test 1: Safe loop with enforced bounds [0, 99]\n");
    process_loop(&safe_loop, stmts, n);
    
    printf("\nTest 2: Unsafe loop\n");
    LoopInfo unsafe_loop = {0, 99, false};
    process_loop(&unsafe_loop, stmts, n);
    
    printf("\nWhen Bounds Checks Can Be Eliminated:\n");
    printf("  1. Loop bounds are statically determinable\n");
    printf("  2. Array access provably within bounds\n");
    printf("  3. Index already validated by previous check\n");
    printf("  4. After range analysis proves safety\n");
    
    printf("\nBenefits:\n");
    printf("  - Eliminates branch overhead\n");
    printf("  - Enables vectorization\n");
    printf("  - Reduces code size\n");
    
    return 0;
}
