# 18. Code Review Process

## Pull Request Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│                  Pull Request Flow                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Create Branch ──→ Develop ──→ Submit PR ──→ Review ──→ Merge│
│       ↑                                    │            │
│       └────────────────────────────────────┘            │
│                   (May need changes)                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Writing Good PR Descriptions

### PR Description Template

Have AI generate a template for you:

```
You:
Please help me generate a PR description template

AI:
## PR Description Template

```markdown
## Summary
Briefly explain what this PR does.

## Motivation
Why is this change needed?
What problem does it solve?

## Changes
- [ ] Added feature X
- [ ] Modified feature Y
- [ ] Fixed bug Z

## Technical Details
Important implementation details to help reviewers understand.

## Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests

## Screenshots/Recordings
(If UI changes)

## Related Issues
Closes #123
```

### Practical Example

```
## Summary
Implemented user avatar upload with cropping and compression.

## Motivation
Users requested custom avatar functionality.
Issue: #234

## Changes
- Added avatar upload API
- Added image cropping component
- Added image compression utility
- Integrated AWS S3 storage

## Technical Details
- Using Sharp for image processing
- Avatar limited to 200KB, size 200x200
- Using Presigned URL to avoid exposing credentials

## Testing
- [x] Unit tests (upload service)
- [x] Integration tests (complete flow)
- [ ] E2E tests (will add in next PR)
```

## Having AI Help You Write PRs

```
You:
Please help me write a clear PR description in English:

Feature: Implemented "Remember Me" functionality for user login
Implementation:
- Added remember_token field to users table
- Generate 30-day valid token when "Remember Me" is checked
- Auto-extend token on each access

AI:
## PR: Add "Remember Me" functionality

### Summary
Implemented persistent login with "Remember Me" option for enhanced user experience.

### Changes
- Added `remember_token` column to users table
- Generate 30-day token when "Remember Me" is checked
- Auto-extend token on each authenticated request
- Updated login/logout flows

### Technical Details
- Token stored as secure HTTP-only cookie
- Token rotation on each use (security best practice)
- Cleanup expired tokens on login

### Testing
- [x] Unit tests for token generation/validation
- [x] Integration test for login flow
- [x] Manual testing on staging

### Screenshots
[Login form with "Remember Me" checkbox]
```

## PR Review Checklist

### As a Reviewer

```
┌─────────────────────────────────────────────────────────┐
│                  PR Review Checklist                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Functionality                                          │
│  □ Is the code logic correct?                          │
│  □ Are all edge cases handled?                         │
│  □ Are there security risks?                           │
│                                                         │
│  Testing                                                │
│  □ Are there tests?                                     │
│  □ Is test coverage sufficient?                        │
│  □ Do tests pass?                                      │
│                                                         │
│  Code Quality                                          │
│  □ Is the code clear and understandable?              │
│  □ Are variable/function names appropriate?           │
│  □ Is there duplicate code?                            │
│  □ Are there comments? (Where needed, not where not)  │
│                                                         │
│  Integration                                            │
│  □ Is it consistent with existing code style?         │
│  □ Won't it break other features?                      │
│  □ Is documentation updated?                          │
│                                                         │
│  Performance                                            │
│  □ Are there performance issues?                      │
│  □ Are database queries optimized?                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Have AI Do Code Review

```
You:
Please review this PR as a code reviewer:

Changes: Added user avatar upload feature
Code: [code]

Please focus on:
1. Security
2. Performance
3. Error handling

AI:
## PR Review

### Overall Assessment
Feature is complete, implementation is reasonable. Suggested changes before merging.

---

### 🔴 Must Fix (Blocking)

**1. Missing file type validation (Security)**
```javascript
// Current: accepts any file
const upload = await s3.upload(params).promise();

// Suggestion: validate file type
const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
if (!allowedTypes.includes(file.mimetype)) {
  throw new Error('Invalid file type');
}
```

**2. Missing file size limit (DoS risk)**
```javascript
// Suggestion: limit file size
const MAX_SIZE = 5 * 1024 * 1024; // 5MB
if (file.size > MAX_SIZE) {
  throw new Error('File too large');
}
```

---

### 🟡 Suggested Fixes (Non-blocking)

**3. Missing error handling**
```javascript
// Current: direct upload
const upload = await s3.upload(params).promise();

// Suggestion: add error handling
try {
  const upload = await s3.upload(params).promise();
} catch (error) {
  logger.error('S3 upload failed', error);
  throw new Error('Failed to upload image');
}
```

**4. S3 path is predictable**
Current path: `avatars/{userId}.jpg`
Suggestion: add random prefix to prevent path guessing

---

### 🟢 What Was Done Well

- Using async/await ✅
- Clear parameter validation ✅
- Good code structure ✅

---

### Summary
Can merge after fixing security-related issues.
Suggestion: Add unit tests covering edge cases.
```

## Providing Effective Feedback

### The Art of Feedback

```
❌ Poor feedback:
"This code is not good"

✅ Good feedback:
"This implementation may cause N+1 query issues. Suggest using eager loading:
```javascript
const users = await User.findAll({
  include: [{ model: Post }]  // Single query
});
```"

Reason:
1. Point out specific issue
2. Explain why
3. Provide solution
4. Give code example
```

### Feedback Template

```
## Code Review Feedback

### 🔴 Issue: [Title]
**Location:** `src/path/file.ts:45`

**Problem:** [Description]

**Suggestion:** [Solution]

---

### 🟡 Suggestion: [Title]
**Location:** Same as above

**Suggestion:** [Improvement suggestion]
(If time permits)

---

### ✅ What Was Done Well
- [List good practices]
```

### Replying to Feedback

As PR author, how to respond to reviewer feedback:

```
You:
Please help me write a reply to the reviewer:

Reviewer pointed out: Missing file type validation

AI:
## Reply Template

### Reply Example 1 - Accepting Feedback
```
[@reviewer] You're right, this is a security vulnerability.
Added file type validation:
commit abc123

Please re-review.
```

### Reply Example 2 - Explaining Decision
```
[@reviewer] About this suggestion:

My reasoning is: [your reason]

If you still think changes are needed, let me know, we can discuss.
```

### Reply Example 3 - Raising Questions
```
[@reviewer] Great question!

My current understanding is: [your understanding]

But I may not have considered [reviewer's point].

How do you think we should handle this?
```
```

## PR Automation

### CI/CD Configuration

Have AI help you configure PR automation:

```
You:
Please help me configure GitHub Actions with these requirements:
1. Run tests on PR creation
2. Tests must pass before merging
3. Automatically run lint

AI:
## GitHub Actions Configuration

```yaml
# .github/workflows/pr-check.yml
name: PR Check

on:
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run Lint
        run: npm run lint

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run Tests
        run: npm test

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
```

## Practice Exercises

```
1. Create a complete PR with detailed description
2. Use AI to review your own PR
3. Practice writing different types of feedback
4. Configure a PR template
5. Set up CI automated checks
```

**A good PR is not just for passing review, but for knowledge transfer and maintaining code quality.**
