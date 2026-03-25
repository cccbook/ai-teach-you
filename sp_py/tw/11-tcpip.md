# 11. TCP/IP 網路堆疊

TCP/IP 是現代網際網路的基礎通訊協定族，幾乎所有網路應用都構建在這個協定堆疊之上。理解 TCP/IP 的運作原理對於系統程式設計、網路應用開發、效能調校和故障排除都至關重要。本章將深入探討網路分層模型、IP/TCP/UDP 協定的詳細規格、TCP 連線管理與可靠傳輸機制、網路程式設計實務，以及網路效能優化策略。

## 11.1 OSI 與 TCP/IP 模型

### 11.1.1 網路分層的原理

網路分層是網路架構的核心理念，其核心思想是將複雜的網路通訊問題分解為多個相對獨立的層次，每層只關注自己的職責，並透過定義良好的介面與相鄰層互動。這種設計提供了以下優勢：

- **模組化**：每層可以被獨立開發、測試和最佳化
- **可置換性**：某層的實作可以被替換，而不影響其他層
- **標準化**：各層的介面標准化使得不同廠商的設備可以互操作
- **簡化複雜度**：每層只需處理特定範圍的問題

**OSI 七層模型**是國際標準組織（ISO）在 1984 年提出的標準化網路架構參考模型。雖然 TCP/IP 協定族並非嚴格按照 OSI 模型設計，但 OSI 模型作為教學工具和概念框架被廣泛使用：

| 層次 | 名稱 | 職責 | 範例協定 |
|------|------|------|----------|
| 7 | 應用層 | 為應用程式提供網路服務介面 | HTTP, DNS, FTP, SMTP |
| 6 | 表達層 | 處理資料格式轉換、編碼、加解密 | JPEG, SSL/TLS, ASCII |
| 5 | 會議層 | 管理通訊會話、建立/維護同步 | RPC, NetBIOS, SIP |
| 4 | 傳輸層 | 提供端到端的可靠或不可靠傳輸 | TCP, UDP, SCTP |
| 3 | 網路層 | 實現路由轉送，跨多個網路傳輸 | IP, ICMP, OSPF, BGP |
| 2 | 資料連結層 | 相鄰節點之間的可靠傳輸 | Ethernet, Wi-Fi, PPP |
| 1 | 實體層 | 定義物理傳輸介質和訊號 | 電纜、光纖、無線電 |

**TCP/IP 四層模型**是網際網路實際使用的協定架構，分為四層：

| 層次 | 對應 OSI | 核心功能 | 範例協定 |
|------|----------|----------|----------|
| 應用層 | 5-7 | 網路應用程式與服務 | HTTP, DNS, FTP, SMTP, SSH |
| 傳輸層 | 4 | 主機到主機的通訊控制 | TCP, UDP, SCTP, DCCP |
| 網路層 | 3 | 跨網路的封包路由 | IP (IPv4/IPv6), ICMP, ICMPv6 |
| 網路介面層 | 1-2 | 區域網路傳輸 | Ethernet, Wi-Fi, ARP, VLAN |

### 11.1.2 封包封裝與解封裝

網路通訊中，資料在傳送端經過每一層時會被「封裝」（encapsulation），添加該層的協定向頭部（或和尾部）。在接收端，過程則相反——每層進行「解封裝」（decapsulation），移除對應層的頭部，將資料傳遞給上層。

