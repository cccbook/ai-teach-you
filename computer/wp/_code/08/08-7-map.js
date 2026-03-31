// Map 集合

// 建立 Map
let map = new Map();

// 添加元素
map.set("name", "王小明");
map.set("age", 25);
map.set(true, "布林鍵");

console.log("Map:", map);

// 取得元素
console.log("get name:", map.get("name"));
console.log("get missing:", map.get("missing"));

// 檢查存在
console.log("has age:", map.has("age"));
console.log("has city:", map.has("city"));

// 大小
console.log("size:", map.size);

// 刪除
map.delete("age");
console.log("after delete:", map.size);

// 清除所有
map.clear();
console.log("after clear:", map.size);

// 初始化 Map
let userMap = new Map([
    ["id", 1],
    ["name", "小明"],
    ["email", "test@example.com"]
]);

console.log("Init map:", userMap);

// 遍歷 Map
for (let [key, value] of userMap) {
    console.log(`${key}: ${value}`);
}

userMap.forEach((value, key) => {
    console.log(`${key} = ${value}`);
});

// keys
for (let key of userMap.keys()) {
    console.log("key:", key);
}

// values
for (let value of userMap.values()) {
    console.log("value:", value);
}

// entries
for (let [key, value] of userMap.entries()) {
    console.log("entry:", key, value);
}

// 轉換為陣列
console.log("to array:", [...userMap]);
console.log("keys array:", [...userMap.keys()]);
console.log("values array:", [...userMap.values()]);

// Map 中的物件
let objKey = { id: 1 };
map.set(objKey, "Object value");
console.log("obj value:", map.get(objKey));

// 練習：計數器
function countChars(str) {
    let counts = new Map();
    for (let char of str) {
        counts.set(char, (counts.get(char) || 0) + 1);
    }
    return counts;
}

console.log("count:", countChars("hello"));