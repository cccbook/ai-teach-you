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

在編譯時計算常數表達式：

```python
def constant_folding(expr):
    """常數折疊：編譯期計算常數表達式"""
    
    # 範例轉換表
    rules = {
        ('+', 5, 0): 5,      # x + 0 = x
        ('*', 5, 1): 5,      # x * 1 = x
        ('*', 5, 2): 10,     # 5 * 2 = 10
        ('/', 5, 1): 5,       # x / 1 = x
        ('&', 5, -1): 5,     # x & -1 = x
    }
    
    # 遞迴折疊
    if isinstance(expr, tuple):
        op, left, right = expr
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if (op, left, right) in rules:
                return rules[(op, left, right)]
        return (op, constant_folding(left), constant_folding(right))
    return expr
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

```python
# 原始程式碼
a = b + c
d = b + c + 1    # 重複計算 b + c

# 最佳化後
t = b + c         # 只計算一次
a = t
d = t + 1
```

### 6.1.4 全域最佳化技術

**公共子表達式消除（CSE）**

```python
def cse_elimination(ir):
    """公共子表達式消除"""
    seen = {}      # 表達式 → 臨時變數
    result = []
    
    for instr in ir:
        if '=' in instr:
            parts = instr.split('=')
            lhs = parts[0].strip()
            rhs = parts[1].strip()
            
            # 檢查是否為公共子表達式
            if rhs in seen:
                # 使用已計算的值
                result.append(f"{lhs} = {seen[rhs]}")
            else:
                result.append(instr)
                # 記錄此表達式
                if lhs.startswith('t'):  # 只記錄臨時變數
                    seen[rhs] = lhs
        else:
            result.append(instr)
    
    return result
```

**死碼消除（Dead Code Elimination）**

```python
def dead_code_elimination(ir):
    """死碼消除：移除不會影響程式結果的程式碼"""
    
    # 建立使用集合
    used = set()
    
    for instr in ir:
        if 'return' in instr:
            # 找出return語句使用的變數
            pass
    
    # 移除從未使用的賦值
    return [instr for instr in ir if not is_dead(instr, used)]
```

### 6.1.5 剖面導向最佳化（Profile-Guided Optimization）

利用程式執行資訊引導最佳化：

```python
class PGO:
    """剖面導向最佳化"""
    
    def __init__(self):
        self.execution_counts = {}  # 基本區塊執行次數
        self.branch_probs = {}      # 分支機率
    
    def instrument(self, program):
        """插入檢測碼"""
        # 在每個區塊前插入計數
        
    def collect_profile(self):
        """收集剖面資料"""
        # 執行檢測過的程式
        
    def apply_optimizations(self, program):
        """根據剖面應用最佳化"""
        # 內聯熱路徑
        # 將執行次數多的區塊最佳化
        # 分支預測最佳化
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

```python
class SemiLattice:
    """
    半格：一個偏序集合，其中每對元素都有最小上界（Join）和最大下界（Meet）
    
    形式定義：
    - 封閉性：(D, ∧) 和 (D, ∨) 都是封閉的
    - 交換律：A ∧ B = B ∧ A
    - 結合律：(A ∧ B) ∧ C = A ∧ (B ∧ C)
    - 冪等律：A ∧ A = A
    """
    
    def __init__(self, elements, meet_op, join_op, top, bottom):
        self.elements = elements
        self.meet = meet_op      # 最大下界（Meet）
        self.join = join_op      # 最小上界（Join）
        self.top = top           # 頂元素（所有其他元素的上界）
        self.bottom = bottom     # 底元素（所有其他元素的下界）
    
    def is_leq(self, a, b):
        """偏序關係：A ≤ B 當且僅當 A ∧ B = A"""
        return self.meet(a, b) == a
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

```python
def compute_gen_kill(block):
    """計算區塊的 GEN 和 KILL 集合"""
    gen = set()
    kill = set()
    defined_vars = set()
    
    for stmt in block.statements:
        if isinstance(stmt, Assignment):
            var = stmt.variable
            defined = f"{var}={stmt.rhs}"
            
            # GEN：此定義本身
            gen.add(defined)
            
            # KILL：同一變數的所有其他定義
            for d in defined_vars:
                kill.add(d)
            
            defined_vars.add(defined)
    
    return gen, kill
```

**迭代演算法**

```python
def reaching_definitions_analysis(cfg):
    """
    可達定義分析 - 迭代求解
    
    資料流方程式：
    IN[B] = ⋃_{P ∈ pred(B)} OUT[P]
    OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])
    """
    
    # 初始化：所有 OUT 為空集合
    out = {block: set() for block in cfg.blocks}
    
    changed = True
    iterations = 0
    
    while changed and iterations < 100:
        changed = False
        iterations += 1
        
        for block in cfg.blocks:
            # IN[B] = ⋃ OUT[前驅]
            in_set = set()
            for pred in block.predecessors:
                in_set |= out.get(pred, set())
            
            # OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])
            new_out = block.gen | (in_set - block.kill)
            
            if new_out != out[block]:
                out[block] = new_out
                changed = True
    
    return out, iterations
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