```
封裝過程（發送端）：
┌──────────────────────────────────────────────────────────────┐
│                     應用層：HTTP 請求                          │
│                     (應用程式資料)                             │
├──────────────────────────────────────────────────────────────┤
│                     傳輸層：TCP 段                             │
│   Source Port: 54321  │  Dest Port: 80                        │
│   Sequence Number: 1000  │  Flags: PSH, ACK                 │
│   Header + 應用層資料                                         │
├──────────────────────────────────────────────────────────────┤
│                     網路層：IP 封包                           │
│   Source IP: 192.168.1.100  │  Dest IP: 93.184.216.34        │
│   Header + TCP 段                                              │
├──────────────────────────────────────────────────────────────┤
│                     資料連結層：乙太網路框架                    │
│   Source MAC: aa:bb:cc:dd:ee:ff  │  Dest MAC: 11:22:33:44    │
│   Header + IP 封包 + Trailer (FCS)                            │
├──────────────────────────────────────────────────────────────┤
│                     實體層：位元流                             │
│   序列化的位元，在網路線上傳輸                                  │
└──────────────────────────────────────────────────────────────┘
```

每層使用的術語也有所不同：應用層稱為「訊息」（message），傳輸層稱為「段」（segment），網路層稱為「封包」（packet），資料連結層稱為「框架」（frame）。

**MTU 與分片**

最大傳輸單元（Maximum Transmission Unit, MTU）是資料連結層可以傳送的最大框架尺寸。常見的 MTU 值包括：

- 乙太網路：1500 位元組（標準）
- PPPoE：1492 位元組
- 乙太網路 + VLAN：1498 位元組
- IPv6：1280 位元組（最小）

當 IP 封包的大小超過下一跳的 MTU 時，IP 層會將封包**分片**（fragmentation）。IPv4 的分片由路由器執行，而 IPv6 只允許源節點進行分片。分片增加了複雜性和不確定性，因此在現代網路中，使用路徑 MTU 發現（Path MTU Discovery）來避免分片。

## 11.2 IP、TCP、UDP 協定

### 11.2.1 IP 協定

IP（Internet Protocol）是網路層的核心協定，負責將封包從源主機傳送到目的主機，跨越一個或多個路由器。IP 是「不可靠」的——它不保證封包一定能到達、不保證封包按順序到達、不保證不重複。這些可靠性特性交由上層（通常是 TCP）提供。

**IPv4 封包格式**

