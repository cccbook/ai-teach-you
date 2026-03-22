# 15. AI Tools for Image Generation and Optimization

## Why Website Images Are Important

Images are the most important visual elements of a website:

> **Good images make your website look professional, attractive, and increase trust**

### The Data Speaks

- Articles with images have 94% longer average reading time
- Visual content is shared 40 times more than text-only content on social media
- 64% of consumers say website images affect their purchase decisions

## Introduction to AI Image Generation Tools

### Comparison of Mainstream Tools

| Tool | Features | Price | Suitable For |
|------|----------|-------|--------------|
| Midjourney | Strong artistic sense, high quality | $10/month | Brand visuals, artistic creation |
| DALL-E 3 | Strong understanding, GPT integration | Paid credits | General use, creative brainstorming |
| Stable Diffusion | Open source free, can be deployed locally | Free (needs hardware) | Need complete control |
| Adobe Firefly | Adobe ecosystem integration | Free credits | Designers, marketers |
| Canva AI | Easy to use, many templates | Free/Pro | Beginners, quick output |
| Ideogram | Strong text generation ability | Free credits | Posters, text logos |

## Midjourney Tutorial

### Basic Operation Process

```
1. Join Discord or use web version
2. Choose paid plan or use free credits
3. Enter /imagine in input box
4. Write Prompt
5. Wait for generation (usually 30-60 seconds)
6. Choose satisfied work to upscale or modify
```

### Basic Prompt Formula

```
Subject description + Style + Light + Angle + Parameters

Example:
A cozy coffee shop interior, warm lighting,
shot from corner angle, 35mm film style,
--ar 16:9 --v 6
```

### Common Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| --ar | Aspect ratio | --ar 16:9 (landscape), --ar 9:16 (mobile) |
| --v | Version | --v 6 (latest version) |
| --niji | Anime style | --niji 5 |
| --style | Style code | --style raw (more realistic) |
| --s | Stylization degree | --s 250 (high stylization) |
| --no | Exclude elements | --no text, watermark |

### Midjourney Website Generation Prompt

```
Theme: [Website type/product/service]
Type: Website UI mockup, clean design
Style: Minimalist, modern, professional
Light: Soft natural lighting
Format: Website screenshot style, browser frame

Example Prompt:
Modern minimalist e-commerce website homepage,
clean white design, product photography showcase,
macbook and iphone mockup, soft lighting,
--ar 16:9 --v 6
```

### Midjourney Background Generation Prompt

```
Type: Abstract background
Elements: [Related elements]
Style: [Desired style]
Colors: [Color scheme]
Format: Seamless, tileable, subtle

Example Prompt:
Abstract geometric background for tech website,
blue and purple gradient, subtle particles,
clean modern style, seamless tileable,
--ar 16:9 --v 6
```

## DALL-E 3 Tutorial

### Usage Methods

```
1. ChatGPT Plus subscribers can use directly in ChatGPT
2. Paid use on OpenAI official website
3. API integration (advanced users)
```

### DALL-E 3 Prompt Characteristics

DALL-E 3 can understand natural language descriptions better than Midjourney, doesn't need precise prompts.

```
Natural description:
"A minimalist yoga mat on wooden floor,
next to a glass of lemonade and an open book,
natural light coming through the window,
giving a calm, relaxed feeling"

DALL-E will automatically understand and generate
```

### Size Selection

| Size | Aspect Ratio | Suitable For |
|------|--------------|--------------|
| 1024x1024 | 1:1 | Social media, icons |
| 1792x1024 | 16:9 | Banners, website Hero |
| 1024x1792 | 9:16 | Mobile banners, Stories |

## Canva AI Tutorial

### Magic Media Feature

Canva's built-in AI image generation tool:

```
1. Enter Canva
2. Click "Apps" → "Magic Media"
3. Enter description
4. Choose style
5. Generate image
```

### Advantages

- Seamlessly integrated with Canva design tools
- Intuitive operation, suitable for beginners
- Can design directly on generated images

## Common Website Image Prompt Library

### Hero Section Background

```
Prompt: A sleek and modern [product/brand type] website hero background,
subtle gradient, professional photography style,
soft and inviting atmosphere, 4k quality

Prompt (Chinese concept): A stylish and modern [type] website hero background,
                          subtle gradient, professional photography style,
                          soft and inviting atmosphere
```

### People Images

```
Prompt: Professional [profession] in modern office,
friendly smile, casual business attire,
natural lighting, head and shoulder shot,
isolated on clean background, high quality

Prompt (Chinese concept): Professional [profession] in modern office,
                          friendly smile, business casual attire, natural light,
                          head and shoulders shot, clean background
```

### Product Display

