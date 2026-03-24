# 7. 看懂 AI 生成的程式碼

## 為什麼要懂程式碼

你可能會問：「既然用 AI 建構平台，我為什麼還要懂程式碼？」

原因很簡單：

1. **更好的溝通**：了解基本概念能讓你更精準地向 AI 描述需求
2. **必要的調整**：平台提供的功能有限時，你需要自己修改程式碼
3. **問題排查**：當網站出問題時，你能大概知道要去哪裡找原因
4. **學習成長**：這是進入網站開發世界的敲門磚

## 網站的基本組成

### 三層結構

任何網站都由三個部分組成：

```
┌─────────────────────────────────────┐
│          HTML (內容層)               │
│     「這是標題」「這是段落」          │
├─────────────────────────────────────┤
│          CSS (樣式層)                │
│   「標題是藍色的」「文字要 16px」     │
├─────────────────────────────────────┤
│       JavaScript (互動層)            │
│    「點擊按鈕要彈出視窗」             │
└─────────────────────────────────────┘
```

### 用房子做比喻

| 概念 | 房屋比喻 |
|------|---------|
| HTML | 房屋的結構：牆壁、門窗、房間 |
| CSS | 房屋的裝修：油漆顏色、地板材質、窗簾款式 |
| JavaScript | 房屋的機電：電燈開關、門鈴、空調遙控 |

## HTML 基礎

### 標籤是什麼

HTML 使用「標籤」(Tag) 來定義內容。標籤通常是成對出現的：

```html
<標籤名稱>內容</標籤名稱>
```

### 常見的 HTML 標籤

**標題**：
```html
<h1>這是一級標題</h1>
<h2>這是二級標題</h2>
<h3>這是三級標題</h3>
```

**段落和文字**：
```html
<p>這是一個段落</p>
<strong>這是粗體文字</strong>
<em>這是斜體文字</em>
```

**連結**：
```html
<a href="https://example.com">點擊這裡</a>
```

**圖片**：
```html
<img src="photo.jpg" alt="圖片描述">
```

**清單**：
```html
<ul>
  <li>第一項</li>
  <li>第二項</li>
  <li>第三項</li>
</ul>
```

### 認識 class 和 id

為了方便 CSS 和 JavaScript 找到特定元素，我們會加上「名字」：

```html
<!-- class：用於一組元素 -->
<div class="header">頁首區塊</div>
<div class="header">另一個頁首</div>

<!-- id：用於唯一元素 -->
<div id="main-menu">主選單</div>
```

## CSS 基礎

### CSS 是什麼

CSS 用來控制 HTML 元素的「外觀」。

### 基本語法

```css
選擇器 {
  屬性: 值;
}
```

### 常見的 CSS 屬性

**顏色**：
```css
color: blue;              /* 文字顏色 */
background-color: #f0f0f0; /* 背景顏色 */
```

**字體**：
```css
font-size: 16px;           /* 字體大小 */
font-family: Arial;       /* 字體類型 */
font-weight: bold;         /* 字體粗細 */
```

**尺寸**：
```css
width: 100px;              /* 寬度 */
height: 200px;             /* 高度 */
max-width: 100%;           /* 最大寬度 */
```

**邊距和間距**：
```css
margin: 20px;              /* 外邊距 */
padding: 15px;             /* 內邊距 */
```

**排列**：
```css
text-align: center;        /* 文字對齊 */
display: flex;             /* 彈性布局 */
justify-content: center;   /* 水平居中 */
```

### 選擇器的種類

```css
/* 標籤選擇器 */
h1 {
  color: red;
}

/* class 選擇器 */
.container {
  width: 1000px;
}

/* id 選擇器 */
#header {
  background: white;
}

/* 複合選擇器 */
.header .logo {
  width: 50px;
}
```

## JavaScript 基礎

### JavaScript 是什麼

JavaScript 用來控制網頁的「行為」和「互動」。

### 基本語法

**變數**：
```javascript
let name = "小明";
let age = 25;
let isMember = true;
```

**函式**：
```javascript
function sayHello() {
  alert("你好！");
}
```

