// JSON 解析

// JSON.stringify - 物件轉字串
let user = {
    name: "王小明",
    age: 25,
    hobbies: ["coding", "reading"],
    address: {
        city: "台北",
        street: "忠孝東路"
    }
};

let jsonString = JSON.stringify(user);
console.log("stringify:", jsonString);

// 格式化輸出
let formatted = JSON.stringify(user, null, 2);
console.log("formatted:", formatted);

// 自訂 replacer
let replacer = function(key, value) {
    if (key === "age") {
        return undefined; // 隱藏 age
    }
    return value;
};

console.log("replacer:", JSON.stringify(user, replacer));

// JSON.parse - 字串轉物件
let jsonData = '{"name":"李小華","age":30}';
let parsed = JSON.parse(jsonData);
console.log("parse:", parsed);

// 解析帶有函數的情況（不安全）
// let withFunction = '{"name":"test","func":function(){ return 1; }}';
// let parsedFunc = JSON.parse(withFunction); // 函數會被移除

// 處理 Date 物件
let dateObj = new Date();
let dateJson = JSON.stringify(dateObj);
let parsedDate = JSON.parse(dateJson);
let dateBack = new Date(parsedDate);
console.log("Date:", dateBack);

// 大數字問題
let bigNumber = { num: BigInt(9007199254740991) };
let bigJson = JSON.stringify(bigNumber);
console.log("BigInt JSON:", bigJson);

// 巢狀物件解析
let nested = {
    company: {
        employees: [
            { name: "小明", role: "工程師" },
            { name: "小華", role: "設計師" }
        ]
    }
};

let nestedJson = JSON.stringify(nested);
let nestedParsed = JSON.parse(nestedJson);
console.log("Employee:", nestedParsed.company.employees[0].name);

// 錯誤處理
function safeJsonParse(str) {
    try {
        return { success: true, data: JSON.parse(str) };
    } catch (e) {
        return { success: false, error: e.message };
    }
}

console.log(safeJsonParse('{"valid":true}'));
console.log(safeJsonParse('invalid'));

// 深度拷貝
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

let original = { a: 1, b: { c: 2 } };
let clone = deepClone(original);
clone.b.c = 3;
console.log("Original:", original.b.c);
console.log("Clone:", clone.b.c);