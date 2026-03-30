# 36. Frontend Performance Optimization and User Experience

## Frontend Performance Metrics

```
┌─────────────────────────────────────────────────────────┐
│                   Core Web Vitals                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   LCP (Largest Contentful Paint)                        │
│   └─ Largest content paint time                          │
│   └─ Target: < 2.5 seconds                               │
│                                                         │
│   FID/INP (First Input Delay / Interaction to Next Paint)│
│   └─ First input delay                                   │
│   └─ Target: < 100 milliseconds                         │
│                                                         │
│   CLS (Cumulative Layout Shift)                          │
│   └─ Cumulative layout shift                            │
│   └─ Target: < 0.1                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Performance Optimization

### Resource Optimization

```
You:
How do I optimize frontend resource loading?

AI:
## Resource Optimization

### 1. Image Optimization
```html
<!-- Responsive images -->
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

<!-- WebP format -->
<picture>
  <source srcset="image.webp" type="image/webp" />
  <img src="image.jpg" alt="..." />
</picture>
```

### 2. Font Optimization
```html
<!-- Preload critical fonts -->
<link rel="preload" href="font.woff2" as="font" crossorigin />
<link rel="preconnect" href="https://fonts.googleapis.com" />

<!-- Use font-display -->
@font-face {
  font-family: 'MyFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;  /* Shows fallback font during loading */
}
```

### 3. CSS/JS Optimization
```html
<!-- Preload critical CSS -->
<link rel="preload" href="/styles/main.css" as="style" />

<!-- Defer non-critical JS -->
<script src="/analytics.js" defer></script>

<!-- Async load third-party scripts -->
<script src="https://analytics.com/script.js" async></script>
```

### 4. CDN
```html
<!-- Use CDN -->
<script src="https://cdn.example.com/vue.js"></script>

<!-- Serve your own resources via CDN -->
<img src="https://cdn.example.com/image.jpg" />
```
```

### 5. Resource Compression
```javascript
// Build-time compression
// Vite / Webpack config
export default {
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true  // Remove console.log
      }
    }
  }
}
```

## JavaScript Optimization

```
You:
What methods are there for JavaScript performance optimization?

AI:
## JavaScript Optimization

### 1. Avoid Unnecessary Re-renders
```jsx
// React
const MemoizedComponent = React.memo(
  Component,
  (prevProps, nextProps) => {
    // Return true if no re-render needed
    return prevProps.items === nextProps.items
  }
)

// Vue
const computedValue = computed(() => items.length)
```

### 2. Debounce and Throttle
```javascript
// Debounce - delay execution
function debounce(fn, delay) {
  let timer = null
  return function(...args) {
    clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}

// Throttle - limit frequency
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

// Usage
const handleSearch = debounce((query) => {
  fetchResults(query)
}, 300)

window.addEventListener('resize', throttle(handleResize, 100))
```

### 3. Virtual List
```jsx
// Handle large data sets
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

// Main thread
const worker = new Worker('heavy-task.js')
worker.postMessage(data)
worker.onmessage = (e) => {
  console.log('Result:', e.data)
}
```

### 5. Lazy Loading
```jsx
// Route lazy loading
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))

// Image lazy loading
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

## User Experience Optimization

```
You:
How do I improve user experience?

AI:
## User Experience Optimization

### 1. Loading States
```jsx
// Skeleton screen
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

// Button loading state
<button disabled={loading}>
  {loading ? 'Loading...' : 'Submit'}
</button>
```

### 2. Error Handling
```jsx
function ErrorBoundary({ children }) {
  const [hasError, setHasError] = useState(false)
  
  if (hasError) {
    return (
      <div className="error-state">
        <h2>Something went wrong</h2>
        <button onClick={() => window.location.reload()}>
          Reload
        </button>
      </div>
    )
  }
  
  return <ErrorBoundaryInner>{children}</ErrorBoundaryInner>
}

// Form errors
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

### 3. Success Feedback
```jsx
// Toast notification
function Toast({ message, type = 'info' }) {
  return (
    <div className={`toast toast-${type}`} role="alert">
      {message}
    </div>
  )
}

// Operation success
async function handleSubmit() {
  try {
    await save(data)
    showToast('Saved successfully', 'success')
  } catch (error) {
    showToast('Failed to save', 'error')
  }
}
```

### 4. Empty State
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

// Usage
{users.length === 0 ? (
  <EmptyState
    icon="👤"
    title="No users yet"
    description="Create a new user to get started"
    action={{ label: 'Create User', onClick: () => {} }}
  />
) : (
  <UserList users={users} />
)}
```

### 5. Offline Support
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

## Monitoring and Analytics

```
You:
How do I monitor frontend performance?

AI:
## Frontend Performance Monitoring

### 1. Performance API
```javascript
// Measure page load
const perfData = performance.getEntriesByType('navigation')[0]
console.log({
  dns: perfData.domainLookupEnd - perfData.domainLookupStart,
  tcp: perfData.connectEnd - perfData.connectStart,
  ttfb: perfData.responseStart - perfData.requestStart,
  download: perfData.responseEnd - perfData.responseStart,
  total: perfData.loadEventEnd - perfData.navigationStart
})

// Measure resources
performance.getEntriesByType('resource').forEach(resource => {
  console.log(`${resource.name}: ${resource.duration}ms`)
})
```

### 2. Web Vitals
```javascript
import { onLCP, onFID, onCLS } from 'web-vitals'

onLCP((metric) => {
  console.log('LCP:', metric.value)
  // Report to analytics service
})

onFID((metric) => {
  console.log('FID:', metric.value)
})

onCLS((metric) => {
  console.log('CLS:', metric.value)
})
```

### 3. Error Monitoring
```javascript
// Global error handler
window.addEventListener('error', (event) => {
  reportError({
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno
  })
})

// Promise errors
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

### 4. Third-Party Monitoring
```javascript
// Sentry
import * as Sentry from '@sentry/browser'

Sentry.init({
  dsn: 'https://xxx@sentry.io/xxx',
  environment: process.env.NODE_ENV
})

// Manual reporting
Sentry.captureException(new Error('Something went wrong'))
```
```

## Hands-On Exercises

```
1. Measure Core Web Vitals for current pages
2. Optimize image loading
3. Implement skeleton screens
4. Add error boundaries
5. Configure performance monitoring
6. Run Lighthouse audit
7. Continuously monitor and improve
```

**Good user experience is key to retaining users. Every small detail is worth optimizing.**

(End of file - total 459 lines)
