# gRPC

## 概述

gRPC 是 Google 開發的高效能、开源的 RPC 框架，使用 Protocol Buffers 作為介面定義語言和訊息序列化格式。

## 特點

- **高效能**：使用 HTTP/2 和 Protocol Buffers
- **跨語言**：支援多種程式語言
- **強類型**：透過 .proto 檔案定義強類型介面
- **雙向串流**：支援客戶端和伺服器雙向串流

## Protocol Buffers

定義服務和訊息格式：

```protobuf
syntax = "proto3";

message User {
    string id = 1;
    string name = 2;
    string email = 3;
}

message GetUserRequest {
    string user_id = 1;
}

message GetUserResponse {
    User user = 1;
}

service UserService {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}
```

## 服務類型

### 一元 RPC

```protobuf
rpc GetUser(GetUserRequest) returns (UserResponse);
```

### 伺服器串流 RPC

```protobuf
rpc StreamUsers(StreamRequest) returns (stream User);
```

### 客戶端串流 RPC

```protobuf
rpc CreateUsers(stream CreateUserRequest) returns (CreateUsersResponse);
```

### 雙向串流 RPC

```protobuf
rpc Chat(stream ChatMessage) returns (stream ChatMessage);
```

## 應用場景

- 微服務之間的通訊
- 行動應用後端
- 即時串流應用
- IoT 設備通訊

## 參考資源

- [gRPC 官方網站](https://grpc.io/)
- [Protocol Buffers 文檔](https://developers.google.com/protocol-buffers)