IPv4 封包由頭部和資料部分組成：

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
│Version│  IHL  │    DSCP   │ECN│         Total Length          │
├───────┼───────┼───────────┼───┼───────────────────────────────┤
│        Identification         │Flags│      Fragment Offset      │
├─────────────────────────────┼─────┴───────────────────────────┤
│  Time to Live │  Protocol   │        Header Checksum           │
├───────────────────────────────────────────────────────────────┤
│                       Source IP Address                        │
├───────────────────────────────────────────────────────────────┤
│                     Destination IP Address                     │
├───────────────────────────────────────────────────────────────┤
│                    Options (if IHL > 5)                       │
└───────────────────────────────────────────────────────────────┘
```

主要欄位說明：

- **Version (4 位元)**：IP 版本，IPv4 為 4
- **IHL (4 位元)**：IP 頭部長度，以 32 位元為單位，最小為 5（20 位元組）
- **DSCP (6 位元)**：差異化服務代碼點，用於 QoS
- **ECN (2 位元)**：顯式擁塞通知
- **Total Length (16 位元)**：整個封包的長度，最大 65,535 位元組
- **Identification (16 位元)**：用於分片重組識別
- **Flags (3 位元)**：控制分片，MF=1 表示更多分片，DF=1 表示不分片
- **Fragment Offset (13 位元)**：分片在原始封包中的位置
- **TTL (8 位元)**：封包存活時間，每經過一個路由器減 1，防止路由環路
- **Protocol (8 位元)**：上層協定（6=TCP, 17=UDP, 1=ICMP）
- **Header Checksum (16 位元)**：頭部校驗和，用於錯誤檢測

**IP 位址與網路劃分**

IPv4 位址是 32 位元的數值，通常用點分十進制表示（如 192.168.1.1）。傳統上，IP 位址被分為 A、B、C、D、E 五類：

| 類別 | 首位 | 位址範圍 | 網路/主機位元 | 用途 |
|------|------|----------|--------------|------|
| A | 0 | 0.0.0.0 - 127.255.255.255 | 8/24 | 大型網路 |
| B | 10 | 128.0.0.0 - 191.255.255.255 | 16/16 | 中型網路 |
| C | 110 | 192.0.0.0 - 223.255.255.255 | 24/8 | 小型網路 |
| D | 1110 | 224.0.0.0 - 239.255.255.255 | - | 多播 |
| E | 1111 | 240.0.0.0 - 255.255.255.255 | - | 保留 |

現代網路使用**無類別域間路由**（CIDR）來代替類別劃分，格式為「位址/前綴長度」（如 192.168.1.0/24）。

**私有 IP 位址範圍**

根據 RFC 1918，以下 IP 範圍保留供私有網路使用，不可路由於公共網際網路：

- 10.0.0.0/8 (10.0.0.0 - 10.255.255.255)
- 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
- 192.168.0.0/16 (192.168.0.0 - 192.168.255.255)

### 11.2.2 TCP 協定

TCP（Transmission Control Protocol）是 Internet 上最廣泛使用的傳輸層協定，提供了可靠、面向連接、位元組流的傳輸服務。TCP 的設計平衡了可靠性、效能和公平性，是現代網路應用的基石。

**TCP 的核心特性**

| 特性 | 說明 |
|------|------|
| 可靠性 | 確認機制、重傳、超時 |
| 順序傳遞 | 序列號、亂序重組 |
| 全雙工 | 雙向資料流 |
| 流量控制 | 滑動視窗、接收端緩衝區管理 |
| 擁塞控制 | 避免網路過載、網路友善 |
| 連接導向 | 建立連線、維護狀態、終止連線 |

**TCP 頭部格式**

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├───────────────────┬───────────────────┬───────────────────┬─────────┤
│   Source Port     │   Dest Port      │                                  │
├───────────────────┼───────────────────┼───────────────────┼─────────┤
│                          Sequence Number                                   │
├───────────────────────────────────────────────────┬─────────────────────┤
│                      Acknowledgment Number                               │
├───────┬─────────┬───────────────────────────────┼─────────────────────┤
│ Data  │         │         Flags                 │    Window Size       │
│ Offset│ Reserved│ URG│ACK│PSH│RST│SYN│FIN     │                     │
├───────┴─────────┴───────────────────────────────┴─────────┬───────────┤
│                  Checksum               │ Urgent Pointer               │
├─────────────────────────────────────────────────────────┴───────────┤
│                    Options (variable length)                           │
└───────────────────────────────────────────────────────────────────────┘
```

主要欄位說明：

- **Source/Dest Port (各 16 位元)**：連線端點的連接埠號
- **Sequence Number (32 位元)**：該段第一個資料位元組的序列號
- **Acknowledgment Number (32 位元)**：期望收到的下一個位元組的序列號
- **Data Offset (4 位元)**：TCP 頭部長度，以 32 位元為單位
- **Flags (6 位元)**：控制標誌
  - URG：緊急指標有效
  - ACK：確認號有效
  - PSH：立即推送資料給應用程式
  - RST：重置連線
  - SYN：同步序列號（建立連線）
  - FIN： Finish，終止連線
- **Window Size (16 位元)**：接收端願意接收的位元組數（流量控制）
- **Checksum (16 位元)**：頭部和資料的校驗和
- **Urgent Pointer (16 位元)**：標記緊急資料的結束位置

### 11.2.3 TCP 連線建立：三次握手

TCP 連線建立過程稱為「三次握手」（three-way handshake），確保雙方都確認彼此可以收發資料：

