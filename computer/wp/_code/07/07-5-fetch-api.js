// Fetch API

// 基本 GET 請求
fetch("https://jsonplaceholder.typicode.com/posts/1")
    .then(response => {
        console.log("Response status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("Data:", data);
    })
    .catch(error => {
        console.error("Error:", error);
    });

// POST 請求
fetch("https://jsonplaceholder.typicode.com/posts", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        title: "標題",
        body: "內容",
        userId: 1
    })
})
    .then(response => response.json())
    .then(data => console.log("Created:", data))
    .catch(console.error);

// PUT 請求 (更新)
fetch("https://jsonplaceholder.typicode.com/posts/1", {
    method: "PUT",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        id: 1,
        title: "更新後的標題",
        body: "更新後的內容",
        userId: 1
    })
})
    .then(response => response.json())
    .then(data => console.log("Updated:", data))
    .catch(console.error);

// DELETE 請求
fetch("https://jsonplaceholder.typicode.com/posts/1", {
    method: "DELETE"
})
    .then(response => {
        console.log("Deleted, status:", response.status);
    })
    .catch(console.error);

// 使用 async/await
async function fetchData() {
    try {
        let response = await fetch("https://jsonplaceholder.typicode.com/users/1");
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        let data = await response.json();
        console.log("User:", data);
        return data;
    } catch (error) {
        console.error("Fetch error:", error);
    }
}

fetchData();

// 處理 headers
fetch("https://jsonplaceholder.typicode.com/posts/1", {
    headers: {
        "Authorization": "Bearer token",
        "Accept": "application/json"
    }
})
    .then(response => {
        console.log("Headers:");
        for (let [key, value] of response.headers) {
            console.log(`${key}: ${value}`);
        }
        return response.json();
    })
    .catch(console.error);

// Request 物件
let request = new Request("https://jsonplaceholder.typicode.com/posts/1", {
    method: "GET",
    headers: new Headers({
        "Content-Type": "application/json"
    })
});

fetch(request).then(r => r.json()).then(console.log);