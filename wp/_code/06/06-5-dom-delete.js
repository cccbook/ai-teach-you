// 刪除元素

let element = document.querySelector("#elementToRemove");

// 移除自身
element.remove();

// 移除子元素 (方法 1)
let parent = document.querySelector("#parent");
while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
}

// 移除子元素 (方法 2)
let container = document.querySelector("#container");
container.innerHTML = "";

// 移除特定子元素
let list = document.querySelector("#list");
let items = list.querySelectorAll("li");
items.forEach((item, index) => {
    if (index % 2 === 0) {
        item.remove();
    }
});

// 移除所有符合條件的元素
let allCards = document.querySelectorAll(".card");
allCards.forEach(card => {
    if (card.dataset.status === "inactive") {
        card.remove();
    }
});

// replaceWith (替換元素)
let oldElement = document.querySelector(".old");
let newElement = document.createElement("div");
newElement.textContent = "新元素";
oldElement.replaceWith(newElement);

// replaceChild (父元素方法)
let parent = document.querySelector("#parent");
let newNode = document.createElement("p");
newNode.textContent = "新段落";
let oldNode = parent.querySelector("p");
parent.replaceChild(newNode, oldNode);

// 清空元素的所有屬性
let element = document.querySelector("#keepElement");
element.removeAttribute("id");
element.removeAttribute("class");
element.style = "";