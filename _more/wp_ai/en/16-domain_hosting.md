# 16. Domain Registration and Hosting Selection

## What Are Domain and Hosting

### Domain (Domain Name)

The domain is your website's "address," for example: `example.com`

```
https://www.example.com
      ↑
   This is the domain
```

### Hosting

Hosting is the "space" where your website files are stored, like the house for your website.

```
How websites work:

User → Enter domain → DNS translation → Find hosting → Display website
                     ↑
                  Domain system
```

## Domain Registration

### Principles for Choosing a Domain

| Principle | Description | Example |
|-----------|-------------|---------|
| Short and memorable | The shorter the better | google.com vs gooooogle.com |
| Easy to spell | Don't use hard-to-spell words | flow vs phlow |
| Brand-oriented | If it's a brand, use brand name | starlight.com |
| Avoid numbers and hyphens | Easy to get confused | my-site.com vs mysite.com |

### Common Domain Name Endings

| Ending | Use For | Price |
|--------|---------|-------|
| .com | Business, company (most common) | $10-20/year |
| .com.tw | Taiwanese company | $30-50/year |
| .org | Organization, non-profit | $10-20/year |
| .net | Network related | $10-20/year |
| .me | Personal, portfolio | $10-20/year |
| .io | Tech, Startup | $30-50/year |
| .co | Company, Startup | $10-20/year |
| .tw | Taiwan | $30-50/year |

### Recommended Domain Registrars

| Service | Features | Price |
|---------|----------|-------|
| Namecheap | User-friendly, transparent pricing | ~$10/year |
| GoDaddy | Largest provider, often has discounts | ~$11/year |
| Google Domains | Google management, simple | ~$12/year |
| Hover | Simple and easy, focused on domains | ~$15/year |
| PChome | Chinese interface, local service | ~$300/year |
| WebNIC | Taiwan local, easy to contact | ~$300/year |

### Domain Purchase Steps (Example with Namecheap)

```
1. Go to namecheap.com
2. Enter desired domain in search box
3. Check if available
4. Add to cart
5. Choose registration period (recommend 1-2 years)
6. Create account
7. Payment
8. Complete! Receive confirmation email
```

### Notes When Purchasing Domain

1. **Privacy protection**: Recommend adding WHOIS privacy protection to avoid personal info being public
2. **Auto-renewal**: Enable auto-renewal to avoid expiration
3. **Enable two-factor verification**: Protect account security
4. **Compare multiple sources**: Different suffixes and providers have very different prices

## Hosting (Virtual Hosting) Selection

### Hosting Types

| Type | Description | Suitable For |
|------|-------------|--------------|
| Shared Hosting | Multiple websites share one server | Personal, small websites |
| VPS | Virtual private server, independent resources | Medium-sized websites |
| Cloud Hosting | AWS, GCP, Azure, etc. cloud services | Websites needing scalability |
| Dedicated Server | One complete server for you | High traffic websites |
| WordPress Hosting | Optimized specifically for WordPress | WordPress users |

### Recommended Hosting Providers

| Provider | Features | Price | Suitable For |
|----------|----------|-------|--------------|
| Bluehost | WordPress official recommendation | $3-8/month | WordPress users |
| SiteGround | Fast speed, good customer service | $4-15/month | Value performance |
| A2 Hosting | Fast speed, affordable | $3-10/month | Value-oriented |
| Hostinger | Cheapest, complete features | $2-10/month | Budget-limited |
| Cloudflare Pages | Free CDN, static sites | Free | Static websites, JAMstack |

### Key Points for Choosing Hosting

| Factor | Description |
|--------|-------------|
| Speed | Check reviews or test yourself |
| Stability | Check uptime guarantee (99.9% or higher) |
| Customer service | 24/7 instant support best |
| Location | Asian data center is faster for Taiwan users |
| Scalability | Easy to upgrade later |
| Price | First year discount vs renewal price |

## Integrated Solutions: Website Platforms

If using platforms like Wix, WordPress.com, Squarespace, you don't need to purchase hosting separately, fees are already included.

### Pros and Cons of Each Solution

