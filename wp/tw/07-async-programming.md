# 第 7 章：非同步編程

## 概述

JavaScript 是單執行緒的語言，非同步編程讓我們能夠處理耗時操作而不阻塞主執行緒。本章介紹回調函數、Promise、async/await 以及 Fetch API。

## 7.1 回調函數

回調函數是非同步編程的基礎模式。

[程式檔案：07-1-callback.js](../_code/07/07-1-callback.js)

```javascript
// 基本回調
function fetchData(callback) {
    setTimeout(() => {
        const data = { id: 1, name: "王小明" };
        callback(data);
    }, 1000);
}

fetchData((result) => {
    console.log("收到資料:", result);
});

// 練習：模擬 API 請求
function getUser(userId, onSuccess, onError) {
    setTimeout(() => {
        if (userId > 0) {
            const user = { id: userId, name: "用戶" + userId };
            onSuccess(user);
        } else {
            onError("無效的用戶 ID");
        }
    }, 500);
}

getUser(
    123,
    (user) => console.log("成功:", user),
    (error) => console.error("錯誤:", error)
);

// 練習：排序後回調
function sortAndReturn(array, callback) {
    const sorted = [...array].sort((a, b) => a - b);
    setTimeout(() => callback(sorted), 100);
}

sortAndReturn([3, 1, 4, 1, 5], (result) => {
    console.log(result); // [1, 1, 3, 4, 5]
});
```

## 7.2 Promise 基礎

Promise 代表一個尚未完成但未來會完成的操作。

[程式檔案：07-2-promise-basic.js](../_code/07/07-2-promise-basic.js)

```javascript
// 建立 Promise
const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        const success = true;
        if (success) {
            resolve("操作成功！");
        } else {
            reject("操作失敗！");
        }
    }, 1000);
});

// 使用 Promise
promise
    .then((result) => {
        console.log(result); // "操作成功！"
    })
    .catch((error) => {
        console.error(error); // "操作失敗！"
    })
    .finally(() => {
        console.log("無論成功或失敗都會執行");
    });

// 練習：Promise 包裝 setTimeout
const delay = (ms) => {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
};

delay(2000).then(() => {
    console.log("2 秒後執行");
});

// 練習：Promise 判斷年齡
const checkAge = (age) => {
    return new Promise((resolve, reject) => {
        if (age >= 18) {
            resolve("已成年");
        } else {
            reject("未成年");
        }
    });
};

checkAge(20)
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
```

## 7.3 Promise 鏈

Promise 可以串聯多個非同步操作。

[程式檔案：07-3-promise-chain.js](../_code/07/07-3-promise-chain.js)

```javascript
// Promise 鏈
const fetchUser = (id) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve({ id, name: "用戶" + id });
        }, 500);
    });
};

const fetchPosts = (userId) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(["文章1", "文章2", "文章3"]);
        }, 500);
    });
};

const fetchComments = (postId) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(["留言1", "留言2"]);
        }, 500);
    });
};

// 鏈式呼叫
fetchUser(1)
    .then((user) => {
        console.log("用戶:", user);
        return fetchPosts(user.id);
    })
    .then((posts) => {
        console.log("文章:", posts);
        return fetchComments(posts[0]);
    })
    .then((comments) => {
        console.log("留言:", comments);
    })
    .catch((error) => {
        console.error("發生錯誤:", error);
    });

// 練習：處理錯誤
const safePromise = (fn) => {
    return (...args) => {
        return Promise.resolve()
            .then(() => fn(...args));
    };
};

// 練習：Promise.all 同時執行多個
const promise1 = Promise.resolve(1);
const promise2 = Promise.resolve(2);
const promise3 = Promise.resolve(3);

Promise.all([promise1, promise2, promise3])
    .then((results) => {
        console.log(results); // [1, 2, 3]
    });

// 練習：Promise.race 競速
const slow = new Promise((r) => setTimeout(() => r("慢"), 2000));
const fast = new Promise((r) => setTimeout(() => r("快"), 1000));

Promise.race([slow, fast]).then((result) => {
    console.log(result); // "快"
});
```

## 7.4 async/await

async/await 是 Promise 的語法糖，讓非同步程式碼更像同步程式碼。

[程式檔案：07-4-async-await.js](../_code/07/07-4-async-await.js)

