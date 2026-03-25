#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

const char* http_response = 
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    "Content-Length: 12\r\n"
    "\r\n"
    "Hello, TCP!";

void print_server_info(struct sockaddr_in* addr) {
    char* ip_str = inet_ntoa(addr->sin_addr);
    int port = ntohs(addr->sin_port);
    printf("Server configuration:\n");
    printf("  Address family: AF_INET (IPv4)\n");
    printf("  IP address: %s\n", ip_str);
    printf("  Port: %d\n", port);
    printf("  Network byte order port: %d\n", addr->sin_port);
}

int main() {
    printf("=== TCP Server Demo ===\n\n");
    
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket creation failed");
        return 1;
    }
    printf("Socket created successfully\n");
    
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    printf("SO_REUSEADDR enabled\n");
    
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);
    
    print_server_info(&server_addr);
    
    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind failed");
        close(server_fd);
        return 1;
    }
    printf("\nBind successful\n");
    
    if (listen(server_fd, 128) < 0) {
        perror("listen failed");
        close(server_fd);
        return 1;
    }
    printf("Server listening on port %d\n", PORT);
    printf("(Note: This is a simulation - actual server would block on accept)\n");
    
    printf("\n=== TCP State Machine ===\n");
    printf("Server socket states:\n");
    printf("  1. socket() -> Created, not bound\n");
    printf("  2. bind() -> Bound to address\n");
    printf("  3. listen() -> Ready to accept connections\n");
    printf("  4. accept() -> Waiting for client connection\n");
    printf("  5. read/write() -> Data transfer\n");
    printf("  6. close() -> Connection terminated\n");
    
    close(server_fd);
    printf("\nSocket closed\n");
    
    return 0;
}
