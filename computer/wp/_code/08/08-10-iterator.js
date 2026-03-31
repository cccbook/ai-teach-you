// 迭代器

// 可迭代物件
let array = [1, 2, 3];

// 使用迭代器
let iterator = array[Symbol.iterator]();
console.log("iterator.next():", iterator.next());
console.log("iterator.next():", iterator.next());
console.log("iterator.next():", iterator.next());
console.log("iterator.next():", iterator.next());

// 自訂迭代器
let range = {
    from: 1,
    to: 5,
    
    [Symbol.iterator]() {
        return {
            current: this.from,
            last: this.to,
            
            next() {
                if (this.current <= this.last) {
                    return { value: this.current++, done: false };
                }
                return { value: undefined, done: true };
            }
        };
    }
};

for (let num of range) {
    console.log("range:", num);
}

// 產生器函數
function* generator() {
    yield 1;
    yield 2;
    yield 3;
}

let gen = generator();
console.log("gen.next():", gen.next());
console.log("gen.next():", gen.next());
console.log("gen.next():", gen.next());

// 使用 for...of
for (let num of generator()) {
    console.log("for...of:", num);
}

// 產生器傳遞參數
function* calculator() {
    let result = yield 1;
    console.log("received:", result);
    yield result * 2;
}

let calc = calculator();
console.log("first:", calc.next());
console.log("second:", calc.next(10)); // 傳遞參數

// yield* 委派
function* numbers() {
    yield 1;
    yield 2;
}

function* letters() {
    yield "a";
    yield "b";
}

function* combined() {
    yield* numbers();
    yield* letters();
}

for (let item of combined()) {
    console.log("combined:", item);
}

// 無限序列
function* fibonacci() {
    let a = 0, b = 1;
    while (true) {
        yield a;
        [a, b] = [b, a + b];
    }
}

let fib = fibonacci();
console.log("fib:", fib.next().value);
console.log("fib:", fib.next().value);
console.log("fib:", fib.next().value);
console.log("fib:", fib.next().value);
console.log("fib:", fib.next().value);

// 練習：字串迭代器
let str = "hello";
let strIterator = str[Symbol.iterator]();

while (true) {
    let result = strIterator.next();
    if (result.done) break;
    console.log("char:", result.value);
}