```
客戶端                                              伺服器
   │                                                 │
   │                  [closed]                      [listening]
   │                                                 │
   │ ────── SYN, seq=x (client_isn) ────────────► │
   │                                                 │
   │              [SYN_SENT]                      [SYN_RCVD]
   │                                                 │
   │ ◄──── SYN+ACK, seq=y, ack=x+1 ──────────── │
   │                                                 │
   │              [ESTABLISHED]                   │
   │                                                 │
   │ ────── ACK, ack=y+1 ──────────────────────► │
   │                                                 │
   │              [ESTABLISHED]                    [ESTABLISHED]
   │                                                 │
```

**三次握手的設計原理**

1. **第一次握手（SYN）**：客戶端發送 SYN 和初始序列號（ISN），告知伺服器客戶端希望建立連線，並告知客戶端的起始序列號

2. **第二次握手（SYN+ACK）**：伺服器回應 SYN+ACK，確認收到客戶端的 SYN，並攜帶伺服器自己的初始序列號

3. **第三次握手（ACK）**：客戶端發送 ACK，確認收到伺服器的 SYN

三次握手確保了：

- 客戶端可以發送，伺服器可以接收（第一次）
- 伺服器可以發送，客戶端可以接收（第二次）
- 客戶端可以接收，伺服器可以發送（第三次）

如果只進行兩次握手，伺服器無法確認客戶端是否真的可以接收資料；如果進行四次握手則是浪費。

### 11.2.4 TCP 連線終止：四次揮手

TCP 連線終止需要四個步驟，因為 TCP 是全雙工的，每個方向需要獨立關閉：

```
客戶端                                              伺服器
   │                                                 │
   │              [ESTABLISHED]                     [ESTABLISHED]
   │                                                 │
   │ ────── FIN, seq=u ──────────────────────────► │
   │                                                 │
   │              [FIN_WAIT_1]                     [CLOSE_WAIT]
   │                                                 │
   │ ◄───── ACK, ack=u+1 ─────────────────────── │
   │                                                 │
   │              [FIN_WAIT_2]                     [CLOSE_WAIT]
   │                                                 │
   │         (伺服器處理剩餘資料...)                │
   │                                                 │
   │ ◄───── FIN, seq=w ────────────────────────── │
   │                                                 │
   │              [TIME_WAIT]                      [LAST_ACK]
   │                                                 │
   │ ────── ACK, ack=w+1 ──────────────────────► │
   │                                                 │
   │              [CLOSED]                         [CLOSED]
```

**為什麼是四次揮手？**

TCP 是全雙工通訊，每個方向都有一個獨立的資料流和獨立的序列號空間。當客戶端發送 FIN 時，只是表示「客戶端不再發送資料了」，但伺服器可能還有資料要發送給客戶端。因此，伺服器需要單獨發送一個 FIN 來關閉伺服器到客戶端的方向。

**TIME_WAIT 狀態**

客戶端在收到伺服器的 FIN 並發送最終的 ACK 後，進入 TIME_WAIT 狀態，保持 2MSL（Maximum Segment Lifetime，通常為 60 秒）時間。這是因為：

1. 確保最後的 ACK 能到達伺服器（如果丟失，伺服器會重發 FIN）
2. 讓網路上的所有封包自然消逝，避免影響新連線

### 11.2.5 TCP 狀態機

TCP 連線在生命週期內會經歷多種狀態。理解狀態機對於除錯和理解連線行為非常重要：

