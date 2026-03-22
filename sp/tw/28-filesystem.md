# 28. 檔案系統——inode 與日誌

## 28.1 xv6 檔案系統架構

xv6 使用 UNIX v6 的檔案系統格式：

```
┌─────────────────────────────────────────────────────────┐
│                   磁碟分區                              │
├─────────────────────────────────────────────────────────┤
│ Boot | Super | Log | Inode | Bitmap | Data blocks       │
└─────────────────────────────────────────────────────────┘
```

## 28.2 磁碟佈局

| 區塊 | 用途 | 大小 |
|------|------|------|
| Boot | 開機區 | 1 區塊 |
| Super | 超級區塊 | 1 區塊 |
| Log | 日誌區 | ? 區塊 |
| Inode | inode 區域 | ? 區塊 |
| Bitmap | 位元圖 | ? 區塊 |
| Data | 資料區 | ? 區塊 |

## 28.3 超級區塊 (super.h)

```c
struct superblock {
    uint magic;                // 檔案系統魔術數
    uint size;                // 檔案系統大小（區塊）
    uint nblocks;             // 資料區塊數
    uint ninodes;             // inode 數量
    uint nlog;                // 日誌區塊數
    uint logstart;            // 日誌起始區塊
    uint inodestart;          // inode 起始區塊
    uint bmapstart;           // 位元圖起始區塊
};
```

## 28.4 inode

inode 是檔案系統的核心結構：

```c
// fs.h
#define NINDIRECT 128
#define NDIR 13
#define MAXFILE (NINDIRECT + NDIR)

struct dinode {
    short type;               // 檔案類型
    short major;              // 主要設備號
    short minor;              // 次要設備號
    short nlink;              // 連結數
    uint size;                // 檔案大小（位元組）
    uint addrs[NDIR + 1];      // 資料區塊指標
};
```

### 28.4.1 inode 類型

```c
enum {
    T_DIR = 1,               // 目錄
    T_FILE = 2,              // 普通檔案
    T_DEVICE = 3,            // 設備
};
```

### 28.4.2 直接和間接區塊

```
inode.addrs[]
├─ addrs[0..12]: 直接區塊 (13 * 4KB = 52KB)
└─ addrs[13]:   一級間接區塊 (128 * 4KB = 512KB)
                    │
                    ├── 資料區塊指標 (128 個)
                    │
                    └── 資料區塊 (128 * 4KB)

最大檔案大小：52KB + 512KB = 564KB
```

## 28.5 目錄結構

目錄是特殊的檔案，包含目錄條目：

```c
struct dirent {
    ushort inum;              // inode 編號
    char name[DIRSIZ];       // 檔案名稱 (14 bytes)
};
```

### 28.5.1 `.` 和 `..`

每個目錄都包含：
- `.`：指向自己
- `..`：指向父目錄

## 28.6 日誌系統

日誌確保檔案系統一致性：

### 28.6.1 為什麼需要日誌？

沒有日誌的情況：
1. 寫入檔案（更新 inode 和資料區塊）
2. 系統崩潰（在寫入中途）
3. 結果：inode 和資料不一致

有日誌的情況：
1. 先將所有修改寫入日誌
2. 標記日誌為 commit
3. 執行真正的寫入
4. 如果崩潰，重做日誌

### 28.6.2 日誌結構

```c
struct logheader {
    int n;
    int block[LOGSIZE];
};

struct log {
    struct spinlock lock;
    int start;                // 日誌區起始
    int size;                 // 日誌大小
    int outstanding;          // 正在進行的系統呼叫數
    int committing;           // 是否正在 commit
    int dev;
    struct logheader lh;
};
```

### 28.6.3 日誌操作

```c
// begin_op / end_op 配對使用
begin_op();
ilock(ip);
iupdate(ip);
iunlock(ip);
end_op();

// end_op 實際執行寫入
end_op() {
    // 1. 複製修改到日誌區
    for (b = 0; b < lh.n; b++) {
        Bread(lh.block[b]);
        memmove(b->data, addr[b->data], BSIZE);
        bwrite(b);
    }
    
    // 2. 標記 commit
    lh.n = 0;
    bwrite(bh);
    
    // 3. 寫入磁碟
    for (b = 0; b < lh.n; b++) {
        brelse(lh.block[b]);
    }
}
```

## 28.7 緩衝區層

```c
struct buf {
    int valid;                 // 已讀取資料
    int disk;                  // 磁碟一致性
    uint dev;
    uint blockno;
    struct sleeplock lock;
    uint refcnt;
    struct buf *prev;
    struct buf *next;
    uint data[BSIZE / 4];
};
```

## 28.8 讀取流程

```c
// 讀取檔案
int
readi(struct inode *ip, int user_dst, uint64 dst, uint off, uint n) {
    // ...
    for (tot = 0; n > 0; ) {
        uint64 addr;
        if ((addr = bmap(ip, off / BSIZE)) == 0) break;
        
        Bread(addr);           // 讀取區塊
        memmove(dst, &buf->data[off % BSIZE], n);
        brelse(buf);
        
        off += n;
        dst += n;
        n -= n;
    }
    return tot;
}
```

## 28.9 寫入流程

```c
int
writei(struct inode *ip, int user_src, uint64 src, uint off, uint n) {
    // ...
    for (tot = 0; n > 0; ) {
        uint64 addr;
        if ((addr = bmap(ip, off / BSIZE)) == 0) break;
        
        Bread(addr);           // 讀取或配置區塊
        memmove(&buf->data[off % BSIZE], src, n);
        bwrite(buf);           // 標記為髒
        
        off += n;
        src += n;
        n -= n;
    }
    return tot;
}
```

## 28.10 小結

本章節我們學習了：
- xv6 檔案系統架構
- 超級區塊結構
- inode 的結構和大小限制
- 目錄的實現
- 日誌系統的目的和實現
- 緩衝區層

## 28.11 習題

1. 計算 xv6 的最大檔案大小
2. 研究 ext2/ext4 與 xv6 的差異
3. 實現連結（link）系統呼叫
4. 研究日誌的兩階段提交
5. 實現檔案截斷（truncate）
