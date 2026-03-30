# 35. 響應式設計與無障礙

## 響應式設計基礎

```
┌─────────────────────────────────────────────────────────┐
│                   响应式设计                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   移动优先（Mobile First）                               │
│   └─ 从最小屏幕开始，逐步增强                           │
│                                                         │
│   断点策略（Breakpoints）                               │
│   └─ sm: 640px, md: 768px, lg: 1024px, xl: 1280px     │
│                                                         │
│   流式布局（Fluid Layout）                              │
│   └─ 使用相对单位，而非固定像素                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助響應式設計

### CSS 媒體查詢

```
你：
请解释响应式 CSS 的最佳实践。

AI：
## 响应式 CSS

### 1. 移动优先
```css
/* 默认（移动端） */
.container {
  width: 100%;
  padding: 1rem;
}

/* 平板 */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
    padding: 2rem;
  }
}

/* 桌面 */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }
}

/* 大屏 */
@media (min-width: 1280px) {
  .container {
    max-width: 1140px;
  }
}
```

### 2. 网格系统
```css
.grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1rem;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
  }
}
```

### 3. 弹性单位
```css
/* 相对单位 */
.rem    /* 相对于根元素字体大小 */
.em     /* 相对于父元素字体大小 */
.vw/vh  /* 视口宽高 */
.%       /* 相对于父元素 */

/* 推荐做法 */
:root {
  --spacing: 1rem;
}

.card {
  padding: var(--spacing);
  font-size: 1rem;  /* 16px */
}

@media (min-width: 768px) {
  .card {
    font-size: 1.125rem;  /* 18px */
  }
}
```

### 4. Flexbox 响应式
```css
/* 导航栏 */
.navbar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .navbar {
    flex-direction: row;
    justify-content: space-between;
  }
}
```

### 5. 图片响应式
```css
/* 自适应图片 */
img {
  max-width: 100%;
  height: auto;
}

/* 背景图片 */
.hero {
  background-image: url('/mobile.jpg');
}

@media (min-width: 768px) {
  .hero {
    background-image: url('/tablet.jpg');
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('/desktop.jpg');
  }
}
```

### 6. 现代化方案：CSS Container
```css
.container {
  container-type: inline-size;
}

.card {
  display: grid;
  grid-template-columns: 1fr;
}

@container (min-width: 400px) {
  .card {
    grid-template-columns: 2fr 1fr;
  }
}
```
```

## 無障礙設計 (Accessibility)

```
你：
如何实现无障碍网页设计？

AI：
## 无障碍设计

### 1. 语义化 HTML
```html
<!-- ❌ 不语义 -->
<div onclick="toggle()">点击</div>
<div class="button">按钮</div>

<!-- ✅ 语义 -->
<button onclick="toggle()">点击</button>
<button class="btn">按钮</button>
```

### 2. 语义标签
```html
<header>头部</header>
<nav>导航</nav>
<main>
  <article>
    <section>
      <h1>标题</h1>
      <p>内容</p>
    </section>
  </article>
</main>
<aside>侧边栏</aside>
<footer>底部</footer>
```

### 3. 表单无障碍
```html
<!-- 正确关联 label -->
<label for="email">邮箱</label>
<input type="email" id="email" aria-describedby="email-help" />
<span id="email-help">请输入有效的邮箱地址</span>

<!-- 错误提示 -->
<div id="email-error" role="alert" aria-live="polite">
  邮箱格式不正确
</div>
```

### 4. 键盘导航
```css
/* 焦点样式 */
:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* 跳过链接 */
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: 1rem;
  background: #0066cc;
  color: white;
}

.skip-link:focus {
  top: 0;
}
```

```html
<a href="#main-content" class="skip-link">跳到主要内容</a>

<nav>...</nav>

<main id="main-content">
  <!-- 主要内容 -->
</main>
```

### 5. ARIA 属性
```html
<!-- 按钮状态 -->
<button aria-expanded="false" aria-controls="menu">
  菜单
</button>

<!-- 动态内容 -->
<div aria-live="polite" aria-atomic="true">
  <!-- 自动播报更新 -->
</div>

<!-- 对话框 -->
<dialog aria-labelledby="title" aria-describedby="desc">
  <h2 id="title">标题</h2>
  <p id="desc">描述</p>
</dialog>
```

### 6. 颜色对比度
```css
/* 满足 WCAG AA 标准 */
.text {
  color: #333;        /* 深灰文字 */
  background: #fff;   /* 白底 */
  /* 对比度 12.6:1 ✅ */
}

.text-secondary {
  color: #666;        /* 浅灰文字 */
  background: #fff;   /* 白底 */
  /* 对比度 5.7:1 ✅ */
}

/* 避免单独用颜色传递信息 */
.error {
  color: red;  /* ❌ 色盲用户看不到 */
  /* 应该配合图标或文字 */
}

.error::before {
  content: "⚠️ ";
}
```
```

## 現代 CSS 框架

### Tailwind CSS

```
你：
Tailwind CSS 有什么优势？

AI：
## Tailwind CSS

### 优势
1. **原子化 CSS** - 只生成使用的样式
2. **无需切换文件** - HTML 中直接写样式
3. **一致的间距和颜色** - 设计系统化
4. **响应式简单** - 添加前缀即可

### 使用示例
```html
<button class="
  px-4 py-2           /* 内边距 */
  bg-blue-500         /* 背景色 */
  text-white          /* 文字颜色 */
  font-medium         /* 字重 */
  rounded-lg          /* 圆角 */
  hover:bg-blue-600   /* 悬停状态 */
  focus:ring-2        /* 焦点状态 */
  disabled:opacity-50 /* 禁用状态 */
">
  按钮
</button>
```

### 响应式
```html
<div class="
  grid
  grid-cols-1         /* 移动端：1列 */
  md:grid-cols-2      /* 平板：2列 */
  lg:grid-cols-4      /* 桌面：4列 */
  gap-4
">
  <!-- 内容 -->
</div>
```

### 组件化
```javascript
// button.js
export function Button({ variant = 'primary', children }) {
  const variants = {
    primary: 'bg-blue-500 hover:bg-blue-600',
    secondary: 'bg-gray-200 hover:bg-gray-300',
    danger: 'bg-red-500 hover:bg-red-600'
  }
  
  return (
    <button className={`px-4 py-2 ${variants[variant]}`}>
      {children}
    </button>
  )
}
```
```

## 實踐練習

```
1. 使用响应式设计改造你的页面
2. 添加无障碍特性
3. 测试键盘导航
4. 验证颜色对比度
5. 使用 Lighthouse 检查可访问性
```

**響應式和無障礙不是可選項，而是每個網站必須具備的基本特性。**
