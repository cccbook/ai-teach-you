// 錯誤處理

// try-catch 基本用法
try {
    let result = 10 / 0;
    console.log("Result:", result);
} catch (error) {
    console.error("Error:", error.message);
}

// try-catch-finally
try {
    console.log("嘗試執行");
    throw new Error("自訂錯誤");
} catch (error) {
    console.error("Catch:", error.message);
} finally {
    console.log("Finally 執行");
}

// 巢狀 try-catch
try {
    try {
        throw new Error("內層錯誤");
    } catch (e) {
        console.log("內層 catch");
        throw e; // 重新拋出
    }
} catch (e) {
    console.log("外層 catch:", e.message);
}

// Error 類型
try {
    throw new TypeError("類型錯誤");
} catch (e) {
    console.log("Type:", e instanceof TypeError);
}

try {
    throw new RangeError("範圍錯誤");
} catch (e) {
    console.log("Range:", e instanceof RangeError);
}

// 自訂錯誤
class CustomError extends Error {
    constructor(message, code) {
        super(message);
        this.name = "CustomError";
        this.code = code;
    }
}

try {
    throw new CustomError("發生錯誤", 500);
} catch (e) {
    console.log("Error:", e.message, "Code:", e.code);
}

// 同步函數中的錯誤
function syncFunction() {
    try {
        JSON.parse("invalid");
    } catch (e) {
        console.log("Sync error:", e.message);
    }
}

syncFunction();

// 非同步錯誤處理 - Promise
new Promise(function(resolve, reject) {
    reject(new Error("Promise error"));
})
    .catch(function(e) {
        console.log("Promise catch:", e.message);
    });

// async/await 錯誤處理
async function asyncError() {
    try {
        await Promise.reject(new Error("Async error"));
    } catch (e) {
        console.log("Async catch:", e.message);
    }
}

asyncError();

// 全域錯誤監聽
window.addEventListener("error", function(event) {
    console.log("Global error:", event.message);
});

window.addEventListener("unhandledrejection", function(event) {
    console.log("Unhandled rejection:", event.reason);
});

// 條件性錯誤拋出
function divide(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    console.log("Divide error:", e.message);
}