// setInterval

// 基本用法
let count = 0;
let intervalId = setInterval(function() {
    count++;
    console.log("Count:", count);
    if (count >= 5) {
        clearInterval(intervalId);
        console.log("Interval 停止");
    }
}, 1000);

// 使用箭頭函數
let counter = 0;
let id = setInterval(() => {
    counter++;
    console.log("Counter:", counter);
    if (counter >= 3) clearInterval(id);
}, 500);

// 清除 interval
let intervalId2 = setInterval(() => {
    console.log("每秒執行");
}, 1000);

setTimeout(() => {
    clearInterval(intervalId2);
    console.log("已停止");
}, 5500);

// 傳遞參數
function logMessage(message, times) {
    console.log(message);
}

let logId = setInterval(logMessage, 1000, "Hello", 3);
setTimeout(() => clearInterval(logId), 3500);

// 實現倒數計時
function countdown(seconds) {
    let remaining = seconds;
    
    let timerId = setInterval(() => {
        console.log(`倒數: ${remaining}`);
        remaining--;
        
        if (remaining < 0) {
            clearInterval(timerId);
            console.log("時間到!");
        }
    }, 1000);
}

countdown(5);

// 模擬時鐘
function clock() {
    setInterval(() => {
        let now = new Date();
        console.log(now.toLocaleTimeString());
    }, 1000);
}

// clock(); // 取消註解查看時鐘

// 使用 clearInterval + setTimeout 實現
function runOncePerSecond(callback) {
    let lastTime = Date.now();
    
    function tick() {
        let now = Date.now();
        if (now - lastTime >= 1000) {
            lastTime = now;
            callback();
        }
        requestAnimationFrame(tick);
    }
    
    tick();
}

let runId = 0;
runOncePerSecond(() => {
    console.log("每秒執行");
    runId++;
    if (runId >= 3) {
        // 停止邏輯需要額外實現
    }
});

// interval 中的錯誤處理
let safeInterval = function(fn, ms) {
    function tick() {
        try {
            fn();
        } catch (e) {
            console.error("Error:", e);
        }
        setTimeout(tick, ms);
    }
    tick();
};

let errorCount = 0;
safeInterval(() => {
    console.log("Safe interval");
    errorCount++;
    if (errorCount >= 3) {
        throw new Error("測試錯誤");
    }
}, 500);

// 防止 interval 累積
let activeInterval = null;
let startInterval = function(fn, ms) {
    if (activeInterval) {
        clearInterval(activeInterval);
    }
    activeInterval = setInterval(fn, ms);
};

let stopInterval = function() {
    if (activeInterval) {
        clearInterval(activeInterval);
        activeInterval = null;
    }
};