// rest 參數

// 基本 rest 參數
function sum(...numbers) {
    console.log("numbers:", numbers);
    return numbers.reduce((a, b) => a + b, 0);
}

console.log("sum(1,2):", sum(1, 2));
console.log("sum(1,2,3,4):", sum(1, 2, 3, 4));

// 配合一般參數
function greet(greeting, ...names) {
    return names.map(name => `${greeting}, ${name}!`);
}

console.log("greet Hello:", greet("Hello", "小明", "小華", "小美"));
console.log("greet Hi:", greet("Hi", "阿明"));

// rest 參數只能是最後一個
function first(first, ...rest) {
    console.log("first:", first);
    console.log("rest:", rest);
}

first(1, 2, 3, 4);

// 替代 arguments
function oldStyle() {
    console.log("arguments:", arguments);
}

function newStyle(...args) {
    console.log("rest:", args);
}

oldStyle(1, 2, 3);
newStyle(1, 2, 3);

// 陣列解構與 rest
let [first, ...rest] = [1, 2, 3, 4, 5];
console.log("first:", first);
console.log("rest:", rest);

// 物件解構與 rest
let { a, b, ...others } = { a: 1, b: 2, c: 3, d: 4 };
console.log("a:", a, "b:", b, "others:", others);

// 函數作為 rest
function apply(operation, ...args) {
    return operation(...args);
}

console.log("apply sum:", apply((...nums) => nums.reduce((a,b)=>a+b,0), 1, 2, 3));
console.log("apply max:", apply((...nums) => Math.max(...nums), 5, 2, 8, 1));

// 計算平均
function average(...numbers) {
    if (numbers.length === 0) return 0;
    return numbers.reduce((a, b) => a + b, 0) / numbers.length;
}

console.log("average():", average());
console.log("average(1,2,3):", average(1, 2, 3));

// 收集剩餘參數
function collect(separator, ...items) {
    return items.join(separator);
}

console.log("collect:", collect("-", "a", "b", "c"));