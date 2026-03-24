// Promise 鏈

// 基本鏈式調用
function step1() {
    return Promise.resolve("步驟1完成");
}

function step2(data) {
    console.log(data);
    return Promise.resolve("步驟2完成");
}

function step3(data) {
    console.log(data);
    return Promise.resolve("步驟3完成");
}

step1()
    .then(step2)
    .then(step3)
    .then(function(finalResult) {
        console.log("全部完成:", finalResult);
    });

// 錯誤處理
function mayFail(shouldFail) {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            if (shouldFail) {
                reject(new Error("操作失敗"));
            } else {
                resolve("成功");
            }
        }, 100);
    });
}

mayFail(false)
    .then(function(result) {
        console.log("第一個成功:", result);
        return mayFail(true);
    })
    .then(function(result) {
        console.log("第二個成功:", result);
    })
    .catch(function(error) {
        console.error("錯誤:", error.message);
    });

// 每次 then 返回新的 Promise
function asyncTask(id) {
    return new Promise(function(resolve) {
        setTimeout(function() {
            resolve(`Task ${id} done`);
        }, 100 * id);
    });
}

asyncTask(1)
    .then(function(result) {
        console.log(result);
        return asyncTask(2);
    })
    .then(function(result) {
        console.log(result);
        return asyncTask(3);
    })
    .then(function(result) {
        console.log(result);
    });

// Promise.resolve 和 Promise.reject
Promise.resolve("直接成功")
    .then(function(result) {
        console.log("Promise.resolve:", result);
    });

Promise.reject(new Error("直接失敗"))
    .catch(function(error) {
        console.error("Promise.reject:", error.message);
    });

// 穿透 (Promise passthrough)
Promise.resolve("value")
    .then(Promise.resolve) // 返回 Promise，會穿透
    .then(function(result) {
        console.log("穿透:", result);
    });

// 返回 Promise vs 返回值
function getPromise() {
    return Promise.resolve("I am a promise");
}

Promise.resolve("value")
    .then(function(v) {
        return getPromise(); // 會等待 Promise 完成
    })
    .then(function(result) {
        console.log("返回 Promise:", result);
    });

Promise.resolve("value")
    .then(function(v) {
        return "I am a value"; // 直接返回值
    })
    .then(function(result) {
        console.log("返回值:", result);
    });