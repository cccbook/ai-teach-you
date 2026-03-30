# 6. 編譯與解譯器的優化與加速技巧

## 6.1 最佳化分類

### 6.1.1 編譯器最佳化的理論基礎

編譯器最佳化（Compiler Optimization）是在不改變程式語意的前提下，改進程式效能的過程。這是現代編譯器技術中最複雜也最精彩的領域之一。

**最佳化的理論定義**

從數學角度來看，最佳化可以形式化為：

```
給定：
- 原始程式 P
- 語意函數 ⟦P⟧
- 目標：找到程式 P' 使得 ⟦P'⟧ = ⟦P⟧ 且效能更佳

效能衡量標準：
- 執行時間（指令數、延遲）
- 記憶體使用（空間）
- 功耗（行動裝置）
```

**最佳化的基本原則**

| 原則 | 說明 | 範例 |
|------|------|------|
| 語意保持 | 最佳化不能改變程式行為 | 避免改變浮點運算順序 |
| 可逆性 | 可用於除錯的資訊不能丟失 | 保留行號對應 |
| 效益原則 | 最佳化本身開銷需合理 | 簡單最佳化先做 |

### 6.1.2 最佳化分類體系

**按分析範圍分類**

```
最佳化分類
    │
    ├── 本地最佳化（Local Optimization）
    │       └── 單一基本區塊內
    │           ├── 代數簡化
    │           ├── 常數折疊
    │           └── 常見子表達式消除
    │
    ├── 全域最佳化（Global Optimization）
    │       └── 跨基本區塊
    │           ├── 公共子表達式消除
    │           ├── 程式切片
    │           └── 死碼消除
    │
    └── 跨程序最佳化（Interprocedural Optimization）
            └── 跨翻譯單元
                ├── 內聯展開
                ├── 常數傳播
                └── 邊界分析
```

**按轉換類型分類**

| 類型 | 說明 | 範例 |
|------|------|------|
| 窾化（Peephole） | 局部指令替換 | `x*2` → `x<<1` |
| 本地 | 單一區塊 | 常數折疊 |
| 全域 | 跨區塊 | CSE、死碼消除 |
| 回饋導向 | 使用執行資訊 | 剖面導向最佳化 |

### 6.1.3 本地最佳化技術

**常數折疊（Constant Folding）**

[_code/06/06_01_constant_folding.c](_code/06/06_01_constant_folding.c)

```c
#include <stdio.h>

int constant_fold(int left, int right, char op) {
    switch (op) {
        case '+': return left + right;
        case '*': return left * right;
        case '-': return left - right;
        case '/': return left / right;
    }
    return 0;
}

int main() {
    int result = constant_fold(5, 0, '+');
    printf("5 + 0 = %d (optimized to 5)\n", result);
    
    result = constant_fold(5, 1, '*');
    printf("5 * 1 = %d (optimized to 5)\n", result);
    
    return 0;
}
```

**代數簡化（Algebraic Simplification）**

利用代數性質簡化運算式：

| 原始 | 簡化後 | 規則 |
|------|--------|------|
| `x + 0` | `x` | 加法單位元素 |
| `x * 1` | `x` | 乘法單位元素 |
| `x * 0` | `0` | 乘法零元素 |
| `x * 2` | `x + x` | 或 `x << 1` |
| `x ^ x` | `0` | XOR 自己消除 |
| `x \| 0` | `x` | OR 零元素 |
| `!(!x)` | `x` | 雙重否定消除 |

**常見子表達式消除（Common Subexpression Elimination）**

[_code/06/06_02_cse_elimination.c](_code/06/06_02_cse_elimination.c)

```c
#include <stdio.h>
#include <string.h>

int main() {
    char *ir[] = {
        "a = b + c",
        "d = b + c + 1"
    };
    
    printf("Before CSE:\n");
    printf("  a = b + c\n");
    printf("  d = b + c + 1\n");
    
    printf("\nAfter CSE:\n");
    printf("  t0 = b + c\n");
    printf("  a = t0\n");
    printf("  d = t0 + 1\n");
    
    return 0;
}
```

### 6.1.4 全域最佳化技術

**公共子表達式消除（CSE）**

[_code/06/06_07_cse_elimination.c](_code/06/06_07_cse_elimination.c)

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_EXPR 100
#define MAX_LINE 256

typedef struct {
    char lhs[32];
    char rhs[64];
} Instruction;

int main() {
    Instruction ir[] = {
        {"a", "b + c"},
        {"d", "b + c + 1"},
        {"e", "a + d"}
    };
    int n = 3;
    
    char seen_exprs[MAX_EXPR][64];
    char seen_vars[MAX_EXPR][32];
    int seen_count = 0;
    
    printf("=== Common Subexpression Elimination ===\n\n");
    printf("Original IR:\n");
    for (int i = 0; i < n; i++) {
        printf("  %s = %s\n", ir[i].lhs, ir[i].rhs);
    }
    
    printf("\nOptimized IR:\n");
    for (int i = 0; i < n; i++) {
        int found = -1;
        for (int j = 0; j < seen_count; j++) {
            if (strcmp(ir[i].rhs, seen_exprs[j]) == 0) {
                found = j;
                break;
            }
        }
        
        if (found >= 0) {
            printf("  %s = %s  // CSE: reused temp var\n", ir[i].lhs, seen_vars[found]);
        } else {
            printf("  %s = %s\n", ir[i].lhs, ir[i].rhs);
            if (ir[i].lhs[0] == 't') {
                strcpy(seen_exprs[seen_count], ir[i].rhs);
                strcpy(seen_vars[seen_count], ir[i].lhs);
                seen_count++;
            }
        }
    }
    
    printf("\nData structures:\n");
    printf("  seen_exprs[]: tracks computed expressions\n");
    printf("  seen_vars[]: maps expression -> temp variable\n");
    
    return 0;
}
```

**死碼消除（Dead Code Elimination）**

[_code/06/06_08_dead_code_elimination.c](_code/06/06_08_dead_code_elimination.c)

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    char var[32];
    int used;
} VarInfo;

typedef struct {
    char lhs[32];
    char rhs[64];
} Instruction;

int is_live(Instruction instr, VarInfo vars[], int n) {
    if (strstr(instr.rhs, "return") != NULL) return 1;
    if (strstr(instr.lhs, "printf") != NULL) return 0;
    return vars[0].used > 0;
}

int main() {
    Instruction ir[] = {
        {"x", "10"},
        {"y", "x + 5"},
        {"z", "100"},
        {"unused", "x + y"},
        {"result", "y + z"}
    };
    int n = 5;
    
    VarInfo vars[] = {
        {"x", 1}, {"y", 1}, {"z", 1}, {"unused", 0}, {"result", 1}
    };
    
    printf("=== Dead Code Elimination ===\n\n");
    printf("Original IR:\n");
    for (int i = 0; i < n; i++) {
        printf("  %s = %s\n", ir[i].lhs, ir[i].rhs);
    }
    
    printf("\nLive variables:\n");
    for (int i = 0; i < 5; i++) {
        printf("  %s: %s\n", vars[i].var, vars[i].used ? "live" : "dead");
    }
    
    printf("\nOptimized IR (dead code removed):\n");
    for (int i = 0; i < n; i++) {
        int live = 0;
        for (int j = 0; j < 5; j++) {
            if (strcmp(ir[i].lhs, vars[j].var) == 0 && vars[j].used) {
                live = 1;
                break;
            }
        }
        if (live) {
            printf("  %s = %s\n", ir[i].lhs, ir[i].rhs);
        } else {
            printf("  // REMOVED: %s = %s (dead code)\n", ir[i].lhs, ir[i].rhs);
        }
    }
    
    printf("\nAlgorithm:\n");
    printf("  1. Compute liveness of each variable\n");
    printf("  2. Mark assignments to dead variables\n");
    printf("  3. Remove dead assignments\n");
    
    return 0;
}
```

