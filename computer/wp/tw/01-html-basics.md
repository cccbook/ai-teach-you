# 第 1 章：HTML 基礎

## 概述

HTML（HyperText Markup Language，超文字標記語言）是建立網頁的基礎技術。本章將介紹 HTML 的基本語法、文件結構，以及常用的 HTML 標籤。

## 1.1 第一個 HTML 網頁

讓我們從最簡單的 HTML 網頁開始。HTML 文件由標籤（tag）組成，標籤通常成對出現，包含開始標籤和結束標籤。

[程式檔案：01-1-hello.html](../_code/01/01-1-hello.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>第一個 HTML 網頁</title>
</head>
<body>
    <h1>你好，World!</h1>
    <p>這是我的第一個 HTML 網頁。</p>
</body>
</html>
```

**說明：**
- `<!DOCTYPE html>`：宣告此文件為 HTML5 格式
- `<html>`：根元素，包含所有 HTML 內容
- `<head>`：存放中繼資料，如標題、字符編碼等
- `<body>`：存放可見的網頁內容
- `<meta charset="UTF-8">`：指定字符編碼，支援中文顯示

## 1.2 HTML 文件結構

一個完整的 HTML 文件應該包含清晰的語義化結構。以下是現代 HTML5 的標準結構：

[程式檔案：01-2-structure.html](../_code/01/01-2-structure.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="這是一個範例網頁">
    <title>HTML 文件結構範例</title>
</head>
<body>
    <header>
        <h1>網頁標題</h1>
    </header>
    <main>
        <article>
            <h2>文章標題</h2>
            <p>文章內容...</p>
        </article>
    </main>
    <footer>
        <p>&copy; 2026 我的網站</p>
    </footer>
</body>
</html>
```

**結構說明：**

| 標籤 | 用途 |
|------|------|
| `<header>` | 頁面或區塊的標題區 |
| `<main>` | 主要內容區（每頁只用一次） |
| `<article>` | 獨立的文章內容 |
| `<footer>` | 頁面或區塊的底部 |
| `<nav>` | 導航連結區 |
| `<aside>` | 側邊欄內容 |

## 1.3 標題標籤

HTML 提供六個層級的標題標籤，從 `<h1>` 到 `<h6>`。`<h1>` 是最重要的標題，每個頁面應該只有一個。

[程式檔案：01-3-headings.html](../_code/01/01-3-headings.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>標題標籤範例</title>
</head>
<body>
    <h1>這是 H1 標題 - 最主要標題</h1>
    <h2>這是 H2 標題 - 次要標題</h2>
    <h3>這是 H3 標題 - 第三層標題</h3>
    <h4>這是 H4 標題 - 第四層標題</h4>
    <h5>這是 H5 標題 - 第五層標題</h5>
    <h6>這是 H6 標題 - 最小的標題</h6>
</body>
</html>
```

**最佳實踐：**
- 每個頁面只用一個 `<h1>` 標題
- 標題層級要連貫，不要跳號
- 使用標題表達內容的層次結構，而非單純為了樣式

## 1.4 段落與換行

文字內容使用 `<p>` 標籤包裹。如果需要單純換行而不分段，可以使用 `<br>` 標籤。

[程式檔案：01-4-paragraph.html](../_code/01/01-4-paragraph.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>段落與換行範例</title>
</head>
<body>
    <p>這是第一個段落。HTML 會自動忽略多餘的空格和換行。</p>
    
    <p>這是第二個段落。
       即使在原始碼中換行，
       顯示出來也會是連續的。</p>
    
    <p>如果要強制換行，<br>可以使用 br 標籤。</p>
    
    <p>這裡有特殊的空白字元：&nbsp;&nbsp;&nbsp;四個不換行空格</p>
</body>
</html>
```

## 1.5 超連結

連結是 HTML 最核心的功能之一。使用 `<a>` 標籤建立連結，`href` 屬性指定目標網址。

[程式檔案：01-5-links.html](../_code/01/01-5-links.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>超連結範例</title>
</head>
<body>
    <a href="https://www.example.com">外部連結</a>
    
    <a href="about.html">站内連結</a>
    
    <a href="#section-id">錨點連結</a>
    
    <a href="mailto:contact@example.com">發送郵件</a>
    
    <a href="https://example.com" target="_blank" rel="noopener noreferrer">
        在新分頁開啟
    </a>
</body>
</html>
```

**連結屬性說明：**
- `href`：連結目標
- `target="_blank"`：在新分頁開啟
- `rel="noopener noreferrer"`：安全屬性，防止跨站攻擊

## 1.6 圖片標籤

`<img>` 是自閉合標籤，用於嵌入圖片。必須包含 `src`（圖片路徑）和 `alt`（替代文字）屬性。

[程式檔案：01-6-images.html](../_code/01/01-6-images.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>圖片標籤範例</title>
</head>
<body>
    <img src="photo.jpg" alt="風景照片">
    
    <img src="https://example.com/image.png" alt="遠端圖片">
    
    <figure>
        <img src="diagram.png" alt="示意圖">
        <figcaption>圖 1: 系統架構圖</figcaption>
    </figure>
</body>
</html>
```

## 1.7 列表

HTML 支援有序列表（`<ol>`）和無序列表（`<ul>`）。

[程式檔案：01-7-lists.html](../_code/01/01-7-lists.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>列表範例</title>
</head>
<body>
    <h2>無序列表</h2>
    <ul>
        <li>項目一</li>
        <li>項目二</li>
        <li>項目三</li>
    </ul>
    
    <h2>有序列表</h2>
    <ol>
        <li>第一個步驟</li>
        <li>第二個步驟</li>
        <li>第三個步驟</li>
    </ol>
    
    <h2>巢狀列表</h2>
    <ul>
        <li>
            主項目
            <ul>
                <li>子項目 A</li>
                <li>子項目 B</li>
            </ul>
        </li>
    </ul>
</body>
</html>
```

## 1.8 表格

使用 `<table>` 建立表格，包含 `<thead>`、`<tbody>`、`<tr>`（列）和 `<td>`（儲存格）。

[程式檔案：01-8-tables.html](../_code/01/01-8-tables.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>表格範例</title>
</head>
<body>
    <table border="1">
        <thead>
            <tr>
                <th>姓名</th>
                <th>年齡</th>
                <th>城市</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>王小明</td>
                <td>25</td>
                <td>台北</td>
            </tr>
            <tr>
                <td>陳小美</td>
                <td>30</td>
                <td>高雄</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
```

## 1.9 表單元素

表單用於收集使用者輸入。常用元素包括 `<input>`、`<textarea>`、`<select>` 和 `<button>`。

[程式檔案：01-9-forms.html](../_code/01/01-9-forms.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>表單元素範例</title>
</head>
<body>
    <form action="/submit" method="POST">
        <label for="name">姓名：</label>
        <input type="text" id="name" name="name" required>
        
        <label for="email">電子郵件：</label>
        <input type="email" id="email" name="email">
        
        <label for="password">密碼：</label>
        <input type="password" id="password" name="password">
        
        <fieldset>
            <legend>性別</legend>
            <input type="radio" id="male" name="gender" value="male">
            <label for="male">男</label>
            <input type="radio" id="female" name="gender" value="female">
            <label for="female">女</label>
        </fieldset>
        
        <label for="message">留言：</label>
        <textarea id="message" name="message" rows="4"></textarea>
        
        <label for="country">國家：</label>
        <select id="country" name="country">
            <option value="tw">台灣</option>
            <option value="hk">香港</option>
            <option value="sg">新加坡</option>
        </select>
        
        <button type="submit">送出</button>
        <button type="reset">重設</button>
    </form>
</body>
</html>
```

## 1.10 語義化標籤

HTML5 引入許多語義化標籤，讓文件結構更清晰、有意義。

[程式檔案：01-10-semantic.html](../_code/01/01-10-semantic.html)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>語義化標籤範例</title>
</head>
<body>
    <header>
        <nav>
            <a href="/">首頁</a>
            <a href="/about">關於</a>
        </nav>
    </header>
    
    <main>
        <article>
            <header>
                <h1>文章標題</h1>
                <time datetime="2026-03-24">2026年3月24日</time>
            </header>
            <section>
                <h2>第一節</h2>
                <p>內容...</p>
            </section>
            <section>
                <h2>第二節</h2>
                <p>內容...</p>
            </section>
            <footer>
                <p>作者：王小明</p>
            </footer>
        </article>
        
        <aside>
            <h3>側邊欄</h3>
            <p>相關連結...</p>
        </aside>
    </main>
    
    <footer>
        <p>&copy; 2026 網站名稱</p>
    </footer>
</body>
</html>
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| HTML 標籤 | 成對出現，包裹內容 |
| DOCTYPE | 宣告文件類型 |
| 語義化 | 使用有意義的標籤描述內容 |
| 屬性 | 提供元素的額外資訊 |
| 空元素 | 不需要結束標籤的元素 |

## 練習題

1. 建立一個包含標題、段落和圖片的簡單網頁
2. 製作一個連絡人表單，包含姓名、郵件和留言欄位
3. 建立一個商品列表頁面，使用表格展示商品資訊
4. 使用語義化標籤重構一個現有的網頁結構
