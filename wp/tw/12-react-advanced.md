# 第 12 章：React 進階

## 概述

本章介紹 React 的進階技術，包括 Context API、Redux 狀態管理、React Router 路由，以及高階元件模式。

## 12.1 Context API 基礎

Context API 提供一種在元件樹間共享資料的方式。

[程式檔案：12-1-context-basic.jsx](../_code/12/12-1-context-basic.jsx)

```jsx
import React, { createContext } from 'react';

const ThemeContext = createContext({
  theme: 'light',
  toggleTheme: () => {}
});

export default ThemeContext;
```

**適合使用 Context 的場景：**
- 登入使用者資訊
- 主題設定
- 語言設定
- 全域錯誤處理

## 12.2 Context Provider

Provider 包裹元件樹，使 Context 值可用。

[程式檔案：12-2-context-provider.jsx](../_code/12/12-2-context-provider.jsx)

```jsx
import React, { useState } from 'react';
import ThemeContext from './12-1-context-basic.jsx';

const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;
```

## 12.3 Context Consumer

Consumer 訂閱 Context 變化（現在推薦使用 useContext）。

[程式檔案：12-3-context-consumer.jsx](../_code/12/12-3-context-consumer.jsx)

```jsx
import React from 'react';
import ThemeContext from './12-1-context-basic.jsx';

const ThemedContent = () => (
  <ThemeContext.Consumer>
    {({ theme }) => (
      <div className={theme}>
        <p>Current theme: {theme}</p>
      </div>
    )}
  </ThemeContext.Consumer>
);

export default ThemedContent;
```

## 12.4 Redux 基礎

Redux 是 JavaScript 應用的狀態管理容器。

[程式檔案：12-4-redux-basic.js](../_code/12/12-4-redux-basic.js)

```jsx
import { createStore } from 'redux';

const initialState = { count: 0 };

const counterReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'DECREMENT':
      return { count: state.count - 1 };
    default:
      return state;
  }
};

const store = createStore(counterReducer);

export default store;
```

## 12.5 Redux Store

Store 是 Redux 的核心，儲存所有狀態。

[程式檔案：12-5-redux-store.js](../_code/12/12-5-redux-store.js)

```jsx
import { createStore } from 'redux';
import counterReducer from './12-6-redux-reducer.js';

const store = createStore(counterReducer);

console.log('Initial state:', store.getState());

store.subscribe(() => {
  console.log('State changed:', store.getState());
});

export default store;
```

## 12.6 Redux Reducer

Reducer 是純函數，根據 action 計算新狀態。

[程式檔案：12-6-redux-reducer.js](../_code/12/12-6-redux-reducer.js)

```jsx
const initialState = { count: 0 };

const counterReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + (action.payload || 1) };
    case 'DECREMENT':
      return { count: state.count - (action.payload || 1) };
    case 'RESET':
      return { count: 0 };
    default:
      return state;
  }
};

export default counterReducer;
```

## 12.7 React Router 基礎

React Router 是 React 的標準路由解決方案。

[程式檔案：12-7-react-router-basic.jsx](../_code/12/12-7-react-router-basic.jsx)

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

const Home = () => <h1>Home</h1>;
const About = () => <h1>About</h1>;
const Contact = () => <h1>Contact</h1>;

const App = () => (
  <BrowserRouter>
    <nav>
      <Link to="/">Home</Link>
      <Link to="/about">About</Link>
      <Link to="/contact">Contact</Link>
    </nav>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
    </Routes>
  </BrowserRouter>
);

export default App;
```

## 12.8 路由配置

使用 Routes 和 Route 定義路由結構。

[程式檔案：12-8-router-config.jsx](../_code/12/12-8-router-config.jsx)

```jsx
import { Routes, Route, Navigate } from 'react-router-dom';

const PrivateRoute = ({ children, isAuthenticated }) => (
  <Routes>
    <Route
      path="/"
      element={isAuthenticated ? children : <Navigate to="/login" />}
    />
  </Routes>
);

const Dashboard = () => <h1>Dashboard</h1>;
const Login = () => <h1>Login</h1>;

export { PrivateRoute, Dashboard, Login };
```

## 12.9 路由參數

使用 URL 參數傳遞動態資料。

[程式檔案：12-9-router-params.jsx](../_code/12/12-9-router-params.jsx)

```jsx
import { BrowserRouter, Routes, Route, useParams } from 'react-router-dom';

const UserProfile = () => {
  const { id } = useParams();
  return <h1>User ID: {id}</h1>;
};

const PostDetail = () => {
  const { postId } = useParams();
  return <h1>Post ID: {postId}</h1>;
};

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/user/:id" element={<UserProfile />} />
      <Route path="/post/:postId" element={<PostDetail />} />
    </Routes>
  </BrowserRouter>
);

export default App;
```

## 12.10 高階元件

高階元件（HOC）是一種重用元件邏輯的模式。

[程式檔案：12-10-hoc.jsx](../_code/12/12-10-hoc.jsx)

```jsx
import React from 'react';

const withLogger = (WrappedComponent) => {
  return (props) => {
    console.log('Props received:', props);
    return <WrappedComponent {...props} />;
  };
};

const MyComponent = ({ name, value }) => (
  <div>{name}: {value}</div>
);

const EnhancedComponent = withLogger(MyComponent);

export { withLogger, EnhancedComponent };
```

**常見 HOC 用途：**
- 認證檢查
- 日誌記錄
- 效能監控
- 樣式注入

## 重點回顧

| 概念 | 說明 |
|------|------|
| Context API | 元件樹共享資料 |
| Redux | 集中式狀態管理 |
| React Router | 客戶端路由 |
| useParams | 取得 URL 參數 |
| HOC | 高階元件模式 |

## 練習題

1. 建立一個 AuthContext 提供登入/登出功能
2. 使用 Redux Toolkit 實作待辦事項狀態管理
3. 建立一個部落格路由系統
4. 實作一個 withLoading HOC