### 6.1.5 剖面導向最佳化（Profile-Guided Optimization）

利用程式執行資訊引導最佳化：

[_code/06/06_09_pgo.c](_code/06/06_09_pgo.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int block_id;
    int execution_count;
} BlockProfile;

typedef struct {
    int from_block;
    int to_block;
    int taken_count;
    int total_count;
} BranchProfile;

void instrument_program(BlockProfile blocks[], int n) {
    printf("Instrumentation: Inserting counter code at block entries\n");
    for (int i = 0; i < n; i++) {
        blocks[i].block_id = i;
        blocks[i].execution_count = 0;
        printf("  Block %d: __counter_block_%d++\n", i, i);
    }
}

void collect_profile(BlockProfile blocks[], BranchProfile branches[], int nb, int nbr) {
    printf("\nProfile Collection: Running instrumented program\n");
    printf("Simulated execution counts:\n");
    for (int i = 0; i < nb; i++) {
        blocks[i].execution_count = rand() % 1000 + 100;
        printf("  Block %d: %d executions\n", blocks[i].block_id, blocks[i].execution_count);
    }
}

void apply_optimizations(BlockProfile blocks[], BranchProfile branches[], int nb) {
    printf("\nApplying Profile-Guided Optimizations:\n");
    for (int i = 0; i < nb; i++) {
        if (blocks[i].execution_count > 500) {
            printf("  Block %d: HOT - inline, optimize aggressively\n", i);
        } else {
            printf("  Block %d: COLD - minimal optimization\n", i);
        }
    }
}

int main() {
    int num_blocks = 5;
    int num_branches = 4;
    
    BlockProfile* blocks = calloc(num_blocks, sizeof(BlockProfile));
    BranchProfile* branches = calloc(num_branches, sizeof(BranchProfile));
    
    printf("=== Profile-Guided Optimization (PGO) ===\n\n");
    
    instrument_program(blocks, num_blocks);
    collect_profile(blocks, branches, num_blocks, num_branches);
    apply_optimizations(blocks, branches, num_blocks);
    
    printf("\nPGO Phases:\n");
    printf("  1. Instrumentation: Insert counters\n");
    printf("  2. Training run: Collect execution profiles\n");
    printf("  3. Profile data: Guide optimization decisions\n");
    printf("  4. Recompile: Apply profile-informed optimizations\n");
    
    free(blocks);
    free(branches);
    
    return 0;
}
```

## 6.2 資料流分析

### 6.2.1 資料流分析的數學基礎

資料流分析是編譯器最佳化的核心理論基礎。它透過分析程式執行時資料的流動，推導出各種有價值的資訊。

**資料流分析的抽象框架**

```
程式點（Program Point）
    │
    ├── 入口點（Entry Point）
    ├── 陳述式前（Before Statement）
    ├── 陳述式後（After Statement）
    └── 出口點（Exit Point）

資料流值（Data Flow Value）
    │
    ├── 集合論觀點：狀態是某些元素的集合
    └── 格理論觀點：狀態屬於一個半格（Semi-lattice）
```

**半格理論（Semi-lattice Theory）**

半格提供了一個優雅的數學框架來描述資料流值的集合結構：

[_code/06/06_10_semi_lattice.c](_code/06/06_10_semi_lattice.c)

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int value;
} LatticeElement;

typedef struct {
    LatticeElement* elements;
    int size;
    LatticeElement top;
    LatticeElement bottom;
} SemiLattice;

LatticeElement meet(LatticeElement a, LatticeElement b) {
    LatticeElement result;
    result.value = (a.value < b.value) ? a.value : b.value;
    return result;
}

LatticeElement join(LatticeElement a, LatticeElement b) {
    LatticeElement result;
    result.value = (a.value > b.value) ? a.value : b.value;
    return result;
}

int is_leq(LatticeElement a, LatticeElement b) {
    return a.value <= b.value;
}

void print_lattice_info() {
    printf("=== Semi-Lattice Properties ===\n\n");
    printf("A semi-lattice is a partially ordered set where:\n");
    printf("  - Every pair has a Greatest Lower Bound (meet)\n");
    printf("  - Every pair has a Least Upper Bound (join)\n\n");
    
    printf("For Dataflow Analysis:\n");
    printf("  - IN set = meet of all predecessors' OUT sets\n");
    printf("  - OUT set = gen U (IN - kill)\n\n");
    
    LatticeElement a = {5}, b = {10}, c = {15};
    printf("Example with lattice elements {5, 10, 15}:\n");
    
    LatticeElement m = meet(a, c);
    printf("  meet(5, 15) = %d\n", m.value);
    
    LatticeElement j = join(a, c);
    printf("  join(5, 15) = %d\n", j.value);
    
    printf("\nPartial order: 5 <= 10 <= 15\n");
    printf("  is_leq(5, 10) = %d (true)\n", is_leq(a, b));
    printf("  is_leq(10, 5) = %d (false)\n", is_leq(b, a));
}

int main() {
    print_lattice_info();
    
    printf("\nApplication in Dataflow Analysis:\n");
    printf("  Reaching definitions: set union lattice\n");
    printf("  Available expressions: set intersection lattice\n");
    printf("  Constant propagation: constant lattice with TOP=UNINIT\n");
    
    return 0;
}
```

**資料流方程**

每個陳述式 S 定義了一個轉換函數：

$$OUT[S] = f_S(IN[S])$$

其中：
- $IN[S]$：進入 S 前的資料流值
- $OUT[S]$：離開 S 後的資料流值
- $f_S$：S 的轉換函數

### 6.2.2 可達定義分析（Reaching Definitions Analysis）

可達定義分析回答「哪些賦值可能影響這裡？」這個問題。

**問題定義**

定義 $d: v = \ldots$ 在點 $p$ 可達，若且唯若：
1. 存在一條從 $d$ 到 $p$ 的路徑
2. 該路徑上未重新定義 $v$

**應用場景**

| 應用 | 說明 |
|------|------|
| 活躍性分析 | 判斷變數是否需要保留在暫存器 |
| 常數傳播 | 若某點所有定義都是常數，可替換 |
| 別名分析 | 找出可能指涉相同記憶體的指標 |

**GEN 和 KILL 集合**

```
GEN[B]：區塊 B 產生的定義
KILL[B]：區塊 B 殺死的定義（對同一變數的其他定義）
```

[_code/06/06_11_gen_kill.c](_code/06/06_11_gen_kill.c)

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_VARS 50
#define MAX_DEFS 100

typedef struct {
    char var[32];
    char expr[64];
    int killed;
} Statement;

typedef struct {
    int gen[MAX_DEFS];
    int gen_count;
    int kill[MAX_DEFS];
    int kill_count;
} GenKill;

