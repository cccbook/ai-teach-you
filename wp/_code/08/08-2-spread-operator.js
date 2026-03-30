// 展開運算子

// 陣列展開
let arr1 = [1, 2, 3];
let arr2 = [4, 5, 6];
let combined = [...arr1, ...arr2];
console.log("Combined:", combined);

// 複製陣列
let original = [1, 2, 3];
let copy = [...original];
console.log("Copy:", copy);

// 添加元素
let fruits = ["apple", "banana"];
let moreFruits = ["orange", ...fruits, "grape"];
console.log("Add:", moreFruits);

// 物件展開
let obj1 = { a: 1, b: 2 };
let obj2 = { c: 3, d: 4 };
let merged = { ...obj1, ...obj2 };
console.log("Merged:", merged);

// 複製物件
let user = { name: "王小明", age: 25 };
let userCopy = { ...user };
console.log("Copy:", userCopy);

// 覆蓋屬性
let defaults = { theme: "light", lang: "zh" };
let userSettings = { ...defaults, theme: "dark" };
console.log("Override:", userSettings);

// 函數參數展開
function sum(a, b, c) {
    return a + b + c;
}

let numbers = [1, 2, 3];
console.log("Spread:", sum(...numbers));

// 其餘參數 (Rest Parameters)
function collect(...items) {
    return items;
}

console.log("Rest:", collect(1, 2, 3, 4));

// 淺拷貝
let originalObj = { a: 1, b: { c: 2 } };
let shallowCopy = { ...originalObj };
shallowCopy.b.c = 3;
console.log("Shallow copy:", originalObj.b.c); // 3

// 深拷貝
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

let deepCopy = deepClone(originalObj);
deepCopy.b.c = 4;
console.log("Deep copy:", originalObj.b.c); // 3

// 字串展開
let str = "hello";
console.log("String spread:", [...str]);

// 轉換為陣列
let arrayLike = { 0: "a", 1: "b", length: 2 };
let array = [...arrayLike];
console.log("Array-like:", array);