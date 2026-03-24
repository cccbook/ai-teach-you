// Promise 基礎

// 建立 Promise
let promise = new Promise(function(resolve, reject) {
    let success = true;
    
    if (success) {
        resolve("操作成功");
    } else {
        reject("操作失敗");
    }
});

promise
    .then(function(result) {
        console.log("成功:", result);
    })
    .catch(function(error) {
        console.error("失敗:", error);
    });

// Promise 狀態
let pendingPromise = new Promise(function(resolve, reject) {
    console.log("Promise 處理中...");
});

console.log("pendingPromise state:", pendingPromise);

// 模擬非同步操作
function fetchData(url) {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            if (url) {
                resolve({ url: url, data: "Mock data" });
            } else {
                reject(new Error("URL is required"));
            }
        }, 1000);
    });
}

fetchData("https://api.example.com/data")
    .then(function(response) {
        console.log("Response:", response);
    })
    .catch(function(error) {
        console.error("Error:", error.message);
    });

// Promise 鏈
fetchData("https://api.example.com/user")
    .then(function(response) {
        return response.data;
    })
    .then(function(user) {
        console.log("User:", user);
        return user.name;
    })
    .then(function(name) {
        console.log("Name:", name);
    })
    .catch(function(error) {
        console.error("Error:", error);
    });

// Promise.all - 等待所有 Promise 完成
let promise1 = Promise.resolve(1);
let promise2 = Promise.resolve(2);
let promise3 = Promise.resolve(3);

Promise.all([promise1, promise2, promise3])
    .then(function(results) {
        console.log("All results:", results);
    });

// Promise.race - 回傳最快完成的
Promise.race([
    new Promise(resolve => setTimeout(() => resolve("fast"), 100)),
    new Promise(resolve => setTimeout(() => resolve("slow"), 500))
])
.then(function(result) {
    console.log("Race winner:", result);
});