# C 語言

## 概述

C 語言是一種通用的程式語言，由 Dennis Ritchie 於 1972 年在貝爾實驗室（Bell Labs）發明。它是系統程式設計的主流語言，Unix 作業系統就是用 C 寫成的。C 語言結合了高階語言的便利性和低階語言的效率，至今仍是最重要的程式語言之一。

## 歷史

- **1972 年**：Dennis Ritchie 在貝爾實驗室發明 C 語言
- **1978 年**：《The C Programming Language》出版（C 的第一本書籍）
- **1989 年**：ANSI C（C89）標準化
- **1999 年**：C99 標準引入新特性
- **2011 年**：C11 標準
- **2018 年**：C17 標準
- **2023 年**：C23 標準

## 核心特性

### 1. 指標（Pointer）

指標是 C 語言的核心特色，讓程式可以直接操作記憶體：

```c
#include <stdio.h>

int main() {
    int x = 10;
    int *ptr = &x;  // 取址運算子
    
    printf("x 的值: %d\n", x);
    printf("x 的位址: %p\n", (void*)&x);
    printf("指標指向的值: %d\n", *ptr);  // 解引用
    
    // 指標算術
    int arr[] = {1, 2, 3, 4, 5};
    int *p = arr;
    for (int i = 0; i < 5; i++) {
        printf("arr[%d] = %d\n", i, *(p + i));
    }
    
    return 0;
}
```

### 2. 結構體（Struct）

結構體允許將不同類型的資料組合成單一類型：

```c
#include <stdio.h>
#include <string.h>

struct Person {
    char name[50];
    int age;
    float salary;
};

int main() {
    struct Person p1;
    strcpy(p1.name, "John");
    p1.age = 30;
    p1.salary = 5000.0f;
    
    printf("Name: %s\n", p1.name);
    printf("Age: %d\n", p1.age);
    printf("Salary: %.2f\n", p1.salary);
    
    // 使用指標
    struct Person *ptr = &p1;
    printf("Name: %s\n", ptr->name);
    
    return 0;
}
```

### 3. 動態記憶體配置

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 配置整數記憶體
    int *num = (int*)malloc(sizeof(int));
    *num = 42;
    printf("Dynamic int: %d\n", *num);
    free(num);
    
    // 配置陣列
    int *arr = (int*)malloc(5 * sizeof(int));
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 10;
    }
    for (int i = 0; i < 5; i++) {
        printf("arr[%d] = %d\n", i, arr[i]);
    }
    free(arr);
    
    // calloc（自動初始化為 0）
    int *arr2 = (int*)calloc(5, sizeof(int));
    printf("arr2[0] = %d\n", arr2[0]);
    free(arr2);
    
    return 0;
}
```

### 4. 函數指標

```c
#include <stdio.h>

int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }
int multiply(int a, int b) { return a * b; }

int main() {
    // 函數指標
    int (*operation)(int, int);
    
    operation = add;
    printf("3 + 4 = %d\n", operation(3, 4));
    
    operation = multiply;
    printf("3 * 4 = %d\n", operation(3, 4));
    
    return 0;
}
```

### 5. 前置處理器（Preprocessor）

```c
#include <stdio.h>

#define MAX_SIZE 100
#define SQUARE(x) ((x) * (x))
#define DEBUG

int main() {
    printf("MAX_SIZE = %d\n", MAX_SIZE);
    printf("SQUARE(5) = %d\n", SQUARE(5));
    
#ifdef DEBUG
    printf("Debug mode is on\n");
#endif
    
    return 0;
}
```

## 經典範例：鏈結串列

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Node {
    int data;
    struct Node *next;
};

void insert(struct Node **head, int value) {
    struct Node *newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->next = *head;
    *head = newNode;
}

void printList(struct Node *head) {
    struct Node *current = head;
    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\n");
}

int main() {
    struct Node *head = NULL;
    
    insert(&head, 30);
    insert(&head, 20);
    insert(&head, 10);
    
    printList(head);
    
    return 0;
}
```

## C 標準庫常用函數

### 字串處理

```c
#include <stdio.h>
#include <string.h>

int main() {
    char s1[50] = "Hello";
    char s2[] = " World";
    
    // 連接
    strcat(s1, s2);
    printf("%s\n", s1);  // "Hello World"
    
    // 複製
    char s3[50];
    strcpy(s3, s1);
    printf("%s\n", s3);
    
    // 比較
    if (strcmp(s1, s3) == 0) {
        printf("Equal\n");
    }
    
    // 長度
    printf("Length: %zu\n", strlen(s1));
    
    return 0;
}
```

### 檔案操作

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("data.txt", "w");
    if (file == NULL) {
        printf("Failed to open file\n");
        return 1;
    }
    
    fprintf(file, "Hello, World!\n");
    fprintf(file, "Number: %d\n", 42);
    fclose(file);
    
    // 讀取
    file = fopen("data.txt", "r");
    char buffer[100];
    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        printf("%s", buffer);
    }
    fclose(file);
    
    return 0;
}
```

## 為什麼學習 C 語言？

1. **系統程式設計**：作業系統、驅動程式、嵌入式系統
2. **效能關鍵**：遊戲引擎、資料庫、編譯器
3. **理解底層**：指標、記憶體管理、硬體運作
4. **語言基礎**：許多語言深受 C 影響（C++、Java、C#）
5. **標準化**：ANSI/ISO 標準，跨平台相容

## 參考資源

- "The C Programming Language" by Brian Kernighan and Dennis Ritchie
- "C Programming Language" wiki
- ISO C 標準文檔
- C99/C11/C17 規格說明
