# 監控設定

> 來源：第 8 章「部署監控」

---

## 監控工具清單

| 工具 | 用途 | 費用 |
|------|------|------|
| Sentry | 錯誤追蹤 | 免費額度 |
| LogSnag | 日誌分析 | 免費額度 |
| UptimeRobot | 可用性 | 免費 |
| Vercel Analytics | 效能 | 免費 |
| Datadog | 企業監控 | $15/月 |

---

## Sentry 設定

```javascript
// next.config.js
const Sentry = require("@sentry/nextjs");

module.exports = {
  sentry: {
    hideSourceMaps: true,
  },
};
```

---

## 告警規則

| 指標 | 閾值 | 動作 |
|------|------|------|
| 錯誤率 | > 1% | Slack |
| 回應時間 | > 2s | Email |
| 服務宕機 | - | SMS |
| CPU 使用率 | > 80% | Slack |
