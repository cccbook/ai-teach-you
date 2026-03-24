# CSS

## 概述

CSS（Cascading Style Sheets，層疊樣式表）用於控制網頁的外觀和格式，包括顏色、版面、字體等。

## 歷史

- 1996 年：CSS1 發布
- 1998 年：CSS2 成為標準
- 2011 年：CSS3 模組化

## 核心概念

### 選擇器

選擇器用於選取要套用樣式的元素：

```css
/* 元素選擇器 */
p { color: blue; }

/* 類別選擇器 */
.highlight { background: yellow; }

/* ID 選擇器 */
#header { font-size: 24px; }

/* 複合選擇器 */
.container p { line-height: 1.6; }
```

### 盒模型

每個元素都是一個矩形「盒子」：

```css
.box {
    width: 200px;
    padding: 20px;
    border: 2px solid #333;
    margin: 10px;
}
```

### 優先級

當多個規則衝突時，優先級決定哪個生效：

1. `!important`
2. 行內樣式（`style` 屬性）
3. ID 選擇器
4. 類別/屬性/偽類選擇器
5. 元素選擇器

## 佈局系統

### Flexbox

一維佈局模型：

```css
.container {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

### Grid

二維佈局系統：

```css
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}
```

## 響應式設計

使用媒體查詢：

```css
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }
}
```

## 參考資源

- [MDN CSS 文件](https://developer.mozilla.org/zh-TW/docs/Web/CSS)
- [CSS Tricks](https://css-tricks.com/)
