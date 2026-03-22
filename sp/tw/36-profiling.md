# 36. 效能分析——perf 與火焰圖

## 36.1 為什麼需要效能分析？

- 找出效能瓶頸
- 優化最有影響力的程式碼
- 避免過早最佳化

## 36.2 perf

Linux 效能分析工具。

### 36.2.1 基本使用

```bash
# 記錄程式執行
perf record -g ./program

# 查看報告
perf report
```

### 36.2.2 CPU 分析

```bash
# 軟體事件
perf stat -e cycles,instructions ./program

# 硬體事件
perf stat -e branch-misses,cache-misses ./program
```

### 36.2.3 熱點分析

```bash
perf record -F 99 ./program
perf report --symbol-filter=main
```

## 36.3 火焰圖

視覺化效能分析。

### 36.3.1 安裝

```bash
git clone https://github.com/brendangregg/FlameGraph
```

### 36.3.2 生成火焰圖

```bash
# 1. 用 perf 記錄
perf record -F 99 -g -- ./program

# 2. 轉換為火焰圖格式
perf script > out.perf

# 3. 生成火焰圖
stackcollapse-perf.pl out.perf > out.folded
flamegraph.pl out.folded > flamegraph.svg
```

### 36.3.3 解讀火焰圖

```
                           [main]
                             |
                    +--------+--------+
                    |        |        |
                 [foo]    [bar]    [baz]
                   |        |        |
                  ...      ...      ...
```

越寬的框表示該函式消耗的 CPU 時間越多。

## 36.4 熱點函式

### 36.4.1 找熱點

```bash
perf report -g --stdio | head -50
```

### 36.4.2 Annotate

```bash
perf annotate --symbol=hot_function
```

## 36.5 範例分析

### 36.5.1 測試程式

```c
// hot.c
#include <stdio.h>

long hot_function(int n) {
    long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += i * i;
    }
    return sum;
}

int main() {
    long result = 0;
    for (int i = 0; i < 1000; i++) {
        result += hot_function(1000000);
    }
    printf("Result: %ld\n", result);
    return 0;
}
```

### 36.5.2 分析

```bash
gcc -g -O2 hot.c -o hot
perf record -g ./hot
perf report
```

## 36.6 小結

本章節我們學習了：
- perf 基本用法
- 火焰圖生成
- 熱點函式分析
- 效能分析流程

## 36.7 習題

1. 分析一個計算密集程式的效能
2. 研究其他效能分析工具（Valgrind, gprof）
3. 比較不同最佳化等級的效能
4. 使用火焰圖分析實際專案
5. 研究 microbenchmark 的陷阱
