# 第 6 章：DOM 操作

## 概述

DOM（Document Object Model）讓 JavaScript 能夠存取和操作 HTML 文件。本章介紹如何選擇元素、建立修改刪除元素，以及處理事件。

## 6.1 DOM 選擇

使用 JavaScript 方法選擇 DOM 元素。

[程式檔案：06-1-dom-select.js](../_code/06/06-1-dom-select.js)

```javascript
// 根據 ID 選擇（最常用）
const header = document.getElementById("header");

// 根據類別選擇（回傳 HTMLCollection）
const items = document.getElementsByClassName("item");

// 根據標籤選擇（回傳 HTMLCollection）
const paragraphs = document.getElementsByTagName("p");

// CSS 選擇器（回傳第一個匹配）
const firstButton = document.querySelector(".btn");
const navItem = document.querySelector("#nav > li");

// CSS 選擇器（回傳所有匹配，NodeList）
const allButtons = document.querySelectorAll(".btn");
const listItems = document.querySelectorAll("ul > li");

// 遍歷 NodeList
allButtons.forEach(btn => {
    console.log(btn.textContent);
});

// 選擇結果都是動態的嗎？
// getElementById: 不是（每次查詢）
// getElementsByClassName: 是（HTMLCollection）
// querySelectorAll: 不是（NodeList，靜態快照）
```

## 6.2 DOM 遍歷

在 DOM 樹中移動，選擇相對位置的元素。

[程式檔案：06-2-dom-traverse.js](../_code/06/06-2-dom-traverse.js)

```javascript
const element = document.querySelector(".card");

// 父元素
const parent = element.parentElement;
const parentNode = element.parentNode;

// 子元素
const children = element.children;           // HTMLCollection
const firstChild = element.firstElementChild;
const lastChild = element.lastElementChild;
const childNodes = element.childNodes;        // NodeList（包含文字節點）

// 兄弟元素
const nextSibling = element.nextElementSibling;
const prevSibling = element.previousElementSibling;

// 巢狀遍歷
const deepTraverse = (element) => {
    let result = [];
    result.push(element);
    for (const child of element.children) {
        result = result.concat(deepTraverse(child));
    }
    return result;
};

// 練習：找出所有孫元素
const getAllDescendants = (element) => {
    let descendants = [];
    for (const child of element.children) {
        descendants.push(child);
        descendants = descendants.concat(getAllDescendants(child));
    }
    return descendants;
};
```

## 6.3 建立元素

動態建立新的 DOM 元素。

[程式檔案：06-3-dom-create.js](../_code/06/06-3-dom-create.js)

```javascript
// 建立元素
const newDiv = document.createElement("div");
const newParagraph = document.createElement("p");
const newText = document.createTextNode("這是文字內容");

// 設定屬性
newDiv.id = "my-div";
newDiv.className = "container highlight";
newDiv.setAttribute("data-id", "123");

// 設定內容
newParagraph.textContent = "純文字內容";
newParagraph.innerHTML = "<strong>HTML</strong> 內容";

// 加入 DOM
document.body.appendChild(newDiv);
newDiv.appendChild(newParagraph);

// 插入位置
const container = document.querySelector(".container");

// 末尾加入
container.appendChild(newElement);

// 開頭加入
container.insertBefore(newElement, container.firstChild);

// 便利方法（部分瀏覽器支援）
container.prepend(newElement);     // 開頭
container.append(...nodes);        // 末尾
container.before(element);         // 元素前
container.after(element);          // 元素後

// 練習：建立列表
const createList = (items) => {
    const ul = document.createElement("ul");
    items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        ul.appendChild(li);
    });
    return ul;
};

document.body.appendChild(createList(["蘋果", "香蕉", "橘子"]));
```

## 6.4 修改元素

修改元素的屬性、內容和樣式。

[程式檔案：06-4-dom-modify.js](../_code/06/06-4-dom-modify.js)

