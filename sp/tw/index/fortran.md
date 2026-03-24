# Fortran

## 概述

Fortran（Formula Translation）是第一個高級程式語言，由 John Backus 於 1957 年在 IBM 發明。原本設計用於科學和工程計算，至今仍在天氣預報、計算流體動力學、量子化學等領域廣泛使用。

## 歷史

- **1957 年**：John Backus 在 IBM 發布 Fortran I
- **1958 年**：Fortran II 引入副程式
- **1962 年**：Fortran IV 成為標準
- **1978 年**：Fortran 77 標準化
- **1991 年**：Fortran 90 引入現代特性
- **2003 年**：Fortran 2003 支援物件導向
- **2018 年**：Fortran 2018 最新標準

## 核心特性

### 1. 陣列操作

Fortran 擅長矩陣和陣列運算：

```fortran
program array_example
    implicit none
    real :: a(5,5), b(5,5), c(5,5)
    integer :: i, j
    
    ! 初始化矩陣
    do i = 1, 5
        do j = 1, 5
            a(i,j) = real(i + j)
            b(i,j) = real(i * j)
        end do
    end do
    
    ! 矩陣相加
    c = a + b
    
    ! 印出結果
    do i = 1, 5
        print *, (c(i,j), j=1,5)
    end do
end program array_example
```

### 2. 矩陣乘法（內建）

```fortran
program matmul_example
    implicit none
    real :: a(3,3), b(3,3), c(3,3)
    
    a = reshape([1,2,3,4,5,6,7,8,9], [3,3])
    b = reshape([9,8,7,6,5,4,3,2,1], [3,3])
    
    ! 內建矩陣乘法
    c = matmul(a, b)
    
    print *, 'Result:'
    print *, c
end program matmul_example
```

### 3. 副程式與函數

```fortran
program subprogram
    implicit none
    real :: x, y, result
    
    x = 5.0
    y = 3.0
    
    print *, 'Add:', add(x, y)
    print *, 'Multiply:', multiply(x, y)
    
contains
    real function add(a, b)
        real, intent(in) :: a, b
        add = a + b
    end function add
    
    real function multiply(a, b)
        real, intent(in) :: a, b
        multiply = a * b
    end function multiply
end program subprogram
```

### 4. 模組（Module）

```fortran
module math_utils
    implicit none
    private
    public :: factorial, fibonacci
    
contains
    recursive function factorial(n) result(res)
        integer, intent(in) :: n
        integer :: res
        if (n <= 1) then
            res = 1
        else
            res = n * factorial(n - 1)
        end if
    end function factorial
    
    recursive function fibonacci(n) result(res)
        integer, intent(in) :: n
        integer :: res
        if (n <= 1) then
            res = n
        else
            res = fibonacci(n - 1) + fibonacci(n - 2)
        end if
    end function fibonacci
end module math_utils
```

## 編譯與執行

```bash
# 使用 gfortran 編譯
gfortran -o program program.f90

# 使用 ifort（Intel Fortran）
ifort -o program program.f90

# 執行
./program
```

## 為什麼 Fortran 仍然重要？

1. **效能**：優化後的 Fortran 程式可接近 C 的效能
2. **科學計算**：數十年累積的科學計算代碼庫
3. **陣列語法**：內建強大的矩陣操作能力
4. **穩定性**：長期維護的標準庫

## 參考資源

- "Fortran 90/95 Explained"
- "Numerical Recipes in Fortran 90"
- Fortran 官方標準
