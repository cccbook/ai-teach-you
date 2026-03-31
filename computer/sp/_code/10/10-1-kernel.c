// Linux 核心模組範例

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Author");
MODULE_DESCRIPTION("Hello World Kernel Module");

static int __init hello_init(void) {
    printk(KERN_INFO "Hello Kernel Module\n");
    return 0;
}

static void __exit hello_exit(void) {
    printk(KERN_INFO "Goodbye Kernel Module\n");
}

module_init(hello_init);
module_exit(hello_exit);

// Linux 核心子系統
/*
1. 程序排程子系統
   - CFS（完全公平排程器）
   - 實時排程

2. 記憶體管理
   - 分頁
   - 區域記憶體配置

3. 檔案系統
   - VFS（虛擬檔案系統）
   - ext4, Btrfs, XFS

4. 網路堆疊
   - TCP/IP
   - Socket 介面

5. 裝置驅動
   - 字元裝置
   - 區塊裝置
   - 網路裝置
 */
