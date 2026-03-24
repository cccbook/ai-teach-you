// 物件建立

// 物件字面量
let person1 = {
    name: "王小明",
    age: 25,
    greet: function() {
        return "Hello, I'm " + this.name;
    }
};

console.log("字面量:", person1.name);
console.log("方法:", person1.greet());

// 建構函數
function Person(name, age) {
    this.name = name;
    this.age = age;
    this.greet = function() {
        return "Hello, I'm " + this.name;
    };
}

let person2 = new Person("李小華", 30);
console.log("建構函數:", person2.name);

// Object.create()
let animal = {
    type: "動物",
    getType: function() {
        return this.type;
    }
};

let dog = Object.create(animal);
dog.type = "狗";
dog.breed = "黃金獵犬";

console.log("Object.create:", dog.type);
console.log("原型:", dog.getType());

// class 語法 (ES6)
class Car {
    constructor(brand, model) {
        this.brand = brand;
        this.model = model;
    }
    
    getInfo() {
        return `${this.brand} ${this.model}`;
    }
    
    static getCompany() {
        return "Car Company";
    }
}

let myCar = new Car("Toyota", "Camry");
console.log("class:", myCar.getInfo());
console.log("static:", Car.getCompany());

// 工廠函數
function createUser(name, role) {
    return {
        name: name,
        role: role,
        permissions: role === "admin" ? ["read", "write", "delete"] : ["read"]
    };
}

let user1 = createUser("admin", "admin");
let user2 = createUser("user", "user");
console.log("admin permissions:", user1.permissions);
console.log("user permissions:", user2.permissions);