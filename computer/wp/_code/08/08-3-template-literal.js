// 模板字串

// 基本用法
let name = "王小明";
let greeting = `Hello, ${name}!`;
console.log("Basic:", greeting);

// 多行字串
let multiLine = `
    第一行
    第二行
    第三行
`;
console.log("Multi-line:", multiLine);

// 嵌入表達式
let a = 5, b = 3;
let result = `${a} + ${b} = ${a + b}`;
console.log("Expression:", result);

// 呼叫函數
function uppercase(str) {
    return str.toUpperCase();
}
let funcResult = `${uppercase("hello")} world`;
console.log("Function:", funcResult);

// 條件判斷
let score = 85;
let grade = `分數: ${score}, 等級: ${score >= 60 ? "及格" : "不及格"}`;
console.log("Condition:", grade);

// 巢狀模板
let inner = "內層";
let outer = `外層 ${`包含 ${inner}`}`;
console.log("Nested:", outer);

// 標籤模板 (Tagged Template)
function tag(strings, ...values) {
    console.log("Strings:", strings);
    console.log("Values:", values);
    return "Tagged result";
}

let tagged = tag`Hello ${name}, you have ${5} messages`;
console.log("Tagged:", tagged);

// HTML 生成
let items = ["蘋果", "香蕉", "橘子"];
let html = `
<ul>
    ${items.map(item => `<li>${item}</li>`).join("")}
</ul>
`;
console.log("HTML:", html);

// 原始字串 (raw)
let raw = String.raw`Hello\nWorld`;
console.log("Raw:", raw);

// 數字格式化
let price = 1234.567;
let formatted = `價格: $${price.toFixed(2)}`;
console.log("Format:", formatted);

// 國際化
let date = new Date();
let dateStr = `今天日期: ${date.toLocaleDateString()}`;
console.log("Date:", dateStr);