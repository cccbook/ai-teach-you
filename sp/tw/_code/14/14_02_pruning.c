#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    float *weights;
    int size;
    float threshold;
} Model;

void init_model(Model *m, int size) {
    m->size = size;
    m->weights = malloc(size * sizeof(float));
    m->threshold = 0.5f;
    
    for (int i = 0; i < size; i++) {
        m->weights[i] = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
    }
}

void prune_weights(Model *m) {
    int pruned = 0;
    for (int i = 0; i < m->size; i++) {
        if (m->weights[i] > -m->threshold && m->weights[i] < m->threshold) {
            m->weights[i] = 0.0f;
            pruned++;
        }
    }
    printf("Pruned %d / %d weights (%.1f%%)\n", pruned, m->size, 100.0f * pruned / m->size);
}

void free_model(Model *m) {
    free(m->weights);
}

int main() {
    Model m;
    init_model(&m, 10);
    
    printf("Original weights: ");
    for (int i = 0; i < m.size; i++) printf("%.2f ", m.weights[i]);
    printf("\n");
    
    prune_weights(&m);
    
    printf("Pruned weights: ");
    for (int i = 0; i < m.size; i++) printf("%.2f ", m.weights[i]);
    printf("\n");
    
    free_model(&m);
    return 0;
}
