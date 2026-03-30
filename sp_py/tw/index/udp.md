# UDP (User Datagram Protocol)

## 概述

UDP 是簡單的無連接傳輸層協定，提供無須建立連接、不可靠但快速的資料傳輸。UDP 適用於即時語音、影片、線上遊戲等對延遲敏感但可容忍少量資料丟失的應用。

## 歷史

- **1980**：UDP 規範（RFC 768）
- **至今**：廣泛用於即時應用

## UDP 特性

### 1. 簡單的資料封包

```
┌─────────────┬─────────────┐
│ UDP Header  │  Data       │
├─────────────┴─────────────┤
│ SrcPort  (2 bytes)       │
│ DstPort  (2 bytes)       │
│ Length   (2 bytes)       │
│ Checksum (2 bytes)       │
└──────────────────────────┘
```

### 2. C 客戶端範例

```c
#include <stdio.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main() {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(12345);
    inet_pton(AF_INET, "192.168.1.100", &server.sin_addr);
    
    char msg[] = "Hello";
    sendto(sock, msg, strlen(msg), 0,
           (struct sockaddr *)&server, sizeof(server));
    
    char buffer[1024];
    socklen_t len = sizeof(server);
    recvfrom(sock, buffer, sizeof(buffer), 0,
             (struct sockaddr *)&server, &len);
    
    printf("收到: %s\n", buffer);
    close(sock);
    return 0;
}
```

### 3. C 伺服端範例

```c
#include <stdio.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main() {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(12345);
    
    bind(sock, (struct sockaddr *)&server, sizeof(server));
    
    char buffer[1024];
    struct sockaddr_in client;
    socklen_t len = sizeof(client);
    
    recvfrom(sock, buffer, sizeof(buffer), 0,
             (struct sockaddr *)&client, &len);
    
    printf("收到: %s\n", buffer);
    
    char response[] = "ACK";
    sendto(sock, response, strlen(response), 0,
           (struct sockaddr *)&client, len);
    
    close(sock);
    return 0;
}
```

### 4. 使用場景

```c
// DNS 查詢
// 快速、小量資料傳輸
// 即時視訊/語音
// 線上遊戲

// DNS 伺服器查詢
char dns_query[] = "example.com";
sendto(sock, dns_query, strlen(dns_query), 0,
       (struct sockaddr *)&dns_server, sizeof(dns_server));
```

## 為什麼使用 UDP？

1. **低延遲**：無連接建立
2. **簡單**：較少的協定開銷
3. **廣播**：支援廣播
4. **即時性**：可容忍丟包

## 參考資源

- RFC 768
- "Computer Networks"
