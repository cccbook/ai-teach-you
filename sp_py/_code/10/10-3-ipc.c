// 程序間通訊（IPC）

// 1. 管道（Pipe）
#include <unistd.h>
#include <stdlib.h>

int main() {
    int pipefd[2];
    pipe(pipefd);  // 建立管道
    
    if (fork() == 0) {
        // 子程序
        close(pipefd[0]);  // 關閉讀取端
        write(pipefd[1], "Hello", 5);
        close(pipefd[1]);
    } else {
        // 父程序
        close(pipefd[1]);  // 關閉寫入端
        char buf[100];
        read(pipefd[0], buf, 100);
        close(pipefd[0]);
    }
    return 0;
}

// 2. 訊息佇列
#include <sys/msg.h>

struct msgbuf {
    long mtype;
    char mtext[100];
};

// 3. 共用記憶體
#include <sys/shm.h>

int shm_id = shmget(IPC_PRIVATE, 4096, IPC_CREAT | 0666);
char *shm = (char *)shmat(shm_id, NULL, 0);
shmdt(shm);
shmctl(shm_id, IPC_RMID, NULL);

// 4. 訊號
#include <signal.h>

void handler(int sig) {
    printf("收到訊號 %d\n", sig);
}
signal(SIGUSR1, handler);
raise(SIGUSR1);

// 5. 插槽（Socket）
#include <sys/socket.h>
#include <netinet/in.h>

int sock = socket(AF_INET, SOCK_STREAM, 0);
