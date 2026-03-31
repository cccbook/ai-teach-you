# 排程 (Scheduling)

## 概述

排程器是作業系統的核心元件，負責決定哪個程序或執行緒應該獲得 CPU 時間。排程演算法影響系統的回應性、吞吐量和公平性。在多核系統中，排程更加複雜。

## 歷史

- **1962**：IBM 開發早期排程
- **1973**：Unix 引入多級回饋佇列
- **2002**：Linux CFS 排程器
- **現在**：多種排程演算法

## 排程演算法

### 1. FIFO/FCFS

```c
// 先進先出
struct queue {
    struct task *head;
    struct task *tail;
    
    void enqueue(struct task *t) {
        if (!head) head = tail = t;
        else tail->next = t, tail = t;
    }
    
    struct task* dequeue() {
        struct task *t = head;
        if (head) head = head->next;
        return t;
    }
};
```

### 2. 時間片 Round-Robin

```c
// 每個程序獲得固定時間片
void scheduler() {
    struct task *next = runqueue.next;
    
    // 時間片遞減
    current->time_slice--;
    
    if (current->time_slice == 0) {
        // 時間片用完，放回佇列末尾
        enqueue_to_runqueue(current);
        // 選擇下一個執行
        next = dequeue_from_runqueue();
    }
    
    switch_to(next);
}
```

### 3. 多級回饋佇列 (MLFQ)

```c
// 多個優先級佇列
struct runqueue {
    struct list queue[10];  // 10 個優先級
    
    struct task* pick_next() {
        for (int i = 9; i >= 0; i--) {
            if (!list_empty(&queue[i])) {
                return list_first(&queue[i]);
            }
        }
    }
    
    // 提升/降低優先級
    void boost_priority(struct task *t) {
        if (t->priority < 9)
            t->priority++;
    }
    
    void lower_priority(struct task *t) {
        if (t->priority > 0)
            t->priority--;
    }
};
```

### 4. CFS (Completely Fair Scheduler)

```c
// Linux CFS - 紅黑樹
struct cfs_rq {
    struct rb_root tasks_time;
    struct rb_node *rb_leftmost;
    
    struct task *pick_next() {
        if (!rb_leftmost)
            return NULL;
        return container_of(rb_leftmost, struct task, run_node);
    }
    
    void enqueue(struct task *t) {
        // 根據虛擬執行時間插入
        struct rb_node **node = &tasks_time.rb_node;
        while (*node) {
            if (t->vruntime < container_of(*node, struct task, run_node)->vruntime)
                node = &(*node)->rb_left;
            else
                node = &(*node)->rb_right;
        }
        rb_link_node(&t->run_node, parent, node);
        rb_insert_color(&t->run_node, &tasks_time);
    }
};
```

### 5. 優先級排程

```c
// 優先級範圍
#define NICE_TO_PRIORITY(nice)  ((nice) + MAX_RT_PRIO)
#define MAX_RT_PRIO 100

// 即時排程 (FIFO/Round-Robin)
struct sched_param {
    int sched_priority;  // 0-99 for RT
};

pthread_attr_setschedparam(&attr, &param);
param.sched_priority = 50;
```

## 排程策略

```c
// Linux 排程類別
enum {
    SCHED_NORMAL,    // 一般程序
    SCHED_FIFO,      // 即時 FIFO
    SCHED_RR,        // 即時 Round-Robin
    SCHED_BATCH,     // 批次
    SCHED_IDLE,      // 閒置
};
```

## 多核排程

```c
// 負載平衡
void load_balance() {
    int busiest_cpu = find_busiest_cpu();
    struct cfs_rq *busiest = &per_cpu(runqueues, busiest_cpu).cfs;
    
    if (busiest->nr_running > 1) {
        struct task *task = pick_task_to_migrate(busiest);
        pull_task(busiest, task, this_cpu());
    }
}
```

## 為什麼學習排程？

1. **系統效能**：影響回應性和吞吐量
2. **即時系統**：確定性排程
3. **多核優化**：負載平衡
4. **除錯**：效能問題

## 參考資源

- "Linux Kernel Development"
- "Operating Systems: Three Easy Pieces"
- Linux 核心排程器原始碼