```
     │  主動開啟                    │ 被動開啟
     │                             │
     ▼                             ▼
┌─────────┐   SYN_SENT   ┌──────────────────┐   LISTEN    ┌─────────┐
│ CLOSED  │◄──────────► │   SYN_SENT/       │◄──────────►│ LISTEN  │
└─────────┘             │   ESTABLISHED    │             └─────────┘
                        └──────────────────┘                   │
     │                          │                    SYN_RCVD  │
     │  被動開啟                 │  SYN+ACK                     │
     │                          │  + ACK                       │
     │                          ▼                              │
┌─────────┐              ┌──────────────┐                     │
│ CLOSING │              │  ESTABLISHED │                     │
└─────────┘              └──────────────┘                     │
     │                          │                             │
     │  FIN+ACK                  │ FIN                        ▼
     │                          ▼                      ┌───────────┐
┌─────────┐              ┌──────────────┐               │FIN_WAIT_1 │
│ TIME_   │              │  FIN_WAIT_1  │               └───────────┘
│ WAIT    │              └──────────────┘                    │
└─────────┘                     │                             │ FIN
     │                          │ ACK / timeout              ▼
     │                          ▼                      ┌───────────┐
┌─────────┐              ┌──────────────┐               │FIN_WAIT_2 │
│ CLOSED  │              │  CLOSE_WAIT  │               └───────────┘
└─────────┘              └──────────────┘                    │
     │                          │                    ┌───────────┐
     │  LAST_ACK                │ FIN                │ CLOSE_WAIT│
     │                          ▼                    └───────────┘
     │                   ┌──────────────┐                   │
     │                   │ LAST_ACK     │                   │ FIN
     │                   └──────────────┘                   ▼
     │                                                 ┌───────────┐
     │                                                 │ LAST_ACK  │
     │                                                 └───────────┘
```

### 11.2.6 TCP 可靠性機制

TCP 透過多種機制確保可靠傳輸：

**確認與重傳**

- 接收端對成功收到的資料發送 ACK
- 如果發送端在超時時間內未收到 ACK，則重傳資料
- 使用「累計確認」——ACK 確認了所有小於該序號的連續資料

**序列號**

每個 TCP 段都有一個序列號，標識該段第一個資料位元組在位元組流中的位置。這使得：

- 接收端可以檢測丟失的段
- 接收端可以去除重複的段
- 接收端可以按正確順序重組資料

**重傳超時計算**

TCP 使用往返時間（Round-Trip Time, RTT）的估計值來計算重傳超時（Retransmission Timeout, RTO）。使用 Jacobson/Karels 演算法：

```
RTTVAR = (1 - β) * RTTVAR + β * |SRTT - RTT|
SRTT = (1 - α) * SRTT + α * RTT
RTO = SRTT + max(G, 4 * RTTVAR)

其中 α = 1/8, β = 1/4, G 是時鐘粒度
```

### 11.2.7 TCP 流量控制

TCP 使用滑動視窗機制進行流量控制，防止發送端過快傳送，壓垮接收端的緩衝區。

**接收窗口**

接收端在 TCP 頭部中通告「窗口大小」（Window Size），表示接收端願意接收的位元組數。發送端的「可用窗口」等於通告窗口減去已發送但未確認的位元組數：

```
發送端視角：
┌──────────────┬─────────────────────────┬─────────────────┐
│  已確認      │   已發送未確認          │    可發送區域    │
│  (acked)     │   (sent, unacked)       │    (usable)     │
└──────────────┴─────────────────────────┴─────────────────┘
                ▲                         ▲
                │─ ─ ─ 視窗大小 ─ ─ ─ ─ ─ │
```

**零窗口與窗口更新**

當接收端應用程式處理速度慢於網路速度時，緩衝區可能變滿，通告窗口變為零（零窗口）。這時發送端停止發送資料，但會定期發送探測段（window probe）來詢問窗口是否更新。

### 11.2.8 TCP 擁塞控制

擁塞控制是 TCP 最重要的特性之一，防止過多的資料注入網路，造成路由器緩衝區溢出和封包丟失。

**核心概念：擁塞窗口（cwnd）**

除了接收端通告的接收窗口（rwnd）外，發送端還維護一個「擁塞窗口」（congestion window, cwnd）。發送端實際可發送的位元組數為：

```
可發送 = min(cwnd, rwnd)
```

**四個核心演算法**

1. **慢啟動（Slow Start）**

初始時 cwnd 很小（通常為 1-10 個 MSS, Maximum Segment Size），每收到一個 ACK，cwnd 增加一個 MSS。這是指數增長，直到達到慢啟動閾值（ssthresh）。