```javascript
const element = document.querySelector(".box");

// 修改內容
element.textContent = "新文字內容";           // 純文字
element.innerHTML = "<strong>HTML</strong>";  // HTML 內容
element.innerText = "純文字（不解析 HTML）";

// 修改屬性
element.setAttribute("id", "new-id");
element.getAttribute("id");
element.removeAttribute("data-info");

// 直接修改 DOM 屬性
element.id = "new-id";
element.src = "new-image.jpg";
element.href = "https://example.com";

// 修改樣式
element.style.color = "red";
element.style.backgroundColor = "#f0f0f0";
element.style.fontSize = "20px";

// 修改類別
element.classList.add("active");
element.classList.remove("hidden");
element.classList.toggle("active");     // 切換
element.classList.contains("active");   // 檢查
element.classList.replace("old", "new");

// dataset（自訂資料屬性）
element.dataset.userId = "123";
element.dataset["userName"] = "王小明";
console.log(element.dataset.userId);
```

## 6.5 刪除元素

從 DOM 中移除元素。

[程式檔案：06-5-dom-delete.js](../_code/06/06-5-dom-delete.js)

```javascript
// 移除自己
element.remove();

// 移除子元素
parent.removeChild(child);
parent.innerHTML = "";  // 清空所有子元素

// 練習：清空容器
const clearContainer = (container) => {
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
};

// 練習：移除所有匹配的元素
const removeAllByClass = (className) => {
    const elements = document.querySelectorAll(`.${className}`);
    elements.forEach(el => el.remove());
};

// 練習：替換元素
const replaceElement = (oldElement, newElement) => {
    oldElement.parentNode.replaceChild(newElement, oldElement);
};

// 練習：移動元素
const moveElement = (element, newParent) => {
    newParent.appendChild(element);  // 會自動從舊位置移除
};

// 練習：複製元素
const clone = element.cloneNode(true);   // 深拷貝（包含子元素）
const shallowClone = element.cloneNode(false); // 淺拷貝（只有自己）
```

## 6.6 事件綁定

為元素綁定事件處理器。

[程式檔案：06-6-event-basic.js](../_code/06/06-6-event-basic.js)

```javascript
const button = document.querySelector("#myButton");

// HTML 內聯（不推薦）
// <button onclick="handleClick()">點擊</button>

// DOM 屬性（只支援一個處理器）
button.onclick = function(event) {
    console.log("點擊了按鈕");
};

// 事件物件
button.onclick = function(e) {
    console.log("目標元素:", e.target);
    console.log("當前元素:", e.currentTarget);
    console.log("事件類型:", e.type);
    console.log("座標:", e.clientX, e.clientY);
};

// 事件類型
document.onclick = function(e) {};        // 點擊
document.onmouseover = function(e) {};     // 滑鼠移入
document.onmouseout = function(e) {};      // 滑鼠移出
document.onkeydown = function(e) {};       // 鍵盤按下
document.onkeyup = function(e) {};         // 鍵盤放開
document.onload = function(e) {};          // 載入完成
document.onscroll = function(e) {};       // 滾動
document.onfocus = function(e) {};         // 獲得焦點
document.onblur = function(e) {};          // 失去焦點
document.onchange = function(e) {};       // 值改變
document.onsubmit = function(e) {};       // 表單提交
```

## 6.7 事件監聽

使用 addEventListener 綁定多個處理器。

[程式檔案：06-7-event-listener.js](../_code/06/06-7-event-listener.js)

```javascript
const button = document.querySelector("#myButton");

// addEventListener（支援多個處理器）
const handler1 = () => console.log("處理器 1");
const handler2 = () => console.log("處理器 2");

button.addEventListener("click", handler1);
button.addEventListener("click", handler2);

// 移除監聽
button.removeEventListener("click", handler1);

// 事件選項
button.addEventListener("click", handler, {
    capture: false,      // 是否在捕獲階段觸發
    once: false,         // 是否只觸發一次
    passive: false       // 是否承諾不呼叫 preventDefault
});

// once 選項
button.addEventListener("click", handler, { once: true });

// 事件委派（Event Delegation）
document.querySelector(".list").addEventListener("click", (e) => {
    if (e.target.classList.contains("item")) {
        console.log("點擊了:", e.target.textContent);
    }
});

// 練習：鍵盤事件
document.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        console.log("按下 Enter");
    }
    if (e.ctrlKey && e.key === "s") {
        e.preventDefault();
        console.log("Ctrl + S");
    }
});
```

## 6.8 事件傳遞

DOM 事件有三個階段：捕獲、目標、冒泡。

[程式檔案：06-8-event-propagation.js](../_code/06/06-8-event-propagation.js)

