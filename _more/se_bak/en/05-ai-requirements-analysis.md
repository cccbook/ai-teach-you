# 5. Using AI to Clarify Requirements

## Requirements Are the Foundation of Software Development

"Unclear requirements bring endless troubles." Even if AI can generate code, vague requirements may result in something completely different from what you want.

## Why AI Can Help with Requirements Analysis

AI excels at:
- Identifying ambiguities in descriptions
- Listing scenarios that might be missed
- Structuring vague ideas
- Providing different perspectives

## Requirements Analysis Dialogue Patterns

### Pattern 1: Idea Clarification

```
You:
I want to make a note-taking app where users can write notes, categorize notes, and search notes.

AI:
Great! Before you start, let me help you confirm a few questions:

Feature scope:
1. User system - Login required? Or local use?
2. Note format - Plain text? Markdown support? Images?
3. Categorization - Folders? Tags? Both?
4. Search - Keyword search? Full-text search? Both?
5. Sync - Single device? Multi-device sync?

Non-functional requirements:
6. Offline support - Need offline use?
7. Data security - Need encryption?
8. Scalability - Might add collaboration features later?

The answers to these questions will affect architecture design and technology selection.
```

### Pattern 2: Scenario Listing

```
You:
Help me think about what scenarios need to be considered for a user login system.

AI:
Basic scenarios:
✓ Successful login with correct username/password
✓ Failed login with wrong password
✓ Non-existent account

Advanced scenarios:
○ Account lockout after multiple wrong passwords
○ Remember Me functionality
○ Third-party login (Google, GitHub)
○ Social account binding

Security scenarios:
○ Brute force protection
○ Session expiration handling
○ Login from different location notification
○ Device management

Edge cases:
○ Password case sensitivity
○ Special character handling
○ Empty password handling
○ Overly long password handling
```

### Pattern 3: Requirements Conversion

```
You:
Convert the following requirements into technical specifications:
"Users can upload photos, add tags to photos, and others can search photos through tags"

AI:
## Technical Specifications

### Core Features
| Feature | Description | Priority |
|---------|-------------|----------|
| Photo upload | Supported formats, size limits, compression | P0 |
| Tagging system | Multi-tag support, auto tag suggestions | P0 |
| Search | Tag search, combined search | P0 |

### API Design
```
POST /api/photos          - Upload photo
GET  /api/photos?tags=xx  - Search by tags
PUT  /api/photos/:id/tags - Update tags
```

### Data Model
```
Photo {
  id: UUID
  url: string
  user_id: UUID
  created_at: timestamp
}

Tag {
  id: UUID
  name: string
}

PhotoTag {
  photo_id: UUID
  tag_id: UUID
}
```

### Non-functional Requirements
- Photo size limit: 10MB
- Supported formats: JPEG, PNG, WebP
- Thumbnail generation: Yes
- CDN acceleration: Yes
```

## Effective Questioning Techniques

### Technique 1: Provide Context

```
❌ Bad: "Help me design a database"

✅ Good: "I'm developing a blog system using PostgreSQL,
with an estimated 1000 authors, averaging 50 articles per author,
please help me design the database schema"
```

### Technique 2: Explain Constraints

```
❌ Bad: "How to implement this feature?"

✅ Good: "On a server with 512MB memory, how to efficiently process
10GB log files? Please consider memory limits"
```

### Technique 3: Specify Output Format

```
❌ Bad: "Tell me what needs to be considered"

✅ Good: "Please list all features of an e-commerce shopping cart in a Markdown table,
including: feature name, description, acceptance criteria"
```

### Technique 4: Give Framework First, Then Supplement

```
You: Help me list functional modules for user management system
AI: [List modules]

You: For the "permission management" module, explain each permission level definition in detail
AI: [Detailed explanation]
```

## Requirements Document Template

Have AI help you generate requirements documents:

```
Please help me generate a functional requirements document template, including:
1. Feature overview
2. User stories
3. Feature details
4. Acceptance criteria
5. Non-functional requirements
6. Dependencies
7. Risk assessment
```

## Pitfalls to Avoid

### Pitfall 1: Scope Creep

```
You: Add a simple feature
AI: OK [Generate code]
You: Since we're at it, might as well add XX feature...
AI: OK [Modify code]
You: Optimize YY a bit more...

Problem: No clear scope boundary
Solution: Before each confirmation, ask "Is this inside or outside scope?"
```

### Pitfall 2: Assuming AI Knows Your Thoughts

```
What you think: "This should obviously be included"
What AI understands: "You said exactly what you mean"

Solution: Explicitly state your assumptions, have AI verify them
```

## Practice Exercise

Design an AI-assisted requirements analysis dialogue:

```
Topic: Online hairdresser appointment system

Goals:
1. Use AI to help list scenarios to consider
2. Generate a complete feature list
3. Convert to technical specifications
```

Before starting the next chapter, try analyzing requirements for one of your current projects using this workflow.
