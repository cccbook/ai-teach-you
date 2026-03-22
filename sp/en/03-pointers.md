# 3. Pointers and Pointer Arithmetic——The Core of C

## 3.1 What is a Pointer?

A pointer is a variable that stores a memory address. In C, pointers are the key to understanding and manipulating memory.

```
int value = 42;

Pointer variable:
+--------+
| 0x1000 |  →  Stores address of value
+--------+
  ptr

Actual memory:
0x1000: +-------+
        |   42  |  →  value's value
        +-------+
```

## 3.2 Declaring Pointers

```c
int *ptr;        // Pointer to int
char *cptr;      // Pointer to char
float *fptr;     // Pointer to float
void *vptr;      // Generic pointer (can point to any type)
```

Meaning of `int *ptr`:
- `ptr` is a variable
- `*ptr` accesses memory pointed to by ptr
- Type of `ptr` is "pointer to int"

## 3.3 Address-of Operator `&`

`&` operator gets a variable's memory address:

```c
int x = 10;
int *p = &x;   // p stores address of x

printf("x value: %d\n", x);           // prints 10
printf("x address: %p\n", (void *)&x);  // prints address like 0x7ffd...
printf("p value: %p\n", (void *)p);  // same as above
printf("*p value: %d\n", *p);        // prints 10
```

## 3.4 Dereference Operator `*`

`*` operator accesses memory pointed to by a pointer:

```c
int value = 42;
int *ptr = &value;

printf("value = %d\n", value);    // 42
printf("*ptr = %d\n", *ptr);      // 42

*ptr = 100;   // Modify value through pointer

printf("value = %d\n", value);    // 100
printf("*ptr = %d\n", *ptr);      // 100
```

Pointers provide **indirect access**: through pointers, you can read/write the memory they point to.

## 3.5 NULL Pointer

NULL pointer doesn't point to any valid memory:

```c
int *ptr = NULL;

if (ptr == NULL) {
    printf("Pointer is NULL\n");
}

// Dereferencing NULL crashes!
// *ptr = 42;  // Never do this!
```

**Must check** if pointer is NULL before using:

```c
int *find_element(int *arr, int size, int target) {
    for (int i = 0; i < size; i++) {
        if (arr[i] == target) {
            return &arr[i];  // Found, return address
        }
    }
    return NULL;  // Not found
}

int *found = find_element(arr, 10, 42);
if (found != NULL) {
    printf("Found: %d\n", *found);
}
```

## 3.6 Pointer Arithmetic

Pointers can be added/subtracted, but the unit is the **size of the type pointed to**.

### 3.6.1 Pointer + Integer

```c
int arr[] = {10, 20, 30, 40, 50};
int *p = arr;  // arr is same as &arr[0]

printf("*p = %d\n", *p);      // 10
p = p + 1;
printf("*p = %d\n", *p);      // 20
p = p + 2;
printf("*p = %d\n", *p);      // 40
```

In memory (assuming `int` is 4 bytes):
```
arr[0]: 10  →  Address 0x1000
arr[1]: 20  →  Address 0x1004  (+4)
arr[2]: 30  →  Address 0x1008  (+4)
arr[3]: 40  →  Address 0x100C  (+4)
arr[4]: 50  →  Address 0x1010  (+4)

p = arr      →  0x1000
p + 1        →  0x1004  (0x1000 + 1*4)
p + 2        →  0x1008  (0x1000 + 2*4)
```

### 3.6.2 Different Type Pointer Arithmetic

```c
char *c = (char *)0x1000;
int  *i = (int *)0x1000;

c = c + 1;    // 0x1001
i = i + 1;    // 0x1004  (int is 4 bytes)
```

### 3.6.3 Pointer Subtraction

Two pointers of same type subtracted gives **element count** (not address difference):

```c
int arr[] = {10, 20, 30, 40, 50};
int *p1 = &arr[1];
int *p2 = &arr[4];

ptrdiff_t diff = p2 - p1;  // 3 (not 3 * sizeof(int))
```

## 3.7 Relationship Between Pointers and Arrays

