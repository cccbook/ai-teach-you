# 4. 指標的應用——陣列、字串與函式指標

## 4.1 陣列進階

### 4.1.1 陣列的宣告和初始化

```c
// 宣告方式
int arr1[5];              // 未初始化
int arr2[5] = {1, 2, 3};   // 部分初始化，未指定為 0
int arr3[] = {1, 2, 3, 4, 5};  // 大小由初始化值決定
int arr4[5] = {0};        // 全部初始化為 0

// C99 指定初始化器
int arr5[10] = { [0] = 1, [5] = 10 };  // arr5[0]=1, arr5[5]=10, 其餘為0
```

### 4.1.2 多維陣列

```c
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

// 等價於（連續記憶體）
int flat[12] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
```

記憶體佈局（Row-Major）：
```
matrix[0][0] → matrix[0][1] → matrix[0][2] → matrix[0][3]
      ↓
matrix[1][0] → matrix[1][1] → ...
```

### 4.1.3 指標與多維陣列

```c
int matrix[3][4];

// matrix 是指向 int[4] 的指標
int (*row_ptr)[4] = matrix;  // 指向一列（4個int）

// row_ptr[i] 等價於 matrix[i]
// *(row_ptr + i) 等價於 matrix[i]
```

## 4.2 字串在 C 中的表示

C 語言沒有「字串」類型，字串是**以 '\0' 結尾的字元陣列**。

```c
char s1[] = "Hello";  // {'H', 'e', 'l', 'l', 'o', '\0'}
char *s2 = "Hello";   // 指標指向字串常量的第一個字元
```

### 4.2.1 字串與指標

```c
char str[] = "Hello";
char *p = str;

printf("%c\n", str[0]);    // 'H'
printf("%c\n", p[0]);     // 'H'
printf("%c\n", *(p + 1)); // 'e'
printf("%c\n", *p++);     // 'H', p 向後移動
```

### 4.2.2 字元指標與字元陣列的區別

```c
char arr[] = "Hello";  // 可修改的陣列
arr[0] = 'h';          // 正確

char *ptr = "Hello";   // 指向字串常量
// ptr[0] = 'h';       // 錯誤！字串常量在唯讀記憶體
```

### 4.2.3 標準字串函式

```c
// 字串長度
size_t strlen(const char *s) {
    size_t len = 0;
    while (s[len] != '\0') len++;
    return len;
}

// 字串複製
char *strcpy(char *dest, const char *src) {
    char *p = dest;
    while ((*p++ = *src++) != '\0');
    return dest;
}

// 字串連接
char *strcat(char *dest, const char *src) {
    char *p = dest;
    while (*p) p++;
    while ((*p++ = *src++));
    return dest;
}

// 字串比較
int strcmp(const char *s1, const char *s2) {
    while (*s1 && (*s1 == *s2)) {
        s1++;
        s2++;
    }
    return (unsigned char)*s1 - (unsigned char)*s2;
}
```

## 4.3 函式指標

函式指標是指向函式的指標，儲存函式的入口位址。

### 4.3.1 宣告函式指標

```c
// 函式指標語法
int (*func_ptr)(int, int);

// 對比普通函式指標
int add(int a, int b);      // add 是函式
int (*ptr_add)(int, int);   // ptr_add 是函式指標

ptr_add = add;  // 指標指向 add
ptr_add = &add; // 同上，等價
```

### 4.3.2 使用函式指標呼叫函式

```c
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int (*operation)(int, int);

operation = add;
int result1 = operation(10, 5);   // 15
result1 = (*operation)(10, 5);   // 同上

operation = sub;
int result2 = operation(10, 5);   // 5
```

### 4.3.3 函式指標作為參數（回調函式）

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

### 4.3.4 qsort 與函式指標

`qsort` 是 C 標準庫的快速排序，使用函式指標進行自訂比較：

