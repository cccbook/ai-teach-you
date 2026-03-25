#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char input[100];
int pos = 0;
int current_char;

void skip_whitespace() {
    while (input[pos] == ' ' || input[pos] == '\t') {
        pos++;
    }
}

int parse_number() {
    skip_whitespace();
    int result = 0;
    while (input[pos] >= '0' && input[pos] <= '9') {
        result = result * 10 + (input[pos] - '0');
        pos++;
    }
    return result;
}

int parse_factor();
int parse_expr();

int parse_factor() {
    skip_whitespace();
    
    if (input[pos] == '(') {
        pos++;
        int result = parse_expr();
        skip_whitespace();
        if (input[pos] == ')') {
            pos++;
        }
        return result;
    }
    
    return parse_number();
}

int parse_term() {
    skip_whitespace();
    int result = parse_factor();
    
    while (1) {
        skip_whitespace();
        if (input[pos] == '*') {
            pos++;
            int rhs = parse_factor();
            printf("  Reduce: term -> term * factor\n");
            result = result * rhs;
        } else if (input[pos] == '/') {
            pos++;
            int rhs = parse_factor();
            printf("  Reduce: term -> term / factor\n");
            result = result / rhs;
        } else {
            break;
        }
    }
    return result;
}

int parse_expr() {
    skip_whitespace();
    int result = parse_term();
    
    while (1) {
        skip_whitespace();
        if (input[pos] == '+') {
            pos++;
            int rhs = parse_term();
            printf("  Reduce: expr -> expr + expr\n");
            result = result + rhs;
        } else if (input[pos] == '-') {
            pos++;
            int rhs = parse_term();
            printf("  Reduce: expr -> expr - expr\n");
            result = result - rhs;
        } else {
            break;
        }
    }
    return result;
}

int main() {
    printf("=== Recursive Descent Parser (C equivalent of PLY) ===\n\n");
    
    printf("Tokens: NUMBER, PLUS, MINUS, MULT, DIV, LPAREN, RPAREN\n\n");
    
    printf("Grammar:\n");
    printf("  expr   -> expr + expr | expr - expr | term\n");
    printf("  term   -> term * factor | term / factor | factor\n");
    printf("  factor -> NUMBER | ( expr )\n\n");
    
    strcpy(input, "2 + 3 * 4");
    printf("Input: \"%s\"\n\n", input);
    printf("Parsing steps:\n");
    
    int result = parse_expr();
    
    printf("\nResult: %d\n", result);
    printf("\nOperator precedence:\n");
    printf("  * and / have higher precedence than + and -\n");
    printf("  So 2 + 3 * 4 = 2 + (3 * 4) = 14, not (2 + 3) * 4 = 20\n");
    
    printf("\n\nAlternative input: (2 + 3) * 4\n");
    strcpy(input, "(2 + 3) * 4");
    printf("Parsing steps:\n");
    pos = 0;
    result = parse_expr();
    printf("\nResult: %d\n", result);
    
    return 0;
}
