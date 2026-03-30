// 物件方法

let person = {
    name: "王小明",
    age: 25,
    city: "台北"
};

console.log("keys:", Object.keys(person));
console.log("values:", Object.values(person));
console.log("entries:", Object.entries(person));

// 遍歷
Object.keys(person).forEach(key => {
    console.log(`${key}: ${person[key]}`);
});

Object.entries(person).forEach(([key, value]) => {
    console.log(`${key} = ${value}`);
});

// 合併物件
let obj1 = { a: 1, b: 2 };
let obj2 = { b: 3, c: 4 };
let merged = Object.assign({}, obj1, obj2);
console.log("merged:", merged);

// 淺拷貝
let clone = Object.assign({}, person);
let clone2 = { ...person };

// 深拷貝
let deepClone = JSON.parse(JSON.stringify(person));

// 屬性描述符
let descriptor = Object.getOwnPropertyDescriptor(person, "name");
console.log("descriptor:", descriptor);

// 定義屬性
Object.defineProperty(person, "name", {
    writable: false,
    configurable: false,
    enumerable: true
});

// person.name = "新名字"; // 嚴格模式會報錯
console.log("name:", person.name);

// seal 和 freeze
let sealed = { a: 1 };
Object.seal(sealed);
sealed.a = 2;
// sealed.b = 3; // 錯誤
console.log("sealed:", sealed);

let frozen = { a: 1 };
Object.freeze(frozen);
// frozen.a = 2; // 嚴格模式報錯
console.log("frozen:", frozen);

// hasOwnProperty
console.log("hasOwnProperty:", person.hasOwnProperty("name"));
console.log("hasOwnProperty:", person.hasOwnProperty("toString"));

// 物件的 this
let obj = {
    value: 100,
    getValue: function() {
        return this.value;
    }
};

console.log("getValue:", obj.getValue());

let fn = obj.getValue;
console.log("fn():", fn()); // undefined

console.log("fn.call():", fn.call({ value: 200 }));