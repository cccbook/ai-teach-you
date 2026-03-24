# Go

## 概述

Go（又稱 Golang）是由 Google 的 Robert Griesemer、Rob Pike 和 Ken Thompson 於 2009 年發明的程式語言。Go 結合了靜態語言的效能和動態語言的開發效率，強調簡潔、並發支持和快速編譯。Go 廣泛用於雲端服務、網頁伺服器和 DevOps 工具。

## 歷史

- **2007 年**：Google 內部開始設計
- **2009 年**：Go 開源發布
- **2012 年**：Go 1.0 發布
- **2015 年**：Go 1.5 引入自舉編譯
- **2018 年**：Go 1.11 引入模組
- **2022 年**：Go 1.18 引入泛型
- **現在**：Go 1.22 為最新穩定版

## 核心特性

### 1. 簡潔語法

```go
package main

import "fmt"

func main() {
    // 變數宣告
    var name string = "World"
    
    // 短變數宣告
    age := 30
    
    fmt.Printf("Hello, %s! Age: %d\n", name, age)
    
    // 基本資料型態
    numbers := []int{1, 2, 3, 4, 5}
    for i, n := range numbers {
        fmt.Printf("numbers[%d] = %d\n", i, n)
    }
}
```

### 2. 函數多回傳值

```go
package main

import "fmt"

func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 2)
    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Result:", result)
    }
}
```

### 3. Goroutine 並發

```go
package main

import (
    "fmt"
    "time"
)

func worker(id int) {
    for i := 0; i < 3; i++ {
        fmt.Printf("Worker %d: %d\n", id, i)
        time.Sleep(100 * time.Millisecond)
    }
}

func main() {
    // 啟動多個 goroutine
    for i := 1; i <= 3; i++ {
        go worker(i)
    }
    
    time.Sleep(500 * time.Millisecond)
    fmt.Println("Done")
}
```

### 4. Channel 與同步

```go
package main

import "fmt"

func sum(numbers []int, result chan int) {
    total := 0
    for _, n := range numbers {
        total += n
    }
    result <- total
}

func main() {
    numbers := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    
    ch := make(chan int)
    
    go sum(numbers[:5], ch)
    go sum(numbers[5:], ch)
    
    x, y := <-ch, <-ch
    fmt.Println("Total:", x + y)
}
```

### 5. 結構體與方法

```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func (p Person) Greet() {
    fmt.Printf("Hello, I'm %s\n", p.Name)
}

func main() {
    p := Person{Name: "John", Age: 30}
    p.Greet()
}
```

### 6. 介面

```go
package main

import "fmt"

type Writer interface {
    Write([]byte) (int, error)
}

type Logger struct{}

func (l Logger) Write(data []byte) (int, error) {
    fmt.Printf("Log: %s\n", data)
    return len(data), nil
}

func main() {
    var w Writer = Logger{}
    w.Write([]byte("Hello"))
}
```

## 編譯與執行

```bash
# 編譯
go build -o program main.go

# 執行
./program

# 直接執行
go run main.go
```

## 為什麼學習 Go？

1. **簡潔高效**：簡單易學，編譯快速
2. **並發支援**：goroutine 和 channel
3. **雲端開發**：Kubernetes、Docker 使用 Go
4. **網頁服務**：高效能的 HTTP 伺服器
5. **跨平台**：編譯為單一二進制

## 參考資源

- "The Go Programming Language" 官方書
- "Go in Action"
- golang.org
- go.dev
