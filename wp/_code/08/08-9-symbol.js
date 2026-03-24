// Symbol

// 建立 Symbol
let sym1 = Symbol();
let sym2 = Symbol("description");
let sym3 = Symbol("description");

console.log("sym1:", sym1);
console.log("sym2:", sym2);
console.log("sym2 === sym3:", sym2 === sym3); // false

// 使用 Symbol 作為物件屬性
let obj = {
    [Symbol("id")]: 1,
    name: "王小明"
};

console.log("obj:", obj);

// Symbol 不能用 for...in 遍歷
for (let key in obj) {
    console.log("for...in:", key); // 只會顯示 name
}

// Object.getOwnPropertySymbols
let symbols = Object.getOwnPropertySymbols(obj);
console.log("symbols:", symbols);

// 全域 Symbol 註冊表
let globalSym = Symbol.for("global");
let globalSym2 = Symbol.for("global");
console.log("global ===:", globalSym === globalSym2);

// Symbol.keyFor
console.log("keyFor:", Symbol.keyFor(globalSym));

// 內建 Symbol
console.log("Symbol.iterator:", Symbol.iterator);
console.log("Symbol.toStringTag:", Symbol.toStringTag);

// 自訂迭代器
let collection = {
    items: [1, 2, 3],
    [Symbol.iterator]() {
        let index = 0;
        return {
            next: () => {
                return index < this.items.length
                    ? { value: this.items[index++], done: false }
                    : { value: undefined, done: true };
            }
        };
    }
};

for (let item of collection) {
    console.log("item:", item);
}

// 避免屬性衝突
function createObj() {
    return {
        [Symbol.for("private")]: "secret"
    };
}

let privateSym = Symbol.for("private");
let obj = createObj();
console.log("private:", obj[privateSym]);

// Symbol 作為常數
const STATUS = {
    PENDING: Symbol("pending"),
    FULFILLED: Symbol("fulfilled"),
    REJECTED: Symbol("rejected")
};

let currentStatus = STATUS.PENDING;
console.log("status:", currentStatus);