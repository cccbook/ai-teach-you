// for 迴圈

// 標準 for 迴圈
for (let i = 1; i <= 5; i++) {
    console.log("i =", i);
}

// for...in 迴圈 (遍歷索引)
let fruits = ["蘋果", "香蕉", "橘子"];
for (let index in fruits) {
    console.log(index, fruits[index]);
}

// for...of 遍歷 (ES6)
for (let fruit of fruits) {
    console.log(fruit);
}

// forEach 方法
fruits.forEach((fruit, index) => {
    console.log(index, fruit);
});

// 巢狀迴圈
for (let i = 1; i <= 3; i++) {
    for (let j = 1; j <= 3; j++) {
        console.log(`${i} x ${j} = ${i * j}`);
    }
}

// break 和 continue
for (let i = 1; i <= 10; i++) {
    if (i === 5) {
        console.log("遇到 5，跳出迴圈");
        break;
    }
    console.log(i);
}

console.log("---");

for (let i = 1; i <= 5; i++) {
    if (i === 3) {
        console.log("遇到 3，跳過");
        continue;
    }
    console.log(i);
}

// 計算總和
let sum = 0;
for (let i = 1; i <= 100; i++) {
    sum += i;
}
console.log("1+2+...+100 =", sum);

// 找最大值
let numbers = [3, 7, 2, 9, 5];
let max = numbers[0];
for (let i = 1; i < numbers.length; i++) {
    if (numbers[i] > max) {
        max = numbers[i];
    }
}
console.log("最大值:", max);