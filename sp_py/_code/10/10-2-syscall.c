// Linux 系統呼叫範例

#include <unistd.h>
#include <sys/syscall.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>

int main() {
    // write() 系統呼叫
    const char *msg = "Hello, World!\n";
    syscall(SYS_write, 1, msg, 14);
    
    // read() 系統呼叫
    char buf[100];
    syscall(SYS_read, 0, buf, 100);
    
    // open() 系統呼叫
    int fd = syscall(SYS_open, "test.txt", O_RDONLY);
    
    // 透過 syscall() 直接呼叫
    long result = syscall(SYS_getpid);
    printf("PID: %ld\n", result);
    
    return 0;
}

// 使用封裝好的 libc 函數
void use_libc() {
    // open()
    int fd = open("file.txt", O_RDONLY);
    
    // read()
    char buf[1024];
    read(fd, buf, 1024);
    
    // write()
    write(STDOUT_FILENO, "Hello\n", 6);
    
    // close()
    close(fd);
}
