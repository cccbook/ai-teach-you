# 36. 前端效能優化與使用者體驗

## 前端效能指標

```
┌─────────────────────────────────────────────────────────┐
│                   Core Web Vitals                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   LCP (Largest Contentful Paint)                        │
│   └─ 最大内容绘制时间                                    │
│   └─ 目标：< 2.5秒                                      │
│                                                         │
│   FID/INP (First Input Delay / Interaction to Next Paint)│
│   └─ 首次输入延迟                                       │
│   └─ 目标：< 100毫秒                                    │
│                                                         │
│   CLS (Cumulative Layout Shift)                          │
│   └─ 累计布局偏移                                       │
│   └─ 目标：< 0.1                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助效能優化

### 資源優化

```
你：
如何优化前端资源加载？

AI：
## 资源优化

### 1. 图片优化
```html
<!-- 响应式图片 -->
<img
  src="image-400.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="(max-width: 600px) 100vw, 50vw"
  loading="lazy"
  alt="..."
/>

<!-- WebP 格式 -->
<picture>
  <source srcset="image.webp" type="image/webp" />
  <img src="image.jpg" alt="..." />
</picture>
```

### 2. 字体优化
```html
<!-- 预加载关键字体 -->
<link rel="preload" href="font.woff2" as="font" crossorigin />
<link rel="preconnect" href="https://fonts.googleapis.com" />

<!-- 使用 font-display -->
@font-face {
  font-family: 'MyFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;  /* 加载期间显示替代字体 */
}
```

### 3. CSS/JS 优化
```html
<!-- 预加载关键 CSS -->
<link rel="preload" href="/styles/main.css" as="style" />

<!-- 延迟加载非关键 JS -->
<script src="/analytics.js" defer></script>

<!-- 异步加载第三方脚本 -->
<script src="https://analytics.com/script.js" async></script>
```

### 4. CDN
```html
<!-- 使用 CDN -->
<script src="https://cdn.example.com/vue.js"></script>

<!-- 自身资源 CDN 化 -->
<img src="https://cdn.example.com/image.jpg" />
```
```

### 5. 资源压缩
```javascript
// 构建时压缩
// Vite / Webpack 配置
export default {
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true  // 移除 console.log
      }
    }
  }
}
```

## JavaScript 優化

```
你：
JavaScript 性能优化有哪些方法？

AI：
## JavaScript 优化

### 1. 避免不必要的渲染
```jsx
// React
const MemoizedComponent = React.memo(
  Component,
  (prevProps, nextProps) => {
    // 返回 true 表示不需要重新渲染
    return prevProps.items === nextProps.items
  }
)

// Vue
const computedValue = computed(() => items.length)
```

### 2. 防抖和节流
```javascript
// 防抖 - 延迟执行
function debounce(fn, delay) {
  let timer = null
  return function(...args) {
    clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}

// 节流 - 限制频率
function throttle(fn, limit) {
  let inThrottle = false
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

// 使用
const handleSearch = debounce((query) => {
  fetchResults(query)
}, 300)

window.addEventListener('resize', throttle(handleResize, 100))
```

### 3. 虚拟列表
```jsx
// 处理大量数据
import { FixedSizeList } from 'react-window'

function VirtualList({ items }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
    >
      {({ index, style }) => (
        <div style={style}>
          {items[index].name}
        </div>
      )}
    </FixedSizeList>
  )
}
```

### 4. Web Worker
```javascript
// heavy-task.js (Web Worker)
self.onmessage = function(e) {
  const result = heavyComputation(e.data)
  self.postMessage(result)
}

// 主线程
const worker = new Worker('heavy-task.js')
worker.postMessage(data)
worker.onmessage = (e) => {
  console.log('Result:', e.data)
}
```

### 5. 懒加载
```jsx
// 路由懒加载
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))

// 图片懒加载
const LazyImage = ({ src, ...props }) => {
  const [loaded, setLoaded] = useState(false)
  
  return (
    <img
      src={loaded ? src : ''}
      loading="lazy"
      onLoad={() => setLoaded(true)}
      {...props}
    />
  )
}
```

## 使用者體驗優化

