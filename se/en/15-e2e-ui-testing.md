# 15. End-to-End Testing and UI Testing

## What is End-to-End Testing

```
┌─────────────────────────────────────────────────────┐
│              End-to-End Testing                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│   User Action ──→ Frontend ──→ API ──→ Backend ──→ DB│
│                                                     │
│   Verify: Does the entire flow work?                │
│                                                     │
└─────────────────────────────────────────────────────┘

Unit tests: Test individual functions
Integration tests: Test component collaboration
E2E tests: Test entire system (simulating real users)
```

## E2E Testing Tools

| Tool | Use Case | Characteristics |
|------|----------|-----------------|
| Playwright | Web apps | Microsoft, multi-browser support |
| Cypress | Web apps | Great DX, rich ecosystem |
| Selenium | Legacy Web | Multi-language, broad browser support |
| Puppeteer | Node.js | Google, lightweight |
| Detox | Mobile apps | React Native specific |
| Appium | Mobile apps | Universal mobile testing |

## Playwright Quick Start

### Basic Structure

```
You:
Please write an E2E test for a login flow using Playwright.

AI:
## Playwright E2E Test

```javascript
const { test, expect } = require('@playwright/test');

test.describe('Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });
  
  test('Successful login', async ({ page }) => {
    // Fill form
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    
    // Submit
    await page.click('[data-testid="login-button"]');
    
    // Verify redirect
    await expect(page).toHaveURL('/dashboard');
    
    // Verify user info
    await expect(page.locator('[data-testid="user-name"]'))
      .toContainText('Test User');
  });
  
  test('Login failure shows error', async ({ page }) => {
    await page.fill('[data-testid="email-input"]', 'wrong@example.com');
    await page.fill('[data-testid="password-input"]', 'wrongpass');
    
    await page.click('[data-testid="login-button"]');
    
    await expect(page.locator('[data-testid="error-message"]'))
      .toContainText('Invalid credentials');
  });
});
```
```

### Common Selectors

```
┌─────────────────────────────────────────────────────┐
│                  Selector Priority                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. data-testid (recommended)                       │
│     page.locator('[data-testid="submit"]')          │
│                                                     │
│  2. Role selector                                   │
│     page.getByRole('button', { name: 'Submit' })   │
│                                                     │
│  3. Text selector                                   │
│     page.getByText('Hello World')                  │
│                                                     │
│  4. CSS selector                                    │
│     page.locator('.class-name')                    │
│                                                     │
│  5. XPath (last resort)                             │
│     page.locator('//button[@type="submit"]')       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Wait Strategies

```
You:
Please explain Playwright's wait strategies.

AI:
## Playwright Wait Strategies

### 1. Assertion Wait (Recommended)
```javascript
await expect(page.locator('.status')).toHaveText('Ready');
// Playwright automatically waits for condition
```

### 2. Network Wait
```javascript
await page.waitForResponse('**/api/data');
```

### 3. Navigation Wait
```javascript
await page.waitForURL('**/dashboard');
```

### 4. Function Wait
```javascript
await page.waitForFunction(() => {
  return window.someValue === 'ready';
});
```

### Don't Do This ❌
```javascript
// Hard-coded wait - not recommended
await page.waitForTimeout(2000); // Wasteful and flaky
```

