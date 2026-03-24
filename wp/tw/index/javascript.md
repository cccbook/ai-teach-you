# JavaScript

## 概述

JavaScript 是一種腳本語言，用於為網頁添加互動功能。它是 Web 開發的三大核心技術之一（HTML、CSS、JavaScript）。

## 歷史

- 1995 年：Brendan Eich 發明 JavaScript
- 1997 年：成為 ECMA 標準（ECMAScript）
- 2009 年：Node.js 發布
- 2015 年：ES6 重大更新

## 基本語法

### 變數

```javascript
var oldStyle = "已被取代";
let mutable = "可重新賦值";
const constant = "不可重新賦值";
```

### 資料類型

```javascript
// 原始類型
let str = "字串";
let num = 42;
let bool = true;
let empty = null;
let notDefined;
let sym = Symbol("id");
let bigInt = 9007199254740991n;

// 物件
let arr = [1, 2, 3];
let obj = { key: "value" };
```

### 函數

```javascript
// 函數宣告
function greet(name) {
    return `Hello, ${name}!`;
}

// 箭頭函數
const add = (a, b) => a + b;

// 函數表達式
const multiply = function(a, b) {
    return a * b;
};
```

## 非同步編程

```javascript
// Promise
fetch('/api/data')
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.error(err));

// async/await
async function loadData() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();
        return data;
    } catch (err) {
        console.error(err);
    }
}
```

## 模組化

```javascript
// 導出
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export default class Calculator { }

// 導入
import { PI, add } from './math.js';
import Calculator from './math.js';
```

## 參考資源

- [MDN JavaScript](https://developer.mozilla.org/zh-TW/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)
