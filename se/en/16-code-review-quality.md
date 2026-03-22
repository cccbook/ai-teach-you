# 16. Code Review and Quality Control

## Value of Code Review

```
┌─────────────────────────────────────────────────────┐
│               Code Review                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│   Catch Bugs    Share Knowledge  Code Quality  Consistency│
│      ↓              ↓             ↓            ↓    │
│   ────────────────────────────────────────────────  │
│                                                     │
│   Code review is not just about finding bugs:       │
│   • Logic correctness                               │
│   • Security                                        │
│   • Performance                                     │
│   • Maintainability                                 │
│   • Code style consistency                         │
│   • Test coverage                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## AI-Assisted Code Review

### Standard Review Checklist

Have AI create a review checklist for you:

```
You:
Please create a code review checklist for [your tech stack] projects

AI:
## Code Review Checklist

### General Checks
□ Is the code logic correct?
□ Are edge cases handled?
□ Are there obvious errors?
□ Is the code clear and understandable?

### Functionality Checks
□ Does functionality match requirements?
□ Is test coverage sufficient?
□ Is error handling complete?

### Performance Checks
□ Are there performance issues?
□ Are database queries optimized?
□ Are there N+1 query problems?

### Security Checks
□ Are there injection risks?
□ Is sensitive data encrypted?
□ Is permission control correct?
□ Are dependencies secure?

### Code Style
□ Does it follow project standards?
□ Are names clear?
□ Are comments necessary?
□ Is there wheel reinventing?
```

### AI Review Example

```
You:
Please review this code:

```javascript
async function createUser(req, res) {
  const { name, email, password } = req.body;
  
  // Simple validation
  if (!name || !email || !password) {
    return res.status(400).send('Missing fields');
  }
  
  // Create user
  const user = await User.create({ name, email, password });
  
  res.json(user);
}
```

AI:
## Code Review

### 🔴 Issues

**1. Password stored in plain text (Serious security vulnerability)**
Password stored directly in database without hashing.
```javascript
// Should be
const hashedPassword = await bcrypt.hash(password, 10);
const user = await User.create({ name, email, password: hashedPassword });
```

**2. Email format not validated**
```javascript
// Suggestion
if (!isValidEmail(email)) {
  return res.status(400).json({ error: 'Invalid email format' });
}
```

**3. Duplicate email not checked**
Email should be unique in user table.

### 🟡 Improvement Suggestions

**4. Password strength check**
```javascript
if (password.length < 8) {
  return res.status(400).json({ error: 'Password too weak' });
}
```

**5. Improved error handling**
```javascript
// Current: all errors return 500
// Suggestion: differentiate error types
try {
  const existingUser = await User.findOne({ email });
  if (existingUser) {
    return res.status(409).json({ error: 'Email already exists' });
  }
} catch (dbError) {
  // Log database error
  logger.error(dbError);
  return res.status(500).json({ error: 'Database error' });
}
```

### 🟢 Good Practices

- Using async/await ✅
- Parameter destructuring ✅
- Returning appropriate HTTP status codes ✅
```

## Reviewing Different Types of Code

### 1. API Code Review

```
You:
Please review this Express API:

```javascript
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);
});
```

AI:
## API Code Review

### 🔴 Critical Issues

**1. Missing permission check**
Anyone can view any user's information.
```javascript
// Should verify current user's permissions
async function getUser(req, res) {
  const currentUser = await authMiddleware(req);
  const requestedId = req.params.id;
  
  if (currentUser.id !== requestedId && !currentUser.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  const user = await User.findById(requestedId);
  res.json(user);
}
```

**2. Not checking if user exists**
When user doesn't exist, `findById` returns `null`, and `res.json(null)` is not good handling.

**3. Missing error handling**
Database errors cause uncaught Promise rejections.

### 🟡 Suggestions

**4. Field selection**
```javascript
// Don't return sensitive fields
const user = await User.findById(id).select('-password -token');
```

**5. Response caching**
Consider adding caching for public data.

