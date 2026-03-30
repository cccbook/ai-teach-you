# 32. 安全性最佳實踐

## 安全是每個人的責任

```
┌─────────────────────────────────────────────────────────┐
│                   安全意识                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   安全不是事后补救，而是设计阶段就要考虑                  │
│                                                         │
│   OWASP Top 10：                                        │
│   1. Injection                                         │
│   2. Broken Authentication                              │
│   3. Sensitive Data Exposure                           │
│   4. XML External Entities (XXE)                       │
│   5. Broken Access Control                             │
│   6. Security Misconfiguration                          │
│   7. XSS                                                │
│   8. Insecure Deserialization                          │
│   9. Using Components with Known Vulnerabilities        │
│   10. Insufficient Logging & Monitoring                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 注入攻擊防護

```
你：
如何防止 SQL 注入？

AI：
## SQL 注入防护

### 1. 参数化查询（最重要）
```javascript
// ❌ 危险：字符串拼接
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// ✅ 安全：参数化查询
const query = 'SELECT * FROM users WHERE id = $1';
db.query(query, [userId]);

// Node.js + PostgreSQL
const result = await pool.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);
```

### 2. ORM 使用
```javascript
// Sequelize 参数化
const user = await User.findOne({
  where: { email: email }
});

// Prisma 参数化
const user = await prisma.user.findUnique({
  where: { email: email }
});
```

### 3. 验证输入
```javascript
// 白名单验证
const ALLOWED_SORT_FIELDS = ['createdAt', 'name', 'price'];
const sortField = ALLOWED_SORT_FIELDS.includes(sort) ? sort : 'createdAt';

// 类型验证
const userId = parseInt(req.params.userId);
if (isNaN(userId)) {
  return res.status(400).json({ error: 'Invalid user ID' });
}
```

### NoSQL 注入
```javascript
// MongoDB
// ❌ 危险
const query = { username: req.body.username };

// ✅ 安全
const username = String(req.body.username).trim();
const query = { username: username };
```
```

### 防止 XSS

```
你：
如何防止 XSS 攻击？

AI：
## XSS 防护

### 1. 输出转义
```javascript
// 在模板中转义
// React (默认转义)
<div>{userInput}</div>

// 手动转义
const escapeHtml = (str) => {
  const escapeMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;'
  };
  return str.replace(/[&<>"']/g, (c) => escapeMap[c]);
};
```

### 2. CSP (Content Security Policy)
```javascript
// Express
const csp = require('helmet');
app.use(csp({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'nonce-{generated-nonce}'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "https:"],
    connectSrc: ["'self'", "https://api.example.com"]
  }
}));
```

### 3. HTTPOnly + Secure Cookie
```javascript
// 设置安全 Cookie
res.cookie('session', token, {
  httpOnly: true,  // 禁止 JavaScript 访问
  secure: true,    // 仅 HTTPS
  sameSite: 'strict'  // CSRF 保护
});
```
```

## 認證與授權

```
你：
如何设计安全的认证系统？

AI：
## 认证安全

### 1. 密码存储
```javascript
// ❌ 危险：明文或简单哈希
const hash = crypto.createHash('md5').update(password).digest('hex');

// ✅ 安全：Bcrypt
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

const hash = await bcrypt.hash(password, SALT_ROUNDS);
const match = await bcrypt.compare(password, hash);

// ✅ 更安全：Argon2
const argon2 = require('argon2');
const hash = await argon2.hash(password);
const match = await argon2.verify(hash, password);
```

### 2. 密码策略
```javascript
const validatePassword = (password) => {
  const errors = [];
  
  if (password.length < 8) {
    errors.push('密码至少8个字符');
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('密码包含大写字母');
  }
  if (!/[a-z]/.test(password)) {
    errors.push('密码包含小写字母');
  }
  if (!/[0-9]/.test(password)) {
    errors.push('密码包含数字');
  }
  
  return errors;
};
```

### 3. 登录限制
```javascript
// 限制尝试次数
const loginAttempts = new Map();

app.post('/login', async (req, res) => {
  const { email } = req.body;
  const attempts = loginAttempts.get(email) || { count: 0, lastAttempt: 0 };
  
  // 5分钟内超过5次尝试
  if (attempts.count >= 5 && Date.now() - attempts.lastAttempt < 5 * 60 * 1000) {
    return res.status(429).json({ 
      error: '登录尝试过于频繁，请5分钟后重试' 
    });
  }
  
  // 验证逻辑...
  if (!success) {
    loginAttempts.set(email, {
      count: attempts.count + 1,
      lastAttempt: Date.now()
    });
  } else {
    loginAttempts.delete(email);
  }
});
```

### 4. JWT 安全
```javascript
// 安全的 JWT 验证
const jwt = require('jsonwebtoken');

const verifyToken = (token) => {
  try {
    return jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],  // 指定算法
      issuer: 'my-app',       // 发行者验证
      audience: 'my-app-api'  // 受众验证
    });
  } catch (error) {
    return null;
  }
};

// Token 黑名单（登出时）
const blacklistedTokens = new Set();
app.post('/logout', authenticate, (req, res) => {
  blacklistedTokens.add(req.token);
  res.json({ message: '已登出' });
});
```

