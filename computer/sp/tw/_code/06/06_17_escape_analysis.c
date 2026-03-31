#include <stdio.h>
#include <string.h>

typedef enum {
    ESCAPE_LOCAL,
    ESCAPE_ARG,
    ESCAPE_GLOBAL
} EscapeLevel;

typedef struct {
    char name[32];
    EscapeLevel level;
} ObjectInfo;

typedef struct {
    int is_global;
    int is_return;
    int is_store_through_pointer;
    int is_passed_as_argument;
} UseInfo;

EscapeLevel analyze_object_escape(UseInfo uses[], int use_count) {
    EscapeLevel escape = ESCAPE_LOCAL;
    
    for (int i = 0; i < use_count; i++) {
        if (uses[i].is_global) {
            return ESCAPE_GLOBAL;
        }
        if (uses[i].is_return) {
            return ESCAPE_GLOBAL;
        }
        if (uses[i].is_store_through_pointer) {
            return ESCAPE_ARG;
        }
        if (uses[i].is_passed_as_argument) {
            escape = ESCAPE_ARG;
        }
    }
    
    return escape;
}

const char* escape_level_str(EscapeLevel level) {
    switch (level) {
        case ESCAPE_LOCAL: return "Local (No Escape)";
        case ESCAPE_ARG: return "Arg Escape";
        case ESCAPE_GLOBAL: return "Global Escape";
    }
    return "Unknown";
}

void stack_allocate(ObjectInfo* obj, EscapeLevel level) {
    if (level == ESCAPE_LOCAL) {
        obj->level = ESCAPE_LOCAL;
        printf("  %s: STACK allocation (does not escape)\n", obj->name);
    } else {
        obj->level = ESCAPE_GLOBAL;
        printf("  %s: HEAP allocation (escapes)\n", obj->name);
    }
}

int main() {
    printf("=== Escape Analysis ===\n\n");
    
    ObjectInfo objects[] = {
        {"local_obj", ESCAPE_LOCAL},
        {"passed_obj", ESCAPE_ARG},
        {"global_obj", ESCAPE_GLOBAL}
    };
    
    printf("Escape Levels:\n");
    printf("  1. No Escape: Object used only in creating function\n");
    printf("  2. Arg Escape: Object passed as argument\n");
    printf("  3. Global Escape: Object escapes to global scope or heap\n\n");
    
    UseInfo test_uses1[] = {
        {.is_global = 0, .is_return = 0, .is_store_through_pointer = 0, .is_passed_as_argument = 0}
    };
    
    UseInfo test_uses2[] = {
        {.is_global = 0, .is_return = 0, .is_store_through_pointer = 0, .is_passed_as_argument = 1}
    };
    
    UseInfo test_uses3[] = {
        {.is_global = 1, .is_return = 0, .is_store_through_pointer = 0, .is_passed_as_argument = 0}
    };
    
    printf("Analysis Results:\n");
    
    EscapeLevel level1 = analyze_object_escape(test_uses1, 1);
    printf("  Test object 1: %s\n", escape_level_str(level1));
    
    EscapeLevel level2 = analyze_object_escape(test_uses2, 1);
    printf("  Test object 2: %s\n", escape_level_str(level2));
    
    EscapeLevel level3 = analyze_object_escape(test_uses3, 1);
    printf("  Test object 3: %s\n", escape_level_str(level3));
    
    printf("\nStack Allocation:\n");
    stack_allocate(&objects[0], ESCAPE_LOCAL);
    stack_allocate(&objects[1], ESCAPE_ARG);
    stack_allocate(&objects[2], ESCAPE_GLOBAL);
    
    printf("\nBenefits of Stack Allocation:\n");
    printf("  - Faster allocation/deallocation\n");
    printf("  - No GC needed\n");
    printf("  - Better cache locality\n");
    
    return 0;
}