```
Prompt: [product type] on minimalist white background,
professional product photography,
three-quarter angle, soft shadows,
studio lighting, clean and modern

Prompt (Chinese concept): [product type] on minimalist white background,
                          professional product photography, three-quarter angle,
                          soft shadows, studio lighting
```

### Contextual Images

```
Prompt: Lifestyle photo of [usage scenario],
authentic and natural feeling,
candid moment, warm tones,
magazine quality, 4k

Prompt (Chinese concept): [usage scenario] life photo,
                          authentic natural feeling,
                          captured moment, warm tones, magazine quality
```

### Concept/Illustration

```
Prompt: Abstract illustration of [concept],
flat design style, modern color palette,
clean vector graphics, minimal,
perfect for website hero section

Prompt (Chinese concept): [concept] abstract illustration,
                          flat design style, modern color scheme,
                          clean vector graphics, minimal, suitable for website hero
```

### Icons

```
Prompt: Minimalist [type] icon set,
line art style, consistent stroke width,
[color] color, clean and modern,
transparent background

Prompt (Chinese concept): Minimalist [type] icon set,
                          line art style, consistent stroke width,
                          [color], clean modern, transparent background
```

## AI Image Post-Processing and Optimization

### Remove Background

```
Recommended tools:
- remove.bg (online)
- Canva (built-in feature)
- Photoshop Remove Background (AI feature)

Use for:
- Product image background removal
- People image background removal
- Create transparent PNGs
```

### Image Enlargement

```
Recommended tools:
- Upscayl (free open source)
- VanceAI
- Let's Enhance

Use for:
- Enlarge small images without losing quality
- Improve image resolution
```

### Image Style Transfer

```
Recommended tools:
- Canva (filter styles)
- DeepAI
- Fotor

Use for:
- Adjust image color tone
- Unify website style
- Enhance visual effects
```

### Generate Variations

```
Recommended tools:
- Canva (Magic Edit)
- Adobe Firefly (generate variations)

Use for:
- Generate multiple versions of same concept
- Test different styles
- Get more options
```

## Image Optimization Technical Details

### File Size Optimization

| Tool | Description |
|------|-------------|
| TinyPNG | Compress PNG/JPG, free |
| Squoosh | Google developed, powerful |
| ShortPixel | Supports WebP, online/plugin |
| ImageOptim | Mac specific, high compression rate |

### Recommended Formats

| Format | Use For | Pros/Cons |
|--------|---------|-----------|
| WebP | First choice general format | Small file size, good support |
| JPEG | Photos, complex images | Small file size, some loss |
| PNG | Need transparent background | Large file size, no loss |
| AVIF | Latest format | Smallest file size, new browser support |

### Size Suggestions

| Use | Recommended Size | Max File Size |
|-----|------------------|---------------|
| Hero banner | 1920x1080 | 200KB |
| Body images | 1200x800 | 100KB |
| Product images | 800x800 | 80KB |
| Thumbnails | 300x300 | 30KB |

## AI Image Copyright Notes

### Important Reminders

1. **Read each platform's terms of use**: Different tools have different commercial use permissions
2. **Midjourney**: Paid version can be used for commercial purposes
3. **DALL-E**: Can be used for commercial purposes
4. **Stable Diffusion**: Depends on model used, pay attention to each model's license

### Risks to Avoid

- Don't generate images that imitate brands
- Don't generate images of famous people
- Don't generate any NSFW content
- After generation, recommend making some modifications to ensure uniqueness

### Recommended Practices

1. **Keep generation records**: Screenshot prompts and settings
2. **Do secondary processing**: Add your own design elements
3. **Mix and match**: Combine AI-generated and your own photos
4. **Credit source**: If needed, indicate AI-assisted creation

## Build Your Image Asset Library

### Recommended Folder Structure

```
images/
├── raw/           # AI original generated images
├── edited/        # Edited images
├── web/           # Images for website
├── social/        # Images for social media
└── icons/         # Icons and UI assets
```

### Naming Standards

```
Use meaningful file names:
✓ hero-coffee-shop-1920.jpg
✓ product-sneakers-front.png
✓ icon-play-button.svg

Avoid:
✗ IMG_001.jpg
✗ photo123.png
✗ unnamed-2.gif
```

## Checklist

### Before Generation
- [ ] Clearly know what type of image is needed
- [ ] Prepare detailed Prompt
- [ ] Choose suitable tool

### After Generation
- [ ] Check image quality and resolution
- [ ] Confirm content meets requirements
- [ ] Any copyright concerns?
- [ ] Need post-processing editing?

### Before Use
- [ ] Optimize file size
- [ ] Choose correct file format
- [ ] Add Alt text (SEO)
- [ ] Test display on different screen sizes

---

Part Four complete! You now have core skills for AI-assisted website design.

In the final part, we'll learn how to publish websites online and maintain them continuously.