## 敏感資料保護

```
你：
如何保护敏感数据？

AI：
## 敏感数据保护

### 1. 环境变量
```bash
# .env（不提交）
DATABASE_URL=postgres://...
JWT_SECRET=your-secret-key
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

### 2. 密钥管理
```javascript
// ❌ 硬编码
const API_KEY = 'sk_live_abc123';

// ✅ 环境变量
const API_KEY = process.env.API_KEY;

// ✅ 密钥管理服务
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

const client = new SecretsManagerClient({ region: 'ap-northeast-1' });
const command = new GetSecretValueCommand({ SecretId: 'my-api-key' });
const response = await client.send(command);
const API_KEY = JSON.parse(response.SecretString).apiKey;
```

### 3. 数据加密
```javascript
// 文件加密
const fs = require('fs');
const crypto = require('crypto');

const encrypt = (data, key) => {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return { iv: iv.toString('hex'), encrypted, authTag: authTag.toString('hex') };
};

// 数据库字段加密
const encryptField = (value, encryptionKey) => {
  const key = Buffer.from(encryptionKey, 'hex');
  return encrypt(JSON.stringify(value), key);
};
```

### 4. 敏感日志脱敏
```javascript
const redactSensitive = (data) => {
  const sensitiveFields = ['password', 'token', 'secret', 'apiKey', 'creditCard'];
  
  const redact = (obj) => {
    if (!obj || typeof obj !== 'object') return obj;
    
    const redacted = Array.isArray(obj) ? [...obj] : { ...obj };
    
    for (const key of Object.keys(redacted)) {
      if (sensitiveFields.some(f => key.toLowerCase().includes(f))) {
        redacted[key] = '***REDACTED***';
      } else if (typeof redacted[key] === 'object') {
        redacted[key] = redact(redacted[key]);
      }
    }
    
    return redacted;
  };
  
  return redact(data);
};
```

## CSRF 與 CORS

```
你：
如何防止 CSRF 攻击？

AI：
## CSRF 防护

### 1. CSRF Token
```javascript
// 生成 Token
app.get('/form', authenticate, (req, res) => {
  const csrfToken = crypto.randomBytes(32).toString('hex');
  req.session.csrfToken = csrfToken;
  res.json({ csrfToken });
});

// 验证 Token
const csrfMiddleware = (req, res, next) => {
  const token = req.headers['x-csrf-token'] || req.body._csrf;
  
  if (token !== req.session.csrfToken) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  
  next();
};

app.post('/transfer', authenticate, csrfMiddleware, (req, res) => {
  // 处理请求
});
```

### 2. SameSite Cookie
```javascript
res.cookie('sessionId', sessionId, {
  httpOnly: true,
  sameSite: 'strict',  // CSRF 保护
  secure: true
});
```

### CORS 配置
```javascript
const cors = require('cors');

const corsOptions = {
  origin: ['https://example.com', 'https://app.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400  // 预检请求缓存 24 小时
};

app.use(cors(corsOptions));
```
```

## 安全 Headers

```
你：
需要设置哪些安全 headers？

AI：
## 安全 Headers

### Express + Helmet
```javascript
const helmet = require('helmet');

app.use(helmet());

// 详细配置
app.use(helmet({
  // 防止点击劫持
  frameguard: { action: 'deny' },
  
  // XSS 过滤器
  xssFilter: true,
  
  // 禁用 IE XSS 过滤器
  noSniff: true,
  
  // 强制 HTTPS
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  
  // 内容类型猜测
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'"]
    }
  }
}));
```

### 完整 Headers 列表
```yaml
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```
```

## 安全掃描

```
你：
如何进行安全扫描？

AI：
## 安全扫描工具

### 1. 依赖扫描
```bash
# npm audit
npm audit

# Snyk
npm install -g snyk
snyk test

# GitHub 依赖检查
# Settings → Security → Dependency review
```

### 2. 代码扫描
```bash
# SonarQube
sonar-scanner

# Semgrep
semgrep --config=auto .
```

### 3. 渗透测试
```bash
# OWASP ZAP (DAST)
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://myapp.com
```

### 4. CI 集成
```yaml
# GitHub Actions
- name: Security scan
  run: |
    npm audit --audit-level=high
    snyk test
    semgrep --config=auto .
```

### 自动化扫描清单
```
□ 依赖漏洞扫描（npm audit, Snyk）
□ 代码质量扫描（SonarQube, CodeQL）
□ SAST（静态应用安全测试）
□ DAST（动态应用安全测试）
□ 秘密扫描（Gitleaks, TruffleHog）
```
```

## 實踐練習

```
1. 审计你的代码安全
2. 修复所有高危漏洞
3. 配置安全 Headers
4. 设置依赖扫描
5. 配置 WAF（如适用）
6. 建立安全检查清单
7. 定期安全培训
```

**安全不是功能，而是態度。將安全納入開發流程的每一步。**
