#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    float* input_data;
    float* output_data;
    float* model_weights;
    int input_size;
    int output_size;
} Model;

Model* model_create(int input_size, int output_size) {
    Model* model = (Model*)malloc(sizeof(Model));
    model->input_size = input_size;
    model->output_size = output_size;
    model->model_weights = (float*)malloc(sizeof(float) * input_size * output_size);
    model->input_data = (float*)malloc(sizeof(float) * input_size);
    model->output_data = (float*)malloc(sizeof(float) * output_size);
    return model;
}

void model_destroy(Model* model) {
    free(model->model_weights);
    free(model->input_data);
    free(model->output_data);
    free(model);
}

void model_forward(Model* model) {
    for (int i = 0; i < model->output_size; i++) {
        model->output_data[i] = 0.0f;
        for (int j = 0; j < model->input_size; j++) {
            model->output_data[i] += model->input_data[j] * 
                model->model_weights[i * model->input_size + j];
        }
    }
}

float* preprocess(void* raw_data, int* size) {
    printf("  [Preprocess] Convert raw data to tensor format\n");
    float* tensor = (float*)malloc(sizeof(float) * 224 * 224 * 3);
    *size = 224 * 224 * 3;
    return tensor;
}

float* postprocess(float* output, int size) {
    printf("  [Postprocess] Convert tensor to response format\n");
    float* response = (float*)malloc(sizeof(float) * size);
    memcpy(response, output, sizeof(float) * size);
    return response;
}

int main() {
    printf("=== TorchServe Handler Pattern (C Concept) ===\n\n");
    
    printf("Inference pipeline:\n\n");
    
    printf("  1. Load model\n");
    printf("     Model* model = model_create(input_size, output_size);\n\n");
    
    printf("  2. Handle request\n");
    printf("     float* preprocess(void* raw_data, int* size) {\n");
    printf("         // Convert raw data to tensor format\n");
    printf("         return tensor;\n");
    printf("     }\n\n");
    
    printf("  3. Inference\n");
    printf("     model_forward(model);\n\n");
    
    printf("  4. Postprocess\n");
    printf("     float* postprocess(float* output, int size) {\n");
    printf("         // Convert tensor to response format\n");
    printf("         return response;\n");
    printf("     }\n\n");
    
    printf("TorchServe model archive (.mar):\n");
    printf("  mymodel.mar/\n");
    printf("    - model.py       (model definition)\n");
    printf("    - handler.py     (inference logic)\n");
    printf("    - model.pt       (trained weights)\n");
    printf("    - index_to_name.json\n\n");
    
    printf("TorchServe deployment:\n");
    printf("  $ torch-model-archiver ... --export-path model_store\n");
    printf("  $ torchserve --model-store model_store --models mymodel=mymodel.mar\n");
    
    printf("\nExample inference flow:\n");
    Model* model = model_create(784, 10);
    printf("  Created model: input=784, output=10\n");
    
    int input_size;
    void* raw_data = NULL;
    float* tensor = preprocess(raw_data, &input_size);
    printf("  Preprocessed: %d elements\n", input_size);
    
    model_forward(model);
    printf("  Forward pass complete\n");
    
    float* response = postprocess(model->output_data, model->output_size);
    printf("  Postprocessed: %d elements\n", model->output_size);
    
    free(tensor);
    free(response);
    model_destroy(model);
    
    return 0;
}
