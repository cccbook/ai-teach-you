# 第 3 章：CSS 進階

## 概述

本章介紹現代 CSS 的進階技術，包括 Flexbox 彈性盒模型、Grid 網格佈局、響應式設計的媒體查詢，以及動畫和轉換效果。

## 3.1 Flexbox 基礎

Flexbox 是一維佈局模型，適合處理行或列的排列。

[程式檔案：03-1-flexbox-basic.html](../_code/03/03-1-flexbox-basic.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>Flexbox 基礎範例</title>
    <style>
        .container {
            display: flex;
            background-color: #eee;
            padding: 10px;
        }
        
        .item {
            background-color: #3498db;
            color: white;
            padding: 20px;
            margin: 5px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Flexbox 基礎</h1>
    <div class="container">
        <div class="item">項目 1</div>
        <div class="item">項目 2</div>
        <div class="item">項目 3</div>
    </div>
</body>
</html>
```

## 3.2 Flexbox 對齊

使用 `justify-content` 和 `align-items` 控制主軸和交叉軸的對齊。

[程式檔案：03-2-flexbox-align.html](../_code/03/03-2-flexbox-align.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>Flexbox 對齊範例</title>
    <style>
        .container {
            display: flex;
            height: 200px;
            background-color: #eee;
            margin-bottom: 20px;
        }
        
        .item {
            background-color: #3498db;
            color: white;
            padding: 20px;
            margin: 5px;
        }
        
        .justify-start { justify-content: flex-start; }
        .justify-center { justify-content: center; }
        .justify-end { justify-content: flex-end; }
        .justify-between { justify-content: space-between; }
        
        .align-center { align-items: center; }
        .align-end { align-items: flex-end; }
    </style>
</head>
<body>
    <h2>justify-content: center</h2>
    <div class="container justify-center">
        <div class="item">1</div>
        <div class="item">2</div>
        <div class="item">3</div>
    </div>
    
    <h2>justify-content: space-between</h2>
    <div class="container justify-between">
        <div class="item">1</div>
        <div class="item">2</div>
        <div class="item">3</div>
    </div>
    
    <h2>align-items: center</h2>
    <div class="container align-center">
        <div class="item">1</div>
        <div class="item">2</div>
        <div class="item">3</div>
    </div>
</body>
</html>
```

## 3.3 Flexbox 方向

使用 `flex-direction` 控制主軸方向。

[程式檔案：03-3-flexbox-direction.html](../_code/03/03-3-flexbox-direction.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>Flexbox 方向範例</title>
    <style>
        .container {
            display: flex;
            background-color: #eee;
            padding: 10px;
            margin-bottom: 20px;
        }
        
        .item {
            background-color: #3498db;
            color: white;
            padding: 20px;
            margin: 5px;
        }
        
        .row { flex-direction: row; }
        .row-reverse { flex-direction: row-reverse; }
        .column { flex-direction: column; }
        .column-reverse { flex-direction: column-reverse; }
    </style>
</head>
<body>
    <h2>flex-direction: row</h2>
    <div class="container row">
        <div class="item">1</div>
        <div class="item">2</div>
        <div class="item">3</div>
    </div>
    
    <h2>flex-direction: column</h2>
    <div class="container column">
        <div class="item">1</div>
        <div class="item">2</div>
        <div class="item">3</div>
    </div>
</body>
</html>
```

## 3.4 Grid 基礎

CSS Grid 是二維佈局系統，同時控制行和列。

[程式檔案：03-4-grid-basic.html](../_code/03/03-4-grid-basic.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>Grid 基礎範例</title>
    <style>
        .grid-container {
            display: grid;
            background-color: #eee;
            padding: 10px;
        }
        
        .grid-item {
            background-color: #3498db;
            color: white;
            padding: 20px;
            margin: 5px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Grid 基礎</h1>
    <div class="grid-container" style="grid-template-columns: repeat(3, 1fr);">
        <div class="grid-item">項目 1</div>
        <div class="grid-item">項目 2</div>
        <div class="grid-item">項目 3</div>
        <div class="grid-item">項目 4</div>
        <div class="grid-item">項目 5</div>
        <div class="grid-item">項目 6</div>
    </div>
</body>
</html>
```

## 3.5 Grid 模板

使用 `grid-template-columns` 和 `grid-template-rows` 定義網格結構。

[程式檔案：03-5-grid-template.html](../_code/03/03-5-grid-template.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>Grid 模板範例</title>
    <style>
        .grid-container {
            display: grid;
            gap: 10px;
            background-color: #eee;
            padding: 10px;
        }
        
        .header { grid-column: 1 / -1; background-color: #2c3e50; }
        .sidebar { grid-row: 2 / 4; background-color: #3498db; }
        .main { background-color: #27ae60; }
        .footer { grid-column: 2 / -1; background-color: #e74c3c; }
        
        .grid-item {
            color: white;
            padding: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="grid-container" style="grid-template-columns: 200px 1fr 1fr; grid-template-rows: auto 1fr auto;">
        <div class="grid-item header">Header</div>
        <div class="grid-item sidebar">Sidebar</div>
        <div class="grid-item main">Main Content</div>
        <div class="grid-item main">Content 2</div>
        <div class="grid-item footer">Footer</div>
    </div>
</body>
</html>
```

## 3.6 媒體查詢

媒體查詢是響應式設計的核心，根據設備特性套用不同樣式。

[程式檔案：03-6-media-queries.html](../_code/03/03-6-media-queries.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>媒體查詢範例</title>
    <style>
        .box {
            background-color: #3498db;
            color: white;
            padding: 20px;
            font-size: 18px;
        }
        
        /* 平板 */
        @media (max-width: 768px) {
            .box {
                background-color: #e74c3c;
                font-size: 16px;
            }
        }
        
        /* 手機 */
        @media (max-width: 480px) {
            .box {
                background-color: #27ae60;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div class="box">調整視窗大小查看效果</div>
</body>
</html>
```

## 3.7 響應式版面

結合 Flexbox 和 Grid 創建響應式版面。

[程式檔案：03-7-responsive-layout.html](../_code/03/03-7-responsive-layout.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>響應式版面範例</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        
        .card {
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }
        
        .header {
            grid-column: 1 / -1;
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        @media (max-width: 600px) {
            .container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>響應式網站</h1>
        </div>
        <div class="card">
            <h2>卡片 1</h2>
            <p>響應式內容...</p>
        </div>
        <div class="card">
            <h2>卡片 2</h2>
            <p>響應式內容...</p>
        </div>
        <div class="card">
            <h2>卡片 3</h2>
            <p>響應式內容...</p>
        </div>
    </div>
</body>
</html>
```

## 3.8 CSS 動畫

使用 `@keyframes` 定義動畫效果。

[程式檔案：03-8-animation.html](../_code/03/03-8-animation.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>CSS 動畫範例</title>
    <style>
        .box {
            width: 100px;
            height: 100px;
            background-color: #3498db;
            margin: 50px auto;
            
            animation-name: slideAndFade;
            animation-duration: 2s;
            animation-timing-function: ease-in-out;
            animation-iteration-count: infinite;
            animation-direction: alternate;
        }
        
        @keyframes slideAndFade {
            0% {
                transform: translateX(-100px);
                opacity: 0;
            }
            50% {
                transform: translateX(0);
                opacity: 1;
                background-color: #e74c3c;
            }
            100% {
                transform: translateX(100px);
                opacity: 0;
            }
        }
        
        .pulse {
            width: 100px;
            height: 100px;
            background-color: #27ae60;
            margin: 20px auto;
            border-radius: 50%;
            
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.1);
            }
        }
    </style>
</head>
<body>
    <h1>CSS 動畫</h1>
    <div class="box"></div>
    <div class="pulse"></div>
</body>
</html>
```

## 3.9 轉場效果

`transition` 屬性讓樣式變化更加平滑。

[程式檔案：03-9-transition.html](../_code/03/03-9-transition.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>轉場效果範例</title>
    <style>
        .box {
            width: 200px;
            height: 200px;
            background-color: #3498db;
            margin: 20px;
            transition: all 0.3s ease;
        }
        
        .box:hover {
            background-color: #e74c3c;
            transform: scale(1.1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .button {
            padding: 15px 30px;
            background-color: #2ecc71;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
        }
        
        .button:hover {
            background-color: #27ae60;
        }
        
        .button:active {
            transform: scale(0.95);
        }
    </style>
</head>
<body>
    <h1>轉場效果</h1>
    <div class="box"></div>
    <button class="button">點擊我</button>
</body>
</html>
```

## 3.10 2D/3D 轉換

`transform` 屬性支援 2D 和 3D 空間的變換。

[程式檔案：03-10-transform.html](../_code/03/03-10-transform.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>2D/3D 轉換範例</title>
    <style>
        .container {
            perspective: 1000px;
            margin: 50px;
        }
        
        .box {
            width: 150px;
            height: 150px;
            background-color: #3498db;
            margin: 20px;
            display: inline-block;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .translate:hover {
            transform: translate(50px, 50px);
        }
        
        .rotate:hover {
            transform: rotate(45deg);
        }
        
        .scale:hover {
            transform: scale(1.5);
        }
        
        .skew:hover {
            transform: skew(20deg, 20deg);
        }
        
        .rotate3d {
            background-color: #e74c3c;
        }
        
        .rotate3d:hover {
            transform: rotateY(180deg);
            transition: transform 1s;
        }
    </style>
</head>
<body>
    <h1>2D/3D 轉換</h1>
    <div class="container">
        <div class="box translate">translate</div>
        <div class="box rotate">rotate</div>
        <div class="box scale">scale</div>
        <div class="box skew">skew</div>
        <div class="box rotate3d">3D rotate</div>
    </div>
</body>
</html>
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| Flexbox | 一維佈局，適合行列排列 |
| Grid | 二維佈局，同時控制行和列 |
| 媒體查詢 | 根據設備特性套用樣式 |
| @keyframes | 定義動畫關鍵幀 |
| transition | 樣式變化的平滑過渡 |
| transform | 元素的 2D/3D 變換 |

## 練習題

1. 使用 Flexbox 建立導航列
2. 使用 Grid 建立相簿版面
3. 製作響應式卡片佈局
4. 創建一個載入動畫效果
