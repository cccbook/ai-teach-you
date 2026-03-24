// macOS / XNU 核心概念

/*
XNU 核心架構：
+-------------------+
|   IOKit           |  <- 物件導向驅動框架
+-------------------+
+-------------------+
|   BSD Layer       |  <- Unix 相容（程序、檔案、網路）
+-------------------+
+-------------------+
|   Mach            |  <- 微核心（IPC、虛擬記憶體）
+-------------------+
*/

// Mach 訊息傳遞
#include <mach/mach.h>

kern_return_t inter_process_comm() {
    mach_port_t port;
    mach_port_allocate(mach_task_self(), 
                      MACH_PORT_RIGHT_RECEIVE, &port);
    
    // 傳送訊息
    struct {
        mach_msg_header_t header;
        char data[256];
    } msg;
    
    mach_msg(&msg, MACH_SEND_MSG, sizeof(msg), 0, port, 0, 0);
}

// BSD 系統呼叫
#include <sys/syscall.h>

int main() {
    // fork()
    pid_t pid = fork();
    
    // execve()
    execve("/bin/ls", argv, envp);
    
    // mmap()
    void *mem = mmap(NULL, 4096, 
                    PROT_READ | PROT_WRITE,
                    MAP_ANONYMOUS, -1, 0);
    
    return 0;
}
