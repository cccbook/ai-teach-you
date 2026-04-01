#ifndef CODEGEN_H
#define CODEGEN_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../03/03-1-ast.h"

typedef struct {
    FILE* output;
    int tempCount;
    int labelCount;
} CodeGen;

CodeGen* createCodeGen(FILE* output);
char* generateTemp(CodeGen* gen);
char* generateLabel(CodeGen* gen);
void generate(ASTNode* node, CodeGen* gen);
void generateFunction(ASTNode* node, CodeGen* gen);
void generateExpression(ASTNode* node, CodeGen* gen);
void generateStatement(ASTNode* node, CodeGen* gen);

#endif