```javascript
// async 函數自動回傳 Promise
async function fetchData() {
    return { data: "測試資料" };
}

fetchData().then(console.log);

// await 等待 Promise 完成
async function getUser() {
    const user = await fetchUser(1);
    console.log(user);
}

// 練習：完整範例
async function loadUserPosts() {
    try {
        const user = await fetchUser(1);
        const posts = await fetchPosts(user.id);
        return { user, posts };
    } catch (error) {
        console.error("載入失敗:", error);
        return null;
    }
}

// 並行執行
async function loadAll() {
    const [users, posts] = await Promise.all([
        fetchUsers(),
        fetchPosts()
    ]);
    return { users, posts };
}

// 練習：順序執行 vs 並行執行
async function sequential() {
    const a = await fetchA(); // 1 秒
    const b = await fetchB(); // 1 秒
    // 總共 2 秒
}

async function parallel() {
    const [a, b] = await Promise.all([fetchA(), fetchB()]);
    // 總共 1 秒
}

// 練習：async 迴圈
async function processItems(items) {
    const results = [];
    for (const item of items) {
        const result = await process(item);
        results.push(result);
    }
    return results;
}

// 練習：Promise.all 處理迴圈
async function processParallel(items) {
    return Promise.all(items.map(item => process(item)));
}
```

## 7.5 Fetch API

Fetch API 是現代瀏覽器提供的網路請求介面。

[程式檔案：07-5-fetch-api.js](../_code/07/07-5-fetch-api.js)

```javascript
// 基本 GET 請求
fetch("https://jsonplaceholder.typicode.com/users/1")
    .then((response) => response.json())
    .then(console.log)
    .catch(console.error);

// POST 請求
fetch("https://jsonplaceholder.typicode.com/posts", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        title: "新文章",
        body: "內容",
        userId: 1
    })
})
    .then((response) => response.json())
    .then(console.log);

// 練習：async/await 版本
async function createPost(title, body, userId) {
    try {
        const response = await fetch("https://jsonplaceholder.typicode.com/posts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title, body, userId })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("請求失敗:", error);
        throw error;
    }
}

// 練習：帶認證的請求
async function fetchWithAuth(url) {
    const token = localStorage.getItem("token");
    
    const response = await fetch(url, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    
    return response.json();
}

// 練習：上傳檔案
async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);
    
    const response = await fetch("/api/upload", {
        method: "POST",
        body: formData
    });
    
    return response.json();
}
```

## 7.6 JSON 解析

處理 JSON 資料是日常開發的重要工作。

[程式檔案：07-6-json-parse.js](../_code/07/07-6-json-parse.js)

```javascript
// JSON.parse - 字串轉物件
const jsonString = '{"name": "王小明", "age": 25}';
const obj = JSON.parse(jsonString);
console.log(obj.name); // "王小明"

// JSON.stringify - 物件轉字串
const obj2 = { name: "陳小美", age: 30 };
const jsonStr = JSON.stringify(obj2);
console.log(jsonStr); // '{"name":"陳小美","age":30}'

// 格式化輸出
const pretty = JSON.stringify(obj2, null, 2);
console.log(pretty);
// {
//   "name": "陳小美",
//   "age": 30
// }

// 自訂序列化
const custom = {
    name: "林大明",
    age: 28,
    password: "secret123"
};

const safe = JSON.stringify(custom, (key, value) => {
    if (key === "password") return undefined;
    return value;
});

console.log(safe); // '{"name":"林大明","age":28}'

// 練習：處理日期
const withDate = {
    event: "派對",
    date: new Date("2026-03-24")
};

const dateStr = JSON.stringify(withDate, null, 2);
console.log(dateStr);
// date 會轉換為 ISO 字串

// 練習：解析含日期的字串
const parsed = JSON.parse(dateStr, (key, value) => {
    if (key === "date") {
        return new Date(value);
    }
    return value;
});
console.log(parsed.date instanceof Date); // true
```

## 7.7 錯誤處理

完善的錯誤處理是可靠程式碼的關鍵。

[程式檔案：07-7-error-handling.js](../_code/07/07-7-error-handling.js)

```javascript
// try...catch
async function fetchData() {
    try {
        const response = await fetch("/api/data");
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("取得資料失敗:", error.message);
        throw error;
    }
}

// 自訂錯誤類別
class ApiError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.name = "ApiError";
        this.statusCode = statusCode;
    }
}

async function safeFetch(url) {
    const response = await fetch(url);
    
    if (!response.ok) {
        throw new ApiError(
            "請求失敗",
            response.status
        );
    }
    
    return response.json();
}

// 練習：重試機制
async function fetchWithRetry(url, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            if (i === retries - 1) throw error;
            await delay(1000 * (i + 1));
        }
    }
}

// 練習：finally 用於清理
async function withCleanup() {
    let resource = null;
    
    try {
        resource = await acquire();
        return await use(resource);
    } finally {
        if (resource) {
            await release(resource);
        }
    }
}

// 練習：finally 顯示/隱藏 loading
async function loadData() {
    showLoading();
    try {
        return await fetchData();
    } finally {
        hideLoading();
    }
}
```

## 7.8 setTimeout

setTimeout 用於延遲執行程式碼。

[程式檔案：07-8-timeout.js](../_code/07/07-8-timeout.js)

