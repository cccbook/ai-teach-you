# Angular

## 概述

Angular 是 Google 開發的完整前端框架，用於建立企業級 Web 應用。提供完整的開發工具和最佳實踐。

## 核心概念

### 模組化

```typescript
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';

@NgModule({
    declarations: [AppComponent],
    imports: [BrowserModule],
    bootstrap: [AppComponent]
})
export class AppModule {}
```

### 元件

```typescript
import { Component } from '@angular/core';

@Component({
    selector: 'app-root',
    template: `
        <h1>{{ title }}</h1>
        <button (click)="onClick()">點擊</button>
    `
})
export class AppComponent {
    title = 'My Angular App';
    
    onClick() {
        console.log('Clicked!');
    }
}
```

### 服務與依賴注入

```typescript
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class DataService {
    getData() {
        return ['item1', 'item2', 'item3'];
    }
}
```

## 特性

- **TypeScript 原生支援**
- **強類型檢查**
- **RxJS 反應式編程**
- **完整的測試工具**
- **CLI 命令列工具**

## 參考資源

- [Angular 官方網站](https://angular.io/)
- [Angular 中文文檔](https://angular.cn/)
