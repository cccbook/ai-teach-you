// 物件基礎

// 建立物件
let person = {
    name: "王小明",
    age: 25,
    city: "台北",
    isStudent: true
};

console.log(person);

// 存取屬性
console.log("name:", person.name);
console.log("age:", person["age"]);

// 修改屬性
person.age = 30;
person["email"] = "wang@example.com";
console.log("修改後:", person);

// 刪除屬性
delete person.isStudent;
console.log("刪除後:", person);

// 檢查屬性存在
console.log("hasOwnProperty:", person.hasOwnProperty("name"));
console.log("in:", "age" in person);

// 取得所有鍵/值
console.log("keys:", Object.keys(person));
console.log("values:", Object.values(person));
console.log("entries:", Object.entries(person));

// 巢狀物件
let company = {
    name: "ABC 公司",
    address: {
        city: "台北",
        street: "忠孝東路"
    },
    employees: [
        { name: "小明", age: 25 },
        { name: "小華", age: 30 }
    ]
};

console.log("城市:", company.address.city);
console.log("第一個員工:", company.employees[0].name);

// 物件方法
let obj1 = { a: 1 };
let obj2 = { b: 2 };
let merged = Object.assign({}, obj1, obj2);
console.log("assign:", merged);

// 淺拷貝
let clone = Object.assign({}, person);
let clone2 = { ...person };

// 物件解構
let { name, age } = person;
console.log("解構:", name, age);