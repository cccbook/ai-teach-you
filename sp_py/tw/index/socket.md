# Socket

## 概述

Socket 是網路通訊的抽象端點，是程序間通訊的機制。Socket API 最初由 BSD Unix 開發，現在是網路程式設計的標準介面。Socket 支援 TCP（流式）和 UDP（資料報）兩種模式。

## 歷史

- **1983**：BSD 4.2 引入 Socket
- **1990s**：Windows Winsock
- **現在**：所有平台支援

## Socket 類型

### 1. 流式 Socket（SOCK_STREAM）

```c
// TCP - 面向連接、可靠
int sock = socket(AF_INET, SOCK_STREAM, 0);
```

### 2. 資料報 Socket（SOCK_DGRAM）

```c
// UDP - 無連接、快速
int sock = socket(AF_INET, SOCK_DGRAM, 0);
```

### 3. 原始 Socket（SOCK_RAW）

```c
// 原始套接字 - 存取底層協定
int sock = socket(AF_INET, SOCK_RAW, protocol);
```

## Socket 程式設計

### 1. TCP 客戶端

```c
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in server = {0};
    server.sin_family = AF_INET;
    server.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &server.sin_addr);
    
    connect(sock, (struct sockaddr *)&server, sizeof(server));
    
    send(sock, "Hello", 5, 0);
    
    char buffer[100];
    recv(sock, buffer, sizeof(buffer), 0);
    printf("%s\n", buffer);
    
    close(sock);
}
```

### 2. TCP 伺服端

```c
#include <sys/socket.h>
#include <netinet/in.h>

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8080);
    addr.sin_addr.s_addr = INADDR_ANY;
    
    bind(server_fd, (struct sockaddr *)&addr, sizeof(addr));
    listen(server_fd, 5);
    
    int client_fd = accept(server_fd, NULL, NULL);
    
    char buffer[100];
    read(client_fd, buffer, sizeof(buffer));
    
    write(client_fd, "OK", 2);
    
    close(client_fd);
    close(server_fd);
}
```

### 3. UDP 通訊

```c
// UDP 客戶端
int sock = socket(AF_INET, SOCK_DGRAM, 0);
sendto(sock, data, len, 0, (struct sockaddr *)&server, sizeof(server));

// UDP 伺服端
bind(sock, (struct sockaddr *)&addr, sizeof(addr));
recvfrom(sock, buffer, size, 0, (struct sockaddr *)&client, &len);
```

### 4. 非阻塞 Socket

```c
#include <fcntl.h>

int flags = fcntl(sock, F_GETFL, 0);
fcntl(sock, F_SETFL, flags | O_NONBLOCK);

// 使用 select/poll/epoll 監控
```

### 5. 多客戶端

```c
#include <sys/select.h>

fd_set readfds;
FD_ZERO(&readfds);
FD_SET(server_fd, &readfds);

int max_fd = server_fd;

while (1) {
    fd_set tmp = readfds;
    select(max_fd + 1, &tmp, NULL, NULL, NULL);
    
    if (FD_ISSET(server_fd, &tmp)) {
        int client = accept(server_fd, NULL, NULL);
        FD_SET(client, &readfds);
        max_fd = (client > max_fd) ? client : max_fd;
    }
}
```

## 為什麼學習 Socket？

1. **網路通訊**：基礎 API
2. **客戶端/伺服器**：通訊模型
3. **效能優化**：非阻塞 IO
4. **跨平台**：標準介面

## 參考資源

- "Unix Network Programming"
- Stevens 書籍
- POSIX socket
