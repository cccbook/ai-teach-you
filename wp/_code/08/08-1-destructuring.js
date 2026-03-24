// 解構賦值

// 陣列解構
let [a, b, c] = [1, 2, 3];
console.log("Array:", a, b, c);

// 跳過元素
let [, , third] = [1, 2, 3];
console.log("Skip:", third);

// 預設值
let [x, y = 10] = [5];
console.log("Default:", x, y);

// 剩餘參數
let [head, ...tail] = [1, 2, 3, 4, 5];
console.log("Rest:", head, tail);

// 物件解構
let user = { name: "王小明", age: 25 };
let { name, age } = user;
console.log("Object:", name, age);

// 重新命名
let { name: userName, age: userAge } = user;
console.log("Rename:", userName, userAge);

// 預設值
let { city = "台北" } = user;
console.log("Default:", city);

// 巢狀解構
let data = {
    person: {
        firstName: "王",
        lastName: "小明"
    },
    age: 25
};

let { person: { firstName, lastName } } = data;
console.log("Nested:", firstName, lastName);

// 函數參數解構
function greet({ name, greeting = "Hello" }) {
    console.log(`${greeting}, ${name}!`);
}

greet({ name: "王小明", greeting: "Hi" });

// 多重解構
let arr = [1, 2, 3, 4, 5];
let [first, second, ...rest] = arr;
console.log("Multi:", first, second, rest);

// 交換變數
let p = 1, q = 2;
[p, q] = [q, p];
console.log("Swap:", p, q);

// 解構賦值與 Spread
let colors = ["red", "green", "blue", "yellow"];
let [primary, , tertiary] = colors;
console.log("Primary:", primary, "Tertiary:", tertiary);

// 忽略屬性
let obj = { a: 1, b: 2, c: 3 };
let { a, ...restObj } = obj;
console.log("Ignore:", a, restObj);