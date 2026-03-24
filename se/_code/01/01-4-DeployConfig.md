# 部署設定

> 來源：第 1 章「案例：小型敏捷專案」

---

## 前端部署（Vercel）

### vercel.json

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "nextjs",
  "installCommand": "npm install"
}
```

### 部署步驟

```bash
# 1. 安裝 Vercel CLI
npm i -g vercel

# 2. 登入
vercel login

# 3. 部署
vercel --prod
```

---

## 後端部署（Railway）

### railway.json

```json
{
  "$schema": "https://railway.app/schema.json",
  "build": {
    "builder": "NIXPACKS",
    "nixpacks": {
      "start": "uvicorn main:app --host 0.0.0.0 --port $PORT"
    }
  },
  "deploy": {
    "numReplicas": 1
  }
}
```

### 環境變數

```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
OPENAI_API_KEY=sk-...
CORS_ORIGINS=https://yourdomain.com
```

---

## 部署檢查清單

- [ ] 環境變數設定正確
- [ ] 資料庫遷移完成
- [ ] SSL 憑證生效
- [ ] CDN 快取清除
- [ ] 監控服務串接
- [ ] 告警規則設定
- [ ] 備份機制啟動
