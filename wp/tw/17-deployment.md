# 17. 將 AI 網站部署上線

## 部署的基本概念

### 什麼是「部署」

部署（Deploy）就是把你的網站放到網路上，讓所有人都能訪問。

```
本地端 → 部署 → 網路上
（你自己電腦）  （讓大家都能看到）
```

### 不同平台的部署方式

| 平台類型 | 部署方式 |
|---------|----------|
| Wix、Squarespace | 全自動，平台幫你處理 |
| WordPress 自架 | 手動上傳或主機一鍵安裝 |
| 靜態網站 | 推送至托管服務 |
| AI 生成的 HTML | 匯出後手動上傳 |

## Wix 部署

### 發布你的 Wix 網站

```
1. 在 Wix 編輯器點擊右上角「發布」(Publish)
2. 選擇發布方式：
   - 連接自訂網域
   - 使用 Wix 提供的網址
3. 如果連接自訂網域，按照指示設定 DNS
4. 完成！等待幾分鐘後網站上線
```

### 連接自訂網域

```
Wix 後台 → 網域 → 連接網域

1. 選擇「連接你已有的網域」
2. 輸入網域名稱
3. Wix 會給你 DNS 記錄
4. 去網域註冊商設定 DNS
5. 等待驗證通過
```

## WordPress 部署

### 使用 SiteGround（或其他主機）

```
1. 購買主機後，SiteGround 會寄 email 給你
2. 裡面有登入資訊和 cPanel 連結
3. 登入 cPanel，點擊「WordPress Starter」
4. 選擇安裝 WordPress
5. 填寫網站名稱、管理者帳密
6. 點擊「安裝」，等待完成
7. 前往 yoursite.com/wp-admin 開始管理
```

### 匯入 AI 生成的內容

如果你是用 AI 工具設計，然後想搬到 WordPress：

```
方法 1：手動複製貼上
- 在 AI 工具複製內容
- 在 WordPress 貼上
- 調整格式

方法 2：匯入 HTML
- 許多主題支援匯入 demo content
- 或使用 HTML 頁面產生器外掛

方法 3：重建
- 把 AI 生成的當作參考
- 在 WordPress 主題中重新建立
```

## 靜態網站部署

如果你從 AI 工具匯出的是 HTML/CSS/JS 檔案，可以用這些方法部署：

### 選項 1：Netlify（推薦）

```
1. 前往 netlify.com
2. 免費註冊
3. 點擊「Add new site」→「Deploy manually」
4. 把你的網站資料夾拖進去
5. 完成！Netlify 會給你一個網址
6. 之後更新只需拖入新檔案
```

### 選項 2：Vercel

```
1. 前往 vercel.com
2. GitHub 登入或註冊
3. 點擊「New Project」
4. 上傳或連結 GitHub repo
5. 點擊 Deploy
6. 獲得一個 .vercel.app 網址
```

### 選項 3：Cloudflare Pages

```
1. 前往 pages.cloudflare.com
2. 使用 Cloudflare 帳號登入
3. 建立一個新專案
4. 上傳你的網站檔案
5. 完成！獲得 .pages.dev 網址
```

### 選項 4：GitHub Pages（最免費）

```
1. 在 GitHub 建立一個 repo
2. 把網站檔案上傳到 repo
3. 進入 repo 設定 → Pages
4. 選擇 branch 和資料夾
5. 等待部署，獲得 username.github.io/repo-name 網址
```

## GitHub Desktop 教學

如果你不懂 Git 指令，可以用 GitHub Desktop：

### 安裝與設定

```
1. 前往 desktop.github.com
2. 下載並安裝 GitHub Desktop
3. 登入你的 GitHub 帳號
4. 設定 Git 姓名和 email（第一次需要）
```

### 上傳網站檔案

```
1. 點擊「File」→「New Repository」
2. 填寫名稱（會變成網址的一部分）
3. 選擇本機資料夾（放網站檔案的地方）
4. 點擊「Publish repository」

每次修改後：
1. GitHub Desktop 會偵測變更
2. 填寫「Summary」（這次的修改說明）
3. 點擊「Commit to main」
4. 點擊「Push origin」上傳到 GitHub
```

### 啟用 GitHub Pages

```
1. 在 GitHub 進入你的 repo
2. 點擊「Settings」
3. 左側選單找到「Pages」
4. 在「Source」選擇：
   - Branch: main
   - Folder: / (root)
5. 點擊 Save
6. 等待 1-2 分鐘
7. 你的網站就上線了！
```

