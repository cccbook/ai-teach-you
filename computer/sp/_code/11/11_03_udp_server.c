#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define SERVER_PORT 9000
#define BUFFER_SIZE 1024

void print_udp_server_config() {
    printf("UDP Server configuration:\n");
    printf("  Address family: AF_INET (IPv4)\n");
    printf("  Protocol: UDP (SOCK_DGRAM)\n");
    printf("  Port: %d\n", SERVER_PORT);
}

int main() {
    printf("=== UDP Server Demo ===\n\n");
    
    print_udp_server_config();
    
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket creation failed");
        return 1;
    }
    printf("\nSocket created successfully\n");
    
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(SERVER_PORT);
    
    if (bind(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind failed");
        close(sock);
        return 1;
    }
    printf("Bind successful\n");
    printf("Server listening on port %d\n", SERVER_PORT);
    
    printf("\n=== UDP vs TCP Comparison ===\n");
    printf("UDP characteristics:\n");
    printf("  - Connectionless (no handshake)\n");
    printf("  - No guaranteed delivery\n");
    printf("  - No ordering guarantee\n");
    printf("  - Lower overhead than TCP\n");
    printf("  - Suitable for real-time applications\n");
    
    printf("\nTCP characteristics:\n");
    printf("  - Connection-oriented (3-way handshake)\n");
    printf("  - Reliable delivery\n");
    printf("  - Ordered packets\n");
    printf("  - Higher overhead\n");
    printf("  - Suitable for reliable data transfer\n");
    
    printf("\n(Note: This is a simulation - actual server would block on recvfrom)\n");
    
    close(sock);
    printf("\nSocket closed\n");
    
    return 0;
}
