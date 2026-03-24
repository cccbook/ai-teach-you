// 預設參數

// 基本預設參數
function greet(name = "Guest") {
    console.log(`Hello, ${name}!`);
}

greet(); // Hello, Guest!
greet("王小明"); // Hello, 王小明!

// 多個預設參數
function createUser(name = "Anonymous", age = 0, role = "user") {
    return { name, age, role };
}

console.log(createUser()); // { name: 'Anonymous', age: 0, role: 'user' }
console.log(createUser("小明", 25)); // { name: '小明', age: 25, role: 'user' }

// 表達式作為預設值
function getDiscount(price, discount = price * 0.1) {
    return price - discount;
}

console.log("100 打 9 折:", getDiscount(100));
console.log("100 打 8 折:", getDiscount(100, 80));

// 函數作為預設值
function getTime() {
    return new Date().toLocaleTimeString();
}

function log(message = `Time: ${getTime()}`) {
    console.log(message);
}

log(); // 顯示現在時間
log("自訂訊息");

// 使用其他參數
function calculate(a, b = a + 1, c = a * b) {
    return a + b + c;
}

console.log("calculate(2):", calculate(2)); // 2 + 3 + 6 = 11
console.log("calculate(2, 5):", calculate(2, 5)); // 2 + 5 + 10 = 17

// arguments 物件
function showArgs(a, b = 10, c) {
    console.log("arguments:", arguments.length);
    console.log("a:", a, "b:", b, "c:", c);
}

showArgs(1, undefined, 3); // b 會使用預設值 10

// 箭頭函數的預設參數
const add = (a = 0, b = 0) => a + b;
console.log("add():", add());
console.log("add(1, 2):", add(1, 2));

// 解構賦值中的預設值
function printCoords({ x = 0, y = 0 } = {}) {
    console.log(`x: ${x}, y: ${y}`);
}

printCoords(); // x: 0, y: 0
printCoords({ x: 5 }); // x: 5, y: 0
printCoords({ x: 5, y: 10 }); // x: 5, y: 10

// 展開運算子與預設參數
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}

console.log("sum():", sum()); // 0
console.log("sum(1,2,3):", sum(1, 2, 3)); // 6