## 自訂網域設定

### 在 Netlify 設定自訂網域

```
1. 在 Netlify 新增網站
2. 點擊「Domain settings」
3. 點擊「Add custom domain」
4. 輸入你的網域名稱
5. 按照 Netlify 的指示設定 DNS
6. 開啟 HTTPS（Netlify 會自動申請 SSL）
```

### 在 Vercel 設定自訂網域

```
1. 在 Vercel 新增專案
2. 進入專案設定
3. 點擊「Domains」
4. 輸入網域名稱
5. 設定 DNS
6. Vercel 會自動申請 SSL
```

### DNS 設定指示

每個托管服務都會提供類似的設定：

```
通常需要設定：

1. A 記錄或 CNAME：
   - www → 你的網站網址或 IP
   
2. 驗證記錄（如果有的話）：
   - TXT 記錄用於驗證擁有權

範例（Netlify）：
CNAME www → yoursite.netlify.app

範例（Vercel）：
CNAME www → cname.vercel-dns.com
```

## 驗證網站是否上線

### 檢查清單

```
1. 在瀏覽器輸入你的網址
   └→ 確認網站可以正常顯示

2. 檢查 SSL 憑證
   └→ 網址列左邊應該有鎖頭標示
   └→ 應該是 https:// 而不是 http://

3. 測試所有連結
   └→ 點擊幾個連結確認都能正常運作

4. 用無痕視窗測試
   └→ 確保沒有登入狀態殘留的問題

5. 用不同瀏覽器測試
   └→ Chrome、Safari、Firefox 都試試

6. 用手機測試
   └→ 確保響應式設計正常
```

### 常見問題排查

| 問題 | 可能原因 | 解決方法 |
|------|---------|----------|
| 顯示「找不到網頁」 | DNS 還沒生效 | 等 24-48 小時 |
| 顯示不安全 | SSL 沒設定 | 設定 HTTPS |
| 圖片不顯示 | 路徑錯誤 | 檢查圖片路徑 |
| CSS 樣式錯亂 | CSS 路徑問題 | 檢查路徑 |
| 只有首頁能看 | 其他頁面路徑問題 | 檢查 .htaccess |

## 部署後的確認動作

### 必做的確認

- [ ] 網站首頁正常顯示
- [ ] 所有頁面可以正常訪問
- [ ] 圖片正常顯示
- [ ] 表單可以正常提交
- [ ] 手機版顯示正常
- [ ] SSL 憑證有效（https:// 有鎖頭）
- [ ] 提交網站到 Google Search Console

### 提交到 Google Search Console

這一步很重要，讓 Google 知道你的網站存在：

```
1. 前往 search.google.com/search-console
2. 登入 Google 帳號
3. 點擊「新增資源」
4. 輸入你的網址
5. 選擇驗證方法（DNS、HTML 檔案等）
6. 完成驗證
7. 提交 sitemap（如果有）
```

## 備份你的網站

### 為什麼要備份

防止資料遺失、人為錯誤、駭客攻擊等問題。

### WordPress 備份方法

```
方法 1：主機自動備份
- SiteGround 等主機有每日自動備份
- 可在需要時一鍵還原

方法 2：外掛備份
- UpdraftPlus（推薦）
- 設定自動備份頻率
- 備份到雲端儲存

方法 3：手動備份
- cPanel → File Manager → 下載所有檔案
- phpMyAdmin → 匯出資料庫
```

### 靜態網站備份

```
方法：把檔案存在多處
1. 電腦本機一份
2. GitHub repo（等於雲端備份）
3. Google Drive 或 Dropbox（可選）
```

## 部署檢查清單

### 技術確認
- [ ] 網站可以使用 http:// 正常訪問
- [ ] 已設定 HTTPS/SSL
- [ ] 手機版顯示正常
- [ ] 所有連結測試過
- [ ] 表單測試過（可以送出）
- [ ] 網站載入速度合理（<3 秒）

### 內容確認
- [ ] 所有文字內容已完成
- [ ] 所有圖片正常顯示
- [ ] 版權和隱私政策頁面（如需要）
- [ ] 聯絡資訊正確

### SEO 確認
- [ ] 已提交到 Google Search Console
- [ ] Meta title 和 description 已設定
- [ ] 網站地圖（sitemap）已提交
- [ ] 頁面可以正常被 Google 索引

---

下一章，我們會學習如何分析網站數據並持續優化。
