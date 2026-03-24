# 第 11 章：React Hooks

## 概述

React Hooks 是 React 16.8 引入的功能，允許在函數元件中使用 state 和生命週期等特性。本章介紹最常用的 Hooks。

## 11.1 useState 基礎

useState 是最基本的 Hook，用於在函數元件中添加狀態。

[程式檔案：11-1-usestate-basic.jsx](../_code/11/11-1-usestate-basic.jsx)

```jsx
import React, { useState } from 'react';

const UseStateBasic = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Add</button>
    </div>
  );
};

export default UseStateBasic;
```

**useState 特點：**
- 回傳 `[state, setState]` 陣列
- 可傳入初始值
- setState 是非同步的
- 多次呼叫支援多個狀態

## 11.2 useState 函數更新

當新狀態依賴舊狀態時，應使用函數式更新。

[程式檔案：11-2-usestate-function.jsx](../_code/11/11-2-usestate-function.jsx)

```jsx
import React, { useState } from 'react';

const UseStateFunction = () => {
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount(prevCount => prevCount + 1);
  };

  const decrement = () => {
    setCount(prevCount => prevCount - 1);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
};

export default UseStateFunction;
```

## 11.3 useEffect 基礎

useEffect 用於處理副作用，如資料獲取、訂閱、手動 DOM 操作。

[程式檔案：11-3-useeffect-basic.jsx](../_code/11/11-3-useeffect-basic.jsx)

```jsx
import React, { useState, useEffect } from 'react';

const UseEffectBasic = () => {
  const [data, setData] = useState('');

  useEffect(() => {
    setData('Data loaded!');
  }, []);

  return <p>{data}</p>;
};

export default UseEffectBasic;
```

**useEffect 的用途：**
- 資料獲取
- 事件監聽
- 定時器
- 手動 DOM 操作
- 訂閱/取消訂閱

## 11.4 useEffect 清理

回傳函數用於清理副作用。

[程式檔案：11-4-useeffect-cleanup.jsx](../_code/11/11-4-useeffect-cleanup.jsx)

```jsx
import React, { useState, useEffect } from 'react';

const UseEffectCleanup = () => {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return <p>Window width: {width}</p>;
};

export default UseEffectCleanup;
```

## 11.5 依賴陣列

依賴陣列控制 useEffect 何時執行。

[程式檔案：11-5-useeffect-dependency.jsx](../_code/11/11-5-useeffect-dependency.jsx)

```jsx
import React, { useState, useEffect } from 'react';

const UseEffectDependency = () => {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  useEffect(() => {
    console.log('Count changed:', count);
  }, [count]);

  useEffect(() => {
    console.log('Name changed:', name);
  }, [name]);

  return (
    <div>
      <p>Count: {count}</p>
      <input value={name} onChange={e => setName(e.target.value)} />
      <button onClick={() => setCount(count + 1)}>Add</button>
    </div>
  );
};

export default UseEffectDependency;
```

**依賴陣列選項：**
- `[]`：只在 mount 時執行一次
- `[dep]`：dep 變化時執行
- 無陣列：每次渲染都執行

## 11.6 useContext

useContext 用於存取 React Context，避免 prop drilling。

[程式檔案：11-6-usecontext.jsx](../_code/11/11-6-usecontext.jsx)

```jsx
import React, { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

const ThemedButton = () => {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Button</button>;
};

const App = () => (
  <ThemeContext.Provider value="dark">
    <ThemedButton />
  </ThemeContext.Provider>
);

export default App;
```

## 11.7 useRef

useRef 用於存取 DOM 元素或儲存可變值。

[程式檔案：11-7-useref.jsx](../_code/11/11-7-useref.jsx)

```jsx
import React, { useRef } from 'react';

const UseRefDemo = () => {
  const inputRef = useRef(null);
  const countRef = useRef(0);

  const focusInput = () => {
    inputRef.current.focus();
  };

  const increment = () => {
    countRef.current += 1;
    console.log('Count:', countRef.current);
  };

  return (
    <div>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus</button>
      <button onClick={increment}>Count</button>
    </div>
  );
};

export default UseRefDemo;
```

## 11.8 useMemo

useMemo 用於快取計算結果，優化效能。

[程式檔案：11-8-usememo.jsx](../_code/11/11-8-usememo.jsx)

```jsx
import React, { useState, useMemo } from 'react';

const UseMemoDemo = () => {
  const [count, setCount] = useState(0);
  const [number, setNumber] = useState(5);

  const factorial = useMemo(() => {
    console.log('Calculating...');
    return [...Array(number)].map((_, i) => i + 1).reduce((a, b) => a * b, 1);
  }, [number]);

  return (
    <div>
      <p>Factorial of {number}: {factorial}</p>
      <button onClick={() => setCount(count + 1)}>Re-render: {count}</button>
      <button onClick={() => setNumber(number + 1)}>Number +</button>
    </div>
  );
};

export default UseMemoDemo;
```

## 11.9 useCallback

useCallback 用於快取函數，優化子元件渲染。

[程式檔案：11-9-usecallback.jsx](../_code/11/11-9-usecallback.jsx)

```jsx
import React, { useState, useCallback } from 'react';

const UseCallbackDemo = () => {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    console.log('Clicked!');
  }, []);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <button onClick={handleClick}>Click Me</button>
    </div>
  );
};

export default UseCallbackDemo;
```

## 11.10 自定義 Hook

自定義 Hook 讓你提取和重用有狀態邏輯的函數。

[程式檔案：11-10-custom-hook.jsx](../_code/11/11-10-custom-hook.jsx)

```jsx
import { useState, useEffect } from 'react';

const useWindowSize = () => {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return size;
};

export default useWindowSize;
```

**自定義 Hook 規則：**
- 以 `use` 開頭
- 可呼叫其他 Hooks
- 可接受參數和回傳任意值

## 重點回顧

| Hook | 用途 |
|------|------|
| useState | 管理元件狀態 |
| useEffect | 處理副作用 |
| useContext | 存取 Context |
| useRef | 存取 DOM 或可變值 |
| useMemo | 快取計算結果 |
| useCallback | 快取函數 |
| 自定義 Hook | 封裝和重用邏輯 |

## 練習題

1. 建立一個 useDebounce Hook
2. 實作一個 useLocalStorage Hook
3. 建立一個 useFetch Hook 處理資料獲取
4. 實作一個 usePrevious Hook 取得上一個值
