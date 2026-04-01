#include <stdio.h>
#include <stdlib.h>

int main() {
    int* arr = (int*)malloc(10 * sizeof(int));
    for (int i = 0; i < 10; i++) {
        arr[i] = i * i;
    }
    for (int i = 0; i < 10; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    free(arr);
    return 0;
}
