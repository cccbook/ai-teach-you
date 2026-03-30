# 錯誤追蹤設定

> 來源：第 8 章「部署監控」

---

## Sentry 錯誤追蹤

### 安裝

```bash
npm install @sentry/nextjs
```

### 設定

```javascript
// sentry.client.config.js
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
});
```

---

## 常見錯誤處理

### 前端錯誤邊界

```jsx
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    Sentry.captureException(error, { extra: errorInfo });
  }
  
  render() {
    return this.props.children;
  }
}
```

### 後端錯誤處理

```python
from fastapi import FastAPI
from sentry_sdk import init as sentry_init

sentry_init(dsn="https://...")

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # 記錄錯誤
    return JSONResponse({"error": str(exc)})
```