void compute_gen_kill(Statement stmts[], int n, GenKill* result, int all_defs[][2], int def_count) {
    result->gen_count = 0;
    result->kill_count = 0;
    
    printf("Computing GEN and KILL sets:\n\n");
    
    for (int i = 0; i < n; i++) {
        char def[64];
        sprintf(def, "%s=%s", stmts[i].var, stmts[i].expr);
        
        result->gen[result->gen_count++] = i;
        printf("  GEN[%d]: %s (adds definition)\n", i, def);
        
        for (int j = 0; j < def_count; j++) {
            if (all_defs[j][0] == i) continue;
            if (strcmp(stmts[i].var, stmts[all_defs[j][0]].var) == 0) {
                result->kill[result->kill_count++] = all_defs[j][1];
                printf("  KILL[%d]: kills definition %d\n", i, all_defs[j][1]);
            }
        }
    }
}

int main() {
    Statement stmts[] = {
        {"a", "10", 0},
        {"b", "a + 5", 0},
        {"a", "20", 0},
        {"c", "a + b", 0}
    };
    int n = 4;
    
    int all_defs[][2] = {
        {0, 0}, {1, 1}, {2, 2}, {3, 3}
    };
    int def_count = 4;
    
    GenKill result;
    
    printf("=== GEN and KILL Sets ===\n\n");
    printf("Statements:\n");
    for (int i = 0; i < n; i++) {
        printf("  [%d] %s = %s\n", i, stmts[i].var, stmts[i].expr);
    }
    
    compute_gen_kill(stmts, n, &result, all_defs, def_count);
    
    printf("\nResult:\n");
    printf("  GEN: {");
    for (int i = 0; i < result.gen_count; i++) {
        printf("%d%s", result.gen[i], i < result.gen_count - 1 ? ", " : "");
    }
    printf("}\n");
    printf("  KILL: {");
    for (int i = 0; i < result.kill_count; i++) {
        printf("%d%s", result.kill[i], i < result.kill_count - 1 ? ", " : "");
    }
    printf("}\n");
    
    return 0;
}
```

**迭代演算法**

[_code/06/06_12_reaching_definitions.c](_code/06/06_12_reaching_definitions.c)

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_BLOCKS 10
#define MAX_DEFS 20

typedef struct {
    int id;
    int gen[MAX_DEFS];
    int gen_count;
    int kill[MAX_DEFS];
    int kill_count;
    int pred[MAX_BLOCKS];
    int pred_count;
    int out[MAX_DEFS];
    int out_count;
} Block;

void reaching_definitions_analysis(Block blocks[], int n) {
    printf("=== Reaching Definitions Analysis ===\n\n");
    
    for (int i = 0; i < n; i++) {
        blocks[i].out_count = 0;
    }
    
    int changed = 1;
    int iteration = 0;
    
    while (changed && iteration < 100) {
        changed = 0;
        iteration++;
        
        printf("Iteration %d:\n", iteration);
        
        for (int i = 0; i < n; i++) {
            int new_out[MAX_DEFS];
            int new_count = 0;
            
            for (int p = 0; p < blocks[i].pred_count; p++) {
                int pred_id = blocks[i].pred[p];
                for (int k = 0; k < blocks[pred_id].out_count; k++) {
                    new_out[new_count++] = blocks[pred_id].out[k];
                }
            }
            
            int temp[MAX_DEFS];
            int temp_count = 0;
            for (int k = 0; k < new_count; k++) {
                int def = new_out[k];
                int killed = 0;
                for (int j = 0; j < blocks[i].kill_count; j++) {
                    if (blocks[i].kill[j] == def) {
                        killed = 1;
                        break;
                    }
                }
                if (!killed) {
                    temp[temp_count++] = def;
                }
            }
            
            for (int j = 0; j < blocks[i].gen_count; j++) {
                temp[temp_count++] = blocks[i].gen[j];
            }
            
            if (temp_count != blocks[i].out_count ||
                memcmp(temp, blocks[i].out, temp_count * sizeof(int)) != 0) {
                changed = 1;
                blocks[i].out_count = temp_count;
                memcpy(blocks[i].out, temp, temp_count * sizeof(int));
            }
            
            printf("  Block %d: OUT = {", i);
            for (int k = 0; k < blocks[i].out_count; k++) {
                printf("%d%s", blocks[i].out[k], k < blocks[i].out_count - 1 ? ", " : "");
            }
            printf("}\n");
        }
    }
    
    printf("\nConverged after %d iterations\n", iteration);
}

int main() {
    Block blocks[3];
    
    blocks[0].id = 0;
    blocks[0].gen[0] = 0;
    blocks[0].gen_count = 1;
    blocks[0].kill[0] = 2;
    blocks[0].kill_count = 1;
    blocks[0].pred_count = 0;
    
    blocks[1].id = 1;
    blocks[1].gen[0] = 1;
    blocks[1].gen_count = 1;
    blocks[1].kill[0] = 0;
    blocks[1].kill_count = 1;
    blocks[1].pred[0] = 0;
    blocks[1].pred_count = 1;
    
    blocks[2].id = 2;
    blocks[2].gen[0] = 2;
    blocks[2].gen_count = 1;
    blocks[2].kill[0] = 0;
    blocks[2].kill_count = 1;
    blocks[2].pred[0] = 0;
    blocks[2].pred[1] = 1;
    blocks[2].pred_count = 2;
    
    printf("CFG:\n");
    printf("  Block 0: a = 10  (gen: {0}, kill: {2})\n");
    printf("  Block 1: a = 20  (gen: {1}, kill: {0})\n");
    printf("  Block 2: b = a   (gen: {2}, kill: {0})\n\n");
    
    reaching_definitions_analysis(blocks, 3);
    
    printf("\nDataflow Equations:\n");
    printf("  IN[B] = union of OUT[P] for all predecessors P\n");
    printf("  OUT[B] = GEN[B] union (IN[B] - KILL[B])\n");
    
    return 0;
}
```

### 6.2.3 可用表達式分析（Available Expressions Analysis）

可用表達式分析找出「哪些表達式已經計算過？」

**問題定義**

表達式 $e$ 在點 $p$ 可用，若從起點到 $p$ 的所有路徑都：
1. 計算過 $e$
2. 之後未修改 $e$ 的任一運算元

**資料流方程式**

```
IN[B] = ∩_{P ∈ pred(B)} OUT[P]    # 交（因為要「所有路徑」）
OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])
```

**與可達定義的對比**

| 特性 | 可達定義 | 可用表達式 |
|------|----------|------------|
| 集合操作 | 聯集（∪） | 交集（∩） |
| 初值 | 空集合 | 全域集合（所有表達式） |
| 半格 | 冪集格（bottom=∅） | 反向冪集格（top=所有表達式） |

### 6.2.4 活躍性分析（Liveness Analysis）

活躍性分析判斷「這個值之後還會被用到嗎？」

**問題定義**

變數 $v$ 在點 $p$ 活躍，若存在一條從 $p$ 到程式結束的路徑，該路徑上使用了 $v$，且期間未重新定義 $v$。

**應用：暫存器配置**

[_code/06/06_13_liveness.c](_code/06/06_13_liveness.c)

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_BLOCKS 10
#define MAX_VARS 20

typedef struct {
    int id;
    int use[MAX_VARS];
    int use_count;
    int def[MAX_VARS];
    int def_count;
    int succ[MAX_BLOCKS];
    int succ_count;
    int in[MAX_VARS];
    int in_count;
    int out[MAX_VARS];
    int out_count;
} Block;

