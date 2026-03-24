// DOM 遍歷

// HTML 結構:
// <div id="parent">
//   <p class="child">Child 1</p>
//   <p class="child">Child 2</p>
//   <p class="child">Child 3</p>
// </div>

let parent = document.querySelector("#parent");

// 遍歷方法
console.log("children:", parent.children);
console.log("childNodes:", parent.childNodes);

console.log("firstChild:", parent.firstChild);
console.log("lastChild:", parent.lastChild);
console.log("firstElementChild:", parent.firstElementChild);
console.log("lastElementChild:", parent.lastElementChild);

// 遍歷兄弟姐妹
let child = document.querySelector(".child");
console.log("nextSibling:", child.nextSibling);
console.log("previousSibling:", child.previousSibling);
console.log("nextElementSibling:", child.nextElementSibling);
console.log("previousElementSibling:", child.previousElementSibling);

// 遍歷父節點
console.log("parentNode:", child.parentNode);
console.log("parentElement:", child.parentElement);

// 遍歷祖先
let grandParent = child.closest(".container");
console.log("closest:", grandParent);

// 遍歷所有子元素
Array.from(parent.children).forEach((el, index) => {
    console.log(`child ${index}:`, el.textContent);
});

// 判斷元素關係
console.log("contains:", parent.contains(child));
console.log("contains self:", parent.contains(parent));