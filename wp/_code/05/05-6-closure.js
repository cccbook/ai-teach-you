// 閉包

// 基本閉包
function createCounter() {
    let count = 0;
    
    return function() {
        count++;
        return count;
    };
}

let counter = createCounter();
console.log(counter());
console.log(counter());
console.log(counter());

let counter2 = createCounter();
console.log("新的計數器:", counter2());

// 私有變數
function createPerson(name) {
    let _name = name;
    
    return {
        getName: function() {
            return _name;
        },
        setName: function(newName) {
            _name = newName;
        }
    };
}

let person = createPerson("王小明");
console.log(person.getName());
person.setName("李小華");
console.log(person.getName());

// 閉包記憶體
function createFunctions() {
    let functions = [];
    
    for (var i = 0; i < 3; i++) {
        functions.push(function() {
            console.log("i =", i);
        });
    }
    
    return functions;
}

let funcs = createFunctions();
funcs[0]();
funcs[1]();
funcs[2]();

// 使用 let 修正
function createFunctionsFixed() {
    let functions = [];
    
    for (let i = 0; i < 3; i++) {
        functions.push(function() {
            console.log("i =", i);
        });
    }
    
    return functions;
}

let funcsFixed = createFunctionsFixed();
funcsFixed[0]();
funcsFixed[1]();
funcsFixed[2]();

// 工廠函數
function createMultiplier(factor) {
    return function(number) {
        return number * factor;
    };
}

let double = createMultiplier(2);
let triple = createMultiplier(3);
console.log("double(10):", double(10));
console.log("triple(10):", triple(10));

// 計時器中的閉包
for (var i = 1; i <= 3; i++) {
    (function(index) {
        setTimeout(function() {
            console.log("計時器:", index);
        }, index * 1000);
    })(i);
}