### Best Practices ✅
```javascript
// Use assertion waits
await expect(page.locator('.modal')).toBeVisible();

// Wait for specific element
await page.waitForSelector('.loaded', { state: 'visible' });
```
```

## Common E2E Test Scenarios

### 1. Form Fill and Submit

```
test('Complete form submission flow', async ({ page }) => {
  await page.goto('/register');
  
  // Fill form
  await page.fill('#name', 'John Doe');
  await page.fill('#email', 'john@example.com');
  await page.fill('#password', 'SecurePass123');
  await page.fill('#confirmPassword', 'SecurePass123');
  
  // Upload file
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.click('#avatar-upload');
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles('./test-assets/avatar.jpg');
  
  // Check agreement
  await page.check('#terms-agreement');
  
  // Submit
  await page.click('button[type="submit"]');
  
  // Verify result
  await expect(page).toHaveURL('/profile');
  await expect(page.locator('.welcome-message'))
    .toContainText('Welcome, John Doe');
});
```

### 2. Shopping Cart Flow

```
test('Complete shopping flow', async ({ page }) => {
  // 1. Browse products
  await page.goto('/products');
  await page.click('[data-product-id="prod-001"]');
  
  // 2. Add to cart
  await page.click('[data-testid="add-to-cart"]');
  await expect(page.locator('.cart-badge')).toContainText('1');
  
  // 3. View cart
  await page.click('[data-testid="cart-icon"]');
  await expect(page.locator('.cart-item')).toHaveCount(1);
  
  // 4. Modify quantity
  await page.fill('[data-testid="quantity-input"]', '3');
  await page.click('[data-testid="update-quantity"]');
  
  // 5. Checkout
  await page.click('[data-testid="checkout-button"]');
  await expect(page).toHaveURL('/checkout');
  
  // 6. Fill info and place order
  await page.fill('#address', '123 Main St');
  await page.click('[data-testid="place-order"]');
  
  // 7. Verify order confirmation
  await expect(page.locator('.order-success')).toBeVisible();
  await expect(page.locator('.order-number')).toBeVisible();
});
```

### 3. Authentication Flow

```
test('Complete register-login-logout flow', async ({ page }) => {
  const testEmail = `test${Date.now()}@example.com`;
  
  // Register
  await page.goto('/register');
  await page.fill('#email', testEmail);
  await page.fill('#password', 'SecurePass123');
  await page.click('#register-button');
  
  // Verify email (if email verification exists)
  // ...
  
  // Logout
  await page.click('[data-testid="user-menu"]');
  await page.click('text=Logout');
  
  // Try to access page requiring login
  await page.goto('/dashboard');
  await expect(page).toHaveURL('/login');
  
  // Login with new account
  await page.fill('#email', testEmail);
  await page.fill('#password', 'SecurePass123');
  await page.click('#login-button');
  
  // Verify successful login
  await expect(page).toHaveURL('/dashboard');
});
```

## Common UI Testing Issues

### 1. Flaky Tests

```
You:
Tests frequently timeout and fail, but manual testing works fine. How to fix?

AI:
## Solving Flaky Tests

### 1. Add appropriate waits
❌ Wrong:
await page.click('#submit');
await page.fill('#result', 'xxx'); // May not appear yet

✅ Correct:
await page.click('#submit');
await expect(page.locator('#result')).toBeVisible();
await page.fill('#result', 'xxx');

### 2. Use network condition control
```javascript
await page.route('**/api/**', async (route) => {
  // Simulate slow network
  await route.fulfill({
    status: 200,
    body: '...',
    headers: { 'x-delay': '1000' }
  });
});
```

### 3. Ensure test isolation
```javascript
test.beforeEach(async ({ page }) => {
  // Clear state for each test
  await page.evaluate(() => localStorage.clear());
  await page.reload();
});
```
```

### 2. Fragile Selectors

```
You:
Selectors frequently fail due to UI changes. What to do?

AI:
## Stable Test IDs

### 1. Use data-testid
```html
<button data-testid="submit-button">Submit</button>
```

### 2. Use semantic selectors
```javascript
// Avoid
page.locator('.btn.primary.submit.xl');

// Prefer
page.getByRole('button', { name: 'Submit' });
page.getByLabel('Username');
page.getByPlaceholder('Enter email');
```

### 3. Use test component libraries
Most UI libraries support test IDs:
- Material-UI: `data-testid` prop
- Ant Design: `data-testid` or `id`
- React: Native support
```
```

## Testing辅助工具

### Page Object Pattern

```
You:
Please refactor this test using the Page Object pattern:

```javascript
test('Login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'pass');
  await page.click('.login-btn');
  await expect(page).toHaveURL('/dashboard');
});
```

AI:
## Page Object Pattern

### 1. Create Page Object
```javascript
// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
  }
  
  async goto() {
    await this.page.goto('/login');
  }
  
  async login(email, password) {
    await this.page.fill('#email', email);
    await this.page.fill('#password', password);
    await this.page.click('.login-btn');
  }
}

module.exports = LoginPage;
```

### 2. Use Page Object
```javascript
const LoginPage = require('./pages/LoginPage');

test('Login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  
  await loginPage.goto();
  await loginPage.login('test@example.com', 'pass');
  
  await expect(page).toHaveURL('/dashboard');
});
```

### 3. Benefits
- UI changes only require updating Page Object
- Cleaner test code
- Reusable page operations
```

## Practice Exercises

```
1. Install Playwright or Cypress
2. Configure test environment
3. Write E2E tests for a critical user flow
4. Set up CI integration
5. Report and analyze test results
```

## E2E Testing Best Practices

```
□ Each E2E test verifies one critical flow
□ Use data-testid or semantic selectors
□ Avoid hard-coded waits
□ Ensure test environment matches production
□ Provide meaningful error messages on failure
□ Regularly clean up test data
□ Run E2E tests in CI
□ Monitor flaky tests
```

**E2E tests are the most expensive tests, but also the closest to real users. Only E2E test critical paths.**
