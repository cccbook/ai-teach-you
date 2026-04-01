#ifndef AST_H
#define AST_H

typedef enum {
    AST_PROGRAM,
    AST_FUNCTION,
    AST_CALL,
    AST_RETURN,
    AST_IF,
    AST_WHILE,
    AST_FOR,
    AST_ASSIGN,
    AST_BINARY_OP,
    AST_UNARY_OP,
    AST_VARIABLE,
    AST_NUMBER,
    AST_DECL,
    AST_PARAM_LIST,
    AST_ARG_LIST,
    AST_BLOCK,
    AST_BINOP_ADD,
    AST_BINOP_SUB,
    AST_BINOP_MUL,
    AST_BINOP_DIV,
    AST_BINOP_LT,
    AST_BINOP_GT,
    AST_BINOP_EQ
} ASTNodeType;

typedef struct ASTNode {
    ASTNodeType type;
    char* name;
    int value;
    struct ASTNode* left;
    struct ASTNode* right;
    struct ASTNode* third;
    struct ASTNode* next;
} ASTNode;

ASTNode* createNode(ASTNodeType type);
ASTNode* createNumber(int value);
ASTNode* createVariable(char* name);
ASTNode* createBinaryOp(ASTNodeType op, ASTNode* left, ASTNode* right);
ASTNode* createFunction(char* name, ASTNode* params, ASTNode* body);
ASTNode* createCall(char* name, ASTNode* args);
ASTNode* createReturn(ASTNode* value);
ASTNode* createIf(ASTNode* condition, ASTNode* thenBranch, ASTNode* elseBranch);
ASTNode* createWhile(ASTNode* condition, ASTNode* body);
ASTNode* createAssign(char* name, ASTNode* value);
ASTNode* createDeclaration(char* name);
void printAST(ASTNode* node, int indent);

#endif