```c
#include <stdlib.h>

int compare_int(const void *a, const void *b) {
    int ia = *(const int *)a;
    int ib = *(const int *)b;
    return ia - ib;  // 升序
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

## 4.4 指標的各種形式

### 4.4.1 指標陣列 vs 陣列指標

```c
// 指標陣列：每個元素都是指標
char *names[] = {"Alice", "Bob", "Charlie"};
// names[i] 是 char *
// names 是 char **

// 陣列指標：指向整個陣列的指標
int matrix[3][4];
int (*row_ptr)[4] = matrix;  // row_ptr 是「指向 int[4] 的指標」
```

### 4.4.2 函式指標陣列

```c
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }
int div(int a, int b) { return a / b; }

// 函式指標陣列
int (*operations[4])(int, int) = {add, sub, mul, div};

// 使用
int result = operations[0](10, 5);  // add(10, 5) = 15
result = operations[2](10, 5);       // mul(10, 5) = 50
```

### 4.4.3 指向函式指標的指標

```c
int (**ptr_ptr)(int, int) = &operations[0];
// *ptr_ptr 是函式指標
// **ptr_ptr 可以呼叫函式
```

## 4.5 命令列參數

`main` 函式接收命令列參數：

```c
int main(int argc, char *argv[]) {
    // argc: 參數個數
    // argv: 參數指標陣列
    
    printf("程式名稱: %s\n", argv[0]);
    
    for (int i = 1; i < argc; i++) {
        printf("參數 %d: %s\n", i, argv[i]);
    }
    return 0;
}
```

執行：
```bash
./program hello world 42
```
輸出：
```
程式名稱: ./program
參數 1: hello
參數 2: world
參數 3: 42
```

## 4.6 動態配置記憶體

### 4.6.1 malloc 和 free

```c
#include <stdlib.h>

// 配置單一元素
int *p = (int *)malloc(sizeof(int));
*p = 42;
free(p);

// 配置陣列
int *arr = (int *)malloc(100 * sizeof(int));
if (arr == NULL) {
    // 配置失敗處理
    return -1;
}
arr[0] = 1;
// ...
free(arr);
```

### 4.6.2 calloc（配置並初始化為零）

```c
int *arr = (int *)calloc(100, sizeof(int));
// 等價於 malloc + memset(arr, 0, 100 * sizeof(int))
```

### 4.6.3 realloc（重新配置）

```c
int *arr = (int *)malloc(50 * sizeof(int));
// ... 使用 arr ...

// 擴展大小
int *new_arr = (int *)realloc(arr, 100 * sizeof(int));
if (new_arr == NULL) {
    free(arr);
    return -1;
}
arr = new_arr;  // 更新指標
```

## 4.7 常見指標陷阱

### 4.7.1 野指標（Wild Pointer）

未初始化的指標：
```c
int *ptr;
// *ptr = 42;  // 錯誤！ptr 是野指標，指向未知位址
```

### 4.7.2 懸空指標（dangling Pointer）

指向已釋放記憶體的指標：
```c
int *ptr = (int *)malloc(sizeof(int));
free(ptr);
// ptr 現在是懸空指標！
// *ptr = 42;  // 錯誤！
ptr = NULL;  // 預防：釋放後設為 NULL
```

### 4.7.3 指標偏移錯誤

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;
p = p + 10;  // 超出邊界！未定義行為
```

## 4.8 小結

本章節我們學習了：
- 多維陣列和指標的複雜關係
- C 字串是以 '\0' 結尾的字元陣列
- 函式指標：用於回調、策略模式
- 命令列參數的處理
- 動態記憶體配置：malloc/calloc/realloc/free
- 常見指標錯誤和預防

## 4.9 習題

1. 實現 `strstr` 函式：在一個字串中尋找子字串
2. 實現 `qsort` 的比較函式，用於排序結構體陣列
3. 寫一個簡單的計算器，使用函式指標陣列處理 +, -, *, /
4. 實現動態字串（類似 C++ 的 string），支援 append 操作
5. 比較 `char **argv` 和 `char *argv[]` 的等價性
