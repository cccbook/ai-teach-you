# 第 2 章：CSS 基礎

## 概述

CSS（Cascading Style Sheets，層疊樣式表）用於控制網頁的外觀和格式。本章介紹 CSS 的基本語法、三種引入方式、選擇器，以及最重要的盒模型概念。

## 2.1 行內樣式

行內樣式直接寫在 HTML 元素的 `style` 屬性中，優先級最高，但不利於維護。

[程式檔案：02-1-inline-style.html](../_code/02/02-1-inline-style.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>行內樣式範例</title>
</head>
<body>
    <h1 style="color: blue; font-size: 24px;">這是行內樣式標題</h1>
    <p style="color: red; font-size: 16px;">這是行內樣式的段落。</p>
    <div style="background-color: yellow; padding: 20px;">
        這是行內樣式的 div
    </div>
    <span style="font-weight: bold; font-style: italic;">粗體斜體文字</span>
</body>
</html>
```

**何時使用行內樣式：**
- 測試或快速原型
- 需要覆寫外部樣式時
- 郵件模板（大多數郵件客戶端只支援行內樣式）

## 2.2 內部 CSS

使用 `<style>` 標籤將 CSS 寫在 HTML 文件的 `<head>` 區塊，適合單一頁面使用。

[程式檔案：02-2-internal-css.html](../_code/02/02-2-internal-css.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>內部 CSS 範例</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        
        h1 {
            color: #333;
            border-bottom: 2px solid #333;
        }
        
        p {
            line-height: 1.6;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>內部 CSS 標題</h1>
    <p>這段文字使用了內部定義的樣式。</p>
</body>
</html>
```

## 2.3 外部 CSS

最佳實踐是將 CSS 寫在獨立的 `.css` 檔案中，然後通過 `<link>` 標籤引入。

[程式檔案：02-3-external-css.html](../_code/02/02-3-external-css.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>外部 CSS 範例</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>外部 CSS 標題</h1>
    <p>這個頁面的樣式來自外部 CSS 檔案。</p>
</body>
</html>
```

外部 CSS 檔案（styles.css）：

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
}

h1 {
    color: #2c3e50;
}

p {
    color: #7f8c8d;
}
```

## 2.4 CSS 選擇器

選擇器用於選取要套用樣式的 HTML 元素。

[程式檔案：02-4-selectors.html](../_code/02/02-4-selectors.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>CSS 選擇器範例</title>
    <style>
        /* 元素選擇器 */
        p {
            color: blue;
        }
        
        /* 類別選擇器 */
        .highlight {
            background-color: yellow;
        }
        
        /* ID 選擇器 */
        #header {
            background-color: #333;
            color: white;
            padding: 10px;
        }
        
        /* 複合選擇器 */
        .content p {
            font-size: 16px;
        }
        
        /* 偽類選擇器 */
        a:hover {
            color: red;
        }
        
        /* 萬用選擇器 */
        * {
            box-sizing: border-box;
        }
    </style>
</head>
<body>
    <div id="header">這是 ID 選擇器 (header)</div>
    <p>這是一般段落 (元素選擇器)</p>
    <p class="highlight">這是類別選擇器 (highlight)</p>
    <a href="#">連結 (偽類 :hover)</a>
    <div class="content">
        <p>這是 content 裡面的段落 (複合選擇器)</p>
    </div>
</body>
</html>
```

**選擇器優先級（由高到低）：**
1. `!important`
2. 行內樣式（`style` 屬性）
3. ID 選擇器（`#id`）
4. 類別選擇器（`.class`）、屬性選擇器（`[attr]`）、偽類（`:hover`）
5. 元素選擇器（`p`、`div`）
6. 萬用選擇器（`*`）

## 2.5 選擇器優先級

當多個規則套用到同一元素時，CSS 會根據優先級決定哪個規則生效。

[程式檔案：02-5-specificity.html](../_code/02/02-5-specificity.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>選擇器優先級範例</title>
    <style>
        /* 優先級計算：0-0-1 */
        p {
            color: blue;
        }
        
        /* 優先級計算：0-1-0 */
        .text {
            color: red;
        }
        
        /* 優先級計算：1-0-0 */
        #unique {
            color: green;
        }
        
        /* 優先級計算：0-2-1 */
        .content p.title {
            color: purple;
        }
    </style>
</head>
<body>
    <p id="unique" class="text content">這個段落會是什麼顏色？</p>
</body>
</html>
```

**優先級計算方式：**
- ID 選擇器：100 分
- 類別、屬性、偽類：10 分
- 元素、偽元素：1 分
- 分數最高的規則生效

## 2.6 盒模型

盒模型是 CSS 的核心概念，每個 HTML 元素都被視為一個矩形的「盒子」。

[程式檔案：02-6-box-model.html](../_code/02/02-6-box-model.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>盒模型範例</title>
    <style>
        .box {
            width: 200px;
            padding: 20px;
            border: 5px solid #333;
            margin: 20px;
            background-color: #f0f0f0;
        }
        
        .box-content {
            box-sizing: content-box;
        }
        
        .box-border {
            box-sizing: border-box;
        }
    </style>
</head>
<body>
    <h1>盒模型範例</h1>
    
    <h2>content-box (預設)</h2>
    <div class="box box-content">
        寬度: 200px + padding(40) + border(10) = 250px
    </div>
    
    <h2>border-box</h2>
    <div class="box box-border">
        寬度: 200px (包含 padding 和 border)
    </div>
    
    <h2>盒模型說明</h2>
    <pre>
┌─────────────────────────┐
│      margin (外邊距)      │
├─────────────────────────┤
│      border (邊框)       │
├─────────────────────────┤
│     padding (內邊距)     │
├─────────────────────────┤
│     content (內容)       │
└─────────────────────────┘
    </pre>
</body>
</html>
```

## 2.7 margin 與 padding

`margin` 控制元素外部的空間，`padding` 控制元素內部內容與邊框的距離。

[程式檔案：02-7-margin-padding.html](../_code/02/02-7-margin-padding.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>margin 與 padding 範例</title>
    <style>
        .box {
            background-color: #3498db;
            color: white;
            padding: 20px;
            margin: 30px;
        }
        
        .shorthand {
            /* 四個值：上右下左 */
            padding: 10px 20px 30px 40px;
            margin: 10px 20px 30px 40px;
        }
        
        .two-values {
            /* 兩個值：上下 左右 */
            padding: 10px 20px;
            margin: 10px 20px;
        }
        
        .three-values {
            /* 三個值：上 左右 下 */
            padding: 10px 20px 30px;
            margin: 10px 20px 30px;
        }
        
        .auto-margin {
            /* 水平置中 */
            margin: 0 auto;
            width: 300px;
        }
    </style>
</head>
<body>
    <div class="box">一般 margin 和 padding</div>
    <div class="box shorthand">四個值 shorthand</div>
    <div class="box two-values">兩個值 shorthand</div>
    <div class="box auto-margin">水平置中（auto margin）</div>
</body>
</html>
```

## 2.8 邊框與陰影

邊框和陰影讓元素更具視覺層次感。

[程式檔案：02-8-border.html](../_code/02/02-8-border.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>邊框與陰影範例</title>
    <style>
        .box {
            width: 200px;
            padding: 20px;
            margin: 20px;
            background-color: white;
        }
        
        .border-solid {
            border: 3px solid #333;
        }
        
        .border-dashed {
            border: 3px dashed #e74c3c;
        }
        
        .border-radius {
            border: 3px solid #3498db;
            border-radius: 15px;
        }
        
        .shadow {
            border: 1px solid #ddd;
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .shadow-inset {
            border: 1px solid #ddd;
            box-shadow: inset 3px 3px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="box border-solid">實線邊框</div>
    <div class="box border-dashed">虛線邊框</div>
    <div class="box border-radius">圓角邊框</div>
    <div class="box shadow">外陰影</div>
    <div class="box shadow-inset">內陰影</div>
</body>
</html>
```

## 2.9 顏色與背景

CSS 提供多種方式定義顏色，以及豐富的背景樣式設定。

[程式檔案：02-9-colors.html](../_code/02/02-9-colors.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>顏色與背景範例</title>
    <style>
        .color-examples {
            padding: 20px;
            margin: 10px;
        }
        
        .named-color {
            background-color: coral;
            color: white;
        }
        
        .hex-color {
            background-color: #3498db;
            color: white;
        }
        
        .rgb-color {
            background-color: rgb(155, 89, 182);
            color: white;
        }
        
        .rgba-color {
            background-color: rgba(52, 152, 219, 0.5);
        }
        
        .linear-gradient {
            background: linear-gradient(45deg, #3498db, #9b59b6);
            color: white;
        }
        
        .image-bg {
            background-image: url('bg.jpg');
            background-size: cover;
            color: white;
            height: 200px;
        }
    </style>
</head>
<body>
    <div class="color-examples named-color">命名顏色 (coral)</div>
    <div class="color-examples hex-color">十六進位 (#3498db)</div>
    <div class="color-examples rgb-color">RGB (155, 89, 182)</div>
    <div class="color-examples rgba-color">RGBA 半透明</div>
    <div class="color-examples linear-gradient">漸層背景</div>
    <div class="color-examples image-bg">圖片背景</div>
</body>
</html>
```

## 2.10 文字樣式

文字樣式控制文字的外觀，包括字體、大小、粗細、對齊等。

[程式檔案：02-10-text-styles.html](../_code/02/02-10-text-styles.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>文字樣式範例</title>
    <style>
        .text-examples {
            padding: 15px;
            margin: 10px;
            border: 1px solid #ddd;
        }
        
        .font-family {
            font-family: 'Arial', 'Microsoft JhengHei', sans-serif;
        }
        
        .font-size {
            font-size: 24px;
        }
        
        .font-weight {
            font-weight: bold;
        }
        
        .font-style {
            font-style: italic;
        }
        
        .text-align-left {
            text-align: left;
        }
        
        .text-align-center {
            text-align: center;
        }
        
        .text-align-right {
            text-align: right;
        }
        
        .text-decoration {
            text-decoration: underline overline line-through;
        }
        
        .text-transform {
            text-transform: uppercase;
        }
        
        .line-height {
            line-height: 2;
        }
        
        .letter-spacing {
            letter-spacing: 3px;
        }
        
        .text-shadow {
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <div class="text-examples font-family">字體家族</div>
    <div class="text-examples font-size">字體大小 24px</div>
    <div class="text-examples font-weight">粗體文字</div>
    <div class="text-examples font-style">斜體文字</div>
    <div class="text-examples text-align-left">靠左對齊</div>
    <div class="text-examples text-align-center">居中對齊</div>
    <div class="text-examples text-align-right">靠右對齊</div>
    <div class="text-examples text-decoration">裝飾線</div>
    <div class="text-examples text-transform">文字轉換</div>
    <div class="text-examples line-height">行高 2 倍行高 2 倍行高 2 倍</div>
    <div class="text-examples letter-spacing">字元間距</div>
    <div class="text-examples text-shadow">文字陰影</div>
</body>
</html>
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| 行內樣式 | 直接在 HTML 元素上使用 `style` 屬性 |
| 內部 CSS | 在 `<style>` 標籤中定義 |
| 外部 CSS | 獨立的 `.css` 檔案 |
| 選擇器 | 選取要套用樣式的元素 |
| 盒模型 | Content + Padding + Border + Margin |
| box-sizing | 控制寬度計算方式 |

## 練習題

1. 使用外部 CSS 檔案設定頁面樣式
2. 練習不同優先級選擇器的應用
3. 建立一個卡片元件，了解 margin、padding、border 的應用
4. 設計一個文字排版樣式系統