void print_set(char* name, int set[], int count) {
    printf("%s = {", name);
    for (int i = 0; i < count; i++) {
        printf("%c%s", 'a' + set[i], i < count - 1 ? ", " : "");
    }
    printf("}\n");
}

void liveness_analysis(Block blocks[], int n) {
    printf("=== Liveness Analysis ===\n\n");
    
    for (int i = 0; i < n; i++) {
        blocks[i].in_count = 0;
        blocks[i].out_count = 0;
    }
    
    int changed = 1;
    int iteration = 0;
    
    while (changed && iteration < 100) {
        changed = 0;
        iteration++;
        
        printf("Iteration %d:\n", iteration);
        
        for (int i = n - 1; i >= 0; i--) {
            int new_out[MAX_VARS] = {0};
            int new_out_count = 0;
            
            for (int s = 0; s < blocks[i].succ_count; s++) {
                int succ_id = blocks[i].succ[s];
                for (int k = 0; k < blocks[succ_id].in_count; k++) {
                    int var = blocks[succ_id].in[k];
                    int already = 0;
                    for (int j = 0; j < new_out_count; j++) {
                        if (new_out[j] == var) {
                            already = 1;
                            break;
                        }
                    }
                    if (!already) {
                        new_out[new_out_count++] = var;
                    }
                }
            }
            
            int new_in[MAX_VARS];
            int new_in_count = 0;
            
            for (int k = 0; k < new_out_count; k++) {
                new_in[new_in_count++] = new_out[k];
            }
            for (int k = 0; k < blocks[i].use_count; k++) {
                int var = blocks[i].use[k];
                int already = 0;
                for (int j = 0; j < new_in_count; j++) {
                    if (new_in[j] == var) {
                        already = 1;
                        break;
                    }
                }
                if (!already) {
                    new_in[new_in_count++] = var;
                }
            }
            
            for (int k = 0; k < blocks[i].def_count; k++) {
                int var = blocks[i].def[k];
                int new_in_temp[MAX_VARS];
                int new_in_temp_count = 0;
                for (int j = 0; j < new_in_count; j++) {
                    if (new_in[j] != var) {
                        new_in_temp[new_in_temp_count++] = new_in[j];
                    }
                }
                memcpy(new_in, new_in_temp, sizeof(int) * new_in_temp_count);
                new_in_count = new_in_temp_count;
            }
            
            if (new_out_count != blocks[i].out_count ||
                memcmp(new_out, blocks[i].out, new_out_count * sizeof(int)) != 0) {
                changed = 1;
                blocks[i].out_count = new_out_count;
                memcpy(blocks[i].out, new_out, new_out_count * sizeof(int));
            }
            
            if (new_in_count != blocks[i].in_count ||
                memcmp(new_in, blocks[i].in, new_in_count * sizeof(int)) != 0) {
                changed = 1;
                blocks[i].in_count = new_in_count;
                memcpy(blocks[i].in, new_in, new_in_count * sizeof(int));
            }
            
            printf("  Block %d: ", i);
            print_set("IN", blocks[i].in, blocks[i].in_count);
            printf("          ");
            print_set("OUT", blocks[i].out, blocks[i].out_count);
        }
    }
    
    printf("\nConverged after %d iterations\n", iteration);
}

int main() {
    Block blocks[3];
    
    blocks[0].id = 0;
    blocks[0].use[0] = 0;
    blocks[0].use_count = 1;
    blocks[0].def[0] = 0;
    blocks[0].def_count = 1;
    blocks[0].succ[0] = 1;
    blocks[0].succ_count = 1;
    
    blocks[1].id = 1;
    blocks[1].use[0] = 0;
    blocks[1].use[1] = 1;
    blocks[1].use_count = 2;
    blocks[1].def[0] = 1;
    blocks[1].def_count = 1;
    blocks[1].succ[0] = 2;
    blocks[1].succ_count = 1;
    
    blocks[2].id = 2;
    blocks[2].use[0] = 0;
    blocks[2].use[1] = 1;
    blocks[2].use_count = 2;
    blocks[2].def[0] = 2;
    blocks[2].def_count = 1;
    blocks[2].succ_count = 0;
    
    printf("CFG:\n");
    printf("  Block 0: b = a    (use: {a}, def: {b})\n");
    printf("  Block 1: c = a + b (use: {a,b}, def: {c})\n");
    printf("  Block 2: d = a + c (use: {a,c}, def: {d})\n\n");
    
    liveness_analysis(blocks, 3);
    
    printf("\nDataflow Equations:\n");
    printf("  OUT[B] = union of IN[S] for all successors S\n");
    printf("  IN[B] = USE[B] union (OUT[B] - DEF[B])\n");
    
    return 0;
}
```

### 6.2.5 別名分析（Alias Analysis）

別名分析確定指標和參照可能指向同一物件。

**別名種類**

| 種類 | 說明 | 範例 |
|------|------|------|
| 指標別名 | 指標間接參照 | `p = &x; q = p;` |
| 陣列別名 | 陣列元素間 | `a[i]` 和 `a[j]` |
| 結構別名 | 結構成員 | `s.f1` 和 `s.f2` |
| 等值別名 | 不同名稱指同物件 | `x` 和 `y` |

**Must Alias vs May Alias**

| 類型 | 定義 | 用途 |
|------|------|------|
| Must Alias | 必定指向相同物件 | 最佳化（如消除多餘載入） |
| May Alias | 可能指向相同物件 | 安全分析 |

## 6.3 指令排程與管線化

### 6.3.1 管線化原理

現代 CPU 使用管線化來重疊指令執行，提高指令吞吐率。

**經典五級管線**

```
時鐘:     1     2     3     4     5     6     7     8
        ┌─────┬─────┬─────┬─────┬─────┐
指令 1: │ IF  │ ID  │ EX  │ MEM │ WB  │
        ├─────┼─────┼─────┼─────┼─────┤
指令 2: │     │ IF  │ ID  │ EX  │ MEM │ WB  │
        ├─────┼─────┼─────┼─────┼─────┤
指令 3: │     │     │ IF  │ ID  │ EX  │ MEM │ WB  │
        └─────┴─────┴─────┴─────┴─────┘
```

### 6.3.2 管線冒險（Pipeline Hazards）

管線冒險導致指令無法按預期並行執行。

**結構冒險（Structural Hazard）**

硬體資源不足導致衝突：

```
問題：記憶體只有一組讀寫電路
     IF 和 MEM 同時需要存取記憶體 → 衝突

解決方案：
1. 增加硬體資源（如分開的指令/資料快取）
2. 停頓管線
```

**資料冒險（Data Hazard）**

指令間的資料依賴：

| 類型 | 說明 | 範例 |
|------|------|------|
| RAW（讀後讀） | 必須等前指令寫入 | `x = 1; y = x;` |
| WAR（寫後讀） | 不能過早覆寫 | `x = y; y = 1;` |
| WAW（寫後寫） | 不能覆寫順序 | `x = 1; x = 2;` |

**控制冒險（Control Hazard）**

分支決策延遲：

```
問題：分支條件在執行階段才知曉
     此時 IF 階段已取錯了指令

