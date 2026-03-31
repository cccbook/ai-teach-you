# 第 4 章：JavaScript 基礎

## 概述

JavaScript 是網頁開發的核心語言，用於為網頁添加互動功能。本章介紹 JavaScript 的基本語法、資料類型、運算子和控制流程。

## 4.1 第一個 JavaScript

讓我們從最簡單的 JavaScript 程式碼開始。

[程式檔案：04-1-hello.js](../_code/04/04-1-hello.js)

```javascript
console.log("Hello, World!");

document.write("<h1>Hello, JavaScript!</h1>");

alert("歡迎來到 JavaScript 世界！");
```

## 4.2 變數宣告

JavaScript 使用 `var`、`let` 和 `const` 宣告變數。

[程式檔案：04-2-variables.js](../_code/04/04-2-variables.js)

```javascript
// var：函數作用域，可以重新宣告
var name1 = "張三";
var name1 = "李四";

// let：區塊作用域，可以重新賦值
let age = 25;
age = 26;

// const：區塊作用域，不能重新賦值
const PI = 3.14159;
// PI = 3; // 錯誤：不能重新賦值

// 變數命名規則
let _private = "私有變數";
let $element = "DOM 元素";
let camelCase = "駝峰式命名";
```

## 4.3 資料類型

JavaScript 有七種原始資料類型和 Object。

[程式檔案：04-3-data-types.js](../_code/04/04-3-data-types.js)

```javascript
// 原始類型 (Primitives)
let string = "字串";           // 字串
let number = 42;               // 數字
let float = 3.14;              // 浮點數
let boolean = true;            // 布林值
let empty = null;             // 空值
let notDefined;                // 未定義
let symbol = Symbol("id");     // 符號
let bigInt = 9007199254740991n; // 大整數

// Object
let array = [1, 2, 3];        // 陣列
let object = { key: "value" }; // 物件
let func = function() {};      // 函數

// 類型檢查
console.log(typeof string);   // "string"
console.log(typeof number);    // "number"
console.log(typeof boolean);   // "boolean"
console.log(typeof array);     // "object"
console.log(typeof null);      // "object" (歷史bug)
```

## 4.4 運算子

JavaScript 支援多種運算子進行各種運算。

[程式檔案：04-4-operators.js](../_code/04/04-4-operators.js)

```javascript
// 算術運算子
let a = 10, b = 3;
console.log(a + b);   // 13
console.log(a - b);   // 7
console.log(a * b);   // 30
console.log(a / b);   // 3.333...
console.log(a % b);   // 1 (餘數)
console.log(a ** b);  // 1000 (次方)

// 比較運算子
console.log(5 == "5");   // true (鬆散相等)
console.log(5 === "5");  // false (嚴格相等)
console.log(5 != "5");   // false
console.log(5 !== "5");  // true
console.log(5 > 3);      // true
console.log(5 >= 5);    // true

// 邏輯運算子
console.log(true && false);  // false
console.log(true || false);  // true
console.log(!true);          // false

// 三元運算子
let status = age >= 18 ? "成人" : "未成年";

// 空值合併運算子
let value = null ?? "預設值";  // "預設值"
```

## 4.5 條件判斷

使用 `if...else` 進行條件判斷。

[程式檔案：04-5-if-else.js](../_code/04/04-5-if-else.js)

```javascript
let score = 85;

if (score >= 90) {
    console.log("優等");
} else if (score >= 80) {
    console.log("甲等");
} else if (score >= 70) {
    console.log("乙等");
} else if (score >= 60) {
    console.log("丙等");
} else {
    console.log("不及格");
}

// 巢狀 if
let age = 20;
let hasTicket = true;

if (age >= 18) {
    if (hasTicket) {
        console.log("可以進場");
    } else {
        console.log("需要門票");
    }
} else {
    console.log("未滿十八歲");
}

// 簡化寫法
hasTicket && age >= 18 && console.log("可以進場");
```

## 4.6 switch 語句

當有多個條件時，`switch` 比 `if...else if` 更清晰。

[程式檔案：04-6-switch.js](../_code/04/04-6-switch.js)

```javascript
let day = new Date().getDay();
let dayName;

switch (day) {
    case 0:
        dayName = "星期日";
        break;
    case 1:
        dayName = "星期一";
        break;
    case 2:
        dayName = "星期二";
        break;
    case 3:
        dayName = "星期三";
        break;
    case 4:
        dayName = "星期四";
        break;
    case 5:
        dayName = "星期五";
        break;
    case 6:
        dayName = "星期六";
        break;
    default:
        dayName = "無效日期";
}

// 多個 case 合併
let grade = "B";

switch (grade) {
    case "A":
    case "B":
    case "C":
        console.log("及格");
        break;
    case "D":
    case "F":
        console.log("不及格");
        break;
    default:
        console.log("無效成績");
}
```

## 4.7 for 迴圈

`for` 迴圈用於已知執行次數的場景。

