#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_BLOCKS 10
#define MAX_VARS 20

typedef struct {
    int id;
    int use[MAX_VARS];
    int use_count;
    int def[MAX_VARS];
    int def_count;
    int succ[MAX_BLOCKS];
    int succ_count;
    int in[MAX_VARS];
    int in_count;
    int out[MAX_VARS];
    int out_count;
} Block;

void print_set(char* name, int set[], int count) {
    printf("%s = {", name);
    for (int i = 0; i < count; i++) {
        printf("%c%s", 'a' + set[i], i < count - 1 ? ", " : "");
    }
    printf("}\n");
}

void liveness_analysis(Block blocks[], int n) {
    printf("=== Liveness Analysis ===\n\n");
    
    for (int i = 0; i < n; i++) {
        blocks[i].in_count = 0;
        blocks[i].out_count = 0;
    }
    
    int changed = 1;
    int iteration = 0;
    
    while (changed && iteration < 100) {
        changed = 0;
        iteration++;
        
        printf("Iteration %d:\n", iteration);
        
        for (int i = n - 1; i >= 0; i--) {
            int new_out[MAX_VARS] = {0};
            int new_out_count = 0;
            
            for (int s = 0; s < blocks[i].succ_count; s++) {
                int succ_id = blocks[i].succ[s];
                for (int k = 0; k < blocks[succ_id].in_count; k++) {
                    int var = blocks[succ_id].in[k];
                    int already = 0;
                    for (int j = 0; j < new_out_count; j++) {
                        if (new_out[j] == var) {
                            already = 1;
                            break;
                        }
                    }
                    if (!already) {
                        new_out[new_out_count++] = var;
                    }
                }
            }
            
            int new_in[MAX_VARS];
            int new_in_count = 0;
            
            for (int k = 0; k < new_out_count; k++) {
                new_in[new_in_count++] = new_out[k];
            }
            for (int k = 0; k < blocks[i].use_count; k++) {
                int var = blocks[i].use[k];
                int already = 0;
                for (int j = 0; j < new_in_count; j++) {
                    if (new_in[j] == var) {
                        already = 1;
                        break;
                    }
                }
                if (!already) {
                    new_in[new_in_count++] = var;
                }
            }
            
            for (int k = 0; k < blocks[i].def_count; k++) {
                int var = blocks[i].def[k];
                int new_in_temp[MAX_VARS];
                int new_in_temp_count = 0;
                for (int j = 0; j < new_in_count; j++) {
                    if (new_in[j] != var) {
                        new_in_temp[new_in_temp_count++] = new_in[j];
                    }
                }
                memcpy(new_in, new_in_temp, sizeof(int) * new_in_temp_count);
                new_in_count = new_in_temp_count;
            }
            
            if (new_out_count != blocks[i].out_count ||
                memcmp(new_out, blocks[i].out, new_out_count * sizeof(int)) != 0) {
                changed = 1;
                blocks[i].out_count = new_out_count;
                memcpy(blocks[i].out, new_out, new_out_count * sizeof(int));
            }
            
            if (new_in_count != blocks[i].in_count ||
                memcmp(new_in, blocks[i].in, new_in_count * sizeof(int)) != 0) {
                changed = 1;
                blocks[i].in_count = new_in_count;
                memcpy(blocks[i].in, new_in, new_in_count * sizeof(int));
            }
            
            printf("  Block %d: ", i);
            print_set("IN", blocks[i].in, blocks[i].in_count);
            printf("          ");
            print_set("OUT", blocks[i].out, blocks[i].out_count);
        }
    }
    
    printf("\nConverged after %d iterations\n", iteration);
}

int main() {
    Block blocks[3];
    
    blocks[0].id = 0;
    blocks[0].use[0] = 0;
    blocks[0].use_count = 1;
    blocks[0].def[0] = 0;
    blocks[0].def_count = 1;
    blocks[0].succ[0] = 1;
    blocks[0].succ_count = 1;
    
    blocks[1].id = 1;
    blocks[1].use[0] = 0;
    blocks[1].use[1] = 1;
    blocks[1].use_count = 2;
    blocks[1].def[0] = 1;
    blocks[1].def_count = 1;
    blocks[1].succ[0] = 2;
    blocks[1].succ_count = 1;
    
    blocks[2].id = 2;
    blocks[2].use[0] = 0;
    blocks[2].use[1] = 1;
    blocks[2].use_count = 2;
    blocks[2].def[0] = 2;
    blocks[2].def_count = 1;
    blocks[2].succ_count = 0;
    
    printf("CFG:\n");
    printf("  Block 0: b = a    (use: {a}, def: {b})\n");
    printf("  Block 1: c = a + b (use: {a,b}, def: {c})\n");
    printf("  Block 2: d = a + c (use: {a,c}, def: {d})\n\n");
    
    liveness_analysis(blocks, 3);
    
    printf("\nDataflow Equations:\n");
    printf("  OUT[B] = union of IN[S] for all successors S\n");
    printf("  IN[B] = USE[B] union (OUT[B] - DEF[B])\n");
    
    return 0;
}
