# 28. File System——inode and Logging

## 28.1 xv6 File System Architecture

xv6 uses UNIX v6 file system format:

```
┌─────────────────────────────────────────────────────────┐
│                   Disk Partition                        │
├─────────────────────────────────────────────────────────┤
│ Boot | Super | Log | Inode | Bitmap | Data blocks       │
└─────────────────────────────────────────────────────────┘
```

## 28.2 Disk Layout

| Block | Purpose | Size |
|-------|---------|------|
| Boot | Boot sector | 1 block |
| Super | Superblock | 1 block |
| Log | Log area | ? blocks |
| Inode | Inode area | ? blocks |
| Bitmap | Bitmap | ? blocks |
| Data | Data area | ? blocks |

## 28.3 Superblock (super.h)

```c
struct superblock {
    uint magic;                // File system magic number
    uint size;                // File system size (blocks)
    uint nblocks;             // Number of data blocks
    uint ninodes;             // Number of inodes
    uint nlog;                // Number of log blocks
    uint logstart;            // Log start block
    uint inodestart;          // Inode start block
    uint bmapstart;           // Bitmap start block
};
```

## 28.4 inode

inode is the core structure of the file system:

```c
// fs.h
#define NINDIRECT 128
#define NDIR 13
#define MAXFILE (NINDIRECT + NDIR)

struct dinode {
    short type;               // File type
    short major;              // Major device number
    short minor;              // Minor device number
    short nlink;              // Link count
    uint size;                // File size (bytes)
    uint addrs[NDIR + 1];      // Data block pointers
};
```

### 28.4.1 inode Types

```c
enum {
    T_DIR = 1,               // Directory
    T_FILE = 2,              // Regular file
    T_DEVICE = 3,            // Device
};
```

### 28.4.2 Direct and Indirect Blocks

```
inode.addrs[]
├─ addrs[0..12]: Direct blocks (13 * 4KB = 52KB)
└─ addrs[13]:   Single indirect block (128 * 4KB = 512KB)
                    │
                    ├── Data block pointers (128)
                    │
                    └── Data blocks (128 * 4KB)

Maximum file size: 52KB + 512KB = 564KB
```

## 28.5 Directory Structure

Directory is a special file containing directory entries:

```c
struct dirent {
    ushort inum;              // inode number
    char name[DIRSIZ];       // File name (14 bytes)
};
```

### 28.5.1 `.` and `..`

Every directory contains:
- `.`: Points to itself
- `..`: Points to parent directory

## 28.6 Logging System

Logging ensures file system consistency:

### 28.6.1 Why Logging?

Without logging:
1. Write to file (update inode and data blocks)
2. System crash (during write)
3. Result: inode and data inconsistent

With logging:
1. Write all modifications to log first
2. Mark log as commit
3. Perform actual write
4. If crash, redo log

### 28.6.2 Log Structure

```c
struct logheader {
    int n;
    int block[LOGSIZE];
};

struct log {
    struct spinlock lock;
    int start;                // Log area start
    int size;                 // Log size
    int outstanding;          // Number of ongoing system calls
    int committing;           // Whether committing
    int dev;
    struct logheader lh;
};
```

### 28.6.3 Log Operations

```c
// begin_op / end_op pair
begin_op();
ilock(ip);
iupdate(ip);
iunlock(ip);
end_op();

// end_op actually performs write
end_op() {
    // 1. Copy modifications to log area
    for (b = 0; b < lh.n; b++) {
        Bread(lh.block[b]);
        memmove(b->data, addr[b->data], BSIZE);
        bwrite(b);
    }
    
    // 2. Mark commit
    lh.n = 0;
    bwrite(bh);
    
    // 3. Write to disk
    for (b = 0; b < lh.n; b++) {
        brelse(lh.block[b]);
    }
}
```

## 28.7 Buffer Layer

```c
struct buf {
    int valid;                 // Has data been read
    int disk;                  // Disk consistency
    uint dev;
    uint blockno;
    struct sleeplock lock;
    uint refcnt;
    struct buf *prev;
    struct buf *next;
    uint data[BSIZE / 4];
};
```

## 28.8 Read Flow

```c
// Read file
int
readi(struct inode *ip, int user_dst, uint64 dst, uint off, uint n) {
    // ...
    for (tot = 0; n > 0; ) {
        uint64 addr;
        if ((addr = bmap(ip, off / BSIZE)) == 0) break;
        
        Bread(addr);           ; Read block
        memmove(dst, &buf->data[off % BSIZE], n);
        brelse(buf);
        
        off += n;
        dst += n;
        n -= n;
    }
    return tot;
}
```

## 28.9 Write Flow

```c
int
writei(struct inode *ip, int user_src, uint64 src, uint off, uint n) {
    // ...
    for (tot = 0; n > 0; ) {
        uint64 addr;
        if ((addr = bmap(ip, off / BSIZE)) == 0) break;
        
        Bread(addr);           ; Read or allocate block
        memmove(&buf->data[off % BSIZE], src, n);
        bwrite(buf);           ; Mark dirty
        
        off += n;
        src += n;
        n -= n;
    }
    return tot;
}
```

## 28.10 Summary

In this chapter we learned:
- xv6 file system architecture
- Superblock structure
- inode structure and size limits
- Directory implementation
- Logging system purpose and implementation
- Buffer layer

## 28.11 Exercises

1. Calculate xv6 maximum file size
2. Research differences between ext2/ext4 and xv6
3. Implement link() system call
4. Research two-phase commit for logging
5. Implement file truncation (truncate)