[程式檔案：04-7-for-loop.js](../_code/04/04-7-for-loop.js)

```javascript
// 基本 for 迴圈
for (let i = 0; i < 5; i++) {
    console.log("Iteration:", i);
}

// for...of（遍歷陣列）
const fruits = ["蘋果", "香蕉", "橘子"];
for (const fruit of fruits) {
    console.log(fruit);
}

// for...in（遍歷物件屬性）
const person = { name: "王小明", age: 25, city: "台北" };
for (const key in person) {
    console.log(`${key}: ${person[key]}`);
}

// forEach
fruits.forEach((fruit, index) => {
    console.log(`${index}: ${fruit}`);
});

// 計算 1 到 100 的總和
let sum = 0;
for (let i = 1; i <= 100; i++) {
    sum += i;
}
console.log("總和:", sum);

// 找出陣列中的最大值
const numbers = [5, 10, 2, 8, 15];
let max = numbers[0];
for (let i = 1; i < numbers.length; i++) {
    if (numbers[i] > max) {
        max = numbers[i];
    }
}
console.log("最大值:", max);
```

## 4.8 while 迴圈

當條件為真時重複執行，適合未知執行次數的場景。

[程式檔案：04-8-while-loop.js](../_code/04/04-8-while-loop.js)

```javascript
// 基本 while 迴圈
let count = 0;
while (count < 5) {
    console.log("Count:", count);
    count++;
}

// do...while（至少執行一次）
let num = 0;
do {
    console.log("至少執行一次");
    num++;
} while (num < 0);

// 無限迴圈 + break
let i = 0;
while (true) {
    console.log(i);
    if (i >= 10) break;
    i++;
}

// continue 跳過本次迭代
for (let i = 0; i < 5; i++) {
    if (i === 2) continue;
    console.log(i);
}

// 計算位數
let n = 12345;
let digits = 0;
while (n > 0) {
    digits++;
    n = Math.floor(n / 10);
}
console.log("位數:", digits);
```

## 4.9 陣列基礎

陣列用於儲存多個值，是 JavaScript 中重要的資料結構。

[程式檔案：04-9-array-basic.js](../_code/04/04-9-array-basic.js)

```javascript
// 建立陣列
const fruits = ["蘋果", "香蕉", "橘子"];
const numbers = new Array(1, 2, 3, 4, 5);
const mixed = [1, "文字", true, null, { key: "value" }];

// 存取元素
console.log(fruits[0]);     // "蘋果"
console.log(fruits[fruits.length - 1]); // "橘子"

// 修改元素
fruits[1] = "葡萄";

// 常用方法
fruits.push("草莓");         // 末端新增
fruits.unshift("西瓜");      // 開頭新增
fruits.pop();                // 末端刪除
fruits.shift();              // 開頭刪除
fruits.splice(1, 1);         // 刪除指定位置

// 搜尋
console.log(fruits.indexOf("蘋果"));  // 0
console.log(fruits.includes("香蕉")); // true

// 合併與切片
const arr1 = [1, 2];
const arr2 = [3, 4];
const merged = arr1.concat(arr2);     // [1, 2, 3, 4]
const sliced = merged.slice(1, 3);     // [2, 3]

// 轉字串
console.log(fruits.join(", "));
```

## 4.10 物件基礎

物件用於儲存鍵值對，是 JavaScript 的核心概念。

[程式檔案：04-10-object-basic.js](../_code/04/04-10-object-basic.js)

```javascript
// 建立物件
const person = {
    name: "王小明",
    age: 25,
    city: "台北",
    hobbies: ["閱讀", "游泳"],
    address: {
        street: "中山路",
        number: 123
    }
};

// 存取屬性
console.log(person.name);           // "王小明"
console.log(person["age"]);         // 25
console.log(person.address.street); // "中山路"

// 新增/修改屬性
person.email = "wang@example.com";
person["phone"] = "0912345678";

// 刪除屬性
delete person.city;

// 方法
person.greet = function() {
    return `你好，我是 ${this.name}！`;
};
console.log(person.greet());

// Object.keys / values / entries
console.log(Object.keys(person));    // ["name", "age", ...]
console.log(Object.values(person));  // ["王小明", 25, ...]
console.log(Object.entries(person)); // [["name", "王小明"], ...]

// 解構賦值
const { name, age } = person;
console.log(name, age);
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| var/let/const | 變數宣告方式，const 不能重新賦值 |
| 資料類型 | string, number, boolean, null, undefined, symbol, bigint, object |
| 運算子 | 算術、比較、邏輯、三元 |
| if/switch | 條件判斷 |
| for/while | 迴圈控制 |
| 陣列 | 有序集合，常用方法 push, pop, slice, map |
| 物件 | 鍵值對儲存 |

## 練習題

1. 計算 BMI 並判斷體位（過輕/正常/過重/肥胖）
2. 找出陣列中的最大值和最小值
3. 實作一個簡單的待辦事項清單（使用陣列）
4. 將物件轉換為 URL 查詢字串