In C, array names **decay** to pointers to the first element:

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;  // same as int *p = &arr[0];

// These are equivalent:
arr[2]   ==  *(arr + 2)
*(arr+2) ==  p[2]
p[2]     ==  *(p + 2)
```

But arrays and pointers have important differences:

| Feature | Array | Pointer |
|---------|-------|---------|
| Stores | Element values | Address |
| Size | Fixed (determined at compile time) | Fixed (pointer size) |
| Modifiable | No (array name can't be assigned) | Yes |
| Memory location | Stack/global | Depends on pointer |

```c
int arr[5];
int *p;

sizeof(arr)   // 5 * sizeof(int) = 20
sizeof(p)     // pointer size = 8 (on 64-bit)

arr = p;      // Error! arr can't be assigned
p = arr;      // Correct
```

## 3.8 Common Pointer Types

### 3.8.1 Pointer to Pointer

```c
int value = 42;
int *p1 = &value;
int **p2 = &p1;  // pointer to pointer

**p2 = 100;   // changes value to 100
```

### 3.8.2 Pointer to Constant

```c
int regular = 10;
const int constant = 20;

const int *cp = &constant;  // can point to constant
cp = &regular;              // can point to regular variable
// *cp = 30;                  // Error! can't modify through cp

int *regular_ptr = &regular;
// const int *cp2 = regular_ptr;  // OK (safe)
// int *p3 = &constant;           // Error! (unsafe)
```

### 3.8.3 Constant Pointer

```c
int x = 10, y = 20;
int *const cp = &x;   // constant pointer (pointer itself can't change)

*cp = 30;    // OK! can modify value pointed to
// cp = &y;   // Error! pointer can't point elsewhere
```

### 3.8.4 Constant Pointer to Constant

```c
int x = 10;
const int *const cp = &x;  // both can't change

// *cp = 30;   // Error!
// cp = &y;    // Error!
```

## 3.9 void Pointer

`void *` is a generic pointer that can point to any type:

```c
void *memcpy(void *dest, const void *src, size_t n);
void *malloc(size_t size);
void *memset(void *s, int c, size_t n);
```

Must cast before using:

```c
void *ptr = malloc(sizeof(int));
int *p = (int *)ptr;
*ptr = 42;  // Error! can't dereference void*
*p = 42;    // Correct
free(ptr);
```

## 3.10 Pointer Size

Pointer size depends on architecture:
- **32-bit system**: 4 bytes
- **64-bit system**: 8 bytes

```c
printf("int *: %zu bytes\n", sizeof(int *));
printf("char *: %zu bytes\n", sizeof(char *));
printf("void *: %zu bytes\n", sizeof(void *));
```

## 3.11 Typical Pointer Applications

### 3.11.1 Returning Multiple Values from Functions

```c
void divide(int a, int b, int *quotient, int *remainder) {
    *quotient = a / b;
    *remainder = a % b;
}

int q, r;
divide(17, 5, &q, &r);  // q=3, r=2
```

### 3.11.2 Dynamic Data Structures

```c
struct Node {
    int data;
    struct Node *next;
};

struct Node *head = malloc(sizeof(struct Node));
head->data = 42;
head->next = NULL;
```

### 3.11.3 Arrays as Function Parameters

```c
int sum(int *arr, int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];  // or *(arr + i)
    }
    return total;
}

int numbers[] = {1, 2, 3, 4, 5};
printf("Sum = %d\n", sum(numbers, 5));
```

## 3.12 Summary

In this chapter we learned:
- Pointers store memory addresses
- `&` gets address, `*` dereferences to get value
- Pointer arithmetic unit is element size
- Array names decay to pointers
- NULL pointer usage and checking
- Special pointer types: const, void *

## 3.13 Exercises

1. Write a function `swap(int *a, int *b)` to swap two values
2. Implement `strlen`: calculate C string length
3. Implement `strcpy`: copy C string
4. Explain why `*(arr + i)` is equivalent to `arr[i]`
5. Write a function to find both max and min values in an array