2. **擁塞避免（Congestion Avoidance）**

當 cwnd 達到 ssthresh 後，進入擁塞避免階段。此時每收到一個 ACK，cwnd 只增加 1/cwnd 個 MSS。這是線性增長。

3. **快速重傳（Fast Retransmit）**

當發送端收到 3 個相同的 ACK（表明有段丟失，但網路仍能傳送），立即重傳丟失的段，而不等待超時。

4. **快速恢復（Fast Recovery）**

快速重傳後，進入快速恢復階段。ssthresh 設為 cwnd/2，cwnd 設為 ssthresh + 3*MSS。

**擁塞控制演算法變體**

現代 TCP 使用多種演算法來改進基本演算法的效能：

| 演算法 | 說明 |
|--------|------|
| Tahoe | 基本的慢啟動、擁塞避免、快速重傳/恢復 |
| Reno | Tahoe + 快速恢復 |
| NewReno | 改進 Reno 的多段丟失處理 |
| CUBIC | Linux 預設，高速網路友好 |
| BBR | Google 開發，基於頻寬-延遲積 |
| Westwood+ | 改進的慢啟動，估計可用頻寬 |

### 11.2.9 UDP 協定

UDP（User Datagram Protocol）是一種簡單的無連線傳輸協定，提供最小的傳輸服務。與 TCP 不同，UDP 不保證：

- 封包送達
- 封包順序
- 封包不重複
- 資料完整性

**UDP 頭部格式**

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├───────────────────┬───────────────────┬───────────────────┬─────────┤
│   Source Port     │   Dest Port      │                                  │
├───────────────────┼───────────────────┼───────────────────┴───────────┤
│   Length          │   Checksum       │                                   │
└───────────────────┴───────────────────┴───────────────────────────────────┘
```

UDP 頭部只有 8 位元組，是 TCP 頭部（至少 20 位元組）的一半。UDP 適用於：

| 應用場景 | 原因 |
|---------|------|
| DNS 查詢 | 請求-響應模式，丟失後客戶端會重試 |
| VoIP / 視訊通話 | 實時性比可靠性重要，容忍少量丟失 |
| 線上遊戲 | 實時狀態更新，歷史位置不重要 |
| 串流媒體 | 使用應用層的錯誤恢復或容忍丟失 |
| DHCP | 請求-響應模式 |
| NTP |  時間同步，單向丟失可接受 |

## 11.3 Socket 程式設計

### 11.3.1 TCP Socket 流程

TCP 程式設計遵循標準的客戶端-伺服器模式：

```
    伺服器                             客戶端
       │                                 │
       │ ──────── socket() ──────────── │ ─────── socket() ───────────
       │                                 │
       │ ──────── bind() ─────────────  │ (bind 通常可選)
       │                                 │
       │ ──────── listen() ──────────── │
       │                                 │
       │ ──────── accept() ────────◄── │ ──── connect() ───────────
       │                                 │
       │ ──────── read() ◄──────────── │ ──── write() ────────────
       │                                 │
       │ ──────── write() ──────────── │ ──── read() ────────────
       │                                 │
       │ ──────── close() ──────────── │ ──── close() ────────────
       │                                 │
```

**listen() 的作用**

`listen()` 將 socket 從主動模式（用於 connect）轉換為被動模式（用於 accept）。listen 的第二個參數是「未完成連線佇列」的最大長度，表示已完成三次握手但尚未被 accept 的連線數。

**accept() 的行為**

`accept()` 從已完成連線佇列中取出一個連線，建立一個新的 socket 與客戶端通訊。原始的 listen socket 繼續監聽新連線。

### 11.3.2 TCP 程式設計範例

```python
# TCP 伺服器（Python）
import socket

