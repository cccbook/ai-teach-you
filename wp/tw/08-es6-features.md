# 第 8 章：ES6 新特性

## 概述

ES6（ECMAScript 2015）引入了許多革命性的新特性，讓 JavaScript 更加強大和優雅。本章介紹最實用的 ES6+ 語法。

## 8.1 解構賦值

從陣列或物件中提取值，成為獨立變數。

[程式檔案：08-1-destructuring.js](../_code/08/08-1-destructuring.js)

```javascript
// 陣列解構
const [a, b, c] = [1, 2, 3];
console.log(a, b, c); // 1 2 3

// 跳過元素
const [first, , third] = [1, 2, 3];
console.log(first, third); // 1 3

// 其餘元素
const [head, ...rest] = [1, 2, 3, 4, 5];
console.log(head, rest); // 1 [2, 3, 4, 5]

// 預設值
const [x = 10, y = 20] = [5];
console.log(x, y); // 5 20

// 交換變數
let a = 1, b = 2;
[a, b] = [b, a];
console.log(a, b); // 2 1

// 物件解構
const { name, age } = { name: "王小明", age: 25 };
console.log(name, age); // "王小明" 25

// 重新命名
const { name: userName, age: userAge } = { name: "陳小美", age: 30 };

// 巢狀解構
const { address: { city } } = { name: "林大明", address: { city: "台北" } };

// 函數參數解構
function greet({ name, age }) {
    return `你好，我是 ${name}，${age} 歲`;
}

console.log(greet({ name: "王小明", age: 25 }));

// 練習：解析 API 回應
const response = {
    data: {
        user: {
            name: "用戶",
            email: "user@example.com"
        }
    },
    status: 200
};

const { data: { user: { name, email } }, status } = response;
console.log(name, email, status);
```

## 8.2 展開運算子

使用 `...` 展開可迭代物件。

[程式檔案：08-2-spread-operator.js](../_code/08/08-2-spread-operator.js)

```javascript
// 陣列展開
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];
console.log(combined); // [1, 2, 3, 4, 5, 6]

// 複製陣列
const original = [1, 2, 3];
const copy = [...original];

// 函數參數
const numbers = [1, 2, 3, 4, 5];
const max = Math.max(...numbers);
console.log(max); // 5

// 物件展開（淺拷貝）
const obj1 = { a: 1, b: 2 };
const obj2 = { c: 3, d: 4 };
const mergedObj = { ...obj1, ...obj2 };

// 覆寫屬性
const defaults = { theme: "light", lang: "zh-TW" };
const userPrefs = { lang: "en", fontSize: 14 };
const settings = { ...defaults, ...userPrefs };

// 練習：合併設定檔
const defaultConfig = {
    apiUrl: "https://api.example.com",
    timeout: 5000,
    retries: 3
};

const envConfig = {
    apiUrl: "https://dev.example.com",
    debug: true
};

const config = { ...defaultConfig, ...envConfig };

// 練習：不可變更新
const state = { items: [1, 2, 3], count: 3 };

const addItem = (newItem) => ({
    ...state,
    items: [...state.items, newItem],
    count: state.count + 1
});

const newState = addItem(4);
console.log(state);     // 不變
console.log(newState); // 新狀態
```

## 8.3 模板字串

使用反引號定義字串，支援插值和多行。

[程式檔案：08-3-template-literal.js](../_code/08/08-3-template-literal.js)

```javascript
// 基本用法
const name = "王小明";
const greeting = `你好，${name}！`;
console.log(greeting); // "你好，王小明！"

// 多行字串
const html = `
    <div>
        <h1>標題</h1>
        <p>內容</p>
    </div>
