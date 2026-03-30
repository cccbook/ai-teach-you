// Promise 化

// 將 callback 轉為 Promise
function promisify(callbackBased) {
    return function(...args) {
        return new Promise((resolve, reject) => {
            callbackBased(...args, (error, result) => {
                if (error) {
                    reject(error);
                } else {
                    resolve(result);
                }
            });
        });
    };
}

// 範例：fs.readFile promisify
const fs = require("fs");
// let readFile = promisify(fs.readFile);
// readFile("file.txt", "utf8")
//     .then(console.log)
//     .catch(console.error);

// Node.js 內建 promisify
const { promisify } = require("util");
let readFilePromise = promisify(fs.readFile);

// setTimeout promisify
function setTimeoutPromise(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

setTimeoutPromise(1000).then(() => console.log("1秒"));

// 練習：promisify setInterval
function setIntervalPromise(fn, ms) {
    return new Promise(resolve => {
        let id = setInterval(() => {
            let result = fn();
            if (result === "stop") {
                clearInterval(id);
                resolve("已停止");
            }
        }, ms);
    });
}

// setIntervalPromise(() => {
//     console.log("Interval");
//     return "stop"; // 停止
// }, 500);

// 練習：promisify EventEmitter
function oncePromise(emitter, event) {
    return new Promise(resolve => {
        emitter.once(event, resolve);
    });
}

// Promise.all 的同步版本
async function promiseAll(promises) {
    return new Promise((resolve, reject) => {
        let results = [];
        let pending = promises.length;
        
        if (pending === 0) {
            resolve(results);
            return;
        }
        
        promises.forEach((promise, index) => {
            Promise.resolve(promise)
                .then(result => {
                    results[index] = result;
                    pending--;
                    if (pending === 0) {
                        resolve(results);
                    }
                })
                .catch(reject);
        });
    });
}

// 使用範例
promiseAll([
    Promise.resolve(1),
    Promise.resolve(2),
    Promise.resolve(3)
])
    .then(console.log);

// Promise.race
function promiseRace(promises) {
    return new Promise((resolve, reject) => {
        promises.forEach(promise => {
            Promise.resolve(promise)
                .then(resolve, reject);
        });
    });
}

// Promise.allSettled
function promiseAllSettled(promises) {
    return new Promise(resolve => {
        let results = [];
        let pending = promises.length;
        
        if (pending === 0) {
            resolve(results);
            return;
        }
        
        promises.forEach((promise, index) => {
            Promise.resolve(promise)
                .then(result => {
                    results[index] = { status: "fulfilled", value: result };
                })
                .catch(error => {
                    results[index] = { status: "rejected", reason: error };
                })
                .finally(() => {
                    pending--;
                    if (pending === 0) {
                        resolve(results);
                    }
                });
        });
    });
}