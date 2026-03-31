// 建立元素

// 建立新元素
let newDiv = document.createElement("div");
newDiv.textContent = "我是新元素";
newDiv.id = "new-div";
console.log("createElement:", newDiv);

// 建立帶屬性的元素
let link = document.createElement("a");
link.href = "https://example.com";
link.textContent = "點擊這裡";
link.target = "_blank";
console.log("createElement link:", link);

// 建立文字節點
let textNode = document.createTextNode("這是文字節點");
console.log("createTextNode:", textNode);

// 建立註解節點
let comment = document.createComment("這是註解");
console.log("createComment:", comment);

// 建立 DocumentFragment (效能更好)
let fragment = document.createDocumentFragment();
for (let i = 1; i <= 3; i++) {
    let item = document.createElement("li");
    item.textContent = `項目 ${i}`;
    fragment.appendChild(item);
}
console.log("fragment:", fragment);

// 將元素插入 DOM
let container = document.querySelector("#container");
container.appendChild(newDiv);

// 插入多個元素
let list = document.querySelector("#list");
list.appendChild(fragment);

// cloneNode (複製元素)
let original = document.querySelector(".original");
let clone = original.cloneNode(true); // true 包含子元素
clone.classList.add("cloned");
container.appendChild(clone);

// 另一種建立方式
let htmlString = "<p>HTML 字串</p>";
container.insertAdjacentHTML("beforeend", htmlString);