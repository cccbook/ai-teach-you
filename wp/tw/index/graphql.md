# GraphQL

## 概述

GraphQL 是一種 API 查詢語言和運行時，讓客戶端能夠精確地請求所需的資料。

## 與 REST 的比較

| REST | GraphQL |
|------|---------|
| 多個端點 | 單一端點 |
| 固定資料結構 | 客戶端指定需要的欄位 |
| 過度取得或不足取得 | 精確取得所需資料 |

## 核心概念

### Schema 定義

```graphql
type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
}

type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
}

type Query {
    user(id: ID!): User
    users: [User!]!
    posts: [Post!]!
}

type Mutation {
    createUser(name: String!, email: String!): User!
    createPost(title: String!, content: String!, authorId: ID!): Post!
}
```

### 查詢

```graphql
query GetUser($id: ID!) {
    user(id: $id) {
        name
        email
        posts {
            title
        }
    }
}
```

### 突變

```graphql
mutation CreatePost($title: String!, $content: String!, $authorId: ID!) {
    createPost(title: $title, content: $content, authorId: $authorId) {
        id
        title
    }
}
```

## 工具

- **Apollo Client**：GraphQL 客戶端
- **GraphQL.js**：Schema 執行環境
- **Prisma**：GraphQL 資料庫工具

## 參考資源

- [GraphQL 官方網站](https://graphql.org/)
- [GraphQL 中文網](https://graphql.cn/)
