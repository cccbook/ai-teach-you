// Linux 核心模組範例

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Author");
MODULE_DESCRIPTION("Simple Character Driver");

// 裝置結構
struct my_device {
    dev_t dev_num;
    struct cdev cdev;
};

// 開啟裝置
static int mydev_open(struct inode *inode, struct file *file) {
    printk(KERN_INFO "裝置已開啟\n");
    return 0;
}

// 讀取裝置
static ssize_t mydev_read(struct file *file, char __user *buf, 
                           size_t len, loff_t *offset) {
    printk(KERN_INFO "讀取資料\n");
    return 0;
}

// 寫入裝置
static ssize_t mydev_write(struct file *file, const char __user *buf,
                           size_t len, loff_t *offset) {
    printk(KERN_INFO "寫入資料\n");
    return len;
}

// 檔案操作
static struct file_operations fops = {
    .owner   = THIS_MODULE,
    .open    = mydev_open,
    .read    = mydev_read,
    .write   = mydev_write,
};

// 初始化模組
static int __init mydev_init(void) {
    printk(KERN_INFO "模組載入\n");
    // 註冊字元裝置
    register_chrdev(255, "mydev", &fops);
    return 0;
}

// 移除模組
static void __exit mydev_exit(void) {
    printk(KERN_INFO "模組卸載\n");
    unregister_chrdev(255, "mydev");
}

module_init(mydev_init);
module_exit(mydev_exit);