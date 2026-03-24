# 2. What AI Can and Cannot Do

## Understanding AI's Boundaries

Blindly trusting AI or completely dismissing AI are both mistakes made by beginners. To become an effective human-AI collaborator, you must clearly understand AI's capability boundaries.

## What AI Excels At

### 1. Code Generation
AI can quickly generate syntax-correct code based on descriptions. This covers:
- Implementing standard algorithms
- Applying common design patterns
- CRUD operations
- API client code
- Test cases

### 2. Syntax and Documentation Queries
Forgot the parameter order of a function? Want to know the exact usage of some syntax? AI is the best on-demand documentation.

### 3. Code Explanation
Give AI some unfamiliar code, and it can explain:
- What the code is doing
- Why it was designed this way
- Possible execution results

### 4. Refactoring Suggestions
AI can identify code smells and provide refactoring suggestions.

### 5. Multi-language Translation
Translating code from one language to another, AI usually does well.

## What AI Does Not Excel At

### 1. Perfect Business Logic
AI doesn't understand your company's business, industry rules, or special requirements. It may generate code that looks reasonable but has logical errors.

```
Problem example:
You: "Create an order for the user"
AI might: "Just create the order"
What you need: "Check inventory, calculate discounts, validate coupons, send notifications, update membership points..."
```

### 2. Complete System Design
AI is suitable for helping design individual components, but struggles to grasp the complexity of entire systems. A system involving 10 microservices and 5 databases requires humans to ensure architectural consistency and feasibility.

### 3. Latest Technologies and Tools
AI's knowledge has a cutoff date. It may not know:
- New frameworks released last week
- Security vulnerabilities fixed yesterday
- APIs being deprecated tomorrow

### 4. Questions Without Standard Answers
"Is this architecture good?" "Is this design reasonable?" These questions require business context and human judgment.

### 5. Handling Unexpected Edge Cases
Production problems are often unexpected. AI excels at common problems but has limited capability when facing errors it has never seen before.

## Practical Principle: Red Flag List

In these situations, **do not rely on AI's direct answers**:

| Situation | Reason | Correct Approach |
|-----------|--------|------------------|
| Security-related code | AI may produce vulnerabilities | Manual review + security tool scanning |
| APIs requiring authentication | AI doesn't have your credentials | Check official documentation |
| Newly released frameworks | Knowledge may be outdated | Check official tutorials |
| Involving sensitive data | Information security risk | Handle locally |
| Legal/compliance issues | Requires professional judgment | Consult professionals |

## Red Flag Thinking

Cultivate this habit: Every time you see AI's response, ask yourself:

```
1. Is this answer reasonable?
2. Are there any situations I haven't considered?
3. What will happen if this code executes?
4. What tests do I need to verify?
```

## Best Practice: Pair Programming Model

Treat AI as your "junior engineer":

```
┌─────────────┐         ┌─────────────┐
│   Human     │  ←────→  │     AI      │
│ (Senior Eng)│  Collab  │ (Junior Eng)│
└─────────────┘         └─────────────┘

Human responsibilities: Review, decisions, quality control
AI responsibilities: Generate, query, try
```

You are still the person ultimately responsible; AI is just your tool.
