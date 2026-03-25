#include <stdio.h>
#include <stdlib.h>

#define MAX_INSTRUCTIONS 100
#define MAX_READY 50

typedef struct {
    int id;
    int depth;
    int issued;
    int ready_at;
} Instruction;

int compare_by_depth(const void* a, const void* b) {
    return ((Instruction*)b)->depth - ((Instruction*)a)->depth;
}

void list_scheduling_demo() {
    printf("=== List Scheduling Algorithm ===\n\n");
    
    Instruction instrs[] = {
        {0, 3, 0, 0},
        {1, 2, 0, 0},
        {2, 4, 0, 0},
        {3, 1, 0, 0},
        {4, 2, 0, 0},
        {5, 3, 0, 0}
    };
    int n = 6;
    
    printf("Instructions with depths:\n");
    for (int i = 0; i < n; i++) {
        printf("  Instr %d: depth=%d\n", instrs[i].id, instrs[i].depth);
    }
    
    printf("\nScheduling steps:\n");
    
    int scheduled[6] = {0};
    int schedule_count = 0;
    int clock = 0;
    int issue_width = 2;
    
    while (schedule_count < n) {
        printf("  Clock %d: ", clock);
        
        Instruction ready[MAX_READY];
        int ready_count = 0;
        
        for (int i = 0; i < n; i++) {
            if (!scheduled[i] && instrs[i].ready_at <= clock) {
                ready[ready_count++] = instrs[i];
            }
        }
        
        qsort(ready, ready_count, sizeof(Instruction), compare_by_depth);
        
        int issued = 0;
        for (int i = 0; i < ready_count && issued < issue_width && schedule_count < n; i++) {
            for (int j = 0; j < n; j++) {
                if (instrs[j].id == ready[i].id && !scheduled[j]) {
                    printf("[%d] ", instrs[j].id);
                    scheduled[j] = 1;
                    schedule_count++;
                    issued++;
                    break;
                }
            }
        }
        
        if (issued == 0) {
            printf("(stall)");
        }
        printf("\n");
        
        clock++;
    }
    
    printf("\nTotal scheduling time: %d cycles\n", clock);
}

int main() {
    printf("List Scheduling Algorithm:\n");
    printf("1. Build dependency graph from CFG\n");
    printf("2. Calculate depth (critical path length) for each instruction\n");
    printf("3. Sort by depth (highest first)\n");
    printf("4. Schedule instructions respecting dependencies\n");
    printf("5. Update ready queue with scheduled instructions\n");
    
    printf("\n");
    list_scheduling_demo();
    
    return 0;
}
