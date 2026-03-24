// 資料類型

// 基本類型 (Primitive Types)

// 字串 (String)
let str1 = "Hello";
let str2 = 'World';
let str3 = `模板字串 ${str1} ${str2}`;
console.log(typeof str1, str1);

// 數字 (Number)
let num1 = 42;
let num2 = 3.14;
let num3 = -10;
console.log(typeof num1, num1);

// 布林 (Boolean)
let bool1 = true;
let bool2 = false;
console.log(typeof bool1, bool1);

// undefined
let undef;
console.log(typeof undef, undef);

// null
let empty = null;
console.log(typeof empty, empty);

// Symbol (ES6)
let sym = Symbol("description");
console.log(typeof sym, sym);

// 物件類型 (Reference Types)

// 陣列 (Array)
let arr = [1, 2, 3, "four", true];
console.log(typeof arr, arr);
console.log(Array.isArray(arr));

// 物件 (Object)
let obj = {
    name: "王小明",
    age: 25,
    isStudent: false
};
console.log(typeof obj, obj);

// 函數 (Function)
function greet(name) {
    return "Hello, " + name;
}
console.log(typeof greet, greet);

// 型別轉換
console.log(String(123));
console.log(Number("456"));
console.log(Boolean(1));
console.log(Boolean(0));