```javascript
// 基本用法
setTimeout(() => {
    console.log("2 秒後執行");
}, 2000);

// 帶參數
setTimeout((name, age) => {
    console.log(`${name} is ${age} years old`);
}, 1000, "王小明", 25);

// 取消 setTimeout
const timeoutId = setTimeout(() => {
    console.log("這不會執行");
}, 5000);

clearTimeout(timeoutId);

// 練習：防抖（debounce）
function debounce(func, wait) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, wait);
    };
}

const debouncedSearch = debounce((query) => {
    console.log("搜尋:", query);
}, 300);

// 練習：動畫計時器
const animate = (duration, callback) => {
    const start = Date.now();
    
    const tick = () => {
        const elapsed = Date.now() - start;
        const progress = Math.min(elapsed / duration, 1);
        
        callback(progress);
        
        if (progress < 1) {
            requestAnimationFrame(tick);
        }
    };
    
    requestAnimationFrame(tick);
};

animate(2000, (progress) => {
    console.log(`動畫進度: ${(progress * 100).toFixed(0)}%`);
});
```

## 7.9 setInterval

setInterval 用於重複執行程式碼。

[程式檔案：07-9-interval.js](../_code/07/07-9-interval.js)

```javascript
// 基本用法
const intervalId = setInterval(() => {
    console.log("每 1 秒執行一次");
}, 1000);

// 取消 setInterval
setTimeout(() => {
    clearInterval(intervalId);
    console.log("停止");
}, 5000);

// 練習：計時器
class Timer {
    constructor() {
        this.startTime = null;
        this.intervalId = null;
    }
    
    start() {
        this.startTime = Date.now();
        this.intervalId = setInterval(() => {
            const elapsed = Date.now() - this.startTime;
            console.log(`已過: ${Math.floor(elapsed / 1000)} 秒`);
        }, 1000);
    }
    
    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    reset() {
        this.stop();
        this.startTime = null;
    }
}

// 練習：倒數計時
function countdown(seconds) {
    let remaining = seconds;
    
    const intervalId = setInterval(() => {
        if (remaining > 0) {
            console.log(remaining);
            remaining--;
        } else {
            console.log("時間到！");
            clearInterval(intervalId);
        }
    }, 1000);
}

// 練習：輪播圖
class Carousel {
    constructor(images, container) {
        this.images = images;
        this.currentIndex = 0;
        this.container = container;
    }
    
    start(interval = 3000) {
        this.intervalId = setInterval(() => {
            this.next();
        }, interval);
    }
    
    next() {
        this.currentIndex = (this.currentIndex + 1) % this.images.length;
        this.show(this.currentIndex);
    }
    
    show(index) {
        this.container.src = this.images[index];
    }
    
    stop() {
        clearInterval(this.intervalId);
    }
}
```

## 7.10 Promise 化

將回調式 API 轉換為 Promise。

[程式檔案：07-10-promisify.js](../_code/07/07-10-promisify.js)

```javascript
// 手動 promisify
const readFile = (path) => {
    return new Promise((resolve, reject) => {
        fs.readFile(path, "utf8", (err, data) => {
            if (err) reject(err);
            else resolve(data);
        });
    });
};

// promisify 工具
const { promisify } = require("util");
const readFilePromise = promisify(fs.readFile);

// 練習：通用 promisify 函數
const promisifyAll = (obj) => {
    const result = {};
    
    for (const key of Object.keys(obj)) {
        const value = obj[key];
        if (typeof value === "function") {
            result[key] = (...args) => {
                return new Promise((resolve, reject) => {
                    value.call(obj, ...args, (err, ...results) => {
                        if (err) reject(err);
                        else resolve(...results);
                    });
                });
            };
        }
    }
    
    return result;
};

// 練習：包裝 XMLHttpRequest
const request = (options) => {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(options.method, options.url);
        
        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.responseText);
            } else {
                reject(new Error(xhr.statusText));
            }
        };
        
        xhr.onerror = () => reject(new Error("網路錯誤"));
        
        xhr.send(options.body);
    });
};

// 練習：包裝事件監聽
const once = (element, event) => {
    return new Promise((resolve) => {
        element.addEventListener(event, resolve, { once: true });
    });
};

// 練習：超時 Promise
const withTimeout = (promise, ms) => {
    return Promise.race([
        promise,
        new Promise((_, reject) => {
            setTimeout(() => reject(new Error("超時")), ms);
        })
    ]);
};
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| 回調函數 | 傳入另一函數，稍後呼叫 |
| Promise | 代表非同步操作的最終結果 |
| then/catch | Promise 的鏈式處理 |
| async/await | Promise 的語法糖 |
| Fetch API | 瀏覽器網路請求介面 |
| setTimeout | 延遲執行一次 |
| setInterval | 重複執行 |

## 練習題

1. 實作一個非同步請求庫，支援 GET/POST 和錯誤處理
2. 實作 Promise.all 版本的平行請求
3. 實作圖片懶載入功能
4. 建立一個支援取消的 fetch 封裝
