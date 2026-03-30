// 參數與回傳值

// 基本參數
function sum(a, b) {
    return a + b;
}
console.log("sum:", sum(3, 5));

// 預設參數
function greet(name = "Guest", greeting = "Hello") {
    return `${greeting}, ${name}!`;
}
console.log(greet());
console.log(greet("小明", "Hi"));

// 其餘參數 (Rest Parameters)
function sumAll(...numbers) {
    let total = 0;
    for (let n of numbers) {
        total += n;
    }
    return total;
}
console.log("sumAll:", sumAll(1, 2, 3, 4, 5));

// arguments 物件
function showArgs() {
    console.log("arguments:", arguments);
    console.log("length:", arguments.length);
    console.log("arguments[0]:", arguments[0]);
}
showArgs("a", "b", "c");

// 解構參數
function displayInfo({ name, age, city = "台北" }) {
    console.log(`姓名: ${name}, 年齡: ${age}, 城市: ${city}`);
}

displayInfo({ name: "王小明", age: 25 });

// 陣列解構
function getCoordinates([x, y]) {
    console.log(`x: ${x}, y: ${y}`);
}
getCoordinates([10, 20]);

// 回傳多個值
function getMinMax(numbers) {
    return {
        min: Math.min(...numbers),
        max: Math.max(...numbers)
    };
}

let result = getMinMax([3, 1, 4, 1, 5, 9]);
console.log("min:", result.min, "max:", result.max);

// 回傳函數
function multiplier(factor) {
    return function(number) {
        return number * factor;
    };
}

let double = multiplier(2);
let triple = multiplier(3);
console.log("double(5):", double(5));
console.log("triple(5):", triple(5));