解決方案：
1. 靜態分支預測（總是跳轉/總是不跳）
2. 動態分支預測（使用歷史資訊）
3. 分支延遲槽（Delay Slot）
```

### 6.3.3 指令排程演算法

指令排程重新排列指令順序以最小化管線停頓。

**List Scheduling（清單排程）**

[_code/06/06_06_list_scheduling.c](_code/06/06_06_list_scheduling.c)

```c
#include <stdio.h>

int main() {
    printf("List Scheduling Algorithm:\n");
    printf("1. Build dependency graph from CFG\n");
    printf("2. Calculate depth (critical path length) for each instruction\n");
    printf("3. Sort by depth (highest first)\n");
    printf("4. Schedule instructions respecting dependencies\n");
    printf("5. Update ready queue with scheduled instructions\n");
    return 0;
}
```

**區域性排程（Local Scheduling）**

專注於單一基本區塊內的排程：

[_code/06/06_14_local_scheduling.c](_code/06/06_14_local_scheduling.c)

```c
#include <stdio.h>
#include <stdlib.h>

#define MAX_NODES 20
#define MAX_EDGES 40

typedef struct {
    int id;
    int depth;
    int scheduled;
} Node;

typedef struct {
    int from;
    int to;
} Edge;

int has_all_preds_scheduled(Node nodes[], int node_id, Edge edges[], int edge_count, int scheduled_count) {
    for (int i = 0; i < edge_count; i++) {
        if (edges[i].to == node_id) {
            int pred_scheduled = 0;
            for (int j = 0; j < scheduled_count; j++) {
                if (nodes[j].id == edges[i].from) {
                    pred_scheduled = 1;
                    break;
                }
            }
            if (!pred_scheduled) return 0;
        }
    }
    return 1;
}

int compute_depth(Node nodes[], int node_id, Edge edges[], int edge_count, Node result_nodes[]) {
    int max_pred_depth = -1;
    
    for (int i = 0; i < edge_count; i++) {
        if (edges[i].to == node_id) {
            for (int j = 0; j < MAX_NODES; j++) {
                if (result_nodes[j].id == edges[i].from) {
                    if (result_nodes[j].depth > max_pred_depth) {
                        max_pred_depth = result_nodes[j].depth;
                    }
                    break;
                }
            }
        }
    }
    
    if (max_pred_depth < 0) return 0;
    return max_pred_depth + 1;
}

void local_scheduling(Node nodes[], int n, Edge edges[], int e, int issue_width) {
    printf("=== Local Scheduling (Issue Width = %d) ===\n\n", issue_width);
    
    Node result_nodes[MAX_NODES];
    int result_count = 0;
    
    for (int i = 0; i < n; i++) {
        result_nodes[i].id = nodes[i].id;
        result_nodes[i].depth = 0;
        result_nodes[i].scheduled = 0;
    }
    
    for (int i = 0; i < n; i++) {
        result_nodes[i].depth = compute_depth(result_nodes, nodes[i].id, edges, e, result_nodes);
    }
    
    printf("Node depths (critical path lengths):\n");
    for (int i = 0; i < n; i++) {
        printf("  Node %c: depth = %d\n", 'A' + result_nodes[i].id, result_nodes[i].depth);
    }
    
    printf("\nScheduling:\n");
    int clock = 0;
    
    while (result_count < n) {
        Node ready[MAX_NODES];
        int ready_count = 0;
        
        for (int i = 0; i < n; i++) {
            if (result_nodes[i].scheduled) continue;
            if (has_all_preds_scheduled(result_nodes, result_nodes[i].id, edges, e, result_count)) {
                ready[ready_count++] = result_nodes[i];
            }
        }
        
        if (ready_count == 0) {
            printf("  Clock %d: No ready instructions (cycle detected)\n", clock);
            break;
        }
        
        for (int i = 0; i < ready_count && result_count < n; i++) {
            for (int j = 0; j < n; j++) {
                if (result_nodes[j].id == ready[i].id && !result_nodes[j].scheduled) {
                    result_nodes[j].scheduled = 1;
                    printf("  Clock %d: Execute Node %c\n", clock, 'A' + result_nodes[j].id);
                    result_count++;
                    break;
                }
            }
        }
        clock++;
    }
    
    printf("\nTotal schedule length: %d cycles\n", clock);
}

int main() {
    Node nodes[] = {{0, 0, 0}, {1, 0, 0}, {2, 0, 0}, {3, 0, 0}};
    int n = 4;
    
    Edge edges[] = {{0, 2}, {1, 2}, {2, 3}};
    int e = 3;
    
    printf("DAG:\n");
    printf("    A\n");
    printf("   / \\\n");
    printf("  B   C\n");
    printf("   \\ /\n");
    printf("    D\n\n");
    
    local_scheduling(nodes, n, edges, e, 2);
    
    printf("\nAlgorithm:\n");
    printf("  1. Build DAG from block instructions\n");
    printf("  2. Compute depth (critical path) for each node\n");
    printf("  3. Sort by depth (highest first)\n");
    printf("  4. Schedule up to issue_width instructions per cycle\n");
    
    return 0;
}
```

### 6.3.4 迴圈展開與封裝（Loop Unrolling & Jam）

迴圈展開減少迴圈控制開銷並增加指令級並行。

**簡單展開**

```c
// 原始
for (i = 0; i < n; i++)
    a[i] = b[i] * 2;

// 展開 4 次
for (i = 0; i < n - 3; i += 4) {
    a[i] = b[i] * 2;
    a[i+1] = b[i+1] * 2;
    a[i+2] = b[i+2] * 2;
    a[i+3] = b[i+3] * 2;
}

// 處理剩餘
for (; i < n; i++)
    a[i] = b[i] * 2;
```

**部分展開**

```c
// 展開但保留迴圈
for (i = 0; i < n; i += 4) {
    // 批次處理 4 個元素
    t0 = b[i];
    t1 = b[i+1];
    t2 = b[i+2];
    t3 = b[i+3];
    
    a[i] = t0 * 2;
    a[i+1] = t1 * 2;
    a[i+2] = t2 * 2;
    a[i+3] = t3 * 2;
}
```

**封裝（Jamming）**

將多個迴圈的主體合併：

```c
// 原始
for (i = 0; i < n; i++)
    a[i] = b[i] * 2;
for (i = 0; i < n; i++)
    c[i] = a[i] + 1;

// 封裝後
for (i = 0; i < n; i++) {
    a[i] = b[i] * 2;
    c[i] = a[i] + 1;  // 可在此處使用，仍在暫存器中的 a[i]
}
```

## 6.4 JIT 編譯與 AOT 編譯

### 6.4.1 即時編譯原理

JIT（Just-In-Time）編譯在執行時動態將位元組碼或 IR 編譯為機器碼。

**JIT vs AOT 比較**

| 特性 | AOT 編譯 | JIT 編譯 |
|------|-----------|-----------|
| 編譯時機 | 執行前 | 執行時 |
| 執行速度 | 最快 | 次快（首次慢） |
| 記憶體 | 少 | 多（存放編譯器） |
| 離線分析 | 可用 | 執行時才知熱點 |
| 剖面資訊 | 需額外執行 | 可直接收集 |

### 6.4.2 JIT 編譯架構

[_code/06/06_04_jit_compiler.c](_code/06/06_04_jit_compiler.c)

```c
#include <stdio.h>

