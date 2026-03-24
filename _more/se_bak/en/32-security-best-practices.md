# 32. Security Best Practices

## Security is Everyone's Responsibility

```
┌─────────────────────────────────────────────────────────┐
│                   Security Awareness                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Security is not an afterthought, it's designed in      │
│                                                         │
│   OWASP Top 10:                                        │
│   1. Injection                                         │
│   2. Broken Authentication                             │
│   3. Sensitive Data Exposure                          │
│   4. XML External Entities (XXE)                       │
│   5. Broken Access Control                            │
│   6. Security Misconfiguration                        │
│   7. XSS                                              │
│   8. Insecure Deserialization                        │
│   9. Using Components with Known Vulnerabilities      │
│   10. Insufficient Logging & Monitoring              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Injection Attack Prevention

```
You:
How to prevent SQL injection?

AI:
## SQL Injection Prevention

### 1. Parameterized Queries (Most Important)
```javascript
// ❌ Dangerous: String concatenation
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// ✅ Safe: Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
db.query(query, [userId]);

// Node.js + PostgreSQL
const result = await pool.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);
```

### 2. Using ORM
```javascript
// Sequelize parameterized
const user = await User.findOne({
  where: { email: email }
});

// Prisma parameterized
const user = await prisma.user.findUnique({
  where: { email: email }
});
```

### 3. Input Validation
```javascript
// Whitelist validation
const ALLOWED_SORT_FIELDS = ['createdAt', 'name', 'price'];
const sortField = ALLOWED_SORT_FIELDS.includes(sort) ? sort : 'createdAt';

// Type validation
const userId = parseInt(req.params.userId);
if (isNaN(userId)) {
  return res.status(400).json({ error: 'Invalid user ID' });
}
```

### NoSQL Injection
```javascript
// MongoDB
// ❌ Dangerous
const query = { username: req.body.username };

// ✅ Safe
const username = String(req.body.username).trim();
const query = { username: username };
```

## Preventing XSS

```
You:
How to prevent XSS attacks?

AI:
## XSS Prevention

### 1. Output Escaping
```javascript
// In templates
// React (auto-escapes by default)
<div>{userInput}</div>

// Manual escape
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
// Set secure cookie
res.cookie('session', token, {
  httpOnly: true,  // Block JavaScript access
  secure: true,    // HTTPS only
  sameSite: 'strict'  // CSRF protection
});
```

## Authentication and Authorization

```
You:
How to design a secure authentication system?

AI:
## Authentication Security

### 1. Password Storage
```javascript
// ❌ Dangerous: Plaintext or simple hash
const hash = crypto.createHash('md5').update(password).digest('hex');

// ✅ Safe: Bcrypt
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

const hash = await bcrypt.hash(password, SALT_ROUNDS);
const match = await bcrypt.compare(password, hash);

// ✅ Even Safer: Argon2
const argon2 = require('argon2');
const hash = await argon2.hash(password);
const match = await argon2.verify(hash, password);
```

### 2. Password Policy
```javascript
const validatePassword = (password) => {
  const errors = [];
  
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters');
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain uppercase letter');
  }
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain lowercase letter');
  }
  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain number');
  }
  
  return errors;
};
```

### 3. Login Rate Limiting
```javascript
// Limit login attempts
const loginAttempts = new Map();

app.post('/login', async (req, res) => {
  const { email } = req.body;
  const attempts = loginAttempts.get(email) || { count: 0, lastAttempt: 0 };
  
  // More than 5 attempts in 5 minutes
  if (attempts.count >= 5 && Date.now() - attempts.lastAttempt < 5 * 60 * 1000) {
    return res.status(429).json({ 
      error: 'Too many login attempts, please try again in 5 minutes' 
    });
  }
  
  // Verification logic...
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

### 4. JWT Security
```javascript
// Secure JWT verification
const jwt = require('jsonwebtoken');

const verifyToken = (token) => {
  try {
    return jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],  // Specify algorithm
      issuer: 'my-app',       // Issuer verification
      audience: 'my-app-api'  // Audience verification
    });
  } catch (error) {
    return null;
  }
};

