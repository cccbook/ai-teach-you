# TCP (Transmission Control Protocol)

## 概述

TCP 是網路傳輸層的可靠連接導向協定，提供面向連接、可靠、基於位元組流的通訊服務。TCP 確保資料順序正確、不重複、不遺失，是 HTTP、FTP、SMTP 等應用層協定的基礎。

## 歷史

- **1974**：TCP 最初規範（RFC 675）
- **1981**：TCP 標準化（RFC 793）
- **1983**：TCP/IP 在 ARPANET 啟用
- **現在**：網際網路核心協定

## TCP 特性

### 1. 三向交握

```
客戶端                      伺服器
   |                           |
   |------ SYN --------------->|
   |    seq=x                  |
   |                           |
   |<----- SYN-ACK ------------|
   |    seq=y, ack=x+1         |
   |                           |
   |------ ACK --------------->
   |    ack=y+1                |
   |                           |
   ===== 連接建立 =====
```

### 2. C 客戶端範例

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(80);
    inet_pton(AF_INET, "93.184.216.34", &server.sin_addr);
    
    connect(sock, (struct sockaddr *)&server, sizeof(server));
    
    char request[] = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n";
    send(sock, request, strlen(request), 0);
    
    char response[4096];
    recv(sock, response, sizeof(response), 0);
    printf("%s\n", response);
    
    close(sock);
    return 0;
}
```

### 3. C 伺服端範例

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8080);
    
    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);
    
    int client_fd = accept(server_fd, NULL, NULL);
    
    char buffer[1024] = {0};
    read(client_fd, buffer, 1024);
    printf("收到請求: %s\n", buffer);
    
    char response[] = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, World!";
    send(client_fd, response, strlen(response), 0);
    
    close(client_fd);
    close(server_fd);
    return 0;
}
```

### 4. TCP 狀態機

```
   建立連接:                 結束連接:
   CLOSED ──→ LISTEN      CLOSED ──→ LISTEN
       ↑                  ↓
   SYN_SENT ──→ ESTABLISHED
       ↓                  ↓
   SYN_RCVD ──→ ESTABLISHED ──→ FIN_WAIT_1
       ↑                  ↓
   CLOSE_WAIT ──→ LAST_ACK ──→ CLOSED
       ↓
   CLOSING ──→ TIME_WAIT ──→ CLOSED
```

### 5. 流量控制

```c
// TCP 滑動視窗
// 發送視窗: [snd_unack, snd_wnd]
// 接收視窗: rcv_wnd

// 視窗大小調整
// ACK 攜帶 rcv_wnd
// 發送端根據 rcv_wnd 調整發送量
```

### 6. 壅塞控制

```c
// 慢啟動
if (cwnd < ssthresh)
    cwnd *= 2;      // 指數增長
else
    cwnd += 1;      // 線性增長

// 壅塞避免
// cwnd 達到門檻後進入線性增長

// 快重傳
// 收到 3 個重複 ACK 後立即重傳
```

## TCP vs UDP

| 特性 | TCP | UDP |
|------|-----|-----|
| 連接 | 面向連接 | 無連接 |
| 可靠性 | 可靠 | 不可靠 |
| 順序 | 有序 | 無序 |
| 速度 | 較慢 | 較快 |
| 流量控制 | 有 | 無 |
| 壅塞控制 | 有 | 無 |

## 為什麼學習 TCP？

1. **網路程式設計**：基礎知識
2. **可靠性**：理解可靠傳輸
3. **效能優化**：TCP 調優
4. **除錯**：網路問題

## 參考資源

- RFC 793
- "TCP/IP Illustrated"
- Stevens 網路程式設計
