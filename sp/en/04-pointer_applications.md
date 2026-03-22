# 4. Pointer Applications——Arrays, Strings, and Function Pointers

## 4.1 Advanced Arrays

### 4.1.1 Array Declaration and Initialization

```c
// Declaration
int arr1[5];              // uninitialized
int arr2[5] = {1, 2, 3};  // partially initialized, unspecified = 0
int arr3[] = {1, 2, 3, 4, 5};  // size from initializer
int arr4[5] = {0};        // all initialized to 0

// C99 designated initializers
int arr5[10] = { [0] = 1, [5] = 10 };  // arr5[0]=1, arr5[5]=10, rest=0
```

### 4.1.2 Multi-dimensional Arrays

```c
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

// Equivalent to (contiguous memory)
int flat[12] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
```

Memory layout (Row-Major):
```
matrix[0][0] → matrix[0][1] → matrix[0][2] → matrix[0][3]
      ↓
matrix[1][0] → matrix[1][1] → ...
```

### 4.1.3 Pointers and Multi-dimensional Arrays

```c
int matrix[3][4];

// matrix is a pointer to int[4]
int (*row_ptr)[4] = matrix;  // pointer to one row (4 ints)

// row_ptr[i] is equivalent to matrix[i]
// *(row_ptr + i) is equivalent to matrix[i]
```

## 4.2 String Representation in C

C has no "string" type - strings are **null-terminated character arrays**.

```c
char s1[] = "Hello";  // {'H', 'e', 'l', 'l', 'o', '\0'}
char *s2 = "Hello";   // pointer to first char of string literal
```

### 4.2.1 Strings and Pointers

```c
char str[] = "Hello";
char *p = str;

printf("%c\n", str[0]);    // 'H'
printf("%c\n", p[0]);     // 'H'
printf("%c\n", *(p + 1)); // 'e'
printf("%c\n", *p++);      // 'H', p moves forward
```

### 4.2.2 char Pointer vs char Array

```c
char arr[] = "Hello";  // modifiable array
arr[0] = 'h';          // OK

char *ptr = "Hello";   // points to string literal
// ptr[0] = 'h';       // Error! string literals in read-only memory
```

### 4.2.3 Standard String Functions

```c
// String length
size_t strlen(const char *s) {
    size_t len = 0;
    while (s[len] != '\0') len++;
    return len;
}

// String copy
char *strcpy(char *dest, const char *src) {
    char *p = dest;
    while ((*p++ = *src++) != '\0');
    return dest;
}

// String concatenate
char *strcat(char *dest, const char *src) {
    char *p = dest;
    while (*p) p++;
    while ((*p++ = *src++));
    return dest;
}

// String compare
int strcmp(const char *s1, const char *s2) {
    while (*s1 && (*s1 == *s2)) {
        s1++;
        s2++;
    }
    return (unsigned char)*s1 - (unsigned char)*s2;
}
```

## 4.3 Function Pointers

Function pointers point to functions, storing the function's entry address.

### 4.3.1 Declaring Function Pointers

```c
// Function pointer syntax
int (*func_ptr)(int, int);

// Compare with regular function pointer
int add(int a, int b);      // add is a function
int (*ptr_add)(int, int);   // ptr_add is a function pointer

ptr_add = add;  // pointer points to add
ptr_add = &add; // same as above
```

### 4.3.2 Using Function Pointers to Call Functions

```c
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int (*operation)(int, int);

operation = add;
int result1 = operation(10, 5);   // 15
result1 = (*operation)(10, 5);   // same

operation = sub;
int result2 = operation(10, 5);   // 5
```

### 4.3.3 Function Pointers as Parameters (Callbacks)

```c
int apply(int (*op)(int, int), int a, int b) {
    return op(a, b);
}

int multiply(int a, int b) { return a * b; }

int main() {
    printf("%d\n", apply(add, 10, 5));      // 15
    printf("%d\n", apply(multiply, 10, 5)); // 50
    return 0;
}
```

### 4.3.4 qsort and Function Pointers

