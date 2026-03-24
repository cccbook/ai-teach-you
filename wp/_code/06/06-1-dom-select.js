// DOM 選擇

// HTML: <h1 id="title" class="heading">Hello</h1>
// <p class="content">Paragraph</p>
// <p class="content">Another</p>

// 透過 ID 選擇 (回傳單一元素)
let title = document.getElementById("title");
console.log("getElementById:", title);

// 透過 Class 選擇 (回傳 HTMLCollection)
let paragraphs = document.getElementsByClassName("content");
console.log("getElementsByClassName:", paragraphs);
console.log("length:", paragraphs.length);

// 透過 Tag 選擇 (回傳 HTMLCollection)
let allParagraphs = document.getElementsByTagName("p");
console.log("getElementsByTagName:", allParagraphs);

// querySelector (回傳第一個符合的單一元素)
let firstContent = document.querySelector(".content");
console.log("querySelector:", firstContent);

let firstP = document.querySelector("p");
console.log("querySelector p:", firstP);

// querySelectorAll (回傳 NodeList)
let allContent = document.querySelectorAll(".content");
console.log("querySelectorAll:", allContent);
console.log("forEach:");
allContent.forEach(p => console.log(p));

// 選擇 body
let body = document.body;
console.log("body:", body);

// 選擇 head
let head = document.head;
console.log("head:", head);

// 選擇元素內的選擇器
let container = document.querySelector("#container");
let child = container.querySelector(".child");
console.log("子選擇:", child);