```python
def liveness_analysis(cfg):
    """
    活躍性分析
    
    OUT[B] = ⋃_{S ∈ succ(B)} IN[S]
    IN[B] = USE[B] ∪ (OUT[B] - DEF[B])
    
    其中：
    - USE[B]：區塊中使用但未在區塊內定義的變數
    - DEF[B]：區塊內定義的變數
    """
    
    in_vars = {block: set() for block in cfg.blocks}
    out_vars = {block: set() for block in cfg.blocks}
    
    changed = True
    iterations = 0
    
    while changed and iterations < 100:
        changed = False
        iterations += 1
        
        # 反向迭代（從後往前）
        for block in reversed(cfg.blocks):
            # OUT[B] = ⋃ IN[後繼]
            out_new = set()
            for succ in block.successors:
                out_new |= in_vars.get(succ, set())
            
            # IN[B] = USE[B] ∪ (OUT[B] - DEF[B])
            in_new = block.use | (out_new - block.def_vars)
            
            if in_new != in_vars.get(block, set()):
                in_vars[block] = in_new
                changed = True
            if out_new != out_vars.get(block, set()):
                out_vars[block] = out_new
                changed = True
    
    return in_vars, out_vars


def register_allocation(cfg, in_vars):
    """基於活躍性分析的簡單暫存器配置"""
    
    # 干涉圖：若兩個變數同時活躍，則它們干涉
    interferences = {}
    
    for block in cfg.blocks:
        live = in_vars.get(block, set()).copy()
        
        for stmt in reversed(block.statements):
            # stmt.def 中的變數與 live 中的變數干涉
            for v in stmt.def:
                for u in live:
                    if v != u:
                        add_interference(interferences, v, u)
            
            # 更新活躍集合：加入 stmt.use，移除 stmt.def
            live = live | stmt.use - stmt.def
    
    # 使用圖著色分配暫存器
    return graph_coloring(interferences, num_registers=8)
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

```python
def list_scheduling(cfg, latency_info):
    """
    清單排程演算法
    
    輸入：控制流程圖、指令延遲資訊
    輸出：排程後的指令序列
    """
    ready_queue = []      # 就緒指令佇列
    scheduled = []        # 已排程指令
    clock = 0
    
    # 初始化：沒有前驅的指令加入就緒佇列
    for instr in cfg.entry_block:
        if len(instr.preds) == 0:
            ready_queue.append(instr)
    
    while ready_queue:
        # 選擇一個指令排程
        instr = select_best_instruction(ready_queue)
        
        # 計算最早可用時間
        earliest = max(instr.release_time, clock)
        
        # 考慮資源約束
        start_time = find_available_slot(earliest, instr, resource_availability)
        
        # 排程指令
        instr.scheduled_time = start_time
        scheduled.append(instr)
        ready_queue.remove(instr)
        
        # 更新後繼指令
        for succ in instr.succs:
            update_ready(succ, instr, ready_queue)
        
        clock = start_time + latency_info[instr.type]
    
    return scheduled


def select_best_instruction(ready_queue):
    """選擇最優先的指令"""
    # 各種啟發式策略：
    # 1. 最高優先級
    # 2. 最長路徑
    # 3. 最多後繼
    # 4. 隨機
    return max(ready_queue, key=lambda i: i.priority)
```

**區域性排程（Local Scheduling）**

專注於單一基本區塊內的排程：

```python
def local_scheduling(block, issue_width=2):
    """
    區域性排程 - 簡化版
    
    問題：給定一個區塊的 DAG，儘可能在每個時鐘發射 issue_width 條指令
    """
    
    # 建構依賴圖（DAG）
    dag = build_dag(block)
    
    # 計算每個節點的深度（關鍵路徑長度）
    depths = compute_depths(dag)
    
    # 按深度排序
    sorted_nodes = sorted(dag.nodes, key=lambda n: -depths[n])
    
    scheduled = []
    clock = 0
    
    while sorted_nodes:
        # 選擇可發射且深度最大的指令
        available = [
            n for n in sorted_nodes
            if all(pred in scheduled for pred in dag.preds[n])
            and dag.issue_time[n] <= clock
        ]
        
        if not available:
            clock += 1
            continue
        
        # 選擇深度最大的
        to_schedule = max(available, key=lambda n: depths[n])
        
        # 發射（最多 issue_width 條）
        scheduled.append(to_schedule)
        sorted_nodes.remove(to_schedule)
        
        clock += 1
    
    return scheduled
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

