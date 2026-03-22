# 9. How to Ask AI Questions Effectively

## Questioning Is a Core Skill

"Ask well, get good answers." This is more important in the AI era than ever before.

## Why Same AI, Different Results

```
Two engineers using the same AI:

Engineer A:
"My code has an error"
AI: "Cannot locate the problem, need more information"

Engineer B:
"My code has an error, error message is 'TypeError: Cannot read property
of undefined at line 23', here is the related code:
[code snippet]'"
AI: "The problem is the object returned at line 18 doesn't have 'user' property..."
```

**Engineer B got a useful answer because their question contained more information.**

## Levels of Questioning

### Level 1: Vague Questions

```
❌ Bad:
"How to make a website?"
"What to do about code error?"
"How to learn Python?"
```

AI can only give general answers, usually generic advice or official documentation summaries.

### Level 2: Specific Questions

```
✅ OK:
"How to implement user login with React?"
"What's the difference between list and tuple in Python?"
```

AI can give practical answers but may not be optimal.

### Level 3: Context-Rich Questions

```
✅✅ Best:
"I'm developing a blog system with React + TypeScript,
need to implement third-party login (Google).
Currently using Firebase Auth but encountering CORS errors.
Already tried: [specific methods]
Error screenshot: [description]
How to solve this?"
```

AI can give targeted solutions.

## Elements of Effective Questions

### Element 1: Context

```
❌ Bad:
"Redis connection error"

✅ Good:
"My Node.js app using Redis in Kubernetes environment,
works fine locally, but gets 'ECONNREFUSED' error when requests exceed 100/sec in production"
```

### Element 2: Goal

```
❌ Bad:
"How to optimize this code?"

✅ Good:
"This code takes 30 seconds to process 1 million records,
needs to be optimized to under 5 seconds"
```

### Element 3: Constraints

```
❌ Bad:
"Write a sorting algorithm for me"

✅ Good:
"Write a sorting algorithm with these requirements:
1. Performs well on mostly sorted data
2. Space complexity O(1)
3. Implement in JavaScript"
```

### Element 4: Attempts

```
❌ Bad:
"How to resolve Git merge conflicts?"

✅ Good:
"When resolving Git merge conflicts, I used 'git merge --abort'
to cancel merge, but getting 'refusing to merge unrelated histories' error
when merging again. How should I handle this?"
```

## Question Templates

### Template 1: Code Debugging

```
## Problem Description
[Brief description of the problem]

## Environment Info
- Operating system:
- Programming language and version:
- Related framework/library version:
- Runtime environment (local/server/container):

## Error Message
```
[Complete error message]
```

## Related Code
```[language]
[code snippet]
```

## Attempted Solutions
1. ...
2. ...

## Expected Behavior
[Describe what you expect to happen]
```

### Template 2: Feature Implementation

```
## Requirements Description
[Brief description of the feature you want to implement]

## Background
[Why you need this feature]

## Technical Constraints
- Programming language:
- Framework version:
- Database (if applicable):
- Other constraints:

## References
[Related documentation, tutorials, code snippets]

## Specific Questions
[What you particularly want to know]
```

### Template 3: Code Review

```
## Review Target
[Describe the purpose of this code]

## Code
```[language]
[code]
```

## My Concerns
[What you particularly want to know]
1. ...
2. ...

## Code Style Requirements
[If specific code style requirements exist]
```

## Common Questioning Mistakes

### Mistake 1: Asking for Too Much

```
❌ Bad:
"Help me make a TikTok-like APP"

✅ Good (step-by-step):
1. "Help me design tech architecture for a short video APP"
2. "What are the technical solutions for mobile video upload?"
3. "Help me design the database model for video recommendation system"
```

### Mistake 2: Hiding Key Information

```
❌ Bad:
"This Python code throws an error"

✅ Good:
"This Python 3.9 code runs normally on Windows,
but throws 'ModuleNotFoundError' on macOS"
(revealed OS difference as key information)
```

### Mistake 3: Assuming the Answer

```
❌ Bad:
"Is this performance issue because the database doesn't have an index?"

✅ Good:
"This query is slow, what might be the possible causes?"
(Let AI analyze comprehensively, avoid being biased)
```

### Mistake 4: Asking Too Many Questions at Once

```
❌ Bad:
"What are microservices? How to use Docker? How to deploy K8s?
How to implement CI/CD?"

✅ Good:
"Please explain core concepts of microservices architecture"
(one question at a time)
```

## Iterative Questioning

Sometimes one question can't get a complete answer—this is normal:

```
First round:
You: "Help me implement user login"
AI: [Gives basic implementation]

Second round:
You: "Now need to support Remember Me, keep logged in for 30 days"

Third round:
You: "Also need to view and manage logged-in devices when logging in on multiple devices"

Fourth round:
You: "Finally add security alerts for logins from different locations"
```

Each iteration is more refined than the last.

## Question Checklist

Before sending a question, ask yourself:

```
□ Did I provide enough context?
□ Is my question specific and clear?
□ Did I state constraints?
□ Did I state what I've tried?
□ Is this question too complex, needing breakdown?
□ Did I assume the direction of the answer?
□ Am I asking too many questions at once?
```

## Practice Exercise

Practice questioning with these steps:

1. Choose a technical problem you recently encountered
2. Write the question using "Template 1"
3. Ask AI this question
4. Evaluate the answer quality
5. Adjust the question, ask again
6. Summarize this experience

**A good question is half the battle. Investing in questioning pays back with better answers and higher efficiency.**
