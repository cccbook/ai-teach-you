# 監控儀表板

> 來源：第 1 章「案例：小型敏捷專案」

---

## 監控架構

```
┌─────────────────────────────────────────────┐
│              監控架構                         │
├─────────────────────────────────────────────┤
│  Sentry    │ 錯誤追蹤                        │
│  LogSnag   │ 日誌分析                        │
│  Uptime    │ 服務可用性                      │
│  Vercel    │ 前端效能                        │
└─────────────────────────────────────────────┘
```

---

## 告警規則

| 指標 | 閾值 | 動作 |
|------|------|------|
| 錯誤率 | > 1% | 發送 Slack |
| 回應時間 | > 2s | 發送 Email |
| 服務宕機 | - | 發送 SMS |
| 庫存低於 | < 10 | 發送 LINE |

---

## 儀表板關鍵指標

- **DAU**：每日活躍用戶
- **轉換率**：瀏覽→購買比例
- **客單價**：平均訂單金額
- **錯誤率**：API 錯誤比例
- **回應時間**：平均 API 延遲

---

## Sentry 設定

```javascript
// next.config.js
const Sentry = require("@sentry/nextjs");

module.exports = {
  sentry: {
    hideSourceMaps: true,
  },
  // ... other config
};
```

```python
# main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://...",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)
```
