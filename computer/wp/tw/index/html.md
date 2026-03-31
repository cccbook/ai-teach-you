# HTML

## 概述

HTML（HyperText Markup Language，超文字標記語言）是建立網頁的基礎技術，用於描述網頁的結構和內容。

## 歷史

- 1991 年：Tim Berners-Lee 發明 HTML
- 1995 年：HTML 2.0 標準化
- 1997 年：HTML 3.2、HTML 4.0
- 2014 年：HTML5 成為 W3C 標準

## 核心概念

### 標籤

HTML 使用標籤（tag）來標記內容：

```html
<p>這是段落標籤</p>
<a href="https://example.com">這是連結</a>
```

### 元素

元素由開始標籤、內容和結束標籤組成：

```html
<div class="container">
    <h1>標題</h1>
    <p>段落內容</p>
</div>
```

### 屬性

屬性提供元素的額外資訊：

```html
<a href="https://example.com" target="_blank" class="link">
    連結文字
</a>
```

## 常見標籤

| 標籤 | 用途 |
|------|------|
| `<html>` | 根元素 |
| `<head>` | 中繼資料區 |
| `<body>` | 可見內容區 |
| `<header>` | 頁頭區 |
| `<main>` | 主要內容 |
| `<footer>` | 頁尾區 |
| `<nav>` | 導航區 |
| `<article>` | 文章內容 |
| `<section>` | 區塊 |
| `<div>` | 通用容器 |

## 語意化標籤

HTML5 引入語意化標籤，提高可讀性和可訪問性：

```html
<header>
    <nav>導航連結</nav>
</header>
<main>
    <article>
        <header><h1>文章標題</h1></header>
        <section>內容區塊</section>
    </article>
    <aside>側邊欄</aside>
</main>
<footer>頁腳版權資訊</footer>
```

## 參考資源

- [MDN HTML 文件](https://developer.mozilla.org/zh-TW/docs/Web/HTML)
- [W3C HTML 標準](https://html.spec.whatwg.org/)