`;

// 運算式
const a = 10, b = 20;
console.log(`${a} + ${b} = ${a + b}`); // "10 + 20 = 30"

// 函數呼叫
const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);
console.log(`${capitalize("hello")} World`);

// 巢狀三元
const status = "active";
console.log(`狀態: ${status === "active" ? "啟用" : "停用"}`);

// 練習：產生 HTML
const user = { name: "王小明", email: "wang@example.com" };

const card = `
    <div class="user-card">
        <h2>${user.name}</h2>
        <p>${user.email}</p>
    </div>
`;

// 練習：標籤模板
function highlight(strings, ...values) {
    return strings.reduce((result, str, i) => {
        const value = values[i] ? `<mark>${values[i]}</mark>` : "";
        return result + str + value;
    }, "");
}

const name = "JavaScript";
const result = highlight`學習 ${name} 很有趣！`;
console.log(result);
```

## 8.4 模組化

使用 export 和 import 組織程式碼。

[程式檔案：08-4-modules.js](../_code/08/08-4-modules.js)

```javascript
// ===== math.js =====
// 命名導出
export const PI = 3.14159;

export function add(a, b) {
    return a + b;
}

export function multiply(a, b) {
    return a * b;
}

// 預設導出
export default class Calculator {
    add(a, b) { return a + b; }
}

// ===== main.js =====
// 導入命名導出
import { PI, add, multiply } from "./math.js";

console.log(PI);           // 3.14159
console.log(add(1, 2));    // 3
console.log(multiply(3, 4)); // 12

// 導入預設導出
import Calculator from "./math.js";

// 重新命名導入
import { add as sum } from "./math.js";
console.log(sum(1, 2));

// 導入全部
import * as math from "./math.js";
console.log(math.PI);
console.log(math.add(1, 2));

// ===== utils.js =====
// 重新導出
export { add, multiply } from "./math.js";
export { default as Calc } from "./math.js";

// ===== index.js =====
// 使用 index 模組
import { add } from "./utils.js";
import { Calc } from "./utils.js";

// 練習：工具模組
// config.js
export const API_URL = "https://api.example.com";
export const TIMEOUT = 5000;

// users.js
import { API_URL, TIMEOUT } from "./config.js";

export async function fetchUsers() {
    const response = await fetch(API_URL + "/users", {
        timeout: TIMEOUT
    });
    return response.json();
}
```

## 8.5 預設參數

為函數參數設定預設值。

[程式檔案：08-5-default-parameters.js](../_code/08/08-5-default-parameters.js)

```javascript
// 基本預設參數
function greet(name = "訪客") {
    return `你好，${name}！`;
}

console.log(greet());            // "你好，訪客！"
console.log(greet("王小明"));    // "你好，王小明！"

// 多個預設參數
function createUser(name, age = 18, role = "user") {
    return { name, age, role };
}

console.log(createUser("王小明"));
// { name: "王小明", age: 18, role: "user" }

// 預設參數可以是表達式
function getDiscountedPrice(price, discount = price * 0.1) {
    return price - discount;
}

// 預設參數可以在前面使用後面的參數
function greet(name = "訪客", greeting = `你好，${name}`) {
    return greeting;
}

console.log(greet());                  // "你好，訪客"
console.log(greet("王小明"));         // "你好，王小明"
console.log(greet(undefined, "哈囉")); // "哈囉"

// 解構預設值
function process({ id = 0, name = "Unknown", data = {} }) {
    return { id, name, data };
}

// 練習：設定選項物件
function fetchData(url, options = {}) {
    const {
        method = "GET",
        headers = {},
        timeout = 5000
    } = options;
    
    return fetch(url, { method, headers });
}
```

## 8.6 Rest 參數

使用 `...` 收集剩餘參數為陣列。

[程式檔案：08-6-rest-parameters.js](../_code/08/08-6-rest-parameters.js)

