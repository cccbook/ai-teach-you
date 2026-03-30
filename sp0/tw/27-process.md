# 27. 行程管理——fork、exec 與 wait

## 27.1 UNIX 行程模型

UNIX 的核心概念之一是「一切皆檔案」和「每個程式都是一個行程」。

### 27.1.1 行程系統呼叫

| 系統呼叫 | 說明 |
|---------|------|
| fork() | 建立新行程（複製目前行程） |
| exec() | 執行新程式（取代目前行程） |
| wait() | 等待子行程結束 |
| exit() | 結束目前行程 |

## 27.2 fork() 實現

fork() 建立一個新的行程：

```c
// kernel/sysproc.c
int
sys_fork(void) {
    return fork();
}

// kernel/proc.c
int
fork(void) {
    struct proc *np;
    
    // 分配新行程
    np = allocproc();
    
    // 複製使用者記憶體
    if (uvmcopy(p->pagetable, np->pagetable, p->sz) < 0) {
        freeproc(np);
        release(&np->lock);
        return -1;
    }
    np->sz = p->sz;
    
    // 複製使用者的暫存器狀態
    *np->tf = *p->tf;
    
    // 子行程有不同的返回值
    np->tf->a0 = 0;  // fork() 返回 0 給子行程
    
    // 設定新行程名稱
    safestrcpy(np->name, p->name, sizeof(p->name));
    
    np->state = RUNNABLE;
    
    return np->pid;  // 父行程返回子行程的 PID
}
```

### 27.2.1 fork() 的工作

1. 分配新的 proc 結構
2. 分配新的核心堆疊
3. 複製使用者分頁表
4. 複製暫存器狀態（tf）
5. 子行程：fork() 返回 0
6. 父行程：fork() 返回子行程 PID

## 27.3 exec() 實現

exec() 執行一個新的程式：

```c
// kernel/sysfile.c
int
sys_exec(void) {
    char path[MAXPATH];
    char *argv[MAXARG];
    
    // 取得路徑和參數
    if (argstr(0, path) < 0 || argint(1, (int*)&argv) < 0) {
        return -1;
    }
    
    return exec(path, argv);
}

// kernel/proc.c
int
exec(char *path, char **argv) {
    struct inode *ip;
    struct proghdr ph;
    pagetable_t pagetable;
    
    // 讀取 ELF 檔案
    ip = namei(path);
    el = (struct elfhdr*)pgroot;
    if (readi(ip, 0, (uint64)el, 0, sizeof(*el)) != sizeof(*el))
        goto bad;
    
    // 載入每個程式段
    for (i=0, off=sizeof(*el); i<el->phnum; i++) {
        readi(ip, 0, (uint64)ph, off, sizeof(ph));
        if (ph.type != ELF_PROG_LOAD) continue;
        if (ph.vaddr + ph.memsz < ph.vaddr) goto bad;
        if (ph.vaddr % PGSIZE != 0) goto bad;
        
        // 配置和複製記憶體
        if ((sz = uvmalloc(pagetable, sz, ph.vaddr + ph.memsz)) == 0) goto bad;
    }
    
    // 設定新的分頁表
    p->pagetable = pagetable;
    p->sz = sz;
    
    // 設定程式入口
    p->tf->epc = el->entry;
    
    return 0;
}
```

### 27.2.2 exec() 的工作

1. 讀取 ELF 檔案
2. 驗證 ELF 格式
3. 建立新的分頁表
4. 載入每個程式段到記憶體
5. 設定程式入口點
6. 設定命令列參數

## 27.4 wait() 實現

wait() 等待子行程結束：

```c
// kernel/proc.c
int
wait(uint64 addr) {
    struct proc *p;
    int havekids, pid;
    
    for (;;) {
        // 找一個有子行程的行程
        havekids = 0;
        for (p = proc; p < &proc[NPROC]; p++) {
            acquire(&p->lock);
            if (p->parent == current) {
                havekids = 1;
                if (p->state == ZOMBIE) {
                    // 找到已終止的子行程
                    pid = p->pid;
                    if (addr && copyout(current->pagetable, addr, &p->xstate, sizeof(p->xstate)) < 0) {
                        release(&p->lock);
                        return -1;
                    }
                    freeproc(p);
                    release(&p->lock);
                    return pid;
                }
            }
            release(&p->lock);
        }
        
        // 如果沒有子行程，返回錯誤
        if (!havekids) return -1;
        
        // 睡眠，等待子行程
        sleep(current, &wait_lock);
    }
}
```

## 27.5 行程狀態

```c
enum procstate {
    UNUSED,      // 未使用
    USED,        // 已分配
    SLEEPING,    // 睡眠（等待 I/O）
    RUNNABLE,    // 可執行（在記憶體中）
    RUNNING,     // 正在執行
    ZOMBIE       // 僵屍（已終止，等待父行程收割）
};
```

## 27.6 行程生命週期

```
        fork()                   exit()
UNUSED ─────→ USED ─────→ SLEEPING ─────┐
    ↑            ↓              ↑        │
    │         exec()            │        │
    │            ↓               │        │
    │         RUNNABLE ────→ RUNNING ────┤
    │              ↑                       │
    │              │sched()                │
    │              └───────────────────────┤
    │                                     ↓
    │        ┌──────────────────────────┐ │
    │        │          ZOMBIE          │ │
    │        └──────────────────────────┘ │
    │                  ↑                 │
    └──────────────────┴────────────────┘
                   wait()
```

## 27.7 典型使用模式

### 27.7.1 shell 的工作方式

```c
// 簡化版 shell
if (fork() == 0) {
    // 子行程：執行命令
    exec(cmd, argv);
    exit(1);  // 如果 exec 失敗
} else {
    // 父行程：等待命令結束
    wait(0);
}
```

### 27.7.2 管道

```c
// pipe 的實現使用 fork
int p[2];
pipe(p);

if (fork() == 0) {
    // 子行程：寫入管道
    close(1);      // 關閉 stdout
    dup(p[1]);     // 複製寫端到 stdout
    close(p[0]);   // 關閉讀端
    close(p[1]);   // 關閉寫端
    exec(cmd1);
} else {
    // 父行程：讀取管道
    close(0);      // 關閉 stdin
    dup(p[0]);     // 複製讀端到 stdin
    close(p[0]);   // 關閉讀端
    close(p[1]);   // 關閉寫端
    wait(0);
    exec(cmd2);
}
```

## 27.8 小結

本章節我們學習了：
- UNIX 行程模型
- fork() 的實現（複製行程）
- exec() 的實現（執行新程式）
- wait() 的實現（等待子行程）
- 行程狀態機
- 行程生命週期

## 27.9 習題

1. 實現一個簡單的 shell
2. 研究為什麼 fork() 返回值不同
3. 實現 pipe() 系統呼叫
4. 研究 ZOMBIE 狀態的必要性
5. 實現 dup() 系統呼叫