def handle_client(client_sock, client_addr):
    """處理單個客戶端連線"""
    print(f"Client connected: {client_addr}")
    try:
        while True:
            data = client_sock.recv(4096)
            if not data:
                break
            print(f"Received: {data.decode()}")
            client_sock.sendall(b"Echo: " + data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_sock.close()
        print(f"Client disconnected: {client_addr}")

def main():
    # 建立 socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 設定 socket 選項
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 綁定位址
    sock.bind(('0.0.0.0', 8080))
    
    # 監聽
    sock.listen(128)
    print("Server listening on port 8080")
    
    # 接受連線迴圈
    while True:
        client_sock, client_addr = sock.accept()
        handle_client(client_sock, client_addr)

if __name__ == '__main__':
    main()
```

```python
# TCP 客戶端（Python）
import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect(('127.0.0.1', 8080))
        print("Connected to server")
        
        message = "Hello, TCP Server!"
        sock.sendall(message.encode())
        print(f"Sent: {message}")
        
        response = sock.recv(4096)
        print(f"Received: {response.decode()}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    main()
```

### 11.3.3 UDP 程式設計範例

```python
# UDP 伺服器
import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 9000))
    print("UDP server listening on port 9000")
    
    while True:
        data, addr = sock.recvfrom(4096)
        print(f"Received from {addr}: {data.decode()}")
        sock.sendto(b"ACK: " + data, addr)

if __name__ == '__main__':
    main()
```

### 11.3.4 非阻塞與並發

傳統的同步 socket 程式設計在等待 I/O 時會阻塞執行緒。對於需要同時處理多個連線的伺服器，有幾種常見的並發策略：

**多程序模型**

每個客戶端連線由一個子行程處理：

```python
import socket
import os

def handle_client(sock, addr):
    # 在子行程中處理
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            sock.sendall(data)
    finally:
        sock.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(128)
    
    while True:
        client, addr = sock.accept()
        pid = os.fork()
        if pid == 0:
            # 子行程
            sock.close()
            handle_client(client, addr)
            os._exit(0)
        else:
            # 父行程
            client.close()
```

**事件驅動模型**

使用 I/O 多路復用（非阻塞 select/poll/epoll）處理多個連線：

```python
import select
import socket

def main():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(128)
    sock.setblocking(False)
    
    epoll = select.epoll()
    epoll.register(sock.fileno(), select.EPOLLIN)
    
    connections = {}
    
    try:
        while True:
            events = epoll.poll()
            for fd, event in events:
                if fd == sock.fileno():
                    # 新連線
                    client, addr = sock.accept()
                    client.setblocking(False)
                    connections[client.fileno()] = (client, addr)
                    epoll.register(client.fileno(), select.EPOLLIN)
                elif event & select.EPOLLIN:
                    # 可讀事件
                    client, _ = connections[fd]
                    data = client.recv(1024)
                    if data:
                        client.sendall(data)
                    else:
                        client.close()
                        epoll.unregister(fd)
                        del connections[fd]
    finally:
        epoll.close()
```

## 11.4 網路層級與路由

### 11.4.1 路由表結構

路由表是 IP 層轉送決策的核心。每個路由表項包含：

| 欄位 | 說明 |
|------|------|
| 目的地網路 | 目標網路的前綴和長度 |
| 網路遮罩 | CIDR 表示法 |
| 下一跳 | 轉送的下一個 IP 位址 |
| 介面 | 發送封包的網路介面 |
| 度量值 | 路徑成本，用於多路徑選擇 |

Linux 路由表檢視：

```bash
# 顯示路由表
ip route show
# 或
route -n

# 典型輸出：
# default via 192.168.1.1 dev eth0 proto dhcp
# 192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100
```

### 11.4.2 最長前綴匹配

當 IP 封包需要轉送時，路由器會在路由表中找到「最長前綴匹配」（Longest Prefix Match, LPM）的路由。這意味著選擇位址範圍最精確匹配的路由。

```
目的 IP: 10.1.2.100

