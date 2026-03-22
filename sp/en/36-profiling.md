# 36. Profiling——perf and Flame Graphs

## 36.1 Why Profiling?

- Find performance bottlenecks
- Optimize code with most impact
- Avoid premature optimization

## 36.2 perf

Linux performance analysis tool.

### 36.2.1 Basic Usage

```bash
# Record program execution
perf record -g ./program

# View report
perf report
```

### 36.2.2 CPU Analysis

```bash
# Software events
perf stat -e cycles,instructions ./program

# Hardware events
perf stat -e branch-misses,cache-misses ./program
```

### 36.2.3 Hotspot Analysis

```bash
perf record -F 99 ./program
perf report --symbol-filter=main
```

## 36.3 Flame Graphs

Visualize performance analysis.

### 36.3.1 Installation

```bash
git clone https://github.com/brendangregg/FlameGraph
```

### 36.3.2 Generate Flame Graph

```bash
# 1. Record with perf
perf record -F 99 -g -- ./program

# 2. Convert to flame graph format
perf script > out.perf

# 3. Generate flame graph
stackcollapse-perf.pl out.perf > out.folded
flamegraph.pl out.folded > flamegraph.svg
```

### 36.3.3 Reading Flame Graphs

```
                           [main]
                             |
                    +--------+--------+
                    |        |        |
                 [foo]    [bar]    [baz]
                   |        |        |
                  ...      ...      ...
```

Wider boxes indicate more CPU time consumed by that function.

## 36.4 Hot Functions

### 36.4.1 Find Hotspots

```bash
perf report -g --stdio | head -50
```

### 36.4.2 Annotate

```bash
perf annotate --symbol=hot_function
```

## 36.5 Example Analysis

### 36.5.1 Test Program

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

### 36.5.2 Analysis

```bash
gcc -g -O2 hot.c -o hot
perf record -g ./hot
perf report
```

## 36.6 Summary

In this chapter we learned:
- perf basic usage
- Flame graph generation
- Hot function analysis
- Performance analysis workflow

## 36.7 Exercises

1. Profile a compute-intensive program
2. Research other profiling tools (Valgrind, gprof)
3. Compare performance at different optimization levels
4. Profile a real project using flame graphs
5. Research microbenchmark pitfalls
