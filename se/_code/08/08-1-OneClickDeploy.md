# 一鍵部署指南

> 來源：第 8 章「部署監控」

---

## Vercel 部署

### 步驟

```bash
# 1. 安裝 CLI
npm i -g vercel

# 2. 登入
vercel login

# 3. 部署
vercel --prod
```

### vercel.json

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "nextjs"
}
```

---

## Railway 部署

### railway.json

```json
{
  "$schema": "https://railway.app/schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1
  }
}
```

---

## 部署檢查清單

- [ ] 環境變數設定
- [ ] 資料庫遷移
- [ ] SSL 憑證
- [ ] 監控串接
- [ ] 告警設定
