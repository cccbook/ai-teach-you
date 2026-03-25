#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/select.h>
#include <fcntl.h>

#define MAX_CLIENTS 1024
#define BUFFER_SIZE 1024

int main() {
    printf("=== Event-Driven Server with I/O Multiplexing ===\n\n");
    
    printf("Algorithm:\n");
    printf("  1. Create socket and set non-blocking\n");
    printf("  2. Initialize fd_set for read events\n");
    printf("  3. Loop: select() for ready file descriptors\n");
    printf("  4. Handle events:\n");
    printf("     - Server socket ready -> accept new connection\n");
    printf("     - Client socket ready -> read and echo\n\n");
    
    printf("select() workflow:\n");
    printf("  fd_set readfds;\n");
    printf("  FD_ZERO(&readfds);\n");
    printf("  FD_SET(server_fd, &readfds);\n");
    printf("  for each client: FD_SET(client_fd, &readfds);\n\n");
    
    printf("  while (1) {\n");
    printf("      fd_set r = readfds;\n");
    printf("      int n = select(max_fd+1, &r, NULL, NULL, NULL);\n");
    printf("      \n");
    printf("      if (FD_ISSET(server_fd, &r)) {\n");
    printf("          // New connection ready\n");
    printf("          int client = accept(server_fd, ...);\n");
    printf("          set_nonblocking(client);\n");
    printf("          FD_SET(client, &readfds);\n");
    printf("      }\n");
    printf("      \n");
    printf("      for each client {\n");
    printf("          if (FD_ISSET(client, &r)) {\n");
    printf("              // Client data ready\n");
    printf("              ssize_t n = read(client, buf, sizeof(buf));\n");
    printf("              if (n <= 0) {\n");
    printf("                  close(client);\n");
    printf("                  FD_CLR(client, &readfds);\n");
    printf("              }\n");
    printf("          }\n");
    printf("      }\n");
    printf("  }\n\n");
    
    printf("I/O Multiplexing APIs:\n");
    printf("  +-------------+------+---------+\n");
    printf("  | select()    | POSIX| n <= 1024 |\n");
    printf("  | poll()      | POSIX| Unlimited |\n");
    printf("  | epoll()     | Linux| Unlimited |\n");
    printf("  | kqueue()    | BSD  | Unlimited |\n");
    printf("  +-------------+------+---------+\n\n");
    
    printf("Advantages of event-driven:\n");
    printf("  + Single thread handles many connections\n");
    printf("  + Lower memory overhead than multi-process\n");
    printf("  + Good for I/O-bound workloads\n\n");
    
    printf("Disadvantages:\n");
    printf("  - Cannot utilize multiple CPU cores\n");
    printf("  - Complex to handle long-running tasks\n");
    printf("  - Callback-based code can be harder to follow\n");
    
    return 0;
}
