# 3. 指針與指標算術——C 語言的核心

## 3.1 指標是什麼？

指標（Pointer）是儲存記憶體位址的變數。在 C 語言中，指標是理解和操控記憶體的關鍵。

```
int value = 42;

指標變數：
+--------+
| 0x1000 |  →  儲存 value 的位址
+--------+
  ptr

實際記憶體：
0x1000: +-------+
        |   42  |  →  value 的值
        +-------+
```

## 3.2 宣告指標

```c
int *ptr;        // 指向 int 的指標
char *cptr;      // 指向 char 的指標
float *fptr;     // 指向 float 的指標
void *vptr;      // 通用指標（可指向任意類型）
```

`int *ptr` 的含義：
- `ptr` 是一個變數
- `*ptr` 訪問指標所指向的記憶體
- `ptr` 的類型是「指向 int 的指標」

## 3.3 取址運算子 `&`

`&` 運算子取得變數的記憶體位址：

```c
int x = 10;
int *p = &x;   // p 儲存 x 的位址

printf("x 的值: %d\n", x);           // 印出 10
printf("x 的位址: %p\n", (void *)&x);  // 印出位址，如 0x7ffd...
printf("p 儲存的值: %p\n", (void *)p);  // 同上
printf("*p 的值: %d\n", *p);          // 印出 10
```

## 3.4 解參考運算子 `*`

`*` 運算子存取指標所指向的記憶體：

```c
int value = 42;
int *ptr = &value;

printf("value = %d\n", value);    // 42
printf("*ptr = %d\n", *ptr);      // 42

*ptr = 100;   // 透過指標修改 value

printf("value = %d\n", value);    // 100
printf("*ptr = %d\n", *ptr);      // 100
```

指標提供了**間接存取**的方式：透過指標可以讀寫它所指向的記憶體。

## 3.5 NULL 指標

NULL 指標是不指向任何有效記憶體的指標：

```c
int *ptr = NULL;

if (ptr == NULL) {
    printf("指標為 NULL\n");
}

// 對 NULL 指標解參考會造成程式崩潰！
// *ptr = 42;  // 千萬不要這樣做！
```

使用指標前**必須檢查**是否為 NULL：

```c
int *find_element(int *arr, int size, int target) {
    for (int i = 0; i < size; i++) {
        if (arr[i] == target) {
            return &arr[i];  // 找到，回傳位址
        }
    }
    return NULL;  // 沒找到
}

int *found = find_element(arr, 10, 42);
if (found != NULL) {
    printf("找到：%d\n", *found);
}
```

## 3.6 指標算術

指標可以進行加减運算，但運算單位是**指標所指類型的大小**。

### 3.6.1 指標 + 整數

```c
int arr[] = {10, 20, 30, 40, 50};
int *p = arr;  // arr 等同於 &arr[0]

printf("*p = %d\n", *p);      // 10
p = p + 1;
printf("*p = %d\n", *p);      // 20
p = p + 2;
printf("*p = %d\n", *p);      // 40
```

在記憶體中（假設 `int` 為 4 位元組）：
```
arr[0]: 10  →  位址 0x1000
arr[1]: 20  →  位址 0x1004  (+4)
arr[2]: 30  →  位址 0x1008  (+4)
arr[3]: 40  →  位址 0x100C  (+4)
arr[4]: 50  →  位址 0x1010  (+4)

p = arr      →  0x1000
p + 1        →  0x1004  (0x1000 + 1*4)
p + 2        →  0x1008  (0x1000 + 2*4)
```

### 3.6.2 不同類型的指標算術

```c
char *c = (char *)0x1000;
int  *i = (int *)0x1000;

c = c + 1;    // 0x1001
i = i + 1;    // 0x1004  (int 佔 4 位元組)
```

### 3.6.3 指標相減

兩個同類型指標相減，結果是**元素個數**（不是位址差）：

```c
int arr[] = {10, 20, 30, 40, 50};
int *p1 = &arr[1];
int *p2 = &arr[4];

ptrdiff_t diff = p2 - p1;  // 3（不是 3 * sizeof(int)）
```

## 3.7 指標與陣列的關係

在 C 中，陣列名稱**衰減**為指向第一個元素的指標：

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;  // 等同於 int *p = &arr[0];

