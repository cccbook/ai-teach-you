// 事件監聽

let button = document.querySelector("#myButton");

// addEventListener (推薦方式)
button.addEventListener("click", function(event) {
    console.log("click 事件觸發");
    console.log("event type:", event.type);
    console.log("target:", event.target);
});

// 多個事件監聽器
button.addEventListener("click", function() {
    console.log("另一個監聽器");
});

// 命名函數
function handleMouseOver() {
    console.log("滑鼠移入");
}

button.addEventListener("mouseover", handleMouseOver);
button.removeEventListener("mouseover", handleMouseOver);

// 事件選項
button.addEventListener("click", function() {
    console.log("只執行一次");
}, { once: true });

// useCapture
parent.addEventListener("click", function() {
    console.log("父元素 (捕獲)");
}, true);

child.addEventListener("click", function() {
    console.log("子元素 (目標)");
});

parent.addEventListener("click", function() {
    console.log("父元素 (冒泡)");
}, false);

// 事件代理 (Event Delegation)
let list = document.querySelector("#list");

list.addEventListener("click", function(event) {
    if (event.target.tagName === "LI") {
        console.log("點擊:", event.target.textContent);
    }
});

// 阻止預設行為
let link = document.querySelector("#myLink");
link.addEventListener("click", function(event) {
    event.preventDefault();
    console.log("連結被阻止");
});

// 阻止事件冒泡
let childBtn = document.querySelector("#childBtn");
let parentDiv = document.querySelector("#parentDiv");

childBtn.addEventListener("click", function(event) {
    event.stopPropagation();
    console.log("子按鈕");
});

parentDiv.addEventListener("click", function() {
    console.log("父元素");
});