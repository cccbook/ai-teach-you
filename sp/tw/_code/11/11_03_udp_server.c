#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main() {
    int sock;
    struct sockaddr_in server_addr, client_addr;
    char buffer[1024];
    socklen_t client_len = sizeof(client_addr);
    
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket failed");
        return 1;
    }
    
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(9000);
    
    if (bind(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind failed");
        return 1;
    }
    
    printf("UDP server listening on port 9000\n");
    
    int n = recvfrom(sock, buffer, sizeof(buffer), 0, 
                     (struct sockaddr*)&client_addr, &client_len);
    
    if (n > 0) {
        buffer[n] = '\0';
        printf("Received from client: %s\n", buffer);
        
        sendto(sock, buffer, n, 0, (struct sockaddr*)&client_addr, client_len);
    }
    
    close(sock);
    return 0;
}
