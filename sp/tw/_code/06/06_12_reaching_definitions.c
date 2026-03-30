#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_BLOCKS 10
#define MAX_DEFS 20

typedef struct {
    int id;
    int gen[MAX_DEFS];
    int gen_count;
    int kill[MAX_DEFS];
    int kill_count;
    int pred[MAX_BLOCKS];
    int pred_count;
    int out[MAX_DEFS];
    int out_count;
} Block;

void reaching_definitions_analysis(Block blocks[], int n) {
    printf("=== Reaching Definitions Analysis ===\n\n");
    
    for (int i = 0; i < n; i++) {
        blocks[i].out_count = 0;
    }
    
    int changed = 1;
    int iteration = 0;
    
    while (changed && iteration < 100) {
        changed = 0;
        iteration++;
        
        printf("Iteration %d:\n", iteration);
        
        for (int i = 0; i < n; i++) {
            int new_out[MAX_DEFS];
            int new_count = 0;
            
            for (int p = 0; p < blocks[i].pred_count; p++) {
                int pred_id = blocks[i].pred[p];
                for (int k = 0; k < blocks[pred_id].out_count; k++) {
                    new_out[new_count++] = blocks[pred_id].out[k];
                }
            }
            
            int temp[MAX_DEFS];
            int temp_count = 0;
            for (int k = 0; k < new_count; k++) {
                int def = new_out[k];
                int killed = 0;
                for (int j = 0; j < blocks[i].kill_count; j++) {
                    if (blocks[i].kill[j] == def) {
                        killed = 1;
                        break;
                    }
                }
                if (!killed) {
                    temp[temp_count++] = def;
                }
            }
            
            for (int j = 0; j < blocks[i].gen_count; j++) {
                temp[temp_count++] = blocks[i].gen[j];
            }
            
            if (temp_count != blocks[i].out_count ||
                memcmp(temp, blocks[i].out, temp_count * sizeof(int)) != 0) {
                changed = 1;
                blocks[i].out_count = temp_count;
                memcpy(blocks[i].out, temp, temp_count * sizeof(int));
            }
            
            printf("  Block %d: OUT = {", i);
            for (int k = 0; k < blocks[i].out_count; k++) {
                printf("%d%s", blocks[i].out[k], k < blocks[i].out_count - 1 ? ", " : "");
            }
            printf("}\n");
        }
    }
    
    printf("\nConverged after %d iterations\n", iteration);
}

int main() {
    Block blocks[3];
    
    blocks[0].id = 0;
    blocks[0].gen[0] = 0;
    blocks[0].gen_count = 1;
    blocks[0].kill[0] = 2;
    blocks[0].kill_count = 1;
    blocks[0].pred_count = 0;
    
    blocks[1].id = 1;
    blocks[1].gen[0] = 1;
    blocks[1].gen_count = 1;
    blocks[1].kill[0] = 0;
    blocks[1].kill_count = 1;
    blocks[1].pred[0] = 0;
    blocks[1].pred_count = 1;
    
    blocks[2].id = 2;
    blocks[2].gen[0] = 2;
    blocks[2].gen_count = 1;
    blocks[2].kill[0] = 0;
    blocks[2].kill_count = 1;
    blocks[2].pred[0] = 0;
    blocks[2].pred[1] = 1;
    blocks[2].pred_count = 2;
    
    printf("CFG:\n");
    printf("  Block 0: a = 10  (gen: {0}, kill: {2})\n");
    printf("  Block 1: a = 20  (gen: {1}, kill: {0})\n");
    printf("  Block 2: b = a   (gen: {2}, kill: {0})\n\n");
    
    reaching_definitions_analysis(blocks, 3);
    
    printf("\nDataflow Equations:\n");
    printf("  IN[B] = union of OUT[P] for all predecessors P\n");
    printf("  OUT[B] = GEN[B] union (IN[B] - KILL[B])\n");
    
    return 0;
}
