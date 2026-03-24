// 函數宣告

// 基本函數宣告
function greet(name) {
    return "Hello, " + name + "!";
}

console.log(greet("王小明"));

// 多參數
function add(a, b) {
    return a + b;
}

console.log("3 + 5 =", add(3, 5));

// 沒有 return 回傳 undefined
function print(message) {
    console.log(message);
}

let result = print("測試");
console.log("result:", result);

// 預設參數 (ES6)
function greetWithDefault(name = "Guest") {
    return "Hello, " + name + "!";
}

console.log(greetWithDefault());
console.log(greetWithDefault("小明"));

// 巢狀函數
function outer(x) {
    function inner(y) {
        return x + y;
    }
    return inner(10);
}

console.log("巢狀:", outer(5));