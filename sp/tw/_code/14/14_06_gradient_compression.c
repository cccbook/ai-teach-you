#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct {
    float* data;
    int* indices;
    int size;
    int original_size;
} CompressedGradient;

void get_topk_indices(float* grad, int size, int k, int* indices) {
    for (int i = 0; i < size; i++) indices[i] = i;
    
    for (int i = 0; i < k; i++) {
        for (int j = i + 1; j < size; j++) {
            if (fabs(grad[indices[j]]) > fabs(grad[indices[i]])) {
                int temp = indices[i];
                indices[i] = indices[j];
                indices[j] = temp;
            }
        }
    }
}

CompressedGradient* compress_gradient(float* grad, int size, float compress_ratio) {
    int k = (int)(size * compress_ratio);
    
    CompressedGradient* result = (CompressedGradient*)malloc(sizeof(CompressedGradient));
    result->data = (float*)malloc(sizeof(float) * k);
    result->indices = (int*)malloc(sizeof(int) * k);
    result->size = k;
    result->original_size = size;
    
    int* topk = (int*)malloc(sizeof(int) * size);
    get_topk_indices(grad, size, k, topk);
    
    for (int i = 0; i < k; i++) {
        result->data[i] = grad[topk[i]];
        result->indices[i] = topk[i];
    }
    
    free(topk);
    return result;
}

float* decompress_gradient(CompressedGradient* compressed, int original_size) {
    float* grad = (float*)calloc(original_size, sizeof(float));
    
    for (int i = 0; i < compressed->size; i++) {
        grad[compressed->indices[i]] = compressed->data[i];
    }
    
    return grad;
}

int main() {
    printf("=== Gradient Compression (Top-K Sparsification) ===\n\n");
    
    int size = 1000000;
    float* grad = (float*)malloc(sizeof(float) * size);
    
    printf("Original gradient size: %d elements\n", size);
    printf("Compression ratio: 1%%\n\n");
    
    srand(42);
    for (int i = 0; i < size; i++) {
        grad[i] = (float)(rand() % 100) / 100.0f - 0.5f;
    }
    
    printf("Before compression:\n");
    printf("  Size: %d floats = %d bytes\n", size, (int)(size * sizeof(float)));
    
    float compress_ratio = 0.01f;
    CompressedGradient* compressed = compress_gradient(grad, size, compress_ratio);
    
    printf("\nAfter compression:\n");
    printf("  Size: %d floats = %d bytes\n", 
           compressed->size, (int)(compressed->size * (sizeof(float) + sizeof(int))));
    printf("  Compression ratio: %.2fx\n", 
           (float)(size * sizeof(float)) / (compressed->size * (sizeof(float) + sizeof(int))));
    
    float* decompressed = decompress_gradient(compressed, size);
    
    printf("\nAfter decompression:\n");
    printf("  Restored %d elements\n", size);
    printf("  (Only %d elements were non-zero)\n", compressed->size);
    
    free(grad);
    free(compressed->data);
    free(compressed->indices);
    free(compressed);
    free(decompressed);
    
    printf("\nGradient Compression Methods:\n");
    printf("  +------------+----------+-----------+\n");
    printf("  | Method     | Ratio    | Accuracy  |\n");
    printf("  +------------+----------+-----------+\n");
    printf("  | Quantize   | 4x       | Minimal   |\n");
    printf("  | Top-K 1%%  | 100x     | Acceptable|\n");
    printf("  | Top-K 0.1%%| 1000x    | Moderate  |\n");
    printf("  +------------+----------+-----------+\n");
    
    return 0;
}
