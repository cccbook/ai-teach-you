// 類名切換

let element = document.querySelector("#myElement");

// 檢查 class
console.log("contains active:", element.classList.contains("active"));

// 切換 class
element.classList.toggle("active");
element.classList.toggle("highlight");

// 新增 class
element.classList.add("new-class", "another-class");

// 移除 class
element.classList.remove("old-class");

// 替換 class
element.classList.replace("old", "new");

// 使用 toggle 實現開關效果
let button = document.querySelector("#toggleBtn");
let box = document.querySelector("#box");

button.addEventListener("click", function() {
    box.classList.toggle("visible");
    box.classList.toggle("hidden");
});

// 多狀態切換
let tabs = document.querySelectorAll(".tab");

tabs.forEach(tab => {
    tab.addEventListener("click", function() {
        // 移除所有 tab 的 active
        tabs.forEach(t => t.classList.remove("active"));
        
        // 給目前點擊的 tab 加上 active
        this.classList.add("active");
    });
});

// 結合 CSS 實現動畫
let modal = document.querySelector("#modal");

function openModal() {
    modal.classList.remove("hidden");
    modal.classList.add("visible");
}

function closeModal() {
    modal.classList.remove("visible");
    setTimeout(() => {
        modal.classList.add("hidden");
    }, 300); // 等待動畫完成
}

// classList 操作技巧
let nav = document.querySelector("nav");

window.addEventListener("scroll", function() {
    if (window.scrollY > 50) {
        nav.classList.add("scrolled");
    } else {
        nav.classList.remove("scrolled");
    }
});

// 條件性 class
let card = document.querySelector(".card");
let isImportant = true;

if (isImportant) {
    card.classList.add("important");
}

card.classList.toggle("expanded", card.offsetWidth > 300);