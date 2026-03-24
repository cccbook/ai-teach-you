// 模組化

// math.js
// export function add(a, b) { return a + b; }
// export function subtract(a, b) { return a - b; }
// export const PI = 3.14159;
// export default function multiply(a, b) { return a * b; }

// main.js
import { add, subtract, PI } from './math.js';
import multiply from './math.js';

console.log("add:", add(2, 3));
console.log("subtract:", subtract(5, 3));
console.log("PI:", PI);
console.log("multiply:", multiply(3, 4));

// 重新命名導入
import { add as sum } from './math.js';
console.log("rename:", sum(1, 2));

// 導入所有
import * as math from './math.js';
console.log("all:", math.add(1, 2));

// 動態導入
async function loadModule() {
    let module = await import('./math.js');
    console.log("dynamic:", module.add(1, 2));
}

loadModule();

// 重新導出
// export { add, subtract } from './math.js';
// export default from './math.js';

// 模組作用域
// let moduleVar = "模組內的變數";
// export function getVar() { return moduleVar; }

// 絕對與相對路徑
// import axios from 'https://cdn.jsdelivr.net/npm/axios@0.21.1/dist/axios.esm.js';

// CommonJS vs ES Module
// Node.js 中可以使用 .mjs 或 "type": "module"

export function createAPI() {
    return {
        get: (url) => console.log("GET", url),
        post: (url, data) => console.log("POST", url, data)
    };
}

export default class API {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    request(endpoint) {
        return `${this.baseUrl}${endpoint}`;
    }
}