```python
class JITCompiler:
    """
    JIT 編譯器基本架構
    
    層級：
    1. 解譯器：快速啟動，即時收集剖面
    2. C1 編譯器：快速編譯，輕量最佳化
    3. C2 編譯器：深度最佳化，編譯耗時
    """
    
    def __init__(self):
        self.interpreter = Interpreter()
        self.tier1_compiler = Tier1Compiler()  # C1 等效
        self.tier2_compiler = Tier2Compiler()    # C2 等效
        self.invocation_counts = {}              # 方法呼叫計數
        self.thresholds = {
            'tier1': 1000,   # 觸發 C1
            'tier2': 10000,  # 觸發 C2
            'deopt': 0.5     # 觸發去最佳化
        }
    
    def execute_method(self, method):
        """執行方法的入口"""
        
        # 檢查是否已編譯
        if method in self.tier2_compiler.code_cache:
            # 直接執行 C2 編譯碼
            return self.tier2_compiler.execute(method)
        
        if method in self.tier1_compiler.code_cache:
            # 執行 C1 編譯碼
            return self.tier1_compiler.execute(method)
        
        # 解譯執行，同時收集剖面
        return self.interpret_with_profiling(method)
    
    def handle_backedge(self, method, loop_id):
        """處理迴圈回邊 - 熱點偵測"""
        
        self.invocation_counts[method, loop_id] = \
            self.invocation_counts.get((method, loop_id), 0) + 1
        
        count = self.invocation_counts[method, loop_id]
        
        if count >= self.thresholds['tier2']:
            # 觸發 C2 編譯
            self.compile_tier2(method)
        elif count >= self.thresholds['tier1']:
            # 觸發 C1 編譯
            self.compile_tier1(method)
    
    def compile_tier1(self, method):
        """層級 1 編譯：快速編譯"""
        code = self.tier1_compiler.compile(method)
        self.tier1_compiler.code_cache[method] = code
        self.invocation_counts[method, 'tier'] = 0
    
    def compile_tier2(self, method):
        """層級 2 編譯：深度最佳化"""
        code = self.tier2_compiler.compile(method)
        self.tier2_compiler.code_cache[method] = code
```

### 6.4.3 內嵌快取（Inline Cache）

內嵌快取是 JIT 編譯器常用的最佳化技術，用於加速方法呼叫。

```python
class InlineCache:
    """
    內嵌快取
    
    原理：
    - 大多數方法呼叫的接收者型別是固定的
    - 記憶最後呼叫的接收者型別和跳轉目標
    - 若型別改變，更新快取並重新編譯
    """
    
    def __init__(self, method):
        self.method = method
        self.state = 'uninitialized'
        self.cached_class = None
        self.monomorphic_target = None  # 單態目標
        self.polymorphic_targets = {}   # 多態目標表
        self.megamorphic_threshold = 4  # 超過此數視為 megamorphic
    
    def lookup(self, receiver_class):
        """查詢內嵌快取"""
        
        if self.state == 'uninitialized':
            # 首次呼叫：直接呼叫並快取
            self.state = 'monomorphic'
            self.cached_class = receiver_class
            self.monomorphic_target = self.compile_for_class(receiver_class)
            return self.monomorphic_target
        
        elif self.state == 'monomorphic':
            if receiver_class == self.cached_class:
                # 快取命中
                return self.monomorphic_target
            else:
                # 快取失效：轉為多態
                self.state = 'polymorphic'
                self.polymorphic_targets[self.cached_class] = self.monomorphic_target
                self.cached_class = None
                # 繼續處理...
        
        elif self.state == 'polymorphic':
            if receiver_class in self.polymorphic_targets:
                return self.polymorphic_targets[receiver_class]
            else:
                if len(self.polymorphic_targets) < self.megamorphic_threshold:
                    # 新增一個目標
                    self.polymorphic_targets[receiver_class] = \
                        self.compile_for_class(receiver_class)
                else:
                    # 超過閾值：megamorphic，使用 megamorphic 分派
                    self.state = 'megamorphic'
        
        elif self.state == 'megamorphic':
            # megamorphic：使用查表分派
            return self.megamorphic_lookup(receiver_class)
        
        return None  # fallback
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

```python
class Deoptimization:
    """去最佳化處理"""
    
    def handle_deoptimization(self, reason, bci, target):
        """
        處理去最佳化
        
        1. 找到對應的解譯器框架
        2. 複製目前的暫存器/堆疊狀態
        3. 跳轉到解譯器
        4. 可能重新編譯（考慮剖面失效原因）
        """
        
        # 取得目前位元組碼指標
        current_bci = get_bci_from_pc(target)
        
        # 取得目前堆疊框架
        frame = get_current_frame()
        
        # 建立解譯器堆疊框架
        interpreter_frame = create_interpreter_frame(frame)
        
        # 更新剖面資訊（考慮未來重新編譯）
        update_profile(bci, reason)
        
        # 若多次去最佳化，標記為「不穩定」，降低重新編譯優先級
        if self.deopt_counts[bci] > 3:
            mark_as_unstable(bci)
        
        # 跳轉到解譯器
        interpreter_loop(interpreter_frame)
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

