// 陣列基礎

// 建立陣列
let fruits = ["蘋果", "香蕉", "橘子"];
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, "hello", true, null];
let empty = [];
let withConstructor = new Array(1, 2, 3);

console.log(fruits);
console.log(numbers);

// 存取元素 (索引從 0 開始)
console.log("第一個:", fruits[0]);
console.log("第三個:", fruits[2]);
console.log("倒數第一個:", fruits[fruits.length - 1]);

// 修改元素
fruits[1] = "葡萄";
console.log("修改後:", fruits);

// 陣列方法
fruits.push("草莓");           // 末尾新增
console.log("push:", fruits);

fruits.pop();                  // 末尾移除
console.log("pop:", fruits);

fruits.unshift("西瓜");        // 開頭新增
console.log("unshift:", fruits);

fruits.shift();                // 開頭移除
console.log("shift:", fruits);

// 搜尋
console.log("indexOf:", fruits.indexOf("橘子"));
console.log("includes:", fruits.includes("蘋果"));

// 合併
let arr1 = [1, 2];
let arr2 = [3, 4];
console.log("concat:", arr1.concat(arr2));

// 轉字串
console.log("join:", fruits.join(", "));

// 切片
console.log("slice:", fruits.slice(1, 3));

// 反轉
console.log("reverse:", [...fruits].reverse());

// 排序
let nums = [3, 1, 4, 1, 5, 9];
console.log("sort:", nums.sort());

// 迭代
numbers.forEach(num => console.log(num));

// map
let doubled = numbers.map(num => num * 2);
console.log("map:", doubled);

// filter
let evens = numbers.filter(num => num % 2 === 0);
console.log("filter:", evens);

// reduce
let sum = numbers.reduce((acc, num) => acc + num, 0);
console.log("reduce:", sum);