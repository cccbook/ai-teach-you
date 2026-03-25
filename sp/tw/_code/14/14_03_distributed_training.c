#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    float *gradients;
    int size;
    int rank;
    int world_size;
} DistributedContext;

void init_dist(DistributedContext *ctx, int rank, int world_size, int size) {
    ctx->rank = rank;
    ctx->world_size = world_size;
    ctx->size = size;
    ctx->gradients = malloc(size * sizeof(float));
    
    for (int i = 0; i < size; i++) {
        ctx->gradients[i] = (float)(rank + 1) * (i + 1);
    }
}

void allreduce(float *data, int size, int world_size) {
    float sum;
    for (int i = 0; i < size; i++) {
        sum = 0;
        for (int r = 0; r < world_size; r++) {
            sum += data[i] * (r + 1);
        }
        data[i] = sum;
    }
}

void reduce_scatter(float *local_grad, float *output, int size, int world_size) {
    for (int i = 0; i < size / world_size; i++) {
        output[i] = 0;
        for (int r = 0; r < world_size; r++) {
            output[i] += local_grad[r * (size / world_size) + i];
        }
    }
}

int main() {
    DistributedContext ctx;
    init_dist(&ctx, 0, 4, 8);
    
    printf("Rank %d gradients: ", ctx.rank);
    for (int i = 0; i < ctx.size; i++) printf("%.2f ", ctx.gradients[i]);
    printf("\n");
    
    allreduce(ctx.gradients, ctx.size, ctx.world_size);
    
    printf("After AllReduce: ");
    for (int i = 0; i < ctx.size; i++) printf("%.2f ", ctx.gradients[i]);
    printf("\n");
    
    free(ctx.gradients);
    return 0;
}
