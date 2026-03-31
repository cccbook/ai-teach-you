// 運算子

// 算術運算子
let a = 10, b = 3;
console.log("a + b =", a + b);   // 加
console.log("a - b =", a - b);   // 減
console.log("a * b =", a * b);   // 乘
console.log("a / b =", a / b);   // 除
console.log("a % b =", a % b);   // 取餘數
console.log("a ** b =", a ** b); // 指數

// 遞增/遞減
let c = 5;
console.log("c++ =", c++); // 先取值後遞增
console.log("c =", c);
console.log("++c =", ++c); // 先遞增後取值
console.log("--c =", --c); // 遞減

// 指派運算子
let x = 10;
x += 5;  // x = x + 5
console.log("x += 5:", x);
x -= 3;  // x = x - 3
console.log("x -= 3:", x);
x *= 2;  // x = x * 2
console.log("x *= 2:", x);

// 比較運算子
let y = 5;
console.log("y == 5:", y == 5);    // 相等
console.log("y === '5':", y === '5'); // 嚴格相等
console.log("y != 5:", y != 5);    // 不相等
console.log("y !== '5':", y !== '5'); // 嚴格不相等
console.log("y > 3:", y > 3);     // 大於
console.log("y < 10:", y < 10);   // 小於
console.log("y >= 5:", y >= 5);   // 大於等於
console.log("y <= 5:", y <= 5);   // 小於等於

// 邏輯運算子
let p = true, q = false;
console.log("p && q:", p && q);   // AND
console.log("p || q:", p || q);   // OR
console.log("!p:", !p);           // NOT

// 三元運算子
let age = 20;
let status = age >= 18 ? "成年人" : "未成年人";
console.log("status:", status);

// 空值合併運算子 (ES11)
let value = null ?? "預設值";
console.log("value:", value);