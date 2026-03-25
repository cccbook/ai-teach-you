#include <stdio.h>

int main() {
    int x = 5;
    int y;
    
    y = (x == 10);
    
    printf("x = %d\n", x);
    printf("x == 10 is %s\n", y ? "true" : "false");
    
    return 0;
}