| Solution | Pros | Cons |
|----------|------|------|
| AI Building Platform (Wix, etc.) | Simple, fast, all-inclusive | Limited customization, platform decides your fate |
| Self-hosted WordPress | Complete control, flexible | Need to manage hosting and updates |
| Static site + hosting | Fast, cheap, secure | Need technical ability |

## DNS Settings Basics

### What Is DNS

DNS (Domain Name System) is like the phonebook of the internet, translating domain names into IP addresses.

### Common DNS Settings

| Record Type | Use For | Example |
|-------------|---------|---------|
| A Record | Point to server IP | 123.456.78.90 |
| CNAME | Point to another domain | www → @ |
| MX Record | Email server | mail.example.com |
| TXT | Verification, SPF, etc. | "v=spf1..." |

### Connecting Domain to Your Website

**Method 1: Use Platform's DNS**

If using Wix, Squarespace, etc.:
1. Get "domain settings instructions" from platform backend
2. Log into your domain management interface
3. Add records according to instructions

**Method 2: Use Cloudflare**

1. Register Cloudflare
2. Add domain to Cloudflare
3. Cloudflare will give you Nameservers
4. Go to domain registrar to update Nameservers
5. Set DNS in Cloudflare to point to your hosting

## Free Options

### Free Domains

| Option | Description |
|--------|-------------|
| Freenom | Used to have free .tk domains, service stopped |
| Platform subdomains | Wix gives you yoursite.wix.com |
| GitHub Pages | Gives you username.github.io |
| Netlify | Gives you yoursite.netlify.app |

**Note**: Disadvantages of free domains:
- Don't look professional
- Can't have complete control
- May have ads
- Hard to build brand

### Free Hosting/Deployment

| Service | Features |
|---------|----------|
| GitHub Pages | Static website, completely free |
| Netlify | First 100GB traffic free |
| Vercel | First 100GB traffic free |
| Cloudflare Pages | Completely free |
| Firebase Hosting | Spark plan free |
| WordPress.com Free | Basic WordPress features free |

### Free SSL

Almost all hosting and CDN services now provide free SSL certificates:
- Let's Encrypt (most popular)
- Cloudflare (automatic HTTPS)
- SiteGround, Bluehost (built into hosting)

## Real Case: Purchasing Domain and Hosting for New Website

### Scenario

Xiao Ming wants to build a personal blog, domain name is `xiaoming.blog`

### Step 1: Purchase Domain

```
1. Go to Namecheap
2. Search xiaoming.blog
3. Assuming available, choose .blog or .com
4. Add to cart
5. Checkout (assuming choose .com, about $12/year)
```

### Step 2: Choose Hosting

```
Choose: SiteGround WordPress hosting
Plan: StartUp ($4/month)
Renewal: $10/month

Reasons:
- WordPress official recommendation
- Fast speed
- Free SSL
- Automatic WordPress installation
```

### Step 3: Set DNS

```
1. Get website IP address from SiteGround (假设 192.168.1.1)
2. In Namecheap DNS settings:
   - A record: @ → 192.168.1.1
   - CNAME: www → @

3. Wait for DNS to take effect (usually 24-48 hours)
```

### Step 4: Install WordPress

```
1. Install WordPress through SiteGround's one-click install
2. Set admin username and password
3. Log into WordPress backend to start building website
```

### Total Cost Estimate

| Item | First Year | Second Year |
|------|------------|-------------|
| Domain | $12 | $15 |
| Hosting | $48 | $120 |
| **Total** | **$60/year** | **$135/year** |

## Common Questions

### Q: Can I change the domain?

A: Yes, but need to:
1. Purchase new domain
2. Set new DNS
3. Connect new domain to hosting
4. Set 301 redirect from old domain to new domain
5. Update all internal and external links

### Q: Can I skip buying a domain?

A: Yes, but can only use platform-provided subdomains (like `yoursite.wix.com`). Not recommended for formal websites.

### Q: When do I need to upgrade hosting?

A: When you encounter:
- Website loading speed slows down
- Hosting occasionally crashes
- Traffic approaching hosting limits
- Need more features (like SSH, cron job)

---

In the next chapter, we'll learn how to deploy AI websites online.