# 第 5 章：函數與物件

## 概述

函數是 JavaScript 的核心 building block，支援多種定義方式。物件導向程式設計則透過類別和原型鏈實現。本章深入探討函數、閉包、原型以及類別繼承。

## 5.1 函數宣告

函數宣告是最傳統的函數定義方式，會被提升（hoisting）。

[程式檔案：05-1-function-declare.js](../_code/05/05-1-function-declare.js)

```javascript
// 函數宣告
function greet(name) {
    return `你好，${name}！`;
}

console.log(greet("王小明"));

// 函數提升
console.log(add(2, 3)); // 5，可以在定義前呼叫

function add(a, b) {
    return a + b;
}

// 多個參數
function sum(...numbers) {
    let total = 0;
    for (const num of numbers) {
        total += num;
    }
    return total;
}

console.log(sum(1, 2, 3, 4, 5)); // 15
```

## 5.2 函數表達式

將函數賦值給變數，適用於回調函數。

[程式檔案：05-2-function-expression.js](../_code/05/05-2-function-expression.js)

```javascript
// 函數表達式
const multiply = function(a, b) {
    return a * b;
};

console.log(multiply(3, 4)); // 12

// 匿名函數作為回調
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(function(n) {
    return n * 2;
});

console.log(doubled); // [2, 4, 6, 8, 10]

// 具名函數表達式
const factorial = function fact(n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
};

console.log(factorial(5)); // 120
```

## 5.3 箭頭函數

ES6 引入的簡潔函數語法。

[程式檔案：05-3-arrow-function.js](../_code/05/05-3-arrow-function.js)

```javascript
// 基本語法
const add = (a, b) => a + b;
console.log(add(2, 3)); // 5

// 單一參數可省略括號
const square = n => n * n;
console.log(square(4)); // 16

// 多行程式碼需要 return
const greet = name => {
    const message = `你好，${name}！`;
    return message;
};

// 在陣列方法中使用
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
const sum = numbers.reduce((acc, n) => acc + n, 0);

console.log(doubled); // [2, 4, 6, 8, 10]
console.log(evens);   // [2, 4]
console.log(sum);     // 15

// 箭頭函數沒有自己的 this
const counter = {
    count: 0,
    increment: () => {
        this.count++;
    }
};

// 比較：傳統函數有自己的 this
const counter2 = {
    count: 0,
    increment: function() {
        this.count++;
    }
};
```

## 5.4 參數與回傳值

函數可以接受參數並回傳值。

[程式檔案：05-4-parameters.js](../_code/05/05-4-parameters.js)

```javascript
// 預設參數
function greet(name = "訪客", greeting = "你好") {
    return `${greeting}，${name}！`;
}

console.log(greet());                    // "你好，訪客！"
console.log(greet("小明"));              // "你好，小明！"
console.log(greet("小明", "哈囉"));     // "哈囉，小明！"

// arguments 物件（傳統函數）
function sumAll() {
    let total = 0;
    for (let i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    return total;
}

console.log(sumAll(1, 2, 3, 4, 5)); // 15

// 展開運算子
function sum(...nums) {
    return nums.reduce((a, b) => a + b, 0);
}

console.log(sum(1, 2, 3)); // 6

// 立即執行函數 (IIFE)
(function() {
    const message = "我會立即執行";
    console.log(message);
})();

// 回傳函數
function createMultiplier(factor) {
    return function(number) {
        return number * factor;
    };
}

const double = createMultiplier(2);
const triple = createMultiplier(3);

console.log(double(5));  // 10
console.log(triple(5));  // 15
```

## 5.5 作用域

JavaScript 使用詞法作用域，變數的可訪問性由其在程式碼中的位置決定。

[程式檔案：05-5-scope.js](../_code/05/05-5-scope.js)

