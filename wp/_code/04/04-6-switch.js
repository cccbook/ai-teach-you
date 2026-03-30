// switch 語句

let day = new Date().getDay();
let dayName;

switch (day) {
    case 0:
        dayName = "星期日";
        break;
    case 1:
        dayName = "星期一";
        break;
    case 2:
        dayName = "星期二";
        break;
    case 3:
        dayName = "星期三";
        break;
    case 4:
        dayName = "星期四";
        break;
    case 5:
        dayName = "星期五";
        break;
    case 6:
        dayName = "星期六";
        break;
    default:
        dayName = "未知";
}

console.log("今天是", dayName);

// 多個 case 合併
let grade = "B";

switch (grade) {
    case "A":
    case "B":
        console.log("表現良好");
        break;
    case "C":
        console.log("需要改進");
        break;
    case "D":
        console.log("不及格");
        break;
    default:
        console.log("無效成績");
}

// 使用表達式
let score = 85;

switch (true) {
    case score >= 90:
        console.log("優秀");
        break;
    case score >= 80:
        console.log("良好");
        break;
    case score >= 70:
        console.log("中等");
        break;
    default:
        console.log("其他");
}

// switch 的嚴格比較
let num = "5";

switch (num) {
    case 5:
        console.log("數字 5");
        break;
    case "5":
        console.log("字串 '5'");
        break;
}