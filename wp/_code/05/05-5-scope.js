// 作用域

// 全域作用域
var globalVar = "我是全域";

function testGlobal() {
    console.log("函數內存取全域:", globalVar);
}

testGlobal();
console.log("函數外存取全域:", globalVar);

// 區域作用域
function testLocal() {
    var localVar = "我是區域";
    console.log("函數內:", localVar);
}

testLocal();
// console.log(localVar); // 錯誤：無法存取

// 區塊作用域 (let/const)
if (true) {
    let blockVar = "區塊內";
    const blockConst = "常數";
    console.log("if 內:", blockVar);
}
// console.log(blockVar); // 錯誤

// 函數作用域
function outer() {
    var x = "outer";
    
    function inner() {
        var y = "inner";
        console.log("inner 存取 x:", x);
        console.log("inner 存取 y:", y);
    }
    
    inner();
    // console.log(y); // 錯誤
}

outer();

// 作用域鏈
var a = "全域 a";

function level1() {
    var a = "level1 a";
    
    function level2() {
        var a = "level2 a";
        console.log("level2:", a);
    }
    
    level2();
    console.log("level1:", a);
}

level1();
console.log("全域:", a);

// 變數提升 (hoisting)
console.log("提升的變數:", hoistVar);
var hoistVar = "已提升";

try {
    console.log(letVar);
} catch (e) {
    console.log("let 沒有提升");
}
let letVar = "沒有提升";