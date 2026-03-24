// 修改元素

let element = document.querySelector("#myElement");

// 修改文字內容
element.textContent = "新文字內容";
element.innerText = "innerText 也可";

// 修改 HTML
element.innerHTML = "<strong>粗體</strong> 和 <em>斜體</em>";

// 修改屬性
element.setAttribute("data-id", "123");
element.id = "newId";
console.log("getAttribute:", element.getAttribute("data-id"));
console.log("dataset:", element.dataset);

// 移除屬性
element.removeAttribute("data-id");

// 修改樣式
element.style.color = "red";
element.style.backgroundColor = "#f0f0f0";
element.style.fontSize = "20px";
element.style.display = "none";

// 新增/移除 class
element.classList.add("active");
element.classList.remove("old");
element.classList.toggle("highlight");
console.log("classList contains:", element.classList.contains("active"));

// 修改 CSS 變數
element.style.setProperty("--bg-color", "blue");

// 取得/設定 data 屬性
element.dataset.userId = "456";
console.log("data-user-id:", element.dataset.userId);

// 修改 input 值
let input = document.querySelector("#myInput");
input.value = "新值";
console.log("input value:", input.value);

// 修改圖片
let img = document.querySelector("#myImg");
img.src = "new-image.jpg";
img.alt = "新圖片說明";