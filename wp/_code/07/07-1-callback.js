// 回調函數

// 基本回調範例
function calculate(a, b, callback) {
    console.log("計算中...");
    let result = callback(a, b);
    return result;
}

let sum = calculate(5, 3, function(a, b) {
    return a + b;
});
console.log("sum:", sum);

let product = calculate(4, 5, function(a, b) {
    return a * b;
});
console.log("product:", product);

// 常見的回調場景：陣列方法
let numbers = [1, 2, 3, 4, 5];

numbers.forEach(function(num) {
    console.log("forEach:", num);
});

let doubled = numbers.map(function(num) {
    return num * 2;
});
console.log("map:", doubled);

let evens = numbers.filter(function(num) {
    return num % 2 === 0;
});
console.log("filter:", evens);

let total = numbers.reduce(function(acc, num) {
    return acc + num;
}, 0);
console.log("reduce:", total);

// 錯誤優先回調 (Error-First Callback)
function readFile(filename, callback) {
    if (!filename) {
        callback(new Error("Filename is required"), null);
        return;
    }
    
    let content = "File content of " + filename;
    callback(null, content);
}

readFile("test.txt", function(err, content) {
    if (err) {
        console.error("Error:", err.message);
        return;
    }
    console.log("Content:", content);
});

readFile("", function(err, content) {
    if (err) {
        console.error("Error:", err.message);
        return;
    }
    console.log("Content:", content);
});

// 巢狀回調 (Callback Hell)
function getData(param, callback) {
    setTimeout(function() {
        let data = param.toUpperCase();
        callback(null, data);
    }, 1000);
}

getData("hello", function(err, result) {
    if (err) {
        console.error(err);
        return;
    }
    console.log("第一階段:", result);
    
    getData(result + " world", function(err, result) {
        if (err) {
            console.error(err);
            return;
        }
        console.log("第二階段:", result);
        
        getData(result + "!!!", function(err, result) {
            if (err) {
                console.error(err);
                return;
            }
            console.log("第三階段:", result);
        });
    });
});