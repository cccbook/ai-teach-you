// setTimeout

// 基本用法
console.log("開始");
setTimeout(function() {
    console.log("1秒後執行");
}, 1000);
console.log("設定完成");

// 使用箭頭函數
setTimeout(() => {
    console.log("箭頭函數版本");
}, 1000);

// 傳遞參數
function greet(name, greeting) {
    console.log(`${greeting}, ${name}!`);
}

setTimeout(greet, 1000, "王小明", "Hello");

// 清除 timeout
let timeoutId = setTimeout(() => {
    console.log("這不會執行");
}, 1000);

clearTimeout(timeoutId);
console.log("Timeout 已清除");

// 巢狀 setTimeout (模擬 setInterval)
function delayedLoop(count) {
    if (count > 0) {
        console.log("Count:", count);
        setTimeout(() => delayedLoop(count - 1), 500);
    }
}

delayedLoop(3);

// 0 毫秒延遲
console.log("1");
setTimeout(() => console.log("2"), 0);
console.log("3");

// Promise + setTimeout
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

delay(1000).then(() => console.log("1秒後"));

// async/await 版本
async function wait(ms) {
    await new Promise(resolve => setTimeout(resolve, ms));
    return "完成";
}

wait(500).then(console.log);

// 計時器中的 this 問題
function Timer() {
    this.time = 0;
    
    setTimeout(function() {
        // this.time = 10; // 錯誤：this 是 timeout
    }, 1000);
    
    setTimeout(() => {
        this.time = 10; // 正確：arrow function
        console.log("time:", this.time);
    }, 1000);
}

new Timer();

// 避免 this 問題
let obj = {
    value: 0,
    start: function() {
        setTimeout(function() {
            console.log("this:", this); // timeout
        }, 1000);
        
        setTimeout(() => {
            console.log("arrow this:", this); // obj
        }, 1000);
    }
};

obj.start();

// 使用 clearTimeout 實現可取消的延遲
let cancellableDelay = function(ms) {
    let timeoutId;
    let promise = new Promise(function(resolve) {
        timeoutId = setTimeout(resolve, ms);
    });
    
    return {
        promise: promise,
        cancel: function() {
            clearTimeout(timeoutId);
        }
    };
};

let delay = cancellableDelay(5000);
delay.promise.then(() => console.log("完成"));
delay.cancel(); // 取消