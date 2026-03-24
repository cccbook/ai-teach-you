# 1. 高階語言

## 1.1 高階語言的歷史與發展

電腦發展初期，程式設計師必須使用機器語言（Machine Language）來撰寫程式。機器語言是電腦可以直接執行的二進制指令編碼，例如在 x86 架構中：

[程式檔案：01-2-x86-assembly.s](../_code/01/01-2-x86-assembly.s)
```assembly
B8 01 00    ; 將數值 1 載入 AX 暫存器
89 C3        ; 將 AX 的值存入 BX 暫存器
```

這種低階語言極難閱讀、維護和除錯。於是誕生了組合語言（Assembly Language），用助記符號代替二進制碼：

[程式檔案：01-3-assembly.s](../_code/01/01-3-assembly.s)
```assembly
mov ax, 1    ; 將 1 載入 AX
mov bx, ax   ; 將 AX 的值複製到 BX
```

1950 年代，高階語言開始出現。Fortran（1957年）用於科學計算：

[程式檔案：01-4-fortran.f90](../_code/01/01-4-fortran.f90)
```fortran
C 計算圓面積
      PROGRAM AREA
      REAL R, A
      READ(*,*) R
      A = 3.14159 * R * R
      PRINT *, 'AREA =', A
      END
```

1960 年代，ALGOL 奠定了結構化程式設計的基礎。1972 年，Dennis Ritchie 在貝爾實驗室發明了 C 語言：

[程式檔案：01-5-c-area.c](../_code/01/01-5-c-area.c)
```c
#include <stdio.h>

int main() {
    int r;
    float area;
    scanf("%d", &r);
    area = 3.14159f * r * r;
    printf("Area = %f\n", area);
    return 0;
}
```

C 語言結合了高階語言的便利性和低階語言的效率，成為作業系統開發的主流語言。Unix 作業系統就是用 C 寫成的。

1995 年，Java 引入「一次編寫，到處執行」的理念：

[程式檔案：01-6-java-hello.java](../_code/01/01-6-java-hello.java)
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

Java 程式被編譯成位元組碼（Bytecode），由 Java 虛擬機（JVM）執行，實現跨平台執行。

2000 年代後，多種現代語言相繼問世。Python 以簡潔語法取勝：

[程式檔案：01-7-python-area.py](../_code/01/01-7-python-area.py)
```python
import math

r = float(input("請輸入半徑: "))
area = math.pi * r * r
print(f"面積 = {area}")
```

Rust 和 Go 則專注於系統程式設計，提供記憶體安全和高並發支援：

[程式檔案：01-8-rust-area.rs](../_code/01/01-8-rust-area.rs)
```rust
fn main() {
    let r: f64 = 3.0;
    let area = std::f64::consts::PI * r * r;
    println!("面積 = {}", area);
}
```

## 1.2 程式語言的分類

### 命令式語言（Imperative Language）

命令式語言透過改變程式狀態來完成計算，代表語言包括 C、C++、Java、Python。

[程式檔案：01-9-c-sum.c](../_code/01/01-9-c-sum.c)
```c
// C 語言 - 命令式範式範例
int sum = 0;
for (int i = 1; i <= 10; i++) {
    sum += i;  // 修改 sum 變數的狀態
}
printf("%d\n", sum);  // 輸出 55
```

### 宣告式語言（Declarative Language）

宣告式語言描述「做什麼」而非「如何做」。SQL 是代表：

[程式檔案：01-10-sql-select.sql](../_code/01/01-10-sql-select.sql)
```sql
-- 從員工表中選取薪水超過 50000 的員工姓名
SELECT name FROM employees WHERE salary > 50000;
```

### 函數式語言（Functional Language）

函數式語言以函數為一等公民，強調不可變性。LISP 範例：

[程式檔案：01-11-lisp-sum.lisp](../_code/01/01-11-lisp-sum.lisp)
```lisp
;; LISP - 計算 1 到 10 的總和
(defun sum (n)
  (if (= n 0)
      0
      (+ n (sum (- n 1)))))

(print (sum 10))  ; 輸出 55
```

Haskell 範例：

