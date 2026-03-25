#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    float value;
} Tensor;

typedef struct {
    Tensor *data;
    int channels;
    int height;
    int width;
} TensorArray;

void quantize_tensor(Tensor *input, int size, int8_t *output, float scale) {
    for (int i = 0; i < size; i++) {
        float val = input[i].value / scale;
        if (val > 127) val = 127;
        if (val < -128) val = -128;
        output[i] = (int8_t)(val + 0.5f);
    }
}

void dequantize_tensor(int8_t *input, int size, float *output, float scale) {
    for (int i = 0; i < size; i++) {
        output[i] = (float)input[i] * scale;
    }
}

int main() {
    int size = 4;
    Tensor input[] = {{1.0f}, {2.0f}, {3.0f}, {4.0f}};
    int8_t quantized[4];
    float dequantized[4];
    float scale = 0.1f;
    
    printf("Original: ");
    for (int i = 0; i < size; i++) printf("%.2f ", input[i].value);
    printf("\n");
    
    quantize_tensor(input, size, quantized, scale);
    printf("Quantized: ");
    for (int i = 0; i < size; i++) printf("%d ", quantized[i]);
    printf("\n");
    
    dequantize_tensor(quantized, size, dequantized, scale);
    printf("Dequantized: ");
    for (int i = 0; i < size; i++) printf("%.2f ", dequantized[i]);
    printf("\n");
    
    return 0;
}