```
你：
如何提升用户体验？

AI：
## 用户体验优化

### 1. 加载状态
```jsx
// 骨架屏
function UserProfile({ user }) {
  if (!user) {
    return (
      <div className="skeleton">
        <div className="skeleton-avatar"></div>
        <div className="skeleton-text"></div>
        <div className="skeleton-text short"></div>
      </div>
    )
  }
  return <Profile user={user} />
}

// 按钮加载状态
<button disabled={loading}>
  {loading ? '加载中...' : '提交'}
</button>
```

### 2. 错误处理
```jsx
function ErrorBoundary({ children }) {
  const [hasError, setHasError] = useState(false)
  
  if (hasError) {
    return (
      <div className="error-state">
        <h2>出错了</h2>
        <button onClick={() => window.location.reload()}>
          重新加载
        </button>
      </div>
    )
  }
  
  return <ErrorBoundaryInner>{children}</ErrorBoundaryInner>
}

// 表单错误
function FormField({ label, error, children }) {
  return (
    <div className={`field ${error ? 'has-error' : ''}`}>
      <label>{label}</label>
      {children}
      {error && <span className="error">{error}</span>}
    </div>
  )
}
```

### 3. 成功反馈
```jsx
// Toast 提示
function Toast({ message, type = 'info' }) {
  return (
    <div className={`toast toast-${type}`} role="alert">
      {message}
    </div>
  )
}

// 操作成功
async function handleSubmit() {
  try {
    await save(data)
    showToast('保存成功', 'success')
  } catch (error) {
    showToast('保存失败', 'error')
  }
}
```

### 4. 空状态
```jsx
function EmptyState({ icon, title, description, action }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{description}</p>
      {action && <Button onClick={action.onClick}>{action.label}</Button>}
    </div>
  )
}

// 使用
{users.length === 0 ? (
  <EmptyState
    icon="👤"
    title="暂无用户"
    description="创建一个新用户开始使用"
    action={{ label: '创建用户', onClick: () => {} }}
  />
) : (
  <UserList users={users} />
)}
```

### 5. 脱机支持
```javascript
// Service Worker
const CACHE_NAME = 'my-app-v1'

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request)
      })
  )
})

// PWA manifest
{
  "name": "My App",
  "short_name": "App",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0066cc"
}
```

## 監控與分析

```
你：
如何监控前端性能？

AI：
## 前端性能监控

### 1. Performance API
```javascript
// 测量页面加载
const perfData = performance.getEntriesByType('navigation')[0]
console.log({
  dns: perfData.domainLookupEnd - perfData.domainLookupStart,
  tcp: perfData.connectEnd - perfData.connectStart,
  ttfb: perfData.responseStart - perfData.requestStart,
  download: perfData.responseEnd - perfData.responseStart,
  total: perfData.loadEventEnd - perfData.navigationStart
})

// 测量资源
performance.getEntriesByType('resource').forEach(resource => {
  console.log(`${resource.name}: ${resource.duration}ms`)
})
```

### 2. Web Vitals
```javascript
import { onLCP, onFID, onCLS } from 'web-vitals'

onLCP((metric) => {
  console.log('LCP:', metric.value)
  // 上报到分析服务
})

onFID((metric) => {
  console.log('FID:', metric.value)
})

onCLS((metric) => {
  console.log('CLS:', metric.value)
})
```

### 3. 错误监控
```javascript
// 全局错误处理
window.addEventListener('error', (event) => {
  reportError({
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno
  })
})

// Promise 错误
window.addEventListener('unhandledrejection', (event) => {
  reportError({
    message: event.reason?.message || 'Unhandled Promise Rejection',
    stack: event.reason?.stack
  })
})

// React Error Boundary
class ErrorBoundary extends React.Component {
  componentDidCatch(error, info) {
    reportError({ error, info })
  }
}
```

### 4. 第三方监控
```javascript
// Sentry
import * as Sentry from '@sentry/browser'

Sentry.init({
  dsn: 'https://xxx@sentry.io/xxx',
  environment: process.env.NODE_ENV
})

// 手动上报
Sentry.captureException(new Error('Something went wrong'))
```
```

## 實踐練習

```
1. 测量当前页面的 Core Web Vitals
2. 优化图片加载
3. 实现骨架屏
4. 添加错误边界
5. 配置性能监控
6. 运行 Lighthouse 审计
7. 持续监控和改进
```

**好的用戶體驗是留住用戶的關鍵。每一個小細節都值得優化。**