```python
def inline_function(call_site, callee):
    """
    內聯展開
    
    優點：
    - 消除函數呼叫開銷
    - 開啟更多最佳化機會（如跨函數 CSE）
    
    缺點：
    - 增加程式大小（程式膨脹）
    - 可能增加暫存器壓力
    """
    
    # 檢查內聯條件
    if not should_inline(call_site, callee):
        return None
    
    # 複製函數主體
    body_copy = copy_body(callee)
    
    # 參數替換
    for param, arg in zip(callee.params, call_site.args):
        body_copy = substitute(body_copy, param, arg)
    
    # 設定返回值的替換
    body_copy = handle_return(body_copy, call_site.lhs)
    
    return body_copy


def should_inline(call_site, callee):
    """決定是否應該內聯"""
    
    # 內聯禁忌：
    # 1. 遞迴呼叫（直接或間接）
    if is_recursive(callee):
        return False
    
    # 2. 函數過大
    if len(callee.body) > 100:
        return False
    
    # 3. 包含可變動的靜態變數
    if has_static_vars(callee):
        return False
    
    # 內聯好處：
    # 1. 函數很小的巢狀呼叫
    # 2. 熱路徑上的呼叫
    # 3. 虚函數呼叫（單態內聯）
    
    if callee.is_leaf and len(callee.body) < 20:
        return True
    
    if call_site.execution_frequency > 1000:
        return True
    
    return False
```

### 6.6.2 逃逸分析（Escape Analysis）

逃逸分析確定物件是否逃離其創建的作用域。

```python
def escape_analysis(method):
    """
    逃逸分析
    
    逃逸等級：
    - 不逃逸（No Escape）：物件僅在建立它的函數中使用
    - 參數逃逸（Arg Escape）：作為參數傳遞
    - 全域逃逸（Global Escape）：逃逸到全域或堆積
    """
    
    # 建立物件的逃逸圖
    escape_graph = {}
    
    for stmt in method.statements:
        if isinstance(stmt, NewObject):
            obj = stmt.object
            escape_level = analyze_object_escape(stmt, method)
            escape_graph[obj] = escape_level
    
    return escape_graph


def analyze_object_escape(stmt, method):
    """分析單一物件的逃逸等級"""
    
    escape = 'local'  # 初始假設：本地
    
    # 分析語句使用
    for use in stmt.uses:
        if use.is_global:
            return 'global'
        if use.is_return:
            return 'global'
        if use.is_store_through_pointer:
            return 'arg_escape'
        if use.is_passed_as_argument:
            escape = max(escape, 'arg_escape')
    
    return escape


# 逃逸分析的應用：棧配置
def stack_allocate(method, escape_graph):
    """
    棧配置：若物件不逃逸，可在棧上配置而非堆積
    
    優點：
    - 配置/釋放速度快
    - 無需 GC 追蹤
    - 提高快取友好性
    """
    
    for obj, escape_level in escape_graph.items():
        if escape_level == 'local':
            # 可在棧上配置
            obj.allocation = 'stack'
        else:
            # 必須在堆積上配置
            obj.allocation = 'heap'
```

### 6.6.3 鎖消除（Lock Elision）

在某些情況下，鎖可以被安全地消除。

```python
def lock_elision(method):
    """
    鎖消除
    
    原理：
    若物件只在單一執行緒中可見，則鎖是不必要的
    """
    
    for stmt in method.statements:
        if isinstance(stmt, LockAcquire):
            obj = stmt.lock_object
            
            # 檢查物件是否為本地且不逃逸
            if is_thread_local(obj) and not escapes_to_other_threads(obj):
                # 鎖可以被消除
                eliminate_lock(stmt)
```

### 6.6.4 邊界消除（Bounds Check Elimination）

在某些情況下，陣列邊界檢查可以被消除。

```python
def bounds_check_elimination(method):
    """
    邊界檢查消除
    
    情況：
    1. 靜態可確定的存取
    2. 已驗證過的索引
    3. 進入安全的迴圈
    """
    
    for loop in method.loops:
        # 檢查迴圈是否收斂
        if loop.bounds_are_enforced():
            # 迴圈內的邊界檢查可能消除
            for stmt in loop.statements:
                if is_bounds_check(stmt):
                    if is_redundant_due_to_loop(loop, stmt):
                        eliminate_bounds_check(stmt)
```
