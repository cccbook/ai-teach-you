// async/await

// async 函數
async function fetchData() {
    return "data";
}

fetchData().then(console.log);

// await 等待 Promise
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
    console.log("開始");
    await delay(1000);
    console.log("1秒後");
    await delay(1000);
    console.log("2秒後");
}

main();

// 錯誤處理 try-catch
async function getData() {
    try {
        await delay(100);
        console.log("成功");
        return "success";
    } catch (error) {
        console.error("錯誤:", error);
        return "failed";
    }
}

getData();

// 多個 await 順序執行
async function sequential() {
    let result1 = await Promise.resolve(1);
    let result2 = await Promise.resolve(2);
    let result3 = await Promise.resolve(3);
    console.log("順序:", result1, result2, result3);
}

sequential();

// 多個 await 並行執行
async function parallel() {
    let promise1 = Promise.resolve(1);
    let promise2 = Promise.resolve(2);
    let promise3 = Promise.resolve(3);
    
    let results = await Promise.all([promise1, promise2, promise3]);
    console.log("並行:", results);
}

parallel();

// async 函數返回值
async function getUser() {
    return { id: 1, name: "王小明" };
}

getUser().then(console.log);

// 立即執行 async 函數
(async function() {
    let result = await Promise.resolve("IIFE");
    console.log("IIFE:", result);
})();

// await in loop
async function processItems(items) {
    let results = [];
    for (let item of items) {
        let result = await Promise.resolve(item * 2);
        results.push(result);
    }
    return results;
}

processItems([1, 2, 3]).then(console.log);

// 處理 rejection
async function riskyFunction() {
    throw new Error("Error occurred");
}

riskyFunction().catch(console.error);

// await Promise.allSettled
async function settled() {
    let results = await Promise.allSettled([
        Promise.resolve(1),
        Promise.reject("error"),
        Promise.resolve(3)
    ]);
    
    results.forEach((result, index) => {
        if (result.status === "fulfilled") {
            console.log(`${index}: ${result.value}`);
        } else {
            console.log(`${index}: ${result.reason}`);
        }
    });
}

settled();