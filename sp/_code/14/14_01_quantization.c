#include <stdio.h>
#include <math.h>

void quantize_fp32_to_int8(float* input, int8_t* output, int size, float scale) {
    for (int i = 0; i < size; i++) {
        float val = input[i] / scale;
        if (val > 127.0f) val = 127.0f;
        if (val < -128.0f) val = -128.0f;
        output[i] = (int8_t)(val + 0.5f);
    }
}

void dequantize_int8_to_fp32(int8_t* input, float* output, int size, float scale) {
    for (int i = 0; i < size; i++) {
        output[i] = (float)input[i] * scale;
    }
}

float find_scale(float* input, int size, float min_val, float max_val) {
    float abs_max = fabsf(min_val) > fabsf(max_val) ? fabsf(min_val) : fabsf(max_val);
    if (abs_max < 1e-6f) abs_max = 1e-6f;
    return abs_max / 127.0f;
}

void print_array(const char* name, float* arr, int size) {
    printf("%s: ", name);
    for (int i = 0; i < size; i++) {
        printf("%.2f ", arr[i]);
    }
    printf("\n");
}

void print_int8_array(const char* name, int8_t* arr, int size) {
    printf("%s: ", name);
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    printf("=== Quantization Demo ===\n\n");
    
    printf("Quantization: Converting FP32 to INT8\n");
    printf("Scale factor: FP32 range / INT8 range\n\n");
    
    float input[] = {1.0f, 2.0f, 3.0f, 4.0f, -1.0f, -2.0f, -3.0f, -4.0f};
    int size = 8;
    
    print_array("Original (FP32)", input, size);
    
    float min_val = input[0], max_val = input[0];
    for (int i = 1; i < size; i++) {
        if (input[i] < min_val) min_val = input[i];
        if (input[i] > max_val) max_val = input[i];
    }
    
    float scale = find_scale(input, size, min_val, max_val);
    printf("Scale: %.4f\n\n", scale);
    
    int8_t quantized[8];
    quantize_fp32_to_int8(input, quantized, size, scale);
    print_int8_array("Quantized (INT8)", quantized, size);
    
    float dequantized[8];
    dequantize_int8_to_fp32(quantized, dequantized, size, scale);
    print_array("Dequantized (FP32)", dequantized, size);
    
    printf("\n=== Quantization Error ===\n");
    float total_error = 0.0f;
    for (int i = 0; i < size; i++) {
        float error = fabsf(input[i] - dequantized[i]);
        printf("  [%d] original=%.2f, dequantized=%.2f, error=%.2f\n", 
               i, input[i], dequantized[i], error);
        total_error += error;
    }
    printf("Average error: %.4f\n", total_error / size);
    
    printf("\n=== Memory Savings ===\n");
    printf("FP32: %d bytes\n", size * 4);
    printf("INT8: %d bytes\n", size * 1);
    printf("Compression ratio: %.1fx\n", (float)(size * 4) / (size * 1));
    
    return 0;
}
