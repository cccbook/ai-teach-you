// 事件綁定

let button = document.querySelector("#myButton");

// 行內事件處理 (不建議)
function handleClick() {
    console.log("按鈕被點擊");
}

// 傳統 DOM Level 0 事件
button.onclick = function(event) {
    console.log("onclick:", event);
    console.log("target:", event.target);
};

button.onmouseover = function(event) {
    console.log("滑鼠移入");
};

button.onmouseout = function(event) {
    console.log("滑鼠移出");
};

// 常用事件類型
let input = document.querySelector("#myInput");

input.onfocus = function() {
    console.log("獲得焦點");
};

input.onblur = function() {
    console.log("失去焦點");
};

input.onchange = function(event) {
    console.log("值改變:", event.target.value);
};

input.oninput = function(event) {
    console.log("輸入中:", event.target.value);
};

let form = document.querySelector("#myForm");

form.onsubmit = function(event) {
    event.preventDefault();
    console.log("表單提交");
};

// 鍵盤事件
document.onkeydown = function(event) {
    console.log("按下:", event.key);
    console.log("keyCode:", event.keyCode);
};

document.onkeyup = function(event) {
    console.log("放開:", event.key);
};

// 滑鼠事件
document.onmousedown = function(event) {
    console.log("滑鼠按下:", event.button);
};

document.onmouseup = function(event) {
    console.log("滑鼠放開");
};

document.onmousemove = function(event) {
    // console.log("移動:", event.clientX, event.clientY);
};

// 視窗事件
window.onload = function() {
    console.log("頁面載入完成");
};

window.onresize = function() {
    console.log("視窗大小改變");
};

window.onscroll = function() {
    console.log("滾動");
};