// 以下三種寫法等價：
arr[2]   ==  *(arr + 2)
*(arr+2) ==  p[2]
p[2]     ==  *(p + 2)
```

但陣列和指標有重要區別：

| 特性 | 陣列 | 指指標 |
|------|------|--------|
| 儲存內容 | 元素值 | 位址 |
| 大小 | 固定（編譯時決定） | 固定（指標大小） |
| 可修改 | 不可（陣列名不可賦值） | 可 |
| 記憶體位置 | 棧/全局 | 取決於指標本身 |

```c
int arr[5];
int *p;

sizeof(arr)   // 5 * sizeof(int) = 20
sizeof(p)     // 指標大小 = 8（在 64 位元系統）

arr = p;      // 錯誤！arr 不可賦值
p = arr;      // 正確
```

## 3.8 常見指標類型

### 3.8.1 指標的指標

```c
int value = 42;
int *p1 = &value;
int **p2 = &p1;  // 指向指標的指標

**p2 = 100;   // 將 value 改為 100
```

### 3.8.2 指向常數的指標

```c
int regular = 10;
const int constant = 20;

const int *cp = &constant;  // 可指向常數
cp = &regular;              // 可指向普通變數
// *cp = 30;                  // 錯誤！不可透過 cp 修改

int *regular_ptr = &regular;
// const int *cp2 = regular_ptr;  // 可（安全）
// int *p3 = &constant;            // 錯誤！（不安全）
```

### 3.8.3 常數指標

```c
int x = 10, y = 20;
int *const cp = &x;   // 常數指標（指標本身不可變）

*cp = 30;    // 正確！可修改指向的值
// cp = &y;   // 錯誤！指標不可指向別處
```

### 3.8.4 常數指標指向常數

```c
int x = 10;
const int *const cp = &x;  // 兩者都不可變

// *cp = 30;   // 錯誤！
// cp = &y;    // 錯誤！
```

## 3.9 void 指標

`void *` 是通用指標，可指向任意類型：

```c
void *memcpy(void *dest, const void *src, size_t n);
void *malloc(size_t size);
void *memset(void *s, int c, size_t n);
```

使用前需強制轉換：

```c
void *ptr = malloc(sizeof(int));
int *p = (int *)ptr;
*ptr = 42;  // 錯誤！void * 不能直接解參考
*p = 42;    // 正確
free(ptr);
```

## 3.10 指標的大小

指標大小取決於架構：
- **32 位元系統**：4 位元組
- **64 位元系統**：8 位元組

```c
printf("int *: %zu bytes\n", sizeof(int *));
printf("char *: %zu bytes\n", sizeof(char *));
printf("void *: %zu bytes\n", sizeof(void *));
```

## 3.11 指標的典型應用

### 3.11.1 函式返回多個值

```c
void divide(int a, int b, int *quotient, int *remainder) {
    *quotient = a / b;
    *remainder = a % b;
}

int q, r;
divide(17, 5, &q, &r);  // q=3, r=2
```

### 3.11.2 動態資料結構

```c
struct Node {
    int data;
    struct Node *next;
};

struct Node *head = malloc(sizeof(struct Node));
head->data = 42;
head->next = NULL;
```

### 3.11.3 陣列作為函式參數

```c
int sum(int *arr, int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];  // 或 *(arr + i)
    }
    return total;
}

int numbers[] = {1, 2, 3, 4, 5};
printf("Sum = %d\n", sum(numbers, 5));
```

## 3.12 小結

本章節我們學習了：
- 指標是儲存記憶體位址的變數
- `&` 取得位址，`*` 解參考取得值
- 指標算術的单位是元素大小
- 陣列名衰減為指標
- NULL 指標的使用和檢查
- 各類特殊指標：const、void *

## 3.13 習題

1. 寫一個函式 `swap(int *a, int *b)` 交換兩個數值
2. 實現 `strlen` 函式：計算 C 字串長度
3. 實現 `strcpy` 函式：複製 C 字串
4. 解釋為什麼 `*(arr + i)` 等價於 `arr[i]`
5. 寫一個函式，找出陣列中的最大和最小值（一次呼叫返回兩個結果）
