# 第 10 章：React 元件

## 概述

本章深入探討 React 元件的各個面向，包括生命週期、類別元件、以及元件組合模式。

## 10.1 生命週期基礎

React 元件從建立到銷毀會經歷多個階段，稱為生命週期。

[程式檔案：10-1-lifecycle-basic.jsx](../_code/10/10-1-lifecycle-basic.jsx)

```jsx
import React, { Component } from 'react';

class LifecycleDemo extends Component {
  constructor(props) {
    super(props);
    this.state = { message: 'Component Created' };
  }

  render() {
    return <p>{this.state.message}</p>;
  }
}

export default LifecycleDemo;
```

**生命週期階段：**
1. **Mounting**：元件被建立並加入 DOM
2. **Updating**：元件因 props 或 state 變化而更新
3. **Unmounting**：元件從 DOM 移除

## 10.2 掛載階段

元件掛載時執行的鉤子方法。

[程式檔案：10-2-component-mount.jsx](../_code/10/10-2-component-mount.jsx)

```jsx
import React, { Component } from 'react';

class MountDemo extends Component {
  constructor(props) {
    super(props);
    console.log('1. Constructor');
  }

  componentDidMount() {
    console.log('3. Component Did Mount');
    this.setState({ mounted: true });
  }

  render() {
    console.log('2. Render');
    return <p>Component Mounted!</p>;
  }
}

export default MountDemo;
```

**掛載階段順序：**
1. `constructor()` - 初始化
2. `render()` - 渲染
3. `componentDidMount()` - DOM 已準備好

## 10.3 更新階段

元件更新時執行的方法。

[程式檔案：10-3-component-update.jsx](../_code/10/10-3-component-update.jsx)

```jsx
import React, { Component } from 'react';

class UpdateDemo extends Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }

  componentDidUpdate(prevProps, prevState) {
    console.log('Component Updated!');
    console.log('Previous state:', prevState.count);
    console.log('Current state:', this.state.count);
  }

  increment = () => {
    this.setState({ count: this.state.count + 1 });
  };

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={this.increment}>Increment</button>
      </div>
    );
  }
}

export default UpdateDemo;
```

## 10.4 卸載階段

元件卸載時的清理工作。

[程式檔案：10-4-component-unmount.jsx](../_code/10/10-4-component-unmount.jsx)

```jsx
import React, { Component } from 'react';

class UnmountDemo extends Component {
  componentWillUnmount() {
    console.log('Component Will Unmount - Cleanup!');
  }

  render() {
    return <p>Component will unmount soon...</p>;
  }
}

export default UnmountDemo;
```

**常見清理工作：**
- 取消計時器
- 移除事件監聽
- 取消網路請求
- 清除計數器

## 10.5 建構函數

建構函數用於初始化狀態和綁定方法。

[程式檔案：10-5-constructor.jsx](../_code/10/10-5-constructor.jsx)

```jsx
import React, { Component } from 'react';

class ConstructorDemo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: props.initialName || 'Guest',
      count: 0
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.setState({ count: this.state.count + 1 });
  }

  render() {
    return (
      <div>
        <h1>Hello, {this.state.name}</h1>
        <p>Count: {this.state.count}</p>
        <button onClick={this.handleClick}>Click</button>
      </div>
    );
  }
}

export default ConstructorDemo;
```

## 10.6 Render 方法

render 是類別元件唯一必需的方法。

[程式檔案：10-6-render-method.jsx](../_code/10/10-6-render-method.jsx)

```jsx
import React, { Component } from 'react';

class RenderDemo extends Component {
  state = { showContent: true };

  toggleContent = () => {
    this.setState({ showContent: !this.state.showContent });
  };

  render() {
    return (
      <div>
        <button onClick={this.toggleContent}>Toggle</button>
        {this.state.showContent && <p>Content is visible!</p>}
      </div>
    );
  }
}

export default RenderDemo;
```

**render 注意事項：**
- 必須回傳 JSX
- 應該是純函數（不修改 state）
- 可回傳 null、false 或陣列

## 10.7 ComponentDidMount

用於初始化操作，如網路請求和 DOM 操作。

[程式檔案：10-7-component-did-mount.jsx](../_code/10/10-7-component-did-mount.jsx)

```jsx
import React, { Component } from 'react';

class DidMountDemo extends Component {
  constructor(props) {
    super(props);
    this.state = { data: null };
  }

  componentDidMount() {
    fetch('https://api.example.com/data')
      .then(res => res.json())
      .then(data => this.setState({ data }));
  }

  render() {
    return <p>Data: {this.state.data || 'Loading...'}</p>;
  }
}

export default DidMountDemo;
```

## 10.8 ComponentDidUpdate

用於回應 props 或 state 的變化。

[程式檔案：10-8-component-did-update.jsx](../_code/10/10-8-component-did-update.jsx)

```jsx
import React, { Component } from 'react';

class DidUpdateDemo extends Component {
  constructor(props) {
    super(props);
    this.state = { value: '' };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.inputValue !== this.props.inputValue) {
      console.log('Input value changed!');
    }
  }

  render() {
    return <input value={this.props.inputValue} readOnly />;
  }
}

export default DidUpdateDemo;
```

## 10.9 ComponentWillUnmount

用於清理訂閱和計時器。

[程式檔案：10-9-component-will-unmount.jsx](../_code/10/10-9-component-will-unmount.jsx)

```jsx
import React, { Component } from 'react';

class WillUnmountDemo extends Component {
  constructor(props) {
    super(props);
    this.timerID = null;
  }

  componentDidMount() {
    this.timerID = setInterval(() => {
      console.log('Timer running...');
    }, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
    console.log('Timer stopped!');
  }

  render() {
    return <p>Timer active...</p>;
  }
}

export default WillUnmountDemo;
```

## 10.10 元件組合

元件可以組合其他元件來建立複雜 UI。

[程式檔案：10-10-composition.jsx](../_code/10/10-10-composition.jsx)

```jsx
import React from 'react';

const Header = () => <header><h1>My App</h1></header>;

const Content = () => <main><p>Main content</p></main>;

const Footer = () => <footer><p>Footer</p></footer>;

const App = () => (
  <div>
    <Header />
    <Content />
    <Footer />
  </div>
);

export default App;
```

**組合模式：**
- `children` prop
- Slot（插槽）模式
- 渲染 prop

## 重點回顧

| 概念 | 說明 |
|------|------|
| constructor | 初始化狀態和事件處理 |
| render | 回傳 JSX |
| componentDidMount | DOM 準備好後執行 |
| componentDidUpdate | 更新後執行 |
| componentWillUnmount | 卸載前清理 |
| 組合 | 元件嵌套形成 UI |

## 練習題

1. 建立一個時鐘元件，顯示當前時間
2. 實作一個資料載入元件，顯示 loading 和錯誤狀態
3. 建立一個表單元件，處理輸入變化
4. 實作一個延遲卸載的確認對話框