`qsort` is C's standard library quicksort, using function pointers for custom comparison:

```c
#include <stdlib.h>

int compare_int(const void *a, const void *b) {
    int ia = *(const int *)a;
    int ib = *(const int *)b;
    return ia - ib;  // ascending order
}

int main() {
    int arr[] = {5, 2, 8, 1, 9, 3};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    qsort(arr, n, sizeof(int), compare_int);
    
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    return 0;
}
```

## 4.4 Pointer Variations

### 4.4.1 Array of Pointers vs Pointer to Array

```c
// Array of pointers: each element is a pointer
char *names[] = {"Alice", "Bob", "Charlie"};
// names[i] is char *
// names is char **

// Pointer to array: pointer to entire array
int matrix[3][4];
int (*row_ptr)[4] = matrix;  // pointer to int[4]
```

### 4.4.2 Array of Function Pointers

```c
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }
int div(int a, int b) { return a / b; }

// Array of function pointers
int (*operations[4])(int, int) = {add, sub, mul, div};

// Usage
int result = operations[0](10, 5);  // add(10, 5) = 15
result = operations[2](10, 5);       // mul(10, 5) = 50
```

### 4.4.3 Pointer to Function Pointer

```c
int (**ptr_ptr)(int, int) = &operations[0];
// *ptr_ptr is a function pointer
// **ptr_ptr can call the function
```

## 4.5 Command Line Arguments

`main` receives command line arguments:

```c
int main(int argc, char *argv[]) {
    // argc: argument count
    // argv: array of argument pointers
    
    printf("Program name: %s\n", argv[0]);
    
    for (int i = 1; i < argc; i++) {
        printf("Argument %d: %s\n", i, argv[i]);
    }
    return 0;
}
```

Running:
```bash
./program hello world 42
```
Output:
```
Program name: ./program
Argument 1: hello
Argument 2: world
Argument 3: 42
```

## 4.6 Dynamic Memory Allocation

### 4.6.1 malloc and free

```c
#include <stdlib.h>

// Allocate single element
int *p = (int *)malloc(sizeof(int));
*p = 42;
free(p);

// Allocate array
int *arr = (int *)malloc(100 * sizeof(int));
if (arr == NULL) {
    // allocation failed
    return -1;
}
arr[0] = 1;
// ...
free(arr);
```

### 4.6.2 calloc (Allocate and Initialize to Zero)

```c
int *arr = (int *)calloc(100, sizeof(int));
// equivalent to malloc + memset(arr, 0, 100 * sizeof(int))
```

### 4.6.3 realloc (Reallocate)

```c
int *arr = (int *)malloc(50 * sizeof(int));
// ... use arr ...

// Expand size
int *new_arr = (int *)realloc(arr, 100 * sizeof(int));
if (new_arr == NULL) {
    free(arr);
    return -1;
}
arr = new_arr;  // update pointer
```

## 4.7 Common Pointer Pitfalls

### 4.7.1 Wild Pointer

Uninitialized pointer:
```c
int *ptr;
// *ptr = 42;  // Error! ptr is wild, points to unknown address
```

### 4.7.2 Dangling Pointer

Pointer to freed memory:
```c
int *ptr = (int *)malloc(sizeof(int));
free(ptr);
// ptr is now dangling!
// *ptr = 42;  // Error!
ptr = NULL;  // Prevention: set to NULL after free
```

### 4.7.3 Pointer Offset Error

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;
p = p + 10;  // out of bounds! undefined behavior
```

## 4.8 Summary

In this chapter we learned:
- Multi-dimensional arrays and complex pointer relationships
- C strings are null-terminated char arrays
- Function pointers: for callbacks, strategy pattern
- Command line argument handling
- Dynamic memory allocation: malloc/calloc/realloc/free
- Common pointer errors and prevention

## 4.9 Exercises

1. Implement `strstr`: find substring in a string
2. Implement qsort comparator for sorting struct array
3. Write a simple calculator using array of function pointers
4. Implement dynamic string (like C++ string) with append
5. Compare `char **argv` and `char *argv[]` equivalence