```javascript
// 基本 rest 參數
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}

console.log(sum(1, 2, 3, 4, 5)); // 15

// 搭配一般參數
function multiply(factor, ...numbers) {
    return numbers.map(n => n * factor);
}

console.log(multiply(2, 1, 2, 3)); // [2, 4, 6]

// 其餘參數收集
const [first, ...rest] = [1, 2, 3, 4, 5];
console.log(first); // 1
console.log(rest);  // [2, 3, 4, 5]

// 練習：除最後一個外的所有參數
function join(separator, ...values) {
    return values.join(separator);
}

console.log(join(", ", "甲", "乙", "丙")); // "甲, 乙, 丙"

// 練習：遞迴收集
function flatten(array) {
    const result = [];
    
    function flat(arr) {
        for (const item of arr) {
            if (Array.isArray(item)) {
                flat(item);
            } else {
                result.push(item);
            }
        }
    }
    
    flat(array);
    return result;
}

console.log(flatten([1, [2, 3], [[4], 5]])); // [1, 2, 3, 4, 5]

// 練習：log 函數
function log(level, ...messages) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${level}]`, ...messages);
}

log("INFO", "伺服器啟動");
log("ERROR", "連線失敗", "192.168.1.1");
```

## 8.7 Map 集合

Map 是鍵值對的集合，鍵可以是任意類型。

[程式檔案：08-7-map.js](../_code/08/08-7-map.js)

```javascript
// 建立 Map
const map = new Map();

// 設定值
map.set("name", "王小明");
map.set(1, "數字鍵");
map.set(true, "布林鍵");
map.set({ id: 1 }, "物件鍵");

// 取得值
console.log(map.get("name")); // "王小明"
console.log(map.get(1));       // "數字鍵"
console.log(map.get({ id: 1 })); // undefined（新物件）

// 檢查鍵是否存在
console.log(map.has("name")); // true

// 刪除
map.delete("name");
console.log(map.has("name")); // false

// 大小
console.log(map.size); // 3

// 迭代
for (const [key, value] of map) {
    console.log(`${key}: ${value}`);
}

// keys, values, entries
console.log([...map.keys()]);
console.log([...map.values()]);
console.log([...map.entries()]);

// 練習：計數
const countOccurrences = (array) => {
    const count = new Map();
    
    for (const item of array) {
        count.set(item, (count.get(item) || 0) + 1);
    }
    
    return count;
};

const items = ["a", "b", "a", "c", "b", "a"];
console.log(countOccurrences(items));
// Map { 'a' => 3, 'b' => 2, 'c' => 1 }

// 練習：快取
const cache = new Map();

function fetchData(key) {
    if (cache.has(key)) {
        console.log("使用快取");
        return cache.get(key);
    }
    
    const data = "expensive operation result";
    cache.set(key, data);
    return data;
}
```

## 8.8 Set 集合

Set 是唯一值的集合。

[程式檔案：08-8-set.js](../_code/08/08-8-set.js)

```javascript
// 建立 Set
const set = new Set();

// 新增值
set.add(1);
set.add(2);
set.add(3);
set.add(1); // 重複，會被忽略

console.log(set.size); // 3

// 檢查是否存在
console.log(set.has(2)); // true
console.log(set.has(5)); // false

// 刪除
set.delete(2);

// 迭代
for (const item of set) {
    console.log(item);
}

// 常用方法
console.log([...set]);           // 轉為陣列
set.forEach(value => console.log(value));

// 練習：去除重複
const array = [1, 2, 3, 2, 1, 4, 3];
const unique = [...new Set(array)];
console.log(unique); // [1, 2, 3, 4]

// 練習：交集
const set1 = new Set([1, 2, 3, 4]);
const set2 = new Set([3, 4, 5, 6]);

const intersection = new Set([...set1].filter(x => set2.has(x)));
console.log([...intersection]); // [3, 4]

// 練習：聯集
const union = new Set([...set1, ...set2]);
console.log([...union]); // [1, 2, 3, 4, 5, 6]