```javascript
// 事件傳遞順序
// 1. 捕獲階段（document -> target）
// 2. 目標階段（target）
// 3. 冒泡階段（target -> document）

// 停止傳遞
element.addEventListener("click", (e) => {
    e.stopPropagation();  // 停止向父元素傳遞
});

// 停止其他監聽器
element.addEventListener("click", (e) => {
    e.stopImmediatePropagation();  // 停止同元素的其他監聽器
});

// preventDefault
const link = document.querySelector("a");
link.addEventListener("click", (e) => {
    e.preventDefault();  // 阻止預設行為
    console.log("連結被點擊了，但不跳轉");
});

// 練習：點擊外部關閉彈窗
modal.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});

// 練習：避免事件重複觸發
let isProcessing = false;

button.addEventListener("click", async () => {
    if (isProcessing) return;
    isProcessing = true;
    
    try {
        await doSomething();
    } finally {
        isProcessing = false;
    }
});
```

## 6.9 表單處理

處理表單輸入和提交。

[程式檔案：06-9-form-handling.js](../_code/06/06-9-form-handling.js)

```javascript
const form = document.querySelector("#myForm");

// 監聽提交事件
form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    // 方式一：FormData
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    // 方式二：手動取值
    const name = form.name.value;
    const email = form.email.value;
    
    // 驗證
    if (!name || !email) {
        alert("請填寫所有欄位");
        return;
    }
    
    console.log("表單資料:", data);
});

// 即時驗證
const input = form.querySelector("input[name='email']");
input.addEventListener("input", (e) => {
    const value = e.target.value;
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    
    if (isValid) {
        e.target.classList.add("valid");
        e.target.classList.remove("invalid");
    } else {
        e.target.classList.add("invalid");
        e.target.classList.remove("valid");
    }
});

// 練習：即時字數統計
const textarea = form.querySelector("textarea");
const counter = document.querySelector(".counter");

textarea.addEventListener("input", () => {
    const length = textarea.value.length;
    counter.textContent = `${length}/200`;
    counter.classList.toggle("warning", length > 180);
});

// 練習：防重複提交
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = "提交中...";
    
    try {
        await submitForm(new FormData(form));
        alert("提交成功！");
    } catch (error) {
        alert("提交失敗");
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "提交";
    }
});
```

## 6.10 類名切換

實作常見的 UI 互動效果。

[程式檔案：06-10-class-toggle.js](../_code/06/06-10-class-toggle.js)

```javascript
// 折疊/展開
const accordionHeader = document.querySelectorAll(".accordion-header");

accordionHeader.forEach(header => {
    header.addEventListener("click", () => {
        const content = header.nextElementSibling;
        content.classList.toggle("active");
        header.classList.toggle("active");
    });
});

// 分頁切換
const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".tab-panel");

tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        const targetId = tab.dataset.tab;
        
        tabs.forEach(t => t.classList.remove("active"));
        panels.forEach(p => p.classList.remove("active"));
        
        tab.classList.add("active");
        document.getElementById(targetId).classList.add("active");
    });
});

// 下拉選單
const dropdown = document.querySelector(".dropdown");
const menu = dropdown.querySelector(".dropdown-menu");

dropdown.addEventListener("click", () => {
    menu.classList.toggle("show");
});

document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target)) {
        menu.classList.remove("show");
    }
});

// 練習：跑馬燈效果
const marquee = document.querySelector(".marquee");
let scrollPosition = 0;

function animateMarquee() {
    scrollPosition++;
    if (scrollPosition >= marquee.scrollWidth / 2) {
        scrollPosition = 0;
    }
    marquee.style.transform = `translateX(-${scrollPosition}px)`;
    requestAnimationFrame(animateMarquee);
}

animateMarquee();
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| getElementById | 根據 ID 選擇單一元素 |
| querySelector | CSS 選擇器選擇元素 |
| createElement | 建立新元素 |
| appendChild | 加入 DOM |
| addEventListener | 綁定事件監聽 |
| stopPropagation | 停止事件傳遞 |
| preventDefault | 阻止預設行為 |

## 練習題

1. 實作待辦事項清單（新增、刪除、完成）
2. 建立一個可折疊的手風琴元件
3. 實作圖片燈箱效果
4. 製作一個表單驗證系統
