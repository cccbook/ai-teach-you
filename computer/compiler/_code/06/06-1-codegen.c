#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "06-1-codegen.h"

CodeGen* createCodeGen(FILE* output) {
    CodeGen* gen = (CodeGen*)malloc(sizeof(CodeGen));
    gen->output = output;
    gen->tempCount = 0;
    gen->labelCount = 0;
    return gen;
}

char* generateTemp(CodeGen* gen) {
    char* temp = (char*)malloc(16);
    sprintf(temp, "%%t%d", gen->tempCount++);
    return temp;
}

char* generateLabel(CodeGen* gen) {
    char* label = (char*)malloc(16);
    sprintf(label, "label%d", gen->labelCount++);
    return label;
}

void generateExpression(ASTNode* node, CodeGen* gen) {
    if (!node) return;
    
    switch (node->type) {
        case AST_NUMBER: {
            char* temp = generateTemp(gen);
            fprintf(gen->output, "  %s = add i32 0, %d\n", temp, node->value);
            break;
        }
        case AST_VARIABLE: {
            char* temp = generateTemp(gen);
            fprintf(gen->output, "  %s = load i32, i32* @%s\n", temp, node->name);
            break;
        }
        case AST_BINOP_ADD: {
            char* leftTemp = generateTemp(gen);
            char* rightTemp = generateTemp(gen);
            generateExpression(node->left, gen);
            generateExpression(node->right, gen);
            fprintf(gen->output, "  %s = add i32 %s, %s\n", 
                leftTemp, leftTemp, rightTemp);
            break;
        }
        case AST_BINOP_SUB: {
            char* leftTemp = generateTemp(gen);
            char* rightTemp = generateTemp(gen);
            generateExpression(node->left, gen);
            generateExpression(node->right, gen);
            fprintf(gen->output, "  %s = sub i32 %s, %s\n", 
                leftTemp, leftTemp, rightTemp);
            break;
        }
        case AST_BINOP_MUL: {
            char* leftTemp = generateTemp(gen);
            char* rightTemp = generateTemp(gen);
            generateExpression(node->left, gen);
            generateExpression(node->right, gen);
            fprintf(gen->output, "  %s = mul i32 %s, %s\n", 
                leftTemp, leftTemp, rightTemp);
            break;
        }
    }
}

void generateStatement(ASTNode* node, CodeGen* gen) {
    if (!node) return;
    
    switch (node->type) {
        case AST_RETURN:
            generateExpression(node->left, gen);
            fprintf(gen->output, "  ret i32 %s\n", generateTemp(gen));
            break;
            
        case AST_DECL:
            fprintf(gen->output, "  @%s = alloca i32\n", node->name);
            break;
            
        case AST_ASSIGN:
            generateExpression(node->left, gen);
            fprintf(gen->output, "  store i32 %s, i32* @%s\n", 
                generateTemp(gen), node->name);
            break;
            
        case AST_IF: {
            char* elseLabel = generateLabel(gen);
            char* endLabel = generateLabel(gen);
            fprintf(gen->output, "  br i1 %%cond, label %%then, label %s\n", elseLabel);
            fprintf(gen->output, "then:\n");
            generateStatement(node->right, gen);
            fprintf(gen->output, "  br label %s\n", endLabel);
            fprintf(gen->output, "%s:\n", elseLabel);
            if (node->third) {
                generateStatement(node->third, gen);
            }
            fprintf(gen->output, "  br label %s\n", endLabel);
            fprintf(gen->output, "%s:\n", endLabel);
            break;
        }
    }
}

void generateFunction(ASTNode* node, CodeGen* gen) {
    fprintf(gen->output, "define i32 @%s() {\n", node->name);
    generateStatement(node->right, gen);
    fprintf(gen->output, "}\n");
}

void generate(ASTNode* node, CodeGen* gen) {
    if (!node) return;
    
    fprintf(gen->output, "; Module\n");
    fprintf(gen->output, "target datalayout = \"e-m:o-i64:64-f80:128-n8:16:32:64-S128\"\n");
    fprintf(gen->output, "target triple = \"x86_64-apple-darwin\"\n\n");
    
    ASTNode* child = node->left;
    while (child) {
        if (child->type == AST_FUNCTION) {
            generateFunction(child, gen);
        }
        child = child->next;
    }
}

int main() {
    FILE* output = fopen("output.ll", "w");
    CodeGen* gen = createCodeGen(output);
    
    fprintf(output, "; Generated LLVM IR\n");
    fprintf(output, "; This is a demonstration of code generation\n");
    
    fclose(output);
    printf("Code generation module created.\n");
    
    return 0;
}