[程式檔案：01-12-haskell-sum.hs](../_code/01/01-12-haskell-sum.hs)
```haskell
-- Haskell - 使用遞迴與模式匹配
sum' :: [Int] -> Int
sum' [] = 0
sum' (x:xs) = x + sum' xs

main = print (sum' [1..10])  -- 輸出 55
```

Python 也支援函數式風格：

[程式檔案：01-13-python-functional.py](../_code/01/01-13-python-functional.py)
```python
# Python - 函數式風格
from functools import reduce

result = reduce(lambda x, y: x + y, range(1, 11))
print(result)  # 輸出 55
```

### 邏輯式語言（Logic Language）

Prolog 是代表性的邏輯式語言，透過事實和規則進行邏輯推論：

[程式檔案：01-14-prolog-family.pl](../_code/01/01-14-prolog-family.pl)
```prolog
% Prolog - 家族關係範例
father(tom, bob).
father(tom, alice).
mother(mary, bob).

parent(X, Y) :- father(X, Y).
parent(X, Y) :- mother(X, Y).

% 查詢：誰是 Bob 的父母？
% ?- parent(Who, bob).
% Who = tom ;
% Who = mary
```

### 物件導向語言（Object-Oriented Language）

物件導向語言將資料和操作封裝為物件：

[程式檔案：01-15-python-oop.py](../_code/01/01-15-python-oop.py)
```python
# Python - 物件導向範例
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

rect = Rectangle(5, 3)
print(rect.area())  # 輸出 15
```

## 1.3 語法與語意

語法（Syntax）定義了語言中合法的表示方式。相同的語法在不同語言中有不同語意：

[程式檔案：01-16-c-syntax.c](../_code/01/01-16-c-syntax.c)
```c
// C 語言：= 是賦值運算子
int x = 5;
int y = x = 10;  // x 被設為 10，y 也被設為 10
```

[程式檔案：01-17-python-syntax.py](../_code/01/01-17-python-syntax.py)
```python
# Python：== 是相等比較，= 是賦值
x = 5
y = (x == 10)  # False
```

[程式檔案：01-18-javascript-equality.js](../_code/01/01-18-javascript-equality.js)
```javascript
// JavaScript：== 會做型別轉換，=== 嚴格相等
console.log(5 == "5");   // true
console.log(5 === "5");  // false
```

## 1.4 語言翻譯簡介

### 編譯器（Compiler）

編譯器在執行前將整個程式翻譯為機器碼：

[程式檔案：01-19-c-hello.c](../_code/01/01-19-c-hello.c)
```c
// hello.c
#include <stdio.h>

int main() {
    printf("Hello!\n");
    return 0;
}
```

編譯並執行：
[程式檔案：01-20-bash-compile.sh](../_code/01/01-20-bash-compile.sh)
```bash
$ gcc hello.c -o hello
$ ./hello
Hello!
```

### 解譯器（Interpreter）

Python 是典型的直譯語言：

[程式檔案：01-21-python-hello.py](../_code/01/01-21-python-hello.py)
```python
# hello.py
print("Hello!")

# 直接執行
$ python hello.py
Hello!
```

### 混合型

Java 先編譯為位元組碼，再由 JVM 執行：

[程式檔案：01-22-java-hello.java](../_code/01/01-22-java-hello.java)
```java
// Hello.java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello!");
    }
}
```

[程式檔案：01-23-bash-java.sh](../_code/01/01-23-bash-java.sh)
```bash
# 編譯為位元組碼
$ javac Hello.java
# 執行（ JVM 解譯位元組碼）
$ java Hello
Hello!
```

可以使用 `javap` 查看生成的位元組碼：

[程式檔案：01-24-bash-javap.sh](../_code/01/01-24-bash-javap.sh)
```bash
$ javap -c Hello
Compiled from "Hello.java"
public class Hello {
  public Hello();
    Code:
       0: aload_0
       1: invokespecial #1
       5: return

  public static void main(java.lang.String[]);
    Code:
       0: getstatic #2
       3: ldc #3
       5: invokevirtual #4
       8: return
}
```

這些位元組碼指令就是 JVM 虛擬機的指令集。
