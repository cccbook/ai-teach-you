#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 8080
#define BUFFER_SIZE 1024

void print_client_config() {
    struct in_addr addr;
    inet_pton(AF_INET, SERVER_IP, &addr);
    
    printf("Client configuration:\n");
    printf("  Address family: AF_INET (IPv4)\n");
    printf("  Server IP: %s\n", SERVER_IP);
    printf("  Server port: %d\n", SERVER_PORT);
}

int main() {
    printf("=== TCP Client Demo ===\n\n");
    
    print_client_config();
    
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("socket creation failed");
        return 1;
    }
    printf("\nSocket created successfully\n");
    
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    
    if (inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr) <= 0) {
        perror("Invalid address");
        close(sock);
        return 1;
    }
    
    printf("Server address configured\n");
    printf("(Note: This is a simulation - connect would block waiting for server)\n");
    
    printf("\n=== Connection Process ===\n");
    printf("  1. socket() -> Create socket\n");
    printf("  2. connect() -> Initiate TCP 3-way handshake\n");
    printf("     - Client sends SYN\n");
    printf("     - Server responds SYN-ACK\n");
    printf("     - Client sends ACK\n");
    printf("  3. Connection established\n");
    printf("  4. read/write() -> Data transfer\n");
    printf("  5. close() -> Connection terminated\n");
    
    close(sock);
    printf("\nSocket closed\n");
    
    return 0;
}