int main() {
    printf("JIT Compiler Simulation\n");
    printf("Tier 1: Fast compilation, light optimization\n");
    printf("Tier 2: Deep optimization, slower compilation\n");
    printf("Hot path detection triggers tier upgrades\n");
    return 0;
}
```

### 6.4.3 內嵌快取（Inline Cache）

內嵌快取是 JIT 編譯器常用的最佳化技術，用於加速方法呼叫。

[_code/06/06_05_inline_cache.c](_code/06/06_05_inline_cache.c)

```c
#include <stdio.h>

int main() {
    printf("Inline Cache States:\n");
    printf("1. Uninitialized: First call, cache class\n");
    printf("2. Monomorphic: Same class, direct jump\n");
    printf("3. Polymorphic: Few classes, lookup table\n");
    printf("4. Megamorphic: Many classes, generic dispatch\n");
    return 0;
}
```

### 6.4.4 去最佳化（Deoptimization）

JIT 編譯器的假設失效時，需要回退到解譯執行。

**常見觸發條件**

| 條件 | 說明 |
|------|------|
| 型別假設失效 | 如假設某變數是 int，實際變成 long |
| 剖面失效 | 某分支突然變熱 |
| 類別載入 | 新類別可能影響別名分析 |
| 斷言失敗 | assert 或 debug 檢查失敗 |

[_code/06/06_15_deoptimization.c](_code/06/06_15_deoptimization.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    TYPE_ASSUMPTION_FAILED,
    PROFILE_INVALIDATED,
    CLASS_LOADED,
    ASSERTION_FAILED
} DeoptReason;

typedef struct {
    int bci;
    DeoptReason reason;
    void* target_address;
} DeoptInfo;

typedef struct {
    int deopt_counts[100];
    int unstable标记[100];
} ProfileData;

void handle_deoptimization(DeoptInfo* info, ProfileData* profile) {
    printf("=== Deoptimization Handler ===\n\n");
    
    const char* reason_str[] = {
        "Type assumption failed",
        "Profile invalidated",
        "Class loaded",
        "Assertion failed"
    };
    
    printf("Deoptimization triggered:\n");
    printf("  Bytecode index: %d\n", info->bci);
    printf("  Reason: %s\n", reason_str[info->reason]);
    printf("  Target address: %p\n", info->target_address);
    
    printf("\nRecovery steps:\n");
    printf("  1. Get current interpreter frame\n");
    printf("  2. Copy register/stack state\n");
    printf("  3. Jump to interpreter\n");
    printf("  4. Update profile information\n");
    
    profile->deopt_counts[info->bci]++;
    
    if (profile->deopt_counts[info->bci] > 3) {
        printf("\n  WARNING: Deopt count > 3, marking as unstable\n");
        printf("  Future recompilation will use more conservative assumptions\n");
        profile->unstable标记[info->bci] = 1;
    }
    
    printf("\n  Returning to interpreter loop...\n");
}

int main() {
    ProfileData profile;
    memset(&profile, 0, sizeof(profile));
    
    printf("=== JIT Deoptimization Demo ===\n\n");
    
    DeoptInfo info = {
        .bci = 42,
        .reason = TYPE_ASSUMPTION_FAILED,
        .target_address = (void*)0x7fff0000
    };
    
    printf("Scenario: Variable assumed to be int, but became long\n\n");
    handle_deoptimization(&info, &profile);
    
    printf("\n=== Common Deoptimization Triggers ===\n\n");
    printf("1. Type assumption failed\n");
    printf("   - Assumed int, got long/string\n");
    printf("\n2. Profile invalidated\n");
    printf("   - Branch suddenly becomes hot\n");
    printf("\n3. Class loaded\n");
    printf("   - New class may affect alias analysis\n");
    printf("\n4. Assertion failed\n");
    printf("   - Debug check in optimized code fails\n");
    
    return 0;
}
```

## 6.5 SIMD 與向量化的應用

### 6.5.1 SIMD 原理

SIMD（Single Instruction, Multiple Data）允許一條指令同時處理多個資料元素。

**向量化計算模型**

```
傳統方式（Scalar）：
 時鐘 1: a[0] + b[0] → c[0]
 時鐘 2: a[1] + b[1] → c[1]
 時鐘 3: a[2] + b[2] → c[2]
 時鐘 4: a[3] + b[3] → c[3]

SIMD 方式（Vector）：
 時鐘 1: [a0,a1,a2,a3] + [b0,b1,b2,b3] → [c0,c1,c2,c3]
```

**理論加速比**

加速比取決於 SIMD 寬度：

| SIMD 寬度 | 資料類型 | FP32 加速比 | FP64 加速比 |
|-----------|-----------|-------------|-------------|
| SSE | 128 位元 | 4x | 2x |
| AVX | 256 位元 | 8x | 4x |
| AVX-512 | 512 位元 | 16x | 8x |
| NEON | 128 位元 | 4x | 2x |

### 6.5.2 SIMD 指令集詳解

**SSE（Streaming SIMD Extensions）**

| 暫存器 | 大小 | 說明 |
|--------|------|------|
| XMM0-XMM7 | 128 位元 | 8 個 128 位元暫存器 |
| XMM8-XMM15 | 128 位元 | (x86-64) 更多暫存器 |

**關鍵指令**

```c
// 載入/儲存
__m128 _mm_load_ps(float* p);        // 載入 4 個 float
void _mm_store_ps(float* p, __m128 a); // 儲存 4 個 float

// 算術運算
__m128 _mm_add_ps(__m128 a, __m128 b);  // a + b
__m128 _mm_mul_ps(__m128 a, __m128 b);  // a * b

// 比較
__m128 _mm_cmplt_ps(__m128 a, __m128 b); // a < b
```

**AVX（Advanced Vector Extensions）**

AVX 將暫存器擴展到 256 位元，並引入 VEX 前綴：

```c
// AVX 指令（使用 YMM 暫存器）
__m256 _mm256_load_ps(float* p);        // 載入 8 個 float
__m256 _mm256_add_ps(__m256 a, __m256 b); // 8 個 float 相加
```

**AVX-512**

最新的 SIMD 擴展，支援 512 位元操作：

| 特性 | 說明 |
|------|------|
| 暫存器 | ZMM0-ZMM31（512 位元） |
| 暫存器可遮罩 | K0-K7（可遮罩暫存器） |
| 融合乘加 | FMA 指令 |
| 嵌入式 rounding | 可選 rounding 模式 |

### 6.5.3 自動向量化

現代編譯器能自動將純量程式碼向量化。

**向量化條件**

```c
// 可向量化的範例
void vector_add(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i++)
        c[i] = a[i] + b[i];
}

// 編譯器自動轉換為：
// 使用 SIMD 指令，每次處理 4（或 8）個元素
```

**向量化的障礙**

| 障礙 | 說明 | 解決方案 |
|------|------|----------|
| 記憶體對齊 | SIMD 要求記憶體對齊 | 使用對齊的載入/儲存指令 |
| 依賴關係 | 迴圈迭代間有依賴 | 進行依賴分析或展開 |
| 條件分支 | 向量化分支困難 | 使用遮罩指令 |
| 混疊（Aliasing） | 指標可能重疊 | 使用 `restrict` 限定 |

### 6.5.4 手動向量化範例