// Token blacklist (for logout)
const blacklistedTokens = new Set();
app.post('/logout', authenticate, (req, res) => {
  blacklistedTokens.add(req.token);
  res.json({ message: 'Logged out' });
});
```

## Sensitive Data Protection

```
You:
How to protect sensitive data?

AI:
## Sensitive Data Protection

### 1. Environment Variables
```bash
# .env (don't commit)
DATABASE_URL=postgres://...
JWT_SECRET=your-secret-key
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

### 2. Secret Management
```javascript
// ❌ Hardcoded
const API_KEY = 'sk_live_abc123';

// ✅ Environment variable
const API_KEY = process.env.API_KEY;

// ✅ Secret management service
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

const client = new SecretsManagerClient({ region: 'us-east-1' });
const command = new GetSecretValueCommand({ SecretId: 'my-api-key' });
const response = await client.send(command);
const API_KEY = JSON.parse(response.SecretString).apiKey;
```

### 3. Data Encryption
```javascript
// File encryption
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

// Database field encryption
const encryptField = (value, encryptionKey) => {
  const key = Buffer.from(encryptionKey, 'hex');
  return encrypt(JSON.stringify(value), key);
};
```

### 4. Sensitive Log Redaction
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

## CSRF and CORS

```
You:
How to prevent CSRF attacks?

AI:
## CSRF Prevention

### 1. CSRF Token
```javascript
// Generate token
app.get('/form', authenticate, (req, res) => {
  const csrfToken = crypto.randomBytes(32).toString('hex');
  req.session.csrfToken = csrfToken;
  res.json({ csrfToken });
});

// Verify token
const csrfMiddleware = (req, res, next) => {
  const token = req.headers['x-csrf-token'] || req.body._csrf;
  
  if (token !== req.session.csrfToken) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  
  next();
};

app.post('/transfer', authenticate, csrfMiddleware, (req, res) => {
  // Handle request
});
```

### 2. SameSite Cookie
```javascript
res.cookie('sessionId', sessionId, {
  httpOnly: true,
  sameSite: 'strict',  // CSRF protection
  secure: true
});
```

### CORS Configuration
```javascript
const cors = require('cors');

const corsOptions = {
  origin: ['https://example.com', 'https://app.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400  // Preflight cache 24 hours
};

app.use(cors(corsOptions));
```

## Security Headers

```
You:
What security headers should I set?

AI:
## Security Headers

### Express + Helmet
```javascript
const helmet = require('helmet');

app.use(helmet());

// Detailed configuration
app.use(helmet({
  // Prevent clickjacking
  frameguard: { action: 'deny' },
  
  // XSS filter
  xssFilter: true,
  
  // Disable IE XSS filter
  noSniff: true,
  
  // Force HTTPS
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  
  // Content type sniffing
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'"]
    }
  }
}));
```

### Complete Headers List
```yaml
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## Security Scanning

```
You:
How to perform security scanning?

AI:
## Security Scanning Tools

### 1. Dependency Scanning
```bash
# npm audit
npm audit

# Snyk
npm install -g snyk
snyk test

# GitHub dependency check
# Settings → Security → Dependency review
```

### 2. Code Scanning
```bash
# SonarQube
sonar-scanner

# Semgrep
semgrep --config=auto .
```

### 3. Penetration Testing
```bash
# OWASP ZAP (DAST)
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://myapp.com
```

### 4. CI Integration
```yaml
# GitHub Actions
- name: Security scan
  run: |
    npm audit --audit-level=high
    snyk test
    semgrep --config=auto .
```

### Automated Scanning Checklist
```
□ Dependency vulnerability scanning (npm audit, Snyk)
□ Code quality scanning (SonarQube, CodeQL)
□ SAST (Static Application Security Testing)
□ DAST (Dynamic Application Security Testing)
□ Secret scanning (Gitleaks, TruffleHog)
```

## Practice Exercises

```
1. Audit your code security
2. Fix all critical vulnerabilities
3. Configure security headers
4. Set up dependency scanning
5. Configure WAF (if applicable)
6. Establish security checklist
7. Regular security training
```

**Security is not a feature, it's an attitude. Integrate security into every step of the development process.**
