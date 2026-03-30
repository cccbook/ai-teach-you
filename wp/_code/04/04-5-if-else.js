// 條件判斷：if-else

let score = 85;

// 簡單 if
if (score >= 60) {
    console.log("及格");
}

// if-else
if (score >= 60) {
    console.log("及格");
} else {
    console.log("不及格");
}

// if-else if-else
if (score >= 90) {
    console.log("優秀");
} else if (score >= 80) {
    console.log("良好");
} else if (score >= 70) {
    console.log("中等");
} else if (score >= 60) {
    console.log("及格");
} else {
    console.log("不及格");
}

// 巢狀 if
let age = 25;
let hasLicense = true;

if (age >= 18) {
    if (hasLicense) {
        console.log("可以開車");
    } else {
        console.log("需要考駕照");
    }
} else {
    console.log("年齡不足");
}

// 邏輯運算子簡化
if (age >= 18 && hasLicense) {
    console.log("可以開車 (簡化)");
}

// 真值與假值
let value = "";
if (value) {
    console.log("真值");
} else {
    console.log("假值"); // 輸出這個
}

value = "Hello";
if (value) {
    console.log("真值"); // 輸出這個
}

// 假值：false, 0, "", null, undefined, NaN