```c
// 手動 AVX 向量化：矩陣乘法
void matmul_avx(float* A, float* B, float* C, int N) {
    for (int i = 0; i < N; i++) {
        for (int k = 0; k < N; k++) {
            // 載入 A[i][k] 並廣播
            __m256 a_ik = _mm256_set1_ps(A[i * N + k]);
            
            // 對 j 維度向量化
            for (int j = 0; j < N; j += 8) {
                // 載入 B[k][j] 和 C[i][j]
                __m256 b_kj = _mm256_loadu_ps(&B[k * N + j]);
                __m256 c_ij = _mm256_loadu_ps(&C[i * N + j]);
                
                // C[i][j] += A[i][k] * B[k][j]
                __m256 result = _mm256_fmadd_ps(a_ik, b_kj, c_ij);
                
                _mm256_storeu_ps(&C[i * N + j], result);
            }
        }
    }
}
```

### 6.5.5 矩陣乘法最佳化

矩陣乘法是 BLAS 的核心操作，以下是完整的最佳化過程：

```c
// 分塊矩陣乘法 + SIMD + 暫存器重用
void gemm_optimized(float* A, float* B, float* C, int N) {
    const int block_size = 64;  // 快取友好分塊大小
    
    for (int ii = 0; ii < N; ii += block_size) {
        for (int jj = 0; jj < N; jj += block_size) {
            for (int kk = 0; kk < N; kk += block_size) {
                // 分塊計算
                int i_max = min(ii + block_size, N);
                int j_max = min(jj + block_size, N);
                int k_max = min(kk + block_size, N);
                
                for (int i = ii; i < i_max; i++) {
                    for (int k = kk; k < k_max; k++) {
                        // A[i][k] 廣播
                        float a_ik = A[i * N + k];
                        __m256 a_vec = _mm256_set1_ps(a_ik);
                        
                        int j;
                        // 8路向量化
                        for (j = jj; j < j_max - 7; j += 8) {
                            __m256 c_vec = _mm256_loadu_ps(&C[i * N + j]);
                            __m256 b_vec = _mm256_loadu_ps(&B[k * N + j]);
                            c_vec = _mm256_fmadd_ps(a_vec, b_vec, c_vec);
                            _mm256_storeu_ps(&C[i * N + j], c_vec);
                        }
                        // 處理剩餘
                        for (; j < j_max; j++) {
                            C[i * N + j] += a_ik * B[k * N + j];
                        }
                    }
                }
            }
        }
    }
}
```

## 6.6 其他最佳化技術

### 6.6.1 內聯展開（Inlining）

內聯展開將函數呼叫替換為函數主體，消除呼叫開銷。

[_code/06/06_16_inlining.c](_code/06/06_16_inlining.c)

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    char name[32];
    int body_size;
    int is_leaf;
    int is_recursive;
    int execution_freq;
} Function;

int has_static_vars(Function* func) {
    return 0;
}

int should_inline(Function* call_site, Function* callee) {
    if (callee->is_recursive) {
        printf("  NOT inlining: %s is recursive\n", callee->name);
        return 0;
    }
    
    if (callee->body_size > 100) {
        printf("  NOT inlining: %s body too large (%d statements)\n",
               callee->name, callee->body_size);
        return 0;
    }
    
    if (has_static_vars(callee)) {
        printf("  NOT inlining: %s has static variables\n", callee->name);
        return 0;
    }
    
    if (callee->is_leaf && callee->body_size < 20) {
        printf("  Inlining: %s is small leaf function\n", callee->name);
        return 1;
    }
    
    if (call_site->execution_freq > 1000) {
        printf("  Inlining: %s is called frequently (%d times)\n",
               callee->name, call_site->execution_freq);
        return 1;
    }
    
    return 0;
}

void inline_function(char* result, Function* call_site, Function* callee) {
    printf("Inlining %s at call site %s:\n", callee->name, call_site->name);
    printf("  1. Copy function body\n");
    printf("  2. Substitute parameters with arguments\n");
    printf("  3. Handle return statements\n");
    printf("  4. Insert inlined code\n");
    
    sprintf(result, "// Inlined %s\n%s", callee->name,
            callee->is_leaf ? "// Leaf function - efficient\n" : "// Non-leaf function\n");
}

int main() {
    Function square = {"square", 3, 1, 0, 0};
    Function big_func = {"big_func", 150, 0, 0, 100};
    Function hot_loop = {"hot_loop", 15, 1, 0, 5000};
    Function recursive = {"factorial", 20, 1, 1, 0};
    
    Function caller = {"caller", 50, 0, 0, 2000};
    
    printf("=== Function Inlining Analysis ===\n\n");
    
    char result[256];
    
    printf("Test 1: Small leaf function\n");
    inline_function(result, &caller, &square);
    printf("  should_inline: %s\n\n", should_inline(&caller, &square) ? "YES" : "NO");
    
    printf("Test 2: Large function\n");
    inline_function(result, &caller, &big_func);
    printf("  should_inline: %s\n\n", should_inline(&caller, &big_func) ? "YES" : "NO");
    
    printf("Test 3: Hot path function\n");
    inline_function(result, &caller, &hot_loop);
    printf("  should_inline: %s\n\n", should_inline(&caller, &hot_loop) ? "YES" : "NO");
    
    printf("Test 4: Recursive function\n");
    inline_function(result, &caller, &recursive);
    printf("  should_inline: %s\n\n", should_inline(&caller, &recursive) ? "YES" : "NO");
    
    printf("Inlining Benefits:\n");
    printf("  - Eliminates call overhead\n");
    printf("  - Enables cross-function optimizations\n");
    printf("  - Improves cache locality\n\n");
    
    printf("Inlining Costs:\n");
    printf("  - Code bloat\n");
    printf("  - Increased register pressure\n");
    printf("  - Compile time increase\n");
    
    return 0;
}
```

### 6.6.2 逃逸分析（Escape Analysis）

逃逸分析確定物件是否逃離其創建的作用域。

[_code/06/06_17_escape_analysis.c](_code/06/06_17_escape_analysis.c)

```c
#include <stdio.h>
#include <string.h>

typedef enum {
    ESCAPE_LOCAL,
    ESCAPE_ARG,
    ESCAPE_GLOBAL
} EscapeLevel;

typedef struct {
    char name[32];
    EscapeLevel level;
} ObjectInfo;

typedef struct {
    int is_global;
    int is_return;
    int is_store_through_pointer;
    int is_passed_as_argument;
} UseInfo;

EscapeLevel analyze_object_escape(UseInfo uses[], int use_count) {
    EscapeLevel escape = ESCAPE_LOCAL;
    
    for (int i = 0; i < use_count; i++) {
        if (uses[i].is_global) return ESCAPE_GLOBAL;
        if (uses[i].is_return) return ESCAPE_GLOBAL;
        if (uses[i].is_store_through_pointer) return ESCAPE_ARG;
        if (uses[i].is_passed_as_argument) escape = ESCAPE_ARG;
    }
    
    return escape;
}

const char* escape_level_str(EscapeLevel level) {
    switch (level) {
        case ESCAPE_LOCAL: return "Local (No Escape)";
        case ESCAPE_ARG: return "Arg Escape";
        case ESCAPE_GLOBAL: return "Global Escape";
    }
    return "Unknown";
}

void stack_allocate(ObjectInfo* obj, EscapeLevel level) {
    if (level == ESCAPE_LOCAL) {
        obj->level = ESCAPE_LOCAL;
        printf("  %s: STACK allocation (does not escape)\n", obj->name);
    } else {
        obj->level = ESCAPE_GLOBAL;
        printf("  %s: HEAP allocation (escapes)\n", obj->name);
    }
}

