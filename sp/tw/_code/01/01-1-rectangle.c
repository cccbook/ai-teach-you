#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int width;
    int height;
} Rectangle;

Rectangle* rectangle_create(int width, int height) {
    Rectangle* rect = (Rectangle*)malloc(sizeof(Rectangle));
    rect->width = width;
    rect->height = height;
    return rect;
}

int rectangle_area(Rectangle* rect) {
    return rect->width * rect->height;
}

void rectangle_destroy(Rectangle* rect) {
    free(rect);
}

int main() {
    Rectangle* rect = rectangle_create(5, 3);
    printf("Area = %d\n", rectangle_area(rect));
    rectangle_destroy(rect);
    return 0;
}
