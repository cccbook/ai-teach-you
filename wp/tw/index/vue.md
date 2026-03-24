# Vue.js

## 概述

Vue.js 是一個漸進式 JavaScript 框架，用於建立使用者介面。易於學習，可逐步整合到專案中。

## 核心概念

### 響應式系統

Vue 自動追蹤資料變化並更新 DOM：

```javascript
const { createApp, ref } = Vue;

createApp({
    setup() {
        const count = ref(0);
        const increment = () => count.value++;
        return { count, increment };
    },
    template: `
        <button @click="increment">
            Count: {{ count }}
        </button>
    `
}).mount('#app');
```

### 指令

- `v-bind`：屬性綁定
- `v-model`：雙向資料綁定
- `v-if/v-show`：條件渲染
- `v-for`：列表渲染
- `v-on`：事件處理

### 組件

```javascript
const ChildComponent = {
    props: ['message'],
    template: `<p>{{ message }}</p>`
};

createApp({
    components: { ChildComponent },
    data() {
        return { msg: 'Hello from parent' };
    }
});
```

## 生態系統

- **Vue Router**：客戶端路由
- **Pinia/Vuex**：狀態管理
- **Vite**：建構工具
- **Nuxt.js**：SSR/SSG 框架

## 參考資源

- [Vue.js 官方網站](https://vuejs.org/)
- [Vue.js 中文文檔](https://cn.vuejs.org/)