**事件監聽**：
```javascript
// 當按鈕被點擊時執行
button.addEventListener('click', function() {
  alert("按鈕被點了！");
});
```

### 常見的使用場景

| 功能 | JavaScript |
|------|-----------|
| 點擊按鈕顯示更多內容 | `addEventListener('click')` |
| 驗證表單填寫 | `if (input.value === "")` |
| 滾動到頁面頂部 | `window.scrollTo(0, 0)` |
| 倒數計時器 | `setInterval()` |

## 在 AI 工具中查看程式碼

### Wix 的程式碼選項

在 Wix 編輯器中：
1. 點擊「Developer Tools」
2. 可以看到 HTML、CSS、JavaScript
3. 可以在這裡添加自訂程式碼

### Durable 的程式碼匯出

Durable 可以匯出程式碼：
1. 點擊「Export」或「Download」
2. 選擇下載格式
3. 取得 HTML、CSS、JavaScript 檔案

### WordPress 的程式碼編輯

WordPress 主題編輯器位置：
1. 外觀 → 主題檔案編輯器
2. 選擇要編輯的檔案
3. 進行修改（小心不要弄壞網站）

## 簡單的程式碼修改範例

### 範例 1：修改文字顏色

**原本**：
```css
h1 {
  color: black;
}
```

**修改為藍色**：
```css
h1 {
  color: blue;
}
```

### 範例 2：調整間距

**原本**：
```css
.container {
  padding: 10px;
}
```

**增加上下間距**：
```css
.container {
  padding: 40px 10px;
}
```

### 範例 3：隱藏不需要的元素

有時候你不想要某個區塊，可以暫時隱藏：

```css
.unwanted-section {
  display: none;
}
```

## 使用 AI 幫你寫程式碼

### 直接請 AI 幫你修改

你可以對 Claude 或 ChatGPT 說：

```
「幫我把這個區塊的背景色改成深灰色，
文字改成白色。」

「幫我寫一個，當使用者點擊按鈕時，
會彈出 '感謝訂閱！' 的 JavaScript 程式碼。」
```

### 提供程式碼請 AI 解釋

如果看到不懂的程式碼，直接問：

```
「這段程式碼在做什麼？
.hello {
  color: red;
  font-size: 24px;
}
```

AI 會幫你解釋。

### 修改 AI 生成的程式碼

當 AI 生成的程式碼不完全符合需求時：

```
「謝謝！不過我想要：
1. 這個按鈕放在左邊，不是中間
2. 按鈕的顏色從藍色改成綠色
可以幫我調整嗎？」
```

## 實用程式碼片段

### 讓圖片置中

```css
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
```

### 讓元素在手機上堆疊顯示

```css
.container {
  display: flex;
  flex-wrap: wrap;
}

.item {
  width: 100%;
}

@media (min-width: 768px) {
  .item {
    width: 33.33%;
  }
}
```

### 簡單的按鈕樣式

```css
.button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}
```

## 重要提醒

### 永遠要先備份

修改程式碼之前，複製一份原始版本。這樣如果改壞了可以還原。

### 小心語法錯誤

程式碼非常「嚴格」，一個分號或括號錯了可能整個就壞了。

```
錯：color: red
對：color: red;

錯：.header { color: blue }
對：.header { color: blue; }
```

### 從小處開始

如果要測試修改，先改一小部分，確認沒問題再繼續。

### 不懂就問 AI

現在你有 Claude 這個強大的工具！任何程式碼相關的問題都可以問它。

## 你不需要會

這些複雜的部分，你不需要自己會：

- 後端程式設計（PHP、Python、Node.js 等）
- 資料庫設計
- 伺服器架設
- 複雜的 JavaScript 邏輯
- 網路安全防護

這些交給專業平台或工程師處理就好。

## 你需要會的

這些基本概念，你最好了解：

- HTML 是什麼
- CSS 用來控制外觀
- JavaScript 用來做互動
- 如何找到你要修改的元素
- 如何在 AI 工具中編輯程式碼
- 如何請 AI 幫你寫或修改程式碼

---

現在你對網站的基本概念已經有了全面的了解。接下來進入實戰演練部分，我們會實際建立四種類型的網站！
