# 11. Refactoring and Optimizing Existing Code

## Why Refactor

```
Code without refactoring = Technical debt = Future nightmare
Proper refactoring = Improved maintainability = Future peace of mind
```

AI is an excellent assistant for refactoring, but refactoring requires caution—making the wrong changes can introduce new bugs.

## Basic Principles of Refactoring

### 1. Small Steps

```
❌ Refactoring too much at once
┌─────────────────────────────────┐
│  Before         After           │
│  1000 lines →   1000 lines (new)│
│                                │
│  Risk: bugs hard to locate     │
└─────────────────────────────────┘

✅ Incremental Refactoring
┌─────────────────────────────────┐
│  Step 1: Extract function A     │
│  Step 2: Extract function B     │
│  Step 3: Rename variables       │
│  Step 4: Optimize logic        │
│                                │
│  Test each step,可控 risk      │
└─────────────────────────────────┘
```

### 2. With Test Protection

There must be tests before refactoring, or tests must be added immediately after refactoring.

### 3. Preserve Functionality

Refactoring is about "changing structure, not behavior."

## Common AI-Assisted Refactoring Scenarios

### Scenario 1: Splitting Long Functions

```
You:
This function is 200 lines. Please help me split it into smaller functions:

[code]

AI:
## Recommended Refactoring Plan

### Current Issues
- Function too long (200 lines)
- Multiple responsibilities
- Hard to test

### Splitting Plan

```javascript
// Main function: coordinate logic
async function processOrder(orderId) {
  const order = await fetchOrder(orderId);
  const validation = validateOrder(order);
  if (!validation.success) {
    return handleValidationError(validation.errors);
  }
  
  const pricing = calculatePricing(order);
  const payment = await processPayment(pricing);
  const fulfillment = await fulfillOrder(payment);
  
  return fulfillment;
}

// Sub-function 1: fetch order
async function fetchOrder(orderId) { ... }

// Sub-function 2: validate order
function validateOrder(order) { ... }

// Sub-function 3: calculate pricing
function calculatePricing(order) { ... }

// Sub-function 4: process payment
async function processPayment(pricing) { ... }

// Sub-function 5: fulfill order
async function fulfillOrder(payment) { ... }

// Sub-function 6: handle validation errors
function handleValidationError(errors) { ... }
```

### Scenario 2: Eliminating Duplicate Code

```
You:
This code has repeated logging logic in multiple places. Please help extract the common logic:

[code]

AI:
## Duplicate Code Analysis

Found 3 repeated logging patterns:

```javascript
// Pattern 1: Error log
console.error(`[ERROR] ${new Date().toISOString()} - ${message}`);

// Pattern 2: Log with context
console.log(`[INFO] ${new Date().toISOString()} - ${context}: ${message}`);
```

## Recommended Solution: Logger Class

```javascript
class Logger {
  constructor(context) {
    this.context = context;
  }
  
  error(message, error = null) {
    console.error(`[ERROR] ${new Date().toISOString()} - ${this.context}: ${message}`, error);
  }
  
  info(message) {
    console.log(`[INFO] ${new Date().toISOString()} - ${this.context}: ${message}`);
  }
}

// Usage
const logger = new Logger('OrderService');
logger.info('Order created');
logger.error('Payment failed', error);
```
```

### Scenario 3: Simplifying Complex Conditions

```
You:
Please help me simplify this complex conditional:

[code]

AI:
## Simplification Plan

### Original Code
```javascript
if (user && user.isActive && user.hasPermission && 
    (user.role === 'admin' || user.role === 'editor' || 
     user.permissions.includes('edit'))) {
  // Execute operation
}
```

### After Simplification
```javascript
function canEdit(user) {
  if (!user?.isActive) return false;
  if (user.role === 'admin') return true;
  if (user.role === 'editor') return true;
  return user.permissions.includes('edit');
}

if (canEdit(user)) {
  // Execute operation
}
```

### Or Using Strategy Pattern
```javascript
const permissions = {
  admin: () => true,
  editor: () => true,
  viewer: (user) => user.permissions.includes('edit')
};

const canEdit = (user) => {
  if (!user?.isActive) return false;
  return permissions[user.role]?.(user) ?? false;
};
```

### Scenario 4: Converting Callback Hell to Promise/Async-Await

```
You:
Please convert this callback hell to async/await:

[code]

AI:
## Refactoring Plan

### Original Code (Callback Hell)
```javascript
getData(function(a) {
  getMoreData(a, function(b) {
    getMoreData(b, function(c) {
      getMoreData(c, function(d) {
        console.log(d);
      });
    });
  });
});
```

### After Refactoring (Async/Await)
```javascript
async function fetchAllData() {
  const a = await getData();
  const b = await getMoreData(a);
  const c = await getMoreData(b);
  const d = await getMoreData(c);
  console.log(d);
  return d;
}
```
```

## Refactoring Workflow

```
┌─────────────────────────────────────────────────────┐
│           AI-Assisted Refactoring Workflow          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Understand Current Code                        │
│     You: "What does this code do?"                  │
│     AI → You: Code purpose and structure           │
│                                                     │
│  2. Identify Problems                               │
│     You: "Please list issues in this code"         │
│     AI → You: Specific issues and improvements     │
│                                                     │
│  3. Create Refactoring Plan                       │
│     You: "Please create a step-by-step plan"       │
│     AI → You: Steps and priorities                 │
│                                                     │
│  4. Refactor Incrementally                         │
│     You: "Please refactor step 1"                  │
│     AI → You: Refactored code                      │
│                                                     │
│  5. Verify and Test                                │
│     You/You run test suite                        │
│                                                     │
│  6. Repeat steps 4-5 until complete                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Boundaries of Refactoring

### Should Refactor

- [ ] Code is hard to understand
- [ ] Obvious duplicate code exists
- [ ] Functions/classes are too long
- [ ] Changing one feature requires modifying multiple places
- [ ] Difficult to add new features
- [ ] Tests are hard to write

### Should NOT Refactor

- [ ] Code is stable, rarely needs changes
- [ ] Rewriting is more cost-effective (ROI issue)
- [ ] No test protection
- [ ] Temporary/deprecated code
- [ ] When rushing to meet deadlines

## AI Refactoring Safety Check

Have AI do a safety check after refactoring:

```
You:
Please check this refactored code:

Before:
[original code]

After:
[new code]

Please confirm:
1. Is functionality equivalent?
2. Are there any new issues introduced?
3. Are edge cases handled consistently?
```

## Practice Exercises

Pick a piece of "smelly" code (yours or someone else's) and refactor it using this workflow:

```
1. Use AI to analyze code issues
2. Create a refactoring plan
3. Have AI refactor incrementally
4. Verify functionality is preserved at each step
5. Document differences before and after
```

**Refactoring is an ongoing process, not a one-time event. Build refactoring habits to keep your codebase healthy.**
