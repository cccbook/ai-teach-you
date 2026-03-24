// 變數宣告

// var - 舊式宣告，可重複宣告
var name = "王小明";
var name = "李小華"; // 可重複宣告
console.log("var:", name);

// let - 區塊作用域，不可重複宣告
let age = 25;
// let age = 30; // 錯誤：已宣告
age = 30; // 可以重新賦值
console.log("let:", age);

// const - 常數，不可重新賦值
const PI = 3.14159;
// PI = 3.14; // 錯誤：不可重新賦值
console.log("const:", PI);

// 全域與區域變數
var globalVar = "全域";

function testScope() {
    var localVar = "區域";
    console.log("函數內:", globalVar, localVar);
}

testScope();
// console.log(localVar); // 錯誤：區域變數無法存取