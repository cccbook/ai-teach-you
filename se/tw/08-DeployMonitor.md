# 第 8 章：部署監控

> 自動化上線與監控

---

## 8.1 一鍵部署工具

> 檔案：[08-1-OneClickDeploy.md](../_code/08/08-1-OneClickDeploy.md)

### 部署平台比較

| 平台 | 費用 | 特點 | 適合 |
|------|------|------|------|
| Vercel | 免費額度 | 零設定 | Next.js |
| Railway | 免費額度 | 彈性 | 後端服務 |
| Render | 免費額度 | 簡單 | 全端 |
| Netlify | 免費額度 | 靜態網站 | 靜態網站 |

---

## 8.2 雲端平台選擇

### 前端部署（Vercel）

```bash
# 部署指令
vercel --prod
```

### 後端部署（Railway）

```bash
# 部署指令
railway deploy
```

---

## 8.3 基礎監控設定

> 檔案：[08-2-MonitoringSetup.md](../_code/08/08-2-MonitoringSetup.md)

### 監控項目

| 項目 | 工具 | 費用 |
|------|------|------|
| 錯誤追蹤 | Sentry | 免費額度 |
| 日誌分析 | LogSnag | 免費額度 |
| 可用性 | UptimeRobot | 免費 |
| 效能 | Vercel Analytics | 免費 |

---

## 8.4 AI 輔助異常偵測

### 異常偵測 Prompt

```
分析以下錯誤日誌：

[貼上錯誤日誌]

請：
1. 找出問題根因
2. 建議解決方案
3. 評估嚴重性
```

---

## 8.5 持續改進循環

### 監控 → 分析 → 優化 → 驗證

```
每日監控 → 每週分析 → 每月優化 → 每季回顧
```

---

## 8.6 本章總結

部署監控要點：

1. **一鍵部署**：減少人為錯誤
2. **基礎監控**：及早發現問題
3. **AI 輔助分析**：加速問題診斷
4. **持續改進**：不斷優化體驗

---

## 相關範例檔案

- [08-1-OneClickDeploy.md](../_code/08/08-1-OneClickDeploy.md)
- [08-2-MonitoringSetup.md](../_code/08/08-2-MonitoringSetup.md)
- [08-3-PrometheusLight.yml](../_code/08/08-3-PrometheusLight.yml)
- [08-4-ErrorTracking.md](../_code/08/08-4-ErrorTracking.md)