路由表：
  0.0.0.0/0          → 預設閘道
  10.0.0.0/8         → 內部網路
  10.1.0.0/16        → 子公司 A
  10.1.2.0/24        → 子公司 A 的部門 B  ← 選擇這個（最長匹配）
```

### 11.4.3 路由協定

在大型網路中，手動配置靜態路由是不可行的。動態路由協定自動發現和維護路由：

**內部閘道協定**（IGP）用於單一自治系統內部：

| 協定 | 說明 |
|------|------|
| RIP | 基於跳數的距離向量，適合小型網路 |
| OSPF | 鏈路狀態協定，適合中大型網路 |
| IS-IS | 類似 OSPF，常用於電信網路 |
| EIGRP | Cisco 專有，混合型 |

**外部閘道協定**（EGP）用於自治系統之間：

| 協定 | 說明 |
|------|------|
| BGP | 唯一的外部閘道協定，Internet 的基礎 |

## 11.5 網路效能優化

### 11.5.1 TCP 效能調校參數

Linux 提供了大量的 TCP 參數可調整：

```bash
# 增加 socket buffer
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216
sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216"

# TCP 視窗擴展（允許更大的窗口）
sysctl -w net.ipv4.tcp_window_scaling=1

# TCP 時間戳（更精確的 RTT 測量）
sysctl -w net.ipv4.tcp_timestamps=1

# TCP 選擇性確認（SACK）
sysctl -w net.ipv4.tcp_sack=1

# TCP 擁塞控制演算法
sysctl -w net.ipv4.tcp_congestion_control=cubic

# 快速打開（減少握手延遲）
sysctl -w net.ipv4.tcp_fastopen=3
```

### 11.5.2 Nagle 演算法

Nagle 演算法（RFC 896）的設計目標是減少小封包造成的網路負載。其規則是：

> 當發送端有未確認的小封包時，緩衝後續的小資料，直到收到 ACK

這減少了網路上小封包的數量，但可能增加延遲。對於即時性要求高的應用（如 SSH、遊戲），可以禁用 Nagle：

```c
// 禁用 Nagle 演算法
int flag = 1;
setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));
```

### 11.5.3 擁塞控制演算法比較

| 演算法 | 優點 | 缺點 | 適用場景 |
|--------|------|------|----------|
| CUBIC | 高頻寬利用率、穩定 | 對低延遲網路不友好 | 現代高速網路 |
| BBR | 低延遲、公平性好 | 需要較新核心 | 高速長肥管道 |
| Reno | 簡單、經典 | 高速網路效能差 | 通用 |
| Westwood+ | 頻寬估計準確 | 複雜度較高 | 無線網路 |

### 11.5.4 常見效能瓶頸與解決方案

| 瓶頸 | 徵兆 | 解決方案 |
|------|------|----------|
| 連線數限制 | Too many open files | 調整 `ulimit -n`、核心參數 |
| 連線終止延遲 | 大量 TIME_WAIT | 啟用 `tcp_tw_reuse` |
| 小封包延遲 | 鍵盤回應慢 | 禁用 Nagle（TCP_NODELAY） |
| 連線建立慢 | 首次請求慢 | 啟用 TCP Fast Open |
| 高並發記憶體 | OOM | 調整 socket buffer 大小 |
| 網路延遲 | RTT 高 | 使用 CDNs、就近部署 |

### 11.5.5 網路監控工具

```bash
# 即時網路監控
watch -n 1 'cat /proc/net/dev'

# 連線統計
ss -s

# 詳細連線資訊
ss -tunapl

# TCP 狀態統計
netstat -tan | awk '/^tcp/ {state[$NF]++} END {for (s in state) print s, state[s]}'

# 網路延遲測試
ping -c 10 example.com

# 頻寬測試
iperf3 -s  # 伺服器
iperf3 -c server_ip  # 客戶端
```