### ✅ Correct Approach
```javascript
app.get('/api/users/:id', 
  authenticate,
  checkPermission,
  async (req, res) => {
    try {
      const user = await User.findById(req.params.id)
        .select('-password -token');
      
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      
      res.json(user);
    } catch (error) {
      logger.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
);
```

### 2. Frontend Code Review

```
You:
Please review this React component:

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => setUser(data));
  }, []);
  
  return <div>{user.name}</div>;
}
```

AI:
## React Code Review

### 🔴 Critical Issues

**1. Empty dependency array**
Data won't be refetched when `userId` changes.
```javascript
useEffect(() => {
  fetch(`/api/users/${userId}`)
    .then(res => res.json())
    .then(data => setUser(data));
}, [userId]); // Add userId
```

**2. Missing loading state**
Accessing `.name` when user is null will throw error.
```jsx
if (!user) return <Loading />;
```

**3. Missing error handling**
No handling for network errors.

**4. Missing Key (in parent component)**
If this is a list item, need to provide key.

### 🟡 Suggestions

**5. Use useCallback/useMemo for optimization**

**6. Consider data fetching library**
```jsx
function UserProfile({ userId }) {
  const { data: user, loading, error } = useSWR(
    `/api/users/${userId}`,
    fetcher
  );
  
  if (loading) return <Loading />;
  if (error) return <Error error={error} />;
  if (!user) return null;
  
  return <div>{user.name}</div>;
}
```

### ✅ Improved Code
```jsx
function UserProfile({ userId }) {
  const { data: user, loading, error } = useSWR(
    userId ? `/api/users/${userId}` : null,
    fetcher
  );
  
  if (loading) return <LoadingSkeleton />;
  if (error) return <ErrorPage message={error.message} />;
  
  return <div>{user.name}</div>;
}
```

## Best Practices for AI Review

### 1. Split Reviews

```
❌ Review too much code at once
✅ Review in batches, focus on one aspect at a time
```

### 2. Define Review Goals

```
You:
Please review this code's security only, don't focus on other aspects.

You:
Please review this code for performance issues.
```

### 3. Iterative Review

```
Round 1: Overall logic
Round 2: Security check
Round 3: Performance optimization
Round 4: Code style
```

## Establishing Team Review Standards

### Review Priority Levels

```
P0 - Must fix (Blocking)
├─ Security vulnerability
├─ Data loss risk
└─ Obvious bugs

P1 - Strongly recommended to fix
├─ Performance issues
├─ Missing edge cases
└─ Insufficient tests

P2 - Suggested improvement (Optional)
├─ Code style
├─ Comment improvements
└─ Minor optimizations
```

### Have AI Generate Team Review Guidelines

```
You:
Please help me generate a code review guide template,
including: review standards, review process, feedback template

AI:
## Code Review Guide

### Review Standards

**Must Pass**
- [ ] Functionality is correct
- [ ] All tests pass
- [ ] No security vulnerabilities
- [ ] Error handling is complete

**Strongly Recommended**
- [ ] Test coverage
- [ ] Performance meets requirements
- [ ] Documentation complete

**Suggested Improvements**
- [ ] Code style
- [ ] Clear comments

### Review Process

1. Author submits PR
2. Automated checks (CI) pass
3. At least 1 reviewer
4. All P0 issues resolved
5. Merge

### Feedback Template

```
## Code Review Feedback

### 🔴 P0 - Must Fix
[Specific issue and suggested fix]

### 🟡 P1 - Suggested Fix
[Suggestions]

### 🟢 P2 - Optional Improvements
[Optional suggestions]

### ✅ What Was Done Well
[Praise points]
```
```

## Practice Exercises

```
1. Find a recent code change
2. Use AI to review (in multiple rounds)
3. Organize discovered issues
4. Assess severity of issues
5. Fix issues
6. Compare before and after differences
```

**Good code review is not about finding the most issues, but finding the important ones and driving improvement.**