```javascript
// 全域作用域
const globalVar = "我在全域";

function outer() {
    // 區塊作用域
    const outerVar = "我在 outer";
    
    function inner() {
        // 巢狀作用域
        const innerVar = "我在 inner";
        
        console.log(globalVar);   // 可訪問
        console.log(outerVar);    // 可訪問
        console.log(innerVar);    // 可訪問
    }
    
    console.log(innerVar);        // 錯誤：innerVar 未定義
}

console.log(outerVar);            // 錯誤：outerVar 未定義

// var 的函數作用域
function varScope() {
    if (true) {
        var functionVar = "函數作用域";
    }
    console.log(functionVar);     // "函數作用域"
}

// let/const 的區塊作用域
function letScope() {
    if (true) {
        let blockVar = "區塊作用域";
        const constVar = "也是區塊作用域";
    }
    console.log(blockVar);        // 錯誤：blockVar 未定義
}
```

## 5.6 閉包

閉包是 JavaScript 強大的特性，允許函數訪問其外部作用域的變數。

[程式檔案：05-6-closure.js](../_code/05/05-6-closure.js)

```javascript
// 經典閉包範例
function createCounter() {
    let count = 0;
    
    return function() {
        count++;
        return count;
    };
}

const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3

// 私有變數
function createBankAccount(initialBalance) {
    let balance = initialBalance;
    
    return {
        deposit: function(amount) {
            balance += amount;
            return balance;
        },
        withdraw: function(amount) {
            if (amount <= balance) {
                balance -= amount;
                return balance;
            }
            return "餘額不足";
        },
        getBalance: function() {
            return balance;
        }
    };
}

const account = createBankAccount(1000);
console.log(account.getBalance()); // 1000
console.log(account.deposit(500)); // 1500
console.log(account.withdraw(200)); // 1300

// 計時器中的閉包
function createTimer() {
    let time = 0;
    
    setInterval(function() {
        time++;
        console.log(time);
    }, 1000);
}

// 工廠函數
function multiply(factor) {
    return function(number) {
        return number * factor;
    };
}

const multiplyBy2 = multiply(2);
const multiplyBy10 = multiply(10);

console.log(multiplyBy2(5));  // 10
console.log(multiplyBy10(5)); // 50
```

## 5.7 物件建立

JavaScript 提供多種建立物件的方式。

[程式檔案：05-7-object-create.js](../_code/05/05-7-object-create.js)

```javascript
// 物件字面量
const person1 = {
    name: "王小明",
    age: 25,
    greet: function() {
        return `你好，我是 ${this.name}`;
    }
};

// Object.create()
const personProto = {
    greet: function() {
        return `你好，我是 ${this.name}`;
    }
};

const person2 = Object.create(personProto);
person2.name = "陳小美";
person2.age = 30;

// 建構函數
function Person(name, age) {
    this.name = name;
    this.age = age;
}

Person.prototype.greet = function() {
    return `你好，我是 ${this.name}`;
};

const person3 = new Person("林大雄", 28);

// new 的過程
function Person(name, age) {
    // 1. 建立空物件
    // const this = {};
    // 2. 設定原型
    // this.__proto__ = Person.prototype;
    // 3. 執行建構函數
    this.name = name;
    this.age = age;
    // 4. 回傳物件
    // return this;
}
```

## 5.8 物件方法

物件可以包含方法來操作其資料。

[程式檔案：05-8-object-method.js](../_code/05/05-8-object-method.js)

```javascript
const calculator = {
    a: 0,
    b: 0,
    setValues: function(x, y) {
        this.a = x;
        this.b = y;
        return this; // 支援鏈式呼叫
    },
    add: function() {
        return this.a + this.b;
    },
    subtract: function() {
        return this.a - this.b;
    },
    multiply: function() {
        return this.a * this.b;
    },
    divide: function() {
        if (this.b === 0) {
            return "不能除以零";
        }
        return this.a / this.b;
    }
};

// 鏈式呼叫
const result = calculator
    .setValues(10, 5)
    .add();

console.log(result); // 15

// Getter 和 Setter
const person = {
    firstName: "王小",
    lastName: "明",
    get fullName() {
        return `${this.firstName}${this.lastName}`;
    },
    set fullName(name) {
        const parts = name.split("");
        this.firstName = parts[0];
        this.lastName = parts.slice(1).join("");
    }
};

console.log(person.fullName);    // "王小明"
person.fullName = "陳小美";
console.log(person.firstName);   // "陳"
console.log(person.lastName);    // "小美"
```

