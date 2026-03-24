// 函數表達式

// 函數表達式
const greet = function(name) {
    return "Hello, " + name + "!";
};

console.log(greet("小明"));

// 命名函數表達式
const factorial = function fact(n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
};

console.log("5! =", factorial(5));

// 作為參數傳遞
function executeFunction(fn, value) {
    return fn(value);
}

const result = executeFunction(function(x) {
    return x * 2;
}, 5);
console.log("executeFunction:", result);

// 回調函數
function processArray(arr, callback) {
    let result = [];
    for (let item of arr) {
        result.push(callback(item));
    }
    return result;
}

let numbers = [1, 2, 3, 4, 5];
let doubled = processArray(numbers, function(n) {
    return n * 2;
});
console.log("doubled:", doubled);

// IIFE (立即執行函數)
(function() {
    console.log("IIFE 執行");
})();

(function(name) {
    console.log("Hello, " + name);
})("小明");