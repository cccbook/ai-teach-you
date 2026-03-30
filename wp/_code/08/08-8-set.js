// Set 集合

// 建立 Set
let set = new Set();

// 添加元素
set.add(1);
set.add(2);
set.add(3);
set.add(1); // 重複，會被忽略

console.log("Set:", set);
console.log("size:", set.size);

// 初始化 Set
let initialSet = new Set([1, 2, 3, 2, 1]);
console.log("Initial:", initialSet); // {1, 2, 3}

// has
console.log("has 2:", set.has(2));
console.log("has 5:", set.has(5));

// delete
set.delete(2);
console.log("after delete:", set);

// clear
set.clear();
console.log("after clear:", set);

// 遍歷 Set
let fruits = new Set(["apple", "banana", "orange"]);

for (let fruit of fruits) {
    console.log("fruit:", fruit);
}

fruits.forEach(fruit => {
    console.log("forEach:", fruit);
});

// 轉換為陣列
console.log("to array:", [...fruits]);
console.log("Array from:", Array.from(fruits));

// 使用 Set 去除重複
let numbers = [1, 2, 3, 2, 1, 4, 5, 3];
let unique = [...new Set(numbers)];
console.log("unique:", unique);

// 去除字串重複
let str = "hello";
let uniqueChars = [...new Set(str)];
console.log("unique chars:", uniqueChars.join(""));

// Set 方法
let set1 = new Set([1, 2, 3]);
let set2 = new Set([3, 4, 5]);

// union (聯集)
let union = new Set([...set1, ...set2]);
console.log("union:", [...union]);

// intersection (交集)
let intersection = [...set1].filter(x => set2.has(x));
console.log("intersection:", intersection);

// difference (差集)
let difference = [...set1].filter(x => !set2.has(x));
console.log("difference:", difference);

// symmetric difference (對稱差集)
let symmetric = [...set1].filter(x => !set2.has(x))
    .concat([...set2].filter(x => !set1.has(x)));
console.log("symmetric:", symmetric);

// 使用 Set 追蹤訪問
let visited = new Set();

function visit(page) {
    if (visited.has(page)) {
        console.log("已訪問:", page);
    } else {
        visited.add(page);
        console.log("新增訪問:", page);
    }
}

visit("home");
visit("about");
visit("home");
visit("contact");

console.log("總訪問:", visited.size);