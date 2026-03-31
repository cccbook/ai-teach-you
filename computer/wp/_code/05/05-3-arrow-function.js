// 箭頭函數

// 基本語法
const add = (a, b) => a + b;
console.log("add:", add(3, 5));

// 多行函數體需要 return
const multiply = (a, b) => {
    const result = a * b;
    return result;
};
console.log("multiply:", multiply(4, 6));

// 單參數可省略括號
const square = x => x * x;
console.log("square:", square(5));

// 無參數
const getTime = () => new Date().toLocaleTimeString();
console.log("time:", getTime());

// 回調函數中的箭頭函數
const numbers = [1, 2, 3, 4, 5];

let doubled = numbers.map(n => n * 2);
console.log("map:", doubled);

let evens = numbers.filter(n => n % 2 === 0);
console.log("filter:", evens);

let sum = numbers.reduce((acc, n) => acc + n, 0);
console.log("reduce:", sum);

// this 綁定
const person = {
    name: "王小明",
    hobbies: ["coding", "reading"],
    
    // 傳統方法
    logTraditional: function() {
        this.hobbies.forEach(function(hobby) {
            // console.log(this.name + " likes " + hobby);
        });
    },
    
    // 箭頭函數繼承 this
    logArrow: function() {
        this.hobbies.forEach(hobby => {
            console.log(this.name + " likes " + hobby);
        });
    }
};

person.logArrow();

// arguments 物件
function traditional() {
    console.log("arguments:", arguments);
}
traditional(1, 2, 3);

// 箭頭函數沒有自己的 arguments
// 可使用其餘參數替代