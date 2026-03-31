# React

## 概述

React 是 Facebook 開發的 JavaScript 函式庫，用於建立使用者介面，特別適合單頁應用（SPA）。

## 核心概念

### 元件

元件是 React 的核心 building block：

```jsx
function Welcome({ name }) {
    return <h1>Hello, {name}!</h1>;
}

class Counter extends React.Component {
    state = { count: 0 };
    
    render() {
        return <p>Count: {this.state.count}</p>;
    }
}
```

### JSX

JSX 允許在 JavaScript 中編寫 HTML-like 語法：

```jsx
const element = (
    <div className="container">
        <h1>Title</h1>
        <p>Content</p>
    </div>
);
```

### Props 和 State

- **Props**：從父元件傳入的資料（唯讀）
- **State**：元件內部的可變狀態

```jsx
function Button({ label, onClick }) {
    const [loading, setLoading] = useState(false);
    return <button onClick={onClick}>{loading ? 'Loading...' : label}</button>;
}
```

### Hooks

Hooks 讓函數元件可以使用 state 和生命週期：

```jsx
import { useState, useEffect, useContext } from 'react';

// useState - 管理狀態
const [count, setCount] = useState(0);

// useEffect - 副作用
useEffect(() => {
    document.title = `Count: ${count}`;
}, [count]);

// useContext - 存取 Context
const theme = useContext(ThemeContext);
```

## 常用 Hooks

| Hook | 用途 |
|------|------|
| useState | 管理元件狀態 |
| useEffect | 處理副作用 |
| useContext | 存取 Context |
| useRef | 存取 DOM 或可變值 |
| useMemo | 快取計算結果 |
| useCallback | 快取函數 |

## 參考資源

- [React 官方文檔](https://react.dev/)
- [React 中文文檔](https://zh-hant.react.dev/)
