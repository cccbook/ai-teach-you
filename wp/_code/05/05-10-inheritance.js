// 繼承

// 原型鏈繼承
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    console.log(`${this.name} 發出聲音`);
};

function Dog(name, breed) {
    Animal.call(this, name);
    this.breed = breed;
}

Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.bark = function() {
    console.log(`${this.name} 叫: 汪汪!`);
};

let dog = new Dog("小白", "黃金獵犬");
dog.speak();
dog.bark();

// ES6 class 繼承
class Vehicle {
    constructor(brand, wheels) {
        this.brand = brand;
        this.wheels = wheels;
    }
    
    drive() {
        console.log(`${this.brand} 行駛中`);
    }
}

class Car extends Vehicle {
    constructor(brand, model) {
        super(brand, 4);
        this.model = model;
    }
    
    drive() {
        console.log(`${this.brand} ${this.model} 行駛中`);
    }
}

let car = new Car("Toyota", "Camry");
car.drive();

// 多層繼承
class ElectricCar extends Car {
    constructor(brand, model, battery) {
        super(brand, model);
        this.battery = battery;
    }
    
    charge() {
        console.log(`${this.brand} 充電中`);
    }
}

let tesla = new ElectricCar("Tesla", "Model 3", "75kWh");
tesla.drive();
tesla.charge();

// mixin (多重繼承替代方案)
const canSwim = {
    swim() {
        console.log(`${this.name} 游泳中`);
    }
};

const canFly = {
    fly() {
        console.log(`${this.name} 飛行中`);
    }
};

class Duck {
    constructor(name) {
        this.name = name;
    }
}

Object.assign(Duck.prototype, canSwim, canFly);

let duck = new Duck("唐老鴨");
duck.swim();
duck.fly();

// instanceof
console.log("instanceof:", dog instanceof Dog);
console.log("instanceof:", dog instanceof Animal);
console.log("instanceof:", car instanceof Car);
console.log("instanceof:", tesla instanceof ElectricCar);