## 5.9 類別基礎

ES6 引入的 class 語法讓物件導向程式設計更直觀。

[程式檔案：05-9-class-basic.js](../_code/05/05-9-class-basic.js)

```javascript
class Person {
    // 建構函數
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    // 方法
    greet() {
        return `你好，我是 ${this.name}，今年 ${this.age} 歲`;
    }
    
    // Getter
    get info() {
        return `${this.name} - ${this.age}歲`;
    }
    
    // 靜態方法
    static create(name, age) {
        return new Person(name, age);
    }
}

const person = new Person("王小明", 25);
console.log(person.greet());        // "你好，我是王小明，今年25歲"
console.log(person.info);            // "王小明 - 25歲"

const person2 = Person.create("陳小美", 30);

// Private 欄位 (#)
class BankAccount {
    #balance = 0;
    
    constructor(initialBalance) {
        this.#balance = initialBalance;
    }
    
    deposit(amount) {
        this.#balance += amount;
        return this;
    }
    
    withdraw(amount) {
        if (amount <= this.#balance) {
            this.#balance -= amount;
            return this;
        }
        return "餘額不足";
    }
    
    getBalance() {
        return this.#balance;
    }
}

const account = new BankAccount(1000);
console.log(account.getBalance());   // 1000
// console.log(account.#balance);    // 語法錯誤
```

## 5.10 繼承

類別可以透過 extends 關鍵字繼承其他類別。

[程式檔案：05-10-inheritance.js](../_code/05/05-10-inheritance.js)

```javascript
// 父類別
class Animal {
    constructor(name) {
        this.name = name;
    }
    
    speak() {
        return `${this.name} 發出聲音`;
    }
    
    eat() {
        return `${this.name} 在吃東西`;
    }
}

// 子類別
class Dog extends Animal {
    constructor(name, breed) {
        super(name); // 呼叫父類別建構函數
        this.breed = breed;
    }
    
    speak() {
        return `${this.name} 汪汪叫`;
    }
    
    fetch() {
        return `${this.name} 在撿球`;
    }
}

class Cat extends Animal {
    constructor(name, color) {
        super(name);
        this.color = color;
    }
    
    speak() {
        return `${this.name} 喵喵叫`;
    }
    
    climb() {
        return `${this.name} 在爬樹`;
    }
}

const dog = new Dog("小白", "黃金獵犬");
const cat = new Cat("小咪", "橘色");

console.log(dog.speak());      // "小白汪汪叫"
console.log(dog.fetch());      // "小白在撿球"
console.log(dog.eat());        // "小白在吃東西"

console.log(cat.speak());      // "小咪喵喵叫"
console.log(cat.climb());      // "小咪在爬樹"

// instanceof
console.log(dog instanceof Dog);    // true
console.log(dog instanceof Animal);  // true
console.log(dog instanceof Cat);     // false
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| 函數宣告 | 會被提升，可用於回調 |
| 箭頭函數 | 簡潔語法，沒有自己的 this |
| 閉包 | 函數存取外部作用域變數 |
| 原型鏈 | 物件繼承屬性和方法 |
| class | ES6 物件導向語法 |
| extends | 類別繼承 |

## 練習題

1. 實作一個計算機類別（支援鏈式呼叫）
2. 創建一個私有變數的計時器類別
3. 實作一個形狀類別系統（矩形、圓形、三角形）
4. 使用閉包實作防抖（debounce）函數
