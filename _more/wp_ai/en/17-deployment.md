# 17. Deploying AI Websites Online

## Basic Concepts of Deployment

### What Is "Deployment"

Deployment (Deploy) is putting your website on the internet so everyone can access it.

```
Local → Deployment → Online
(Your computer)  (Everyone can see)
```

### Deployment Methods for Different Platforms

| Platform Type | Deployment Method |
|---------------|-------------------|
| Wix, Squarespace | Automatic, platform handles for you |
| WordPress self-hosted | Manual upload or host one-click install |
| Static site | Push to hosting service |
| AI-generated HTML | Export then manually upload |

## Wix Deployment

### Publish Your Wix Website

```
1. Click "Publish" in Wix editor
2. Choose publishing method:
   - Connect custom domain
   - Use Wix-provided URL
3. If connecting custom domain, follow instructions to set DNS
4. Complete! Wait a few minutes, website is online
```

### Connect Custom Domain

```
Wix backend → Domains → Connect domain

1. Choose "Connect your existing domain"
2. Enter domain name
3. Wix will give you DNS records
4. Go to domain registrar to set DNS
5. Wait for verification to pass
```

## WordPress Deployment

### Using SiteGround (or other hosts)

```
1. After purchasing hosting, SiteGround will send you email
2. Contains login info and cPanel link
3. Log into cPanel, click "WordPress Starter"
4. Choose to install WordPress
5. Fill in website name, admin account/password
6. Click "Install", wait for completion
7. Go to yoursite.com/wp-admin to start managing
```

### Import AI-Generated Content

If you designed with AI tools and want to move to WordPress:

```
Method 1: Manual copy-paste
- Copy content in AI tool
- Paste in WordPress
- Adjust format

Method 2: Import HTML
- Many themes support importing demo content
- Or use HTML page builder plugin

Method 3: Rebuild
- Use AI-generated as reference
- Rebuild in WordPress theme
```

## Static Site Deployment

If you exported HTML/CSS/JS files from AI tools, you can deploy using these methods:

### Option 1: Netlify (Recommended)

```
1. Go to netlify.com
2. Register for free
3. Click "Add new site" → "Deploy manually"
4. Drag your website folder in
5. Complete! Netlify will give you a URL
6. For updates, just drag in new files
```

### Option 2: Vercel

```
1. Go to vercel.com
2. Log in or register with GitHub
3. Click "New Project"
4. Upload or connect GitHub repo
5. Click Deploy
6. Get a .vercel.app URL
```

### Option 3: Cloudflare Pages

```
1. Go to pages.cloudflare.com
2. Log in with Cloudflare account
3. Create a new project
4. Upload your website files
5. Complete! Get a .pages.dev URL
```

### Option 4: GitHub Pages (Most Free)

```
1. Create a repo on GitHub
2. Upload website files to repo
3. Go to repo settings → Pages
4. Choose branch and folder
5. Wait for deployment, get username.github.io/repo-name URL
```

## GitHub Desktop Tutorial

If you don't understand Git commands, you can use GitHub Desktop:

### Installation and Setup

```
1. Go to desktop.github.com
2. Download and install GitHub Desktop
3. Log into your GitHub account
4. Set Git name and email (needed first time)
```

### Upload Website Files

```
1. Click "File" → "New Repository"
2. Fill in name (will become part of URL)
3. Choose local folder (where website files are)
4. Click "Publish repository"

After each modification:
1. GitHub Desktop will detect changes
2. Fill in "Summary" (this modification's description)
3. Click "Commit to main"
4. Click "Push origin" to upload to GitHub
```

### Enable GitHub Pages

```
1. Go to your repo on GitHub
2. Click "Settings"
3. Find "Pages" in left menu
4. In "Source" choose:
   - Branch: main
   - Folder: / (root)
5. Click Save
6. Wait 1-2 minutes
7. Your website is now online!
```

## Custom Domain Setup

### Set Custom Domain on Netlify

```
1. Add site on Netlify
2. Click "Domain settings"
3. Click "Add custom domain"
4. Enter your domain name
5. Follow Netlify's instructions to set DNS
6. Enable HTTPS (Netlify will automatically apply for SSL)
```

### Set Custom Domain on Vercel

```
1. Add project on Vercel
2. Go to project settings
3. Click "Domains"
4. Enter domain name
5. Set DNS
6. Vercel will automatically apply for SSL
```

### DNS Setup Instructions

Each hosting service provides similar setup:

```
Usually need to set:

1. A record or CNAME:
   - www → your website URL or IP

2. Verification records (if any):
   - TXT record for ownership verification

Example (Netlify):
CNAME www → yoursite.netlify.app

Example (Vercel):
CNAME www → cname.vercel-dns.com
```

## Verify Website Is Online

### Checklist

```
1. Enter your URL in browser
   └→ Confirm website displays normally

2. Check SSL certificate
   └→ There should be a lock icon on left of URL bar
   └→ Should be https:// not http://

3. Test all links
   └→ Click a few links to confirm they work

4. Test with incognito window
   └→ Ensure no login state residue issues

5. Test with different browsers
   └→ Try Chrome, Safari, Firefox

6. Test on mobile
   └→ Ensure responsive design works
```

### Common Problem Troubleshooting

| Problem | Possible Reason | Solution |
|---------|-----------------|----------|
| Shows "Page not found" | DNS hasn't taken effect yet | Wait 24-48 hours |
| Shows insecure | SSL not set | Set up HTTPS |
| Images don't display | Path error | Check image paths |
| CSS styles broken | CSS path issue | Check paths |
| Only homepage works | Other pages path issue | Check .htaccess |

## Post-Deployment Confirmation Actions

### Must Confirm

- [ ] Website homepage displays properly
- [ ] All pages can be accessed normally
- [ ] Images display properly
- [ ] Forms can submit properly
- [ ] Mobile version displays properly
- [ ] SSL certificate valid (https:// has lock icon)
- [ ] Submit website to Google Search Console

### Submit to Google Search Console

This is important so Google knows your website exists:

```
1. Go to search.google.com/search-console
2. Log into Google account
3. Click "Add property"
4. Enter your URL
5. Choose verification method (DNS, HTML file, etc.)
6. Complete verification
7. Submit sitemap (if available)
```

## Back Up Your Website

### Why Backup

Prevent data loss, human errors, hacker attacks, etc.

### WordPress Backup Methods

```
Method 1: Host automatic backup
- SiteGround and other hosts have daily automatic backups
- Can restore with one click when needed

Method 2: Plugin backup
- UpdraftPlus (recommended)
- Set automatic backup frequency
- Backup to cloud storage

Method 3: Manual backup
- cPanel → File Manager → Download all files
- phpMyAdmin → Export database
```

### Static Site Backup

```
Method: Store files in multiple places
1. One copy on local computer
2. GitHub repo (equals cloud backup)
3. Google Drive or Dropbox (optional)
```

## Deployment Checklist

### Technical Confirmation
- [ ] Website can be accessed normally with http://
- [ ] HTTPS/SSL is set
- [ ] Mobile version displays properly
- [ ] All links tested
- [ ] Forms tested (can submit)
- [ ] Website loading speed reasonable (<3 seconds)

### Content Confirmation
- [ ] All text content completed
- [ ] All images display properly
- [ ] Copyright and privacy policy pages (if needed)
- [ ] Contact info correct

### SEO Confirmation
- [ ] Submitted to Google Search Console
- [ ] Meta title and description set
- [ ] Sitemap submitted
- [ ] Pages can be indexed by Google normally

---

In the next chapter, we'll learn how to analyze website data and continuously optimize.