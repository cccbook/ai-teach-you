#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/wait.h>
#include <signal.h>
#include <errno.h>

#define PORT 8080
#define BUFFER_SIZE 1024

void handle_client(int client_fd) {
    char buffer[BUFFER_SIZE];
    
    printf("  [Child %d] Handling client\n", getpid());
    
    while (1) {
        ssize_t n = recv(client_fd, buffer, BUFFER_SIZE - 1, 0);
        if (n <= 0) {
            if (n < 0) perror("recv");
            break;
        }
        buffer[n] = '\0';
        printf("  [Child %d] Received: %s", getpid(), buffer);
        
        send(client_fd, buffer, n, 0);
    }
    
    close(client_fd);
    printf("  [Child %d] Client disconnected\n", getpid());
}

void sigchld_handler(int sig) {
    int saved_errno = errno;
    while (waitpid(-1, NULL, WNOHANG) > 0);
    errno = saved_errno;
}

int main() {
    printf("=== Multi-Process Socket Server ===\n\n");
    
    printf("Algorithm:\n");
    printf("  1. Parent creates listening socket\n");
    printf("  2. For each client connection:\n");
    printf("     - Fork a child process\n");
    printf("     - Child handles client, parent continues listening\n");
    printf("  3. Parent reaps zombie children\n\n");
    
    printf("Process model:\n");
    printf("  +----------------+\n");
    printf("  | Parent Process |\n");
    printf("  | (Listener)    |\n");
    printf("  +-------+--------+\n");
    printf("          |\n");
    printf("    +-----+-----+-----+-----+\n");
    printf("    |     |     |     |     |\n");
    printf("  +-+   +-+   +-+   +-+   +-+\n");
    printf("  |C1|  |C2|  |C3|  |C4|  |C5|\n");
    printf("  +-+   +-+   +-+   +-+   +-+\n");
    printf("  (Each handles one client)\n\n");
    
    printf("Code structure:\n");
    printf("  struct sockaddr_in server_addr;\n");
    printf("  int server_fd = socket(AF_INET, SOCK_STREAM, 0);\n");
    printf("  bind(server_fd, ...);\n");
    printf("  listen(server_fd, 128);\n\n");
    
    printf("  while (1) {\n");
    printf("      int client_fd = accept(server_fd, ...);\n");
    printf("      pid_t pid = fork();\n");
    printf("      if (pid == 0) {\n");
    printf("          close(server_fd);\n");
    printf("          handle_client(client_fd);\n");
    printf("          exit(0);\n");
    printf("      } else {\n");
    printf("          close(client_fd);\n");
    printf("      }\n");
    printf("  }\n\n");
    
    printf("Advantages:\n");
    printf("  + Simple to implement\n");
    printf("  + Good isolation between clients\n");
    printf("  + Can use multiple CPU cores\n\n");
    
    printf("Disadvantages:\n");
    printf("  - Higher memory overhead per connection\n");
    printf("  - Process creation is expensive\n");
    printf("  - IPC needed for shared state\n");
    
    return 0;
}
