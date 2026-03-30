// while 迴圈

// while 迴圈
let count = 0;
while (count < 5) {
    console.log("count =", count);
    count++;
}

// do-while 迴圈 (至少執行一次)
let num = 0;
do {
    console.log("num =", num);
    num++;
} while (num < 5);

// 無限迴圈 + break
let i = 0;
while (true) {
    console.log("i =", i);
    i++;
    if (i >= 3) {
        console.log("跳出");
        break;
    }
}

// 計算階乘
function factorial(n) {
    let result = 1;
    let counter = 1;
    while (counter <= n) {
        result *= counter;
        counter++;
    }
    return result;
}

console.log("5! =", factorial(5));

// 費波那契數列
function fibonacci(n) {
    let a = 0, b = 1;
    let result = [];
    for (let i = 0; i < n; i++) {
        result.push(a);
        let temp = a + b;
        a = b;
        b = temp;
    }
    return result;
}

console.log("費波那契數列:", fibonacci(10));

// while 找質數
function isPrime(num) {
    if (num <= 1) return false;
    let i = 2;
    while (i * i <= num) {
        if (num % i === 0) return false;
        i++;
    }
    return true;
}

console.log("7 是質數:", isPrime(7));
console.log("8 是質數:", isPrime(8));