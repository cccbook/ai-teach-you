# 31. 排程器——CFS 與實時排程

## 31.1 排程基礎

排程器決定哪個行程下一個執行：

```
┌─────────────────────────────────────────────────────────┐
│                    排程器                               │
│  ┌─────────────────────────────────────────────────┐  │
│  │ 1. 選擇最高優先級的行程                          │  │
│  │ 2. 如果優先級相同，Round-Robin                   │  │
│  │ 3. 時間片用完，移到更低優先級                    │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 31.2 xv6 的排程器

### 31.2.1 scheduler()

```c
void
scheduler(void) {
    struct proc *p;
    
    for (;;) {
        // 停用中斷
        intr_on();
        
        for (p = proc; p < &proc[NPROC]; p++) {
            acquire(&p->lock);
            if (p->state == RUNNABLE) {
                // 選擇這個行程
                p->state = RUNNING;
                p->pid = // ...
                
                // 切換到行程
                swtch(&c->context, &p->context);
                
                // 行程返回後，繼續迴圈
            }
            release(&p->lock);
        }
    }
}
```

## 31.3 Context Switch

### 31.3.1 swtch.S

```asm
.globl swtch
swtch:
    sd ra, 0(a0)
    sd sp, 8(a0)
    sd s0, 16(a0)
    sd s1, 24(a0)
    // ... 保存其他 s 暫存器
    ld ra, 0(a1)
    ld sp, 8(a1)
    ld s0, 16(a1)
    ld s1, 24(a1)
    // ... 恢復其他 s 暫存器
    ret
```

## 31.4 排程時機

### 31.4.1 什麼時候觸發排程？

1. **時間片中斷**：時間片用完，強制造程讓出 CPU
2. **阻塞**：行程呼叫 sleep() 等待 I/O
3. **讓出**：行程自願呼叫 yield()

### 31.4.2 yield()

```c
void
yield(void) {
    struct proc *p = myproc();
    acquire(&p->lock);
    p->state = RUNNABLE;
    sched();
    release(&p->lock);
}
```

### 31.4.3 sched()

```c
void
sched(void) {
    int intena;
    struct proc *p = myproc();
    
    if (p->state == RUNNING)
        panic("sched running");
    if (intr_get())
        panic("sched interruptible");
    
    intena = mycpu()->noff;
    if (intena == 1 && mycpu()->intena)
        panic("sched interruptible");
    
    if (p->state == RUNNABLE)
        p->ctime = ticks;  // 記錄開始等待時間
    
    swtch(&p->context, &c->context);
}
```

## 31.5 時間片

### 31.5.1 計時器中斷

```c
void
clockintr(void) {
    if ((r_scause() == 0x80000000 || r_scause() == 0x80000005) &&
        ticks % TICK == 0) {
        if (cpuid() == 0) {
            // 更新時鐘
        }
        // 發送軟體中斷給所有 CPU
    }
}
```

### 31.5.2 搶佔

```c
void
usertrap(void) {
    // ...
    if (r_scause() == 0x80000007) {
        // 計時器中斷
        if (cpuid() == 0)
            clockintr();
        intr_on();
        
        // 強制讓出 CPU
        yield();
    }
    // ...
}
```

## 31.6 睡眠和喚醒

### 31.6.1 sleep()

```c
void
sleep(void *chan, struct spinlock *lk) {
    struct proc *p = myproc();
    
    // 必須持有鎖或已經持有 p->lock
    acquire(&p->lock);
    release(lk);
    
    p->chan = chan;      // 等待的通道
    p->state = SLEEPING; // 設定為睡眠
    sched();              // 讓出 CPU
    
    // 醒來後，清除狀態
    p->chan = 0;
    
    release(&p->lock);
    acquire(lk);
}
```

### 31.6.2 wakeup()

```c
void
wakeup(void *chan) {
    struct proc *p;
    
    for (p = proc; p < &proc[NPROC]; p++) {
        if (p != myproc()) {
            acquire(&p->lock);
            if (p->state == SLEEPING && p->chan == chan) {
                p->state = RUNNABLE;  // 喚醒
            }
            release(&p->lock);
        }
    }
}
```

## 31.7 典型的睡眠模式

```c
// 磁碟 I/O 等待
void
bread(void) {
    acquire(&bache.lock);
    while (b->flags & B_DIRTY) {
        sleep(b, &bache.lock);
    }
    // ...
}
```

## 31.8 與 Linux CFS 的比較

| 特性 | xv6 | Linux CFS |
|------|-----|-----------|
| 排程演算法 | 簡單輪轉 | 完全公平排程 |
| 時間片 | 固定 | 動態 |
| 優先級 | 固定 | 動態調整 |
| 實現複雜度 | 低 | 高 |

## 31.9 小結

本章節我們學習了：
- xv6 排程器的工作方式
- scheduler() 的實現
- swtch 的工作原理
- 排程時機
- 時間片和計時器中斷
- sleep() 和 wakeup()
- 與 Linux CFS 的比較

## 31.10 習題

1. 實現多級反饋佇列排程
2. 實現 O(1) 排程器
3. 研究實時排程（SCHED_FIFO, SCHED_RR）
4. 實現公平排程（每個行程相同時間片）
5. 研究 NUMA 系統的排程考量
