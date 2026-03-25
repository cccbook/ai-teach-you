#include <stdio.h>
#include <stdint.h>

typedef union {
    float f;
    uint32_t u;
} FloatBits;

typedef struct {
    uint16_t mantissa : 10;
    uint16_t exponent : 5;
    uint16_t sign : 1;
} Float16;

float fp16_to_fp32(uint16_t h) {
    FloatBits result;
    uint32_t sign = (h & 0x8000) << 16;
    uint32_t exponent = (h & 0x7c00) >> 10;
    uint32_t mantissa = h & 0x03ff;
    
    if (exponent == 0) {
        if (mantissa == 0) {
            result.u = sign;
        } else {
            exponent = 127 - 15 + 1;
            while ((mantissa & 0x0400) == 0) {
                mantissa <<= 1;
                exponent--;
            }
            mantissa &= 0x03ff;
            result.u = sign | ((exponent + 127) << 23) | (mantissa << 13);
        }
    } else if (exponent == 31) {
        result.u = sign | 0x7f800000 | (mantissa << 13);
    } else {
        result.u = sign | ((exponent + 127 - 15) << 23) | (mantissa << 13);
    }
    
    return result.f;
}

uint16_t fp32_to_fp16(float f) {
    FloatBits bits;
    bits.f = f;
    
    uint32_t sign = bits.u >> 16;
    uint32_t exponent = (bits.u >> 23) & 0xff;
    uint32_t mantissa = bits.u & 0x007fffff;
    
    if (exponent == 0) {
        return sign & 0x8000;
    } else if (exponent >= 142) {
        return sign | (exponent > 142 ? 0x7c00 : 0x7bff);
    } else if (exponent <= 112) {
        uint32_t m = mantissa | 0x00800000;
        int shift = 113 - exponent;
        mantissa = (shift < 24) ? (m >> shift) : 0;
        return sign | (mantissa >> 13);
    } else {
        return sign | (((exponent - 112) & 0x1f) << 10) | (mantissa >> 13);
    }
}

int main() {
    printf("=== Mixed Precision Training ===\n\n");
    
    printf("FP32 vs FP16 comparison:\n");
    printf("+-------------+-------------+-------------+\n");
    printf("| Property    | FP32        | FP16        |\n");
    printf("+-------------+-------------+-------------+\n");
    printf("| Bits        | 32          | 16          |\n");
    printf("| Sign        | 1           | 1           |\n");
    printf("| Exponent    | 8           | 5           |\n");
    printf("| Mantissa    | 23          | 10          |\n");
    printf("| Range       | ~1e38       | ~65504      |\n");
    printf("| Precision   | 7 digits    | 3-4 digits  |\n");
    printf("+-------------+-------------+-------------+\n\n");
    
    printf("Memory savings: 2x\n");
    printf("Performance boost: 2-8x (on tensor cores)\n\n");
    
    printf("Conversion example:\n");
    float f = 3.14159f;
    uint16_t h = fp32_to_fp16(f);
    float f2 = fp16_to_fp32(h);
    
    printf("  FP32: %.6f (0x%08x)\n", f, *(uint32_t*)&f);
    printf("  FP16: 0x%04x\n", h);
    printf("  Back to FP32: %.6f\n", f2);
    printf("  Error: %.6f\n", f - f2);
    
    printf("\nMixed precision training pattern:\n");
    printf("  1. Store weights in FP32 (master copy)\n");
    printf("  2. Convert to FP16 for forward/backward\n");
    printf("  3. Convert gradients to FP32 for optimizer\n");
    printf("  4. Update FP32 weights\n\n");
    
    printf("Gradient scaling (to avoid FP16 underflow):\n");
    printf("  1. Scale loss up by factor S\n");
    printf("  2. Backpropagate (larger gradients)\n");
    printf("  3. Unscale before optimizer step\n");
    printf("  4. PyTorch GradScaler handles this automatically\n");
    
    return 0;
}
