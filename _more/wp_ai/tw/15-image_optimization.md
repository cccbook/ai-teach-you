# 15. 圖片生成與優化的 AI 工具

## 為什麼網站圖片很重要

圖片是網站最重要的視覺元素：

> **好的圖片讓你的網站看起來專業、有吸引力、增加信任感**

### 數據說話

- 包含圖片的文章平均閱讀時間增加 94%
- 視覺內容在社群上的分享率是純文字的 40 倍
- 64% 的消費者表示網站圖片會影響他們的購買決策

## AI 圖片生成工具介紹

### 主流工具比較

| 工具 | 特色 | 價格 | 適合用途 |
|------|------|------|----------|
| Midjourney | 藝術感強、品質高 | $10/月 | 品牌視覺、藝術創作 |
| DALL-E 3 | 理解力強、GPT 整合 | 付費 Credit | 一般用途、創意發想 |
| Stable Diffusion | 開源免費、可本地部署 | 免費（需硬體） | 需要完全控制 |
| Adobe Firefly | Adobe 生態系整合 | 免費 credit | 設計師、行銷人員 |
| Canva AI | 操作簡單、模板多 | 免費/Pro | 初學者、快速產出 |
| Ideogram | 文字生成能力強 | 免費 credit | 海報、文字 Logo |

## Midjourney 使用教學

### 基本操作流程

```
1. 加入 Discord 或使用網頁版
2. 選擇付費方案或使用免費 credit
3. 在輸入框輸入 /imagine
4. 撰寫 Prompt
5. 等待生成（通常 30-60 秒）
6. 選擇满意的作品放大或微調
```

### 基礎 Prompt 公式

```
主體描述 + 風格 + 光線 + 角度 + 參數

範例：
A cozy coffee shop interior, warm lighting,
shot from corner angle, 35mm film style,
--ar 16:9 --v 6
```

### 常用參數

| 參數 | 說明 | 範例 |
|------|------|------|
| --ar | 比例 | --ar 16:9 (横版), --ar 9:16 (手机) |
| --v | 版本 | --v 6 (最新版本) |
| --niji | 動漫風格 | --niji 5 |
| --style | 風格代碼 | --style raw (更真實) |
| --s | 風格化程度 | --s 250 (高風格化) |
| --no | 排除元素 | --no text, watermark |

### Midjourney 網站生成 Prompt

```
主題：[網站類型/產品/服務]
類型：Website UI mockup, clean design
風格：Minimalist, modern, professional
光線：Soft natural lighting
格式：Website screenshot style, browser frame

範例 Prompt：
Modern minimalist e-commerce website homepage,
clean white design, product photography showcase,
macbook and iphone mockup, soft lighting,
--ar 16:9 --v 6
```

### Midjourney 背景生成 Prompt

```
類型：Abstract background
元素：[相關元素]
風格：[想要的風格]
顏色：[色調]
格式：Seamless, tileable, subtle

範例 Prompt：
Abstract geometric background for tech website,
blue and purple gradient, subtle particles,
clean modern style, seamless tileable,
--ar 16:9 --v 6
```

## DALL-E 3 使用教學

### 使用方式

```
1. ChatGPT Plus 訂閱者可以直接在 ChatGPT 使用
2. OpenAI 官網付費使用
3. API 串接（進階用戶）
```

### DALL-E 3 Prompt 特點

DALL-E 3 比 Midjourney 更能理解自然語言描述，不需要太精確的咒語。

```
自然描述：
「一個簡約風格的瑜伽墊，放在木質地板上，
旁邊有一杯檸檬水和一本打開的書，
自然光從窗户照進來，
給人平靜、放鬆的感覺」

DALL-E 會自動理解並生成
```

### 尺寸選擇

| 尺寸 | 比例 | 適合用途 |
|------|------|----------|
| 1024x1024 | 1:1 | 社交媒體、圖示 |
| 1792x1024 | 16:9 | 橫幅、網站 Hero |
| 1024x1792 | 9:16 | 手機橫幅、Story |

## Canva AI 使用教學

### Magic Media 功能

Canva 內建的 AI 圖片生成工具：

```
1. 進入 Canva
2. 點擊「Apps」→「Magic Media」
3. 輸入描述
4. 選擇風格
5. 生成圖片
```

### 優點

- 與 Canva 設計工具無縫整合
- 操作直覺，適合初學者
- 可以直接在生成的圖片上設計

## 網站常用圖片 Prompt 庫

### Hero 區背景

```
Prompt：A sleek and modern [產品/品牌類型] website hero background,
subtle gradient, professional photography style,
soft and inviting atmosphere, 4k quality

 Prompt（中文概念）：一個時尚且現代的[類型]網站主視覺背景，
                    細膩的漸層，專業攝影風格，柔和吸引人的氛圍
```

### 人物圖片

```
 Prompt：Professional [職業] in modern office,
friendly smile, casual business attire,
natural lighting, head and shoulder shot,
isolated on clean background, high quality

 Prompt（中文概念）：專業的[職業]在現代化辦公室，
                    友善的微笑，商務休閒穿著，自然光，
                    頭肩照，乾淨背景
```

### 產品展示

