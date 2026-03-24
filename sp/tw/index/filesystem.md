# 檔案系統 (Filesystem)

## 概述

檔案系統是作業系統用於組織和儲存資料的機制，提供檔案的建立、讀取、寫入、刪除等操作。不同的檔案系統有不同的特性和效能特性，如 ext4、XFS、NTFS 等。

## 歷史

- **1971**：最早的 Unix 檔案系統
- **1984**：MS-DOS FAT
- **1992**：Linux ext2
- **2008**：Btrfs
- **現在**：多種檔案系統並存

## 檔案系統類型

### 1. ext4 (Linux)

```bash
# 建立 ext4 檔案系統
mkfs.ext4 /dev/sdb1

# 掛載
mount /dev/sdb1 /mnt/data

# 檢查
dumpe2fs /dev/sdb1 | less
```

### 2. XFS

```bash
mkfs.xfs /dev/sdb1
mount -t xfs /dev/sdb1 /mnt
```

### 3. FAT/NTFS

```bash
# FAT
mkfs.vfat /dev/sdb1

# NTFS
mkfs.ntfs /dev/sdb1
mount -t ntfs-3g /dev/sdb1 /mnt
```

## 檔案操作

### 1. C 標準庫

```c
#include <stdio.h>

FILE *f = fopen("data.txt", "w");
fprintf(f, "Hello, World!\n");
fclose(f);

// 二進制操作
fwrite(data, 1, size, file);
fread(buffer, 1, size, file);
```

### 2. 系統呼叫

```c
#include <fcntl.h>
#include <unistd.h>

int fd = open("file.txt", O_RDONLY);
read(fd, buffer, 100);
close(fd);
```

### 3. 目錄操作

```c
#include <dirent.h>

DIR *dir = opendir("/tmp");
struct dirent *entry;

while ((entry = readdir(dir)) != NULL) {
    printf("%s\n", entry->d_name);
}
closedir(dir);
```

## 虛擬檔案系統（VFS）

```c
// VFS 超級區塊
struct super_operations {
    struct inode *(*alloc_inode)(struct super_block *);
    void (*destroy_inode)(struct inode *);
    int (*write_inode)(struct inode *, int);
    void (*put_super)(struct super_block *);
};

// 檔案操作
struct file_operations {
    ssize_t (*read)(struct file *, char __user *, size_t, loff_t *);
    ssize_t (*write)(struct file *, const char __user *, size_t, loff_t *);
    int (*open)(struct inode *, struct file *);
};
```

## 為什麼學習檔案系統？

1. **資料管理**：理解資料儲存
2. **效能優化**：選擇合適檔案系統
3. **除錯**：檔案相關問題
4. **系統程式設計**：檔案操作

## 參考資源

- "Linux File System"
- "Understanding the Linux Kernel"
