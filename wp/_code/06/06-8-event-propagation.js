// 事件傳遞

// 事件傳遞三個階段
// 1. 捕獲階段 (Capturing) - 從根節點往下
// 2. 目標階段 (Target) - 目標元素
// 3. 冒泡階段 (Bubbling) - 從目標往上

// DOM 結構:
// <div id="grandparent">
//   <div id="parent">
//     <button id="child">Click</button>
//   </div>
// </div>

let grandparent = document.querySelector("#grandparent");
let parent = document.querySelector("#parent");
let child = document.querySelector("#child");

// 捕獲階段 (useCapture = true)
grandparent.addEventListener("click", function() {
    console.log("Grandparent - Capturing");
}, true);

parent.addEventListener("click", function() {
    console.log("Parent - Capturing");
}, true);

child.addEventListener("click", function() {
    console.log("Child - Target (Capturing)");
}, true);

// 目標階段後的冒泡
child.addEventListener("click", function() {
    console.log("Child - Target (Bubbling)");
}, false);

parent.addEventListener("click", function() {
    console.log("Parent - Bubbling");
}, false);

grandparent.addEventListener("click", function() {
    console.log("Grandparent - Bubbling");
}, false);

// stopPropagation - 阻止繼續傳遞
child.addEventListener("click", function(event) {
    event.stopPropagation();
    console.log("Child - Stop Propagation");
});

// stopImmediatePropagation - 阻止同元素其他監聽器
child.addEventListener("click", function(event) {
    console.log("第一個監聽器");
});

child.addEventListener("click", function(event) {
    event.stopImmediatePropagation();
    console.log("第二個監聽器 (停止)");
});

child.addEventListener("click", function() {
    console.log("第三個監聽器 (不會執行)");
});

// preventDefault - 阻止預設行為
let link = document.querySelector("a");
link.addEventListener("click", function(event) {
    event.preventDefault();
    console.log("連結預設行為被阻止");
});