```
 Prompt：[產品類型] on minimalist white background,
professional product photography,
three-quarter angle, soft shadows,
studio lighting, clean and modern

 Prompt（中文概念）：[產品類型]在極簡白色背景上，
                    專業產品攝影，四分之三角度，
                    柔和陰影，攝影棚燈光
```

### 情境圖片

```
 Prompt：Lifestyle photo of [使用情境],
authentic and natural feeling,
candid moment, warm tones,
magazine quality, 4k

 Prompt（中文概念）：[使用情境]的生活照片，
                    真實自然的感覺，
                    捕捉瞬間，暖色調，雜誌品質
```

### 概念圖/插圖

```
 Prompt：Abstract illustration of [概念],
flat design style, modern color palette,
clean vector graphics, minimal,
perfect for website hero section

 Prompt（中文概念）：[概念]的抽象插圖，
                    扁平設計風格，現代配色，
                    乾淨向量圖形，極簡，適合網站主視覺
```

### 圖示/Icon

```
 Prompt：Minimalist [類型] icon set,
line art style, consistent stroke width,
[顏色] color, clean and modern,
transparent background

 Prompt（中文概念）：極簡[類型]圖示套組，
                    線條藝術風格，一致的線條粗細，
                    [顏色]，乾淨現代，透明背景
```

## AI 圖片後製與優化

### 移除背景

```
推薦工具：
- remove.bg（線上）
- Canva（內建功能）
- Photoshop Remove Background（AI 功能）

用途：
- 產品圖去背
- 人物圖去背
- 製作透明 PNG
```

### 圖片放大

```
推薦工具：
- Upscayl（免費開源）
- VanceAI
- Let’s Enhance

用途：
- 將小圖放大而不失真
- 提升圖片解析度
```

### 圖片風格轉換

```
推薦工具：
- Canva（濾鏡風格）
- DeepAI
- Fotor

用途：
- 調整圖片色調
- 統一網站風格
- 增強視覺效果
```

### 生成變體

```
推薦工具：
- Canva（Magic Edit）
- Adobe Firefly（生成變體）

用途：
- 同一概念生成多個版本
- 測試不同風格
- 獲得更多選擇
```

## 圖片優化技術細節

### 檔案大小優化

| 工具 | 說明 |
|------|------|
| TinyPNG | 壓縮 PNG/JPG，免費 |
| Squoosh | Google 開發，功能強大 |
| ShortPixel | 支援 WebP，在線/插件 |
| ImageOptim | Mac 專用，壓縮率高 |

### 推薦格式

| 格式 | 用途 | 優缺點 |
|------|------|--------|
| WebP | 首選通用格式 | 檔案小，支援度好 |
| JPEG | 照片、複雜圖片 | 檔案小，有失真 |
| PNG | 需要透明背景 | 檔案大，無失真 |
| AVIF | 最新格式 | 最小檔案，新瀏覽器支援 |

### 尺寸建議

| 用途 | 建議尺寸 | 最大檔案大小 |
|------|---------|-------------|
| Hero 橫幅 | 1920x1080 | 200KB |
| 內文圖片 | 1200x800 | 100KB |
| 產品圖 | 800x800 | 80KB |
| 縮圖 | 300x300 | 30KB |

## AI 圖片版權須知

### 重要提醒

1. **閱讀各平台的使用條款**：不同工具有不同的商業使用許可
2. **Midjourney**：付費版可用於商業用途
3. **DALL-E**：可用於商業用途
4. **Stable Diffusion**：取決於使用的模型，注意各模型授權

### 避免的風險

- 不要生成仿冒品牌的圖片
- 不要生成知名人物的圖片
- 不要生成任何 NSFW 內容
- 生成後建議做一些修改，確保獨特性

### 建議做法

1. **保留生成記錄**：截圖 Prompt 和設定
2. **進行二次加工**：加入自己的設計元素
3. **混合使用**：結合 AI 生成和自己拍攝的圖片
4. **標註來源**：如果需要的話標明 AI 輔助創作

## 建立你的圖片素材庫

### 建議的資料夾結構

```
images/
├── raw/           # AI 原始生成圖
├── edited/        # 編輯後的圖片
├── web/           # 網站用圖片
├── social/        # 社群用圖片
└── icons/         # 圖示和 UI 素材
```

### 命名規範

```
使用有意義的檔案名稱：
✓ hero-coffee-shop-1920.jpg
✓ product-sneakers-front.png
✓ icon-play-button.svg

避免：
✗ IMG_001.jpg
✗ photo123.png
✗ 未命名-2.gif
```

## 檢查清單

### 生成前
- [ ] 清楚知道需要什麼類型的圖片
- [ ] 準備好詳細的 Prompt
- [ ] 選擇適合的工具

### 生成後
- [ ] 檢查圖片品質和解析度
- [ ] 確認內容符合需求
- [ ] 是否有版權疑慮
- [ ] 是否需要後製編輯

### 使用前
- [ ] 優化檔案大小
- [ ] 選擇正確的檔案格式
- [ ] 加入 Alt 文字（SEO）
- [ ] 測試不同螢幕尺寸的顯示

---

第四部分完成！你現在已經掌握了 AI 輔助網站設計的核心技巧。

接下來進入最後一部分，我們會學習如何將網站發布上線並持續維護。
