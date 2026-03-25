/* Linux 系統呼叫範例 */
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    // write(1, "Hello\n", 6)
    // 系統呼叫號: 1 (write)
    // fd=1, buf="Hello\n", count=6
    char msg[] = "Hello, World!\n";
    syscall(SYS_write, 1, msg, 14);
    
    // exit(0)
    syscall(SYS_exit, 0);
    return 0;
}