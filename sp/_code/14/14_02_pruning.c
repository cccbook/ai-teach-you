#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define ARRAY_SIZE 20

void prune_weights(float* weights, int size, float threshold) {
    int pruned = 0;
    for (int i = 0; i < size; i++) {
        if (weights[i] > -threshold && weights[i] < threshold) {
            weights[i] = 0.0f;
            pruned++;
        }
    }
    printf("Pruned: %d/%d weights (%.1f%%)\n", pruned, size, 100.0f * pruned / size);
}

float calculate_sparsity(float* weights, int size) {
    int zero_count = 0;
    for (int i = 0; i < size; i++) {
        if (fabsf(weights[i]) < 1e-6f) {
            zero_count++;
        }
    }
    return 100.0f * zero_count / size;
}

void print_weights(float* weights, int size, int cols) {
    printf("[");
    for (int i = 0; i < size; i++) {
        if (fabsf(weights[i]) < 1e-6f) {
            printf("  0  ");
        } else {
            printf("%5.2f", weights[i]);
        }
        if ((i + 1) % cols == 0 && i < size - 1) {
            printf("\n       ");
        }
        if (i < size - 1) printf(" ");
    }
    printf("]\n");
}

int main() {
    printf("=== Weight Pruning Demo ===\n\n");
    
    printf("Pruning: Setting small weights to zero\n");
    printf("Threshold: weights with |value| < threshold are pruned\n\n");
    
    float weights[ARRAY_SIZE];
    srand(42);
    for (int i = 0; i < ARRAY_SIZE; i++) {
        weights[i] = ((float)rand() / RAND_MAX - 0.5f) * 2.0f;
    }
    
    printf("Before pruning (4x5 matrix):\n");
    print_weights(weights, ARRAY_SIZE, 5);
    printf("Sparsity: %.1f%%\n\n", calculate_sparsity(weights, ARRAY_SIZE));
    
    float thresholds[] = {0.1f, 0.25f, 0.5f};
    
    for (int t = 0; t < 3; t++) {
        float original[ARRAY_SIZE];
        for (int i = 0; i < ARRAY_SIZE; i++) {
            original[i] = weights[i];
        }
        
        printf("=== Threshold = %.2f ===\n", thresholds[t]);
        prune_weights(original, ARRAY_SIZE, thresholds[t]);
        printf("After pruning:\n");
        print_weights(original, ARRAY_SIZE, 5);
        printf("Sparsity: %.1f%%\n\n", calculate_sparsity(original, ARRAY_SIZE));
    }
    
    printf("=== Pruning Strategies ===\n");
    printf("1. Magnitude pruning: Prune smallest absolute values\n");
    printf("2. Gradient pruning: Prune weights with small gradients\n");
    printf("3. Random pruning: Randomly prune weights\n");
    printf("4. Layer-wise pruning: Different thresholds per layer\n");
    
    printf("\n=== Benefits ===\n");
    printf("- Reduced model size\n");
    printf("- Faster inference\n");
    printf("- Lower memory bandwidth requirements\n");
    printf("- Potential for improved generalization\n");
    
    return 0;
}
