// Linux Socket 程式設計

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

// 伺服器端
int server() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8080);
    addr.sin_addr.s_addr = INADDR_ANY;
    
    bind(sock, (struct sockaddr *)&addr, sizeof(addr));
    listen(sock, 10);
    
    while (1) {
        int client = accept(sock, NULL, NULL);
        char buf[1024];
        read(client, buf, 1024);
        write(client, "HTTP/1.1 200 OK\r\n\r\n", 21);
        close(client);
    }
    
    close(sock);
    return 0;
}

// 用戶端
int client() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
    
    connect(sock, (struct sockaddr *)&addr, sizeof(addr));
    write(sock, "GET / HTTP/1.0\r\n\r\n", 19);
    
    char buf[1024];
    read(sock, buf, 1024);
    
    close(sock);
    return 0;
}