// 練習：差集
const difference = new Set([...set1].filter(x => !set2.has(x)));
console.log([...difference]); // [1, 2]
```

## 8.9 Symbol

Symbol 是唯一且不可改變的原始值，用於建立唯一屬性鍵。

[程式檔案：08-9-symbol.js](../_code/08/08-9-symbol.js)

```javascript
// 建立 Symbol
const sym1 = Symbol();
const sym2 = Symbol("description");
const sym3 = Symbol("description");

console.log(sym2 === sym3); // false（每個 Symbol 都唯一）

// 作為屬性鍵
const obj = {
    [Symbol("name")]: "王小明",
    [Symbol("age")]: 25
};

// 取得所有 Symbol 屬性
const symbols = Object.getOwnPropertySymbols(obj);
console.log(symbols);

// 練習：定義私有屬性
const createCounter = () => {
    const countSymbol = Symbol("count");
    
    return {
        [countSymbol]: 0,
        increment() {
            this[countSymbol]++;
        },
        getCount() {
            return this[countSymbol];
        }
    };
};

const counter = createCounter();
console.log(Object.keys(counter)); // []（無法看到 countSymbol）
counter.increment();
console.log(counter.getCount()); // 1

// 練習：避免屬性衝突
const RED = Symbol("red");
const GREEN = Symbol("green");
const BLUE = Symbol("blue");

const colors = {
    [RED]: "#FF0000",
    [GREEN]: "#00FF00",
    [BLUE]: "#0000FF"
};

// Symbol.for 全域符號表
const globalSym = Symbol.for("app.name");
const sameSym = Symbol.for("app.name");
console.log(globalSym === sameSym); // true
```

## 8.10 迭代器

迭代器提供統一的遍歷介面。

[程式檔案：08-10-iterator.js](../_code/08/08-10-iterator.js)

```javascript
// 可迭代物件
// Array, String, Map, Set, NodeList 等都是可迭代的

// 手動迭代
const arr = [1, 2, 3];
const iterator = arr[Symbol.iterator]();

console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: 2, done: false }
console.log(iterator.next()); // { value: 3, done: false }
console.log(iterator.next()); // { value: undefined, done: true }

// 自訂可迭代物件
const range = {
    from: 1,
    to: 5,
    
    [Symbol.iterator]() {
        let current = this.from;
        const last = this.to;
        
        return {
            next() {
                if (current <= last) {
                    return { value: current++, done: false };
                }
                return { value: undefined, done: true };
            }
        };
    }
};

for (const num of range) {
    console.log(num); // 1, 2, 3, 4, 5
}

// 練習：產生費波那契數列
const fibonacci = {
    [Symbol.iterator]() {
        let a = 0, b = 1;
        
        return {
            next() {
                const value = a;
                [a, b] = [b, a + b];
                return { value, done: false };
            }
        };
    }
};

const fib10 = [...fibonacci].slice(0, 10);
console.log(fib10); // [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

// 練習：無限迭代器
const random = {
    [Symbol.iterator]() {
        return {
            next() {
                return {
                    value: Math.random(),
                    done: false
                };
            }
        };
    }
};

// 練習：生成器
function* generator() {
    yield 1;
    yield 2;
    yield 3;
}

const gen = generator();
console.log(gen.next().value); // 1
console.log(gen.next().value); // 2
console.log(gen.next().value); // 3
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| 解構賦值 | 從陣列/物件提取值 |
| 展開運算子 | `...` 展開可迭代物件 |
| 模板字串 | 反引號字串支援插值 |
| 模組化 | export/import 組織程式碼 |
| 預設參數 | 參數預設值 |
| Rest 參數 | 收集剩餘參數 |
| Map/Set | 鍵值集合/唯一值集合 |
| Symbol | 唯一屬性鍵 |
| 迭代器 | 統一遍歷介面 |

## 練習題

1. 使用解構交換兩個變數
2. 實作一個不可變的更新函數
3. 建立一個 Symbol 私有屬性系統
4. 實作一個自訂可迭代物件
