# DNS (Domain Name System)

## 概述

DNS 是網域名稱系統，將易於記憶的網域名稱（如 www.example.com）轉換為 IP 位址。DNS 是網際網路的基礎設施，類似於網際網路的電話簿。

## 歷史

- **1983**：DNS 發明（Paul Mockapetris）
- **1987**：RFC 1034/1035 標準化
- **1990s**：根伺服器設立
- **現在**：全球分散式資料庫

## DNS 查詢

### 1. 解析過程

```
1. 用戶端查詢本地 DNS 快取
2. 查詢 ISP DNS 伺服器
3. 如果沒有，遞迴查詢根伺服器 (.com)
4. 查詢 TLD 伺服器 (example.com)
5. 查詢 Authoritative DNS 伺服器
6. 返回 IP 位址
```

### 2. DNS 記錄類型

```bash
# A 記錄 - IPv4 位址
example.com.    IN A     93.184.216.34

# AAAA 記錄 - IPv6 位址
example.com.    IN AAAA  2606:2800:220:1:248:1893:25c8:1946

# CNAME - 別名
www.example.com. IN CNAME example.com.

# MX - 郵件交換
example.com.    IN MX    10 mail.example.com.

# NS - 名稱伺服器
example.com.    IN NS    ns1.example.com.

# TXT - 文字記錄
example.com.    IN TXT   "v=spf1 mx ~all"
```

### 3. Python DNS 查詢

```python
import socket

# 簡單 DNS 查詢
ip = socket.gethostbyname("www.example.com")
print(ip)  # 93.184.216.34

# 反向 DNS
hostname = socket.gethostbyaddr("93.184.216.34")
print(hostname)
```

### 4. 使用 dnspython

```python
import dns.resolver

# A 記錄
answers = dns.resolver.resolve("example.com", "A")
for rdata in answers:
    print(rdata)

# MX 記錄
answers = dns.resolver.resolve("example.com", "MX")
for rdata in answers:
    print(rdata.preference, rdata.exchange)

# TXT 記錄
answers = dns.resolver.resolve("example.com", "TXT")
for rdata in answers:
    print(rdata)
```

### 5. dig 命令

```bash
# 查詢 A 記錄
dig example.com A

# 查詢 MX 記錄
dig example.com MX

# 反向查詢
dig -x 93.184.216.34

# 查看完整回應
dig +noall +answer example.com
```

## DNS 安全

### 1. DNSSEC

```bash
# 驗證 DNSSEC
dig +dnssec example.com
```

### 2. DNS over HTTPS (DoH)

```python
import requests

response = requests.get(
    "https://cloudflare-dns.com/dns-query",
    params={"name": "example.com", "type": "A"},
    headers={"accept": "application/dns-json"}
)
print(response.json())
```

## 為什麼學習 DNS？

1. **網路基礎**：理解網際網路
2. **網頁開發**：網域配置
3. **安全**：DNS 相關攻擊
4. **效能**：DNS 快取

## 參考資源

- RFC 1034, 1035
- "DNS and BIND"
- Cloudflare DNS
