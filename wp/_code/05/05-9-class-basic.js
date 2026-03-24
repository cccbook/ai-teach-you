// 類別基礎

class Animal {
    // 建構函數
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    // 方法
    speak() {
        console.log(`${this.name} 發出聲音`);
    }
    
    getInfo() {
        return `${this.name}, ${this.age} 歲`;
    }
    
    // 靜態方法
    static create(name) {
        return new Animal(name, 0);
    }
}

let animal = new Animal("小狗", 3);
console.log(animal.getInfo());
animal.speak();

let baby = Animal.create("小貓");
console.log("static:", baby.name);

// 繼承
class Dog extends Animal {
    constructor(name, age, breed) {
        super(name, age); // 呼叫父類別建構函數
        this.breed = breed;
    }
    
    speak() {
        console.log(`${this.name} 叫: 汪汪!`);
    }
    
    fetch() {
        console.log(`${this.name} 撿球`);
    }
}

let dog = new Dog("小白", 5, "黃金獵犬");
dog.speak();
dog.fetch();
console.log("breed:", dog.breed);

// Getter 和 Setter
class Rectangle {
    constructor(width, height) {
        this._width = width;
        this._height = height;
    }
    
    get width() {
        return this._width;
    }
    
    set width(value) {
        if (value > 0) this._width = value;
    }
    
    get area() {
        return this._width * this._height;
    }
}

let rect = new Rectangle(10, 5);
console.log("width:", rect.width);
console.log("area:", rect.area);
rect.width = 20;
console.log("new width:", rect.width);

// 私有欄位 (ES2022)
class Counter {
    #count = 0;
    
    increment() {
        this.#count++;
    }
    
    getCount() {
        return this.#count;
    }
}

let counter = new Counter();
counter.increment();
counter.increment();
console.log("count:", counter.getCount());
// console.log(counter.#count); // 錯誤