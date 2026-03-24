# 7. Task Breakdown and Estimation

## Big Task = Small Steps

"How long will this feature take?" — This is one of the hardest questions in software development. AI can help you decompose tasks and identify dependencies, but final estimation is your responsibility.

## Why Decompose Tasks

```
Wrong approach:
"User login feature"
↓
Estimate: 2 days
↓
Actual: 2 weeks (because forgot to consider verification code, third-party login, password recovery...)

Correct approach:
"User login feature" decomposed into:
├── Frontend form
├── Backend API
├── Password verification
├── Session management
├── Remember me
├── Third-party login (optional)
└── Testing
↓
Estimate: 4 days (0.5-1 day per small task)
Actual: 4 days (all dependencies considered)
```

## AI-Assisted Task Decomposition

### Basic Decomposition Pattern

```
You:
Please decompose "e-commerce promotion system" into specific development tasks.

AI:
## E-commerce Promotion System - Task Breakdown

### Phase 1: Infrastructure
- [ ] Promotion data model design
- [ ] Promotion API foundation
- [ ] Coupon code generation service

### Phase 2: Core Features
- [ ] Discount calculation logic
- [ ] Apply discount to orders
- [ ] Inventory reservation/release
- [ ] Coupon claim feature

### Phase 3: Rules Engine
- [ ] Promotion rules DSL design
- [ ] Rules engine implementation
- [ ] Rules conflict handling

### Phase 4: Display and Client
- [ ] Promotion page design
- [ ] Countdown display
- [ ] Discount hint component
- [ ] User coupon list

### Phase 5: Operations Features
- [ ] Promotion management backend
- [ ] Campaign effect reports
- [ ] Inventory alerts

### Phase 6: Testing and Launch
- [ ] Unit tests
- [ ] Integration tests
- [ ] Stress tests
- [ ] Launch deployment
```

### Granularity Principles

```
Too coarse (bad):
[ ] Implement shopping cart feature

Too fine (also bad):
[ ] Implement shopping cart add button CSS style
[ ] Implement shopping cart add button hover effect
[ ] Implement shopping cart add button click event

Just right:
[ ] Shopping cart add item API
[ ] Shopping cart page component
[ ] Shopping cart quantity update logic
[ ] Shopping cart delete item feature
[ ] Shopping cart data persistence
```

AI can help you find this balance.

## Estimation Techniques

### Optimistic/Pessimistic/Most Likely

Give three estimates for each task:

```
Task: User authentication API

Optimistic: 1 day (everything goes smoothly)
Most likely: 2 days (normal development)
Pessimistic: 4 days (encountering problems)

Final estimate = (Optimistic + 4×Most Likely + Pessimistic) / 6
              = (1 + 4×2 + 4) / 6
              = 13 / 6
              ≈ 2.2 days
```

Have AI help you calculate:

```
You:
Help me estimate total workload for this Sprint:
- User authentication API: Most likely 2 days, optimistic 1 day, pessimistic 4 days
- Product list API: Most likely 3 days, optimistic 2 days, pessimistic 5 days
- Order creation API: Most likely 4 days, optimistic 3 days, pessimistic 7 days
- Payment integration: Most likely 5 days, optimistic 4 days, pessimistic 10 days

AI:
## Estimation Summary

| Task | Optimistic | Most Likely | Pessimistic | Expected |
|------|------------|-------------|-------------|----------|
| User auth API | 1 | 2 | 4 | 2.2 |
| Product list API | 2 | 3 | 5 | 3.2 |
| Order creation API | 3 | 4 | 7 | 4.3 |
| Payment integration | 4 | 5 | 10 | 5.7 |

Total expected: 15.4 days
Buffer (20%): 3.1 days
Total estimate: 18.5 days ≈ 3 weeks (5 person-days/week)
```

### Identifying Dependencies

```
You:
Analyze dependencies between these tasks:
A. Database design
B. User authentication API
C. Product management API
D. Order API
E. Payment API
F. Frontend login page

AI:
## Dependency Graph

A(Database) ──┬──→ B(User auth)
           ├──→ C(Product management)
           ├──→ D(Order)
           └──→ E(Payment)

B(User auth) ──→ F(Frontend login page)

D(Order) ──────→ E(Payment)
C(Product management) ──→ D(Order)

## Critical Path
A → B → F (Login page critical path)

## Parallelizable Tasks
- A (Database) can start first
- B, C, D, E can be developed in parallel after A completes
- F starts after B completes
```

## Dealing with Uncertainty

### Technology Uncertainty Matrix

```
                  Familiarity
            Low         High
       ┌──────────┬──────────┐
   High │ Explore  │  Standard │
       │ Research  │  Dev ×1  │
       │   × 2-3   │          │
       ├──────────┼──────────┤
   Diff│          │          │
 iculty│ Split &  │  Cautious│
       │ Research  │   Dev    │
       │   × 3-5   │   × 1.5 │
       └──────────┴──────────┘

× represents estimation multiplier
```

### Have AI Identify Uncertainty

```
You:
For the "integrating AI image recognition for auto-tagging products" feature,
please identify technical uncertainty and give estimation suggestions.

AI:
## Technical Uncertainty Analysis

### High Uncertainty Points
1. AI model selection
   - Uncertain: Which model best suits your scenario
   - Suggestion: First spend 1 week on PoC

2. Model deployment cost
   - Uncertain: Relationship between QPS and cost
   - Suggestion: Evaluate backend cost first

3. Recognition accuracy
   - Uncertain: Can it meet business requirements
   - Suggestion: User acceptance testing

### Adjusted Estimation
Original estimate: 2 weeks
PoC phase: + 1 week
Buffer (30% uncertainty): + 0.9 weeks
Adjusted estimate: 3.9 weeks ≈ 4 weeks

### Recommended Approach
1. Week 1: PoC, verify technical feasibility
2. Week 2+: Re-evaluate based on PoC results
```

## Practical Workflow

```
┌─────────────────────────────────────────────────────┐
│              AI-Assisted Task Breakdown Workflow       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  1. Requirements input                               │
│     You: "Feature: users can share products to social media"│
│                                                      │
│  2. AI initial breakdown                             │
│     AI → List all sub-tasks                         │
│                                                      │
│  3. You add missing items                           │
│     You: Add "error handling", "testing", etc.       │
│                                                      │
│  4. AI identifies dependencies                      │
│     AI → Generate task graph                         │
│                                                      │
│  5. Joint estimation                                │
│     You/AI → Give three estimates for each task     │
│                                                      │
│  6. Identify risks                                 │
│     AI → Identify uncertainties and risk points    │
│                                                      │
│  7. Final decision                                  │
│     You → Decide final scope and deadline           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Practice Exercise

Choose a feature you're working on and have AI help you break it down:

```
You:
Please decompose [feature name] into development tasks,
including most likely estimation for each task,
and identify dependencies between tasks.
```
