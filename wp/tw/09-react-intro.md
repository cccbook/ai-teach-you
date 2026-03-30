# 第 9 章：React 入門

## 概述

React 是 Facebook 開發的 UI 函式庫，用於建立互動式使用者介面。本章介紹 React 的基礎概念，包括 JSX、元件、Props 和 State。

## 9.1 JSX 基礎語法

JSX 是 JavaScript 的語法擴展，允許在 JavaScript 中編寫 HTML -like 的程式碼。

[程式檔案：09-1-jsx-basic.jsx](../_code/09/09-1-jsx-basic.jsx)

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';

const element = <h1>Hello, React!</h1>;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(element);
```

**JSX 規則：**
- 標籤必須閉合
- 只能有一個根元素
- 使用 `className` 而非 `class`
- 使用 `camelCase` 命名屬性

## 9.2 JSX 嵌入表達式

在 JSX 中使用 `{}` 嵌入 JavaScript 表達式。

[程式檔案：09-2-jsx-embed.jsx](../_code/09/09-2-jsx-embed.jsx)

```jsx
import React from 'react';

const name = 'Alice';
const age = 25;

const element = (
  <div>
    <h1>Hello, {name}!</h1>
    <p>You are {age} years old.</p>
    <p>Next year: {age + 1}</p>
  </div>
);

export default element;
```

**可嵌入的內容：**
- 變數和常量
- 運算式
- 函數呼叫
- 三元運算子
- 陣列和物件（部分情況）

## 9.3 第一個元件

元件是 React 的核心概念，用於封裝可重複使用的 UI。

[程式檔案：09-3-hello-component.jsx](../_code/09/09-3-hello-component.jsx)

```jsx
import React from 'react';

function HelloComponent() {
  return <h1>Hello, Component!</h1>;
}

export default HelloComponent;
```

**元件特點：**
- 首字母大寫
- 回傳 JSX
- 單一根元素
- 可重複使用

## 9.4 函數元件

函數元件是現代 React 開發的主流方式。

[程式檔案：09-4-functional-component.jsx](../_code/09/09-4-functional-component.jsx)

```jsx
import React from 'react';

const FunctionalComponent = () => {
  return (
    <div>
      <h1>Functional Component</h1>
      <p>This is a functional component.</p>
    </div>
  );
};

export default FunctionalComponent;
```

## 9.5 類別元件

類別元件是 React 早期的元件寫法，現已被 Hook 取代。

[程式檔案：09-5-class-component.jsx](../_code/09/09-5-class-component.jsx)

```jsx
import React, { Component } from 'react';

class ClassComponent extends Component {
  render() {
    return (
      <div>
        <h1>Class Component</h1>
        <p>This is a class component.</p>
      </div>
    );
  }
}

export default ClassComponent;
```

## 9.6 Props 基礎

Props 是元件的輸入參數，用於父子元件間的資料傳遞。

[程式檔案：09-6-props-basic.jsx](../_code/09/09-6-props-basic.jsx)

```jsx
import React from 'react';

const PropsDemo = (props) => {
  return (
    <div>
      <h2>Hello, {props.name}!</h2>
      <p>Age: {props.age}</p>
    </div>
  );
};

export default PropsDemo;
```

**Props 特點：**
- 唯讀，不可修改
- 從父元件傳入
- 可指定預設值
- 支援任意資料類型

## 9.7 Props 傳遞

使用解構賦值簡化 Props 的使用。

[程式檔案：09-7-props-pass.jsx](../_code/09/09-7-props-pass.jsx)

```jsx
import React from 'react';

const UserCard = ({ name, email, age }) => {
  return (
    <div className="user-card">
      <h3>{name}</h3>
      <p>Email: {email}</p>
      <p>Age: {age}</p>
    </div>
  );
};

export default UserCard;
```

## 9.8 State 基礎

State 是元件內部的狀態，用於儲存會變化的資料。

[程式檔案：09-8-state-basic.jsx](../_code/09/09-8-state-basic.jsx)

```jsx
import React, { useState } from 'react';

const StateDemo = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
};

export default StateDemo;
```

**useState Hook：**
- 回傳狀態值和更新函式
- 初始值只用在第一次渲染
- 更新是非同步的
- 更新會觸發重新渲染

## 9.9 State 更新

更新 State 時應使用函式式更新以避免基於舊值的問題。

[程式檔案：09-9-state-update.jsx](../_code/09/09-9-state-update.jsx)

```jsx
import React, { useState } from 'react';

const StateUpdate = () => {
  const [text, setText] = useState('Hello');

  const updateText = () => {
    setText(text === 'Hello' ? 'World' : 'Hello');
  };

  return (
    <div>
      <p>{text}</p>
      <button onClick={updateText}>Toggle</button>
    </div>
  );
};

export default StateUpdate;
```

## 9.10 條件渲染

根據條件決定要渲染什麼內容。

[程式檔案：09-10-conditional-render.jsx](../_code/09/09-10-conditional-render.jsx)

```jsx
import React, { useState } from 'react';

const ConditionalRender = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div>
      {isLoggedIn ? (
        <p>Welcome back!</p>
      ) : (
        <p>Please log in.</p>
      )}
      <button onClick={() => setIsLoggedIn(!isLoggedIn)}>
        {isLoggedIn ? 'Logout' : 'Login'}
      </button>
    </div>
  );
};

export default ConditionalRender;
```

**條件渲染方式：**
- 三元運算子
- AND 運算子 (`&&`)
- IF 語句（函數內部）
- 早期返回

## 重點回顧

| 概念 | 說明 |
|------|------|
| JSX | JavaScript 語法擴展，描述 UI |
| 元件 | 可重複使用的 UI 區塊 |
| Props | 從父元件傳入的資料 |
| State | 元件內部的可變狀態 |
| 條件渲染 | 根據條件決定渲染內容 |

## 練習題

1. 建立一個顯示使用者資訊的卡片元件
2. 實作一個計數器元件，支援增減功能
3. 建立一個待辦事項列表，根據完成狀態顯示不同樣式
4. 實作一個條件顯示的登入/登出切換器