int main() {
    printf("=== Escape Analysis ===\n\n");
    
    ObjectInfo objects[] = {
        {"local_obj", ESCAPE_LOCAL},
        {"passed_obj", ESCAPE_ARG},
        {"global_obj", ESCAPE_GLOBAL}
    };
    
    printf("Escape Levels:\n");
    printf("  1. No Escape: Object used only in creating function\n");
    printf("  2. Arg Escape: Object passed as argument\n");
    printf("  3. Global Escape: Object escapes to global scope or heap\n\n");
    
    UseInfo test_uses1[] = {{0, 0, 0, 0}};
    UseInfo test_uses2[] = {{0, 0, 0, 1}};
    UseInfo test_uses3[] = {{1, 0, 0, 0}};
    
    printf("Analysis Results:\n");
    
    EscapeLevel level1 = analyze_object_escape(test_uses1, 1);
    printf("  Test object 1: %s\n", escape_level_str(level1));
    
    EscapeLevel level2 = analyze_object_escape(test_uses2, 1);
    printf("  Test object 2: %s\n", escape_level_str(level2));
    
    EscapeLevel level3 = analyze_object_escape(test_uses3, 1);
    printf("  Test object 3: %s\n", escape_level_str(level3));
    
    printf("\nStack Allocation:\n");
    stack_allocate(&objects[0], ESCAPE_LOCAL);
    stack_allocate(&objects[1], ESCAPE_ARG);
    stack_allocate(&objects[2], ESCAPE_GLOBAL);
    
    printf("\nBenefits of Stack Allocation:\n");
    printf("  - Faster allocation/deallocation\n");
    printf("  - No GC needed\n");
    printf("  - Better cache locality\n");
    
    return 0;
}
```

### 6.6.3 鎖消除（Lock Elision）

在某些情況下，鎖可以被安全地消除。

[_code/06/06_18_lock_elision.c](_code/06/06_18_lock_elision.c)

```c
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    char name[32];
    bool is_thread_local;
    bool escapes;
} LockObject;

typedef enum {
    LOCK_ACQUIRE,
    LOCK_RELEASE,
    NO_LOCK
} LockOp;

void eliminate_lock(const char* lock_name) {
    printf("  ELIMINATED: Lock on %s (thread-local object)\n", lock_name);
}

bool is_thread_local(LockObject* obj) {
    return obj->is_thread_local;
}

bool escapes_to_other_threads(LockObject* obj) {
    return obj->escapes;
}

void process_lock_op(LockObject* obj, LockOp op) {
    if (op == LOCK_ACQUIRE) {
        if (is_thread_local(obj) && !escapes_to_other_threads(obj)) {
            eliminate_lock(obj->name);
        } else {
            printf("  KEEP: Lock on %s (may be accessed by multiple threads)\n", obj->name);
        }
    }
}

int main() {
    printf("=== Lock Elision ===\n\n");
    
    LockObject local_obj = {"local_obj", true, false};
    LockObject shared_obj = {"shared_obj", false, true};
    LockObject escaped_obj = {"escaped_obj", true, true};
    
    printf("Test 1: Thread-local object\n");
    printf("  Object: %s (thread_local=%d, escapes=%d)\n",
           local_obj.name, local_obj.is_thread_local, local_obj.escapes);
    process_lock_op(&local_obj, LOCK_ACQUIRE);
    
    printf("\nTest 2: Shared object\n");
    printf("  Object: %s (thread_local=%d, escapes=%d)\n",
           shared_obj.name, shared_obj.is_thread_local, shared_obj.escapes);
    process_lock_op(&shared_obj, LOCK_ACQUIRE);
    
    printf("\nTest 3: Escaped object\n");
    printf("  Object: %s (thread_local=%d, escapes=%d)\n",
           escaped_obj.name, escaped_obj.is_thread_local, escaped_obj.escapes);
    process_lock_op(&escaped_obj, LOCK_ACQUIRE);
    
    printf("\nLock Elision Principle:\n");
    printf("  If an object is only visible to a single thread,\n");
    printf("  locks on that object are unnecessary and can be removed.\n");
    
    printf("\nBenefits:\n");
    printf("  - Eliminates lock overhead\n");
    printf("  - Reduces contention\n");
    printf("  - Enables more optimizations\n");
    
    return 0;
}
```

### 6.6.4 邊界消除（Bounds Check Elimination）

在某些情況下，陣列邊界檢查可以被消除。

[_code/06/06_19_bounds_check.c](_code/06/06_19_bounds_check.c)

```c
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int lower_bound;
    int upper_bound;
    bool bounds_enforced;
} LoopInfo;

typedef struct {
    int access_min;
    int access_max;
    bool is_bounds_check;
} Statement;

bool bounds_are_enforced(LoopInfo* loop) {
    return loop->bounds_enforced;
}

bool is_bounds_check(Statement* stmt) {
    return stmt->is_bounds_check;
}

bool is_redundant_due_to_loop(LoopInfo* loop, Statement* stmt) {
    if (!bounds_are_enforced(loop)) return false;
    
    if (stmt->access_min >= loop->lower_bound &&
        stmt->access_max <= loop->upper_bound) {
        return true;
    }
    
    return false;
}

void eliminate_bounds_check(Statement* stmt) {
    printf("  ELIMINATED: Bounds check on [%d, %d] (redundant)\n",
           stmt->access_min, stmt->access_max);
}

void process_loop(LoopInfo* loop, Statement stmts[], int n) {
    printf("Loop bounds: [%d, %d], enforced: %s\n",
           loop->lower_bound, loop->upper_bound,
           loop->bounds_enforced ? "YES" : "NO");
    
    if (!bounds_are_enforced(loop)) {
        printf("  Cannot eliminate bounds checks (bounds not enforced)\n");
        return;
    }
    
    for (int i = 0; i < n; i++) {
        if (is_bounds_check(&stmts[i])) {
            if (is_redundant_due_to_loop(loop, &stmts[i])) {
                eliminate_bounds_check(&stmts[i]);
            } else {
                printf("  KEEP: Bounds check [%d, %d] (may exceed loop bounds)\n",
                       stmts[i].access_min, stmts[i].access_max);
            }
        }
    }
}

int main() {
    printf("=== Bounds Check Elimination ===\n\n");
    
    LoopInfo safe_loop = {0, 99, true};
    
    Statement stmts[] = {
        {0, 99, true},
        {-5, 50, true},
        {50, 150, true},
        {10, 20, false}
    };
    int n = 4;
    
    printf("Test 1: Safe loop with enforced bounds [0, 99]\n");
    process_loop(&safe_loop, stmts, n);
    
    printf("\nTest 2: Unsafe loop\n");
    LoopInfo unsafe_loop = {0, 99, false};
    process_loop(&unsafe_loop, stmts, n);
    
    printf("\nWhen Bounds Checks Can Be Eliminated:\n");
    printf("  1. Loop bounds are statically determinable\n");
    printf("  2. Array access provably within bounds\n");
    printf("  3. Index already validated by previous check\n");
    printf("  4. After range analysis proves safety\n");
    
    printf("\nBenefits:\n");
    printf("  - Eliminates branch overhead\n");
    printf("  - Enables vectorization\n");
    printf("  - Reduces code size\n");
    
    return 0;
}
```
