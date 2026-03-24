# 31. API Design and RESTful Principles

## RESTful Basics

```
┌─────────────────────────────────────────────────────────┐
│                    REST Principles                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Resource-based                                        │
│   └─ Use nouns for resources: /users, /orders, /products│
│                                                         │
│   Stateless                                             │
│   └─ Each request contains all necessary information    │
│                                                         │
│   Cacheable                                             │
│   └─ Use caching appropriately to improve performance   │
│                                                         │
│   Client-Server                                         │
│   └─ Client doesn't care about server implementation    │
│                                                         │
│   Uniform Interface                                      │
│   └─ Standard HTTP methods and status codes            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## HTTP Methods

```
┌─────────────────────────────────────────────────────────┐
│                   HTTP Methods                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   GET    /users        Get user list                    │
│   GET    /users/:id    Get single user                 │
│   POST   /users        Create user                      │
│   PUT    /users/:id    Full user update                │
│   PATCH  /users/:id    Partial user update             │
│   DELETE /users/:id    Delete user                      │
│                                                         │
│   GET    /users/:id/orders    Get user's orders        │
│   POST   /users/:id/orders    Create order for user    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted API Design

### API Design Example

```
You:
Please help me design RESTful API for a task management system.

AI:
## Task Management API

### Resource Design

```
Users
├─ POST /users          Register
├─ GET /users/:id       Get user info
└─ PUT /users/:id       Update user

Projects
├─ GET /projects        List
├─ POST /projects        Create
├─ GET /projects/:id    Detail
├─ PUT /projects/:id    Update
└─ DELETE /projects/:id Delete

Tasks
├─ GET /projects/:projectId/tasks    List
├─ POST /projects/:projectId/tasks     Create
├─ GET /tasks/:id                     Detail
├─ PUT /tasks/:id                     Update
└─ DELETE /tasks/:id                  Delete
```

### Detailed API Design

#### User Endpoints
```yaml
# POST /users - Register
Request:
  body:
    email: "user@example.com"
    password: "SecurePass123"
    name: "John"

Response 201:
  body:
    id: "uuid"
    email: "user@example.com"
    name: "John"
    createdAt: "2024-01-15T10:00:00Z"

# GET /users/:id
Response 200:
  body:
    id: "uuid"
    email: "user@example.com"
    name: "John"
    avatar: "https://..."
    createdAt: "2024-01-15T10:00:00Z"
```

#### Project Endpoints
```yaml
# GET /projects
Query:
  page: 1
  limit: 20
  status: active
  sort: createdAt

Response 200:
  body:
    data:
      - id: "uuid"
        name: "Project A"
        description: "..."
        status: "active"
        memberCount: 5
    meta:
      total: 100
      page: 1
      limit: 20

# POST /projects
Request:
  body:
    name: "New Project"
    description: "Project description"
    memberIds: ["uuid1", "uuid2"]

Response 201:
  body:
    id: "uuid"
    name: "New Project"
    ...
```

#### Task Endpoints
```yaml
# GET /projects/:projectId/tasks
Query:
  status: pending,in_progress
  assignee: userId
  priority: high
  dueDate: from:2024-01-01,to:2024-12-31

Response 200:
  body:
    data:
      - id: "uuid"
        title: "Complete task"
        status: "pending"
        priority: "high"
        dueDate: "2024-02-01"
        assignee:
          id: "uuid"
          name: "John"
    meta:
      total: 50

# PATCH /tasks/:id - Update task
Request:
  body:
    status: "completed"
    completedAt: "2024-01-20T15:30:00Z"

Response 200:
  body:
    id: "uuid"
    title: "Complete task"
    status: "completed"
    completedAt: "2024-01-20T15:30:00Z"
    updatedAt: "2024-01-20T15:30:00Z"
```

### Error Responses
```yaml
Error 400:
  body:
    error:
      code: "VALIDATION_ERROR"
      message: "Request validation failed"
      details:
        - field: "email"
          message: "Invalid email format"

Error 401:
  body:
    error:
      code: "UNAUTHORIZED"
      message: "Please login first"

Error 404:
  body:
    error:
      code: "NOT_FOUND"
      message: "Task not found"

Error 500:
  body:
    error:
      code: "INTERNAL_ERROR"
      message: "Internal server error"
```

### Implementation

```javascript
// Express implementation example
const express = require('express');
const app = express();

// List projects
app.get('/projects', async (req, res) => {
  const { page = 1, limit = 20, status, sort = 'createdAt' } = req.query;
  
  const projects = await projectService.list({
    page: parseInt(page),
    limit: parseInt(limit),
    status,
    sort
  });
  
  res.json({
    data: projects.data,
    meta: {
      total: projects.total,
      page: parseInt(page),
      limit: parseInt(limit)
    }
  });
});

// Create project
app.post('/projects', async (req, res, next) => {
  try {
    const { name, description, memberIds } = req.body;
    
    // Validation
    if (!name || name.length < 2) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Project name must be at least 2 characters',
          details: [{ field: 'name' }]
        }
      });
    }
    
    const project = await projectService.create({
      name,
      description,
      memberIds
    });
    
    res.status(201).json(project);
  } catch (error) {
    next(error);
  }
});
```

## Versioning

```
You:
How to do API versioning?

AI:
## API Versioning

### Method 1: URL Path (Recommended)
```
GET /api/v1/users
GET /api/v2/users
```
Simple and intuitive, but breaks cache

### Method 2: Header
```
GET /api/users
API-Version: 2024-01-01
```
Doesn't break URL, but less convenient to use

### Method 3: Query Parameter
```
GET /api/users?version=2
```
Not recommended, pollutes URL

### Implementation Tips
```javascript
// Use path versioning
app.use('/api/v1', require('./routes/v1'));
app.use('/api/v2', require('./routes/v2'));

// Migration strategy
// v1 marked as deprecated
app.get('/api/v1/users', (req, res) => {
  res.set('Deprecation', 'true');
  res.set('Sunset', 'Sat, 31 Dec 2024 23:59:59 GMT');
  // Actual handling
});

// Keep both old and new versions
app.get('/api/v2/users', async (req, res) => {
  const users = await getUsers();
  // New response format
  res.json({ data: users });
});
```

## Pagination

```
You:
How to design API pagination?

AI:
## API Pagination Design

### Offset Pagination
```yaml
GET /users?page=2&limit=20

Response:
  data: [...]
  meta:
    page: 2
    limit: 20
    total: 1000
    totalPages: 50
```
Simple but inefficient for deep pagination

### Cursor Pagination
```yaml
GET /users?cursor=abc123&limit=20

Response:
  data: [...]
  meta:
    nextCursor: "def456"
    hasMore: true
```
Suitable for large data, stable performance

### Keyset Pagination
```yaml
GET /users?since=2024-01-01&limit=20

Response:
  data: [...]
  pagination:
    nextSince: "2024-01-02"
```

### Implementation Example
```javascript
// Cursor pagination
app.get('/posts', async (req, res) => {
  const { cursor, limit = 20 } = req.query;
  
  let query = db.posts.where('status', 'published');
  
  if (cursor) {
    const decoded = JSON.parse(atob(cursor));
    query = query.where('createdAt', '<', decoded.createdAt);
  }
  
  const posts = await query
    .orderBy('createdAt', 'desc')
    .limit(parseInt(limit) + 1);
  
  const hasMore = posts.length > parseInt(limit);
  const data = hasMore ? posts.slice(0, -1) : posts;
  
  const nextCursor = hasMore 
    ? btoa(JSON.stringify({ createdAt: data[data.length-1].createdAt }))
    : null;
  
  res.json({
    data,
    meta: {
      nextCursor,
      hasMore
    }
  });
});
```

## Authentication and Authorization

```
You:
How to design API authentication?

AI:
## API Authentication

### Common Methods

| Method | Use Case | Security |
|--------|----------|----------|
| API Key | Service-to-service | Medium |
| Basic Auth | Simple scenarios | Low |
| JWT | Web/Mobile API | High |
| OAuth 2.0 | Third-party login | High |

### JWT Implementation
```javascript
// Login to get token
app.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;
  
  const user = await authService.verify(email, password);
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  const token = jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );
  
  res.json({ token });
});

// Auth middleware
const authenticate = async (req, res, next) => {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' });
  }
  
  const token = authHeader.split(' ')[1];
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Usage
app.get('/profile', authenticate, async (req, res) => {
  const user = await userService.getById(req.user.userId);
  res.json(user);
});
```

### Authorization
```javascript
// RBAC middleware
const authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
};

// Usage
app.delete('/users/:id', 
  authenticate,
  authorize('admin'),
  async (req, res) => {
    await userService.delete(req.params.id);
    res.status(204).send();
  }
);
```

## API Documentation

```
You:
How to generate API documentation?

AI:
## API Documentation

### OpenAPI/Swagger Specification
```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: Task Management API
  version: 1.0.0

paths:
  /projects:
    get:
      summary: Get project list
      tags: [Projects]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectList'
```

### Using Swagger UI
```javascript
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./openapi.json');

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
```

### Documentation Comments
```javascript
/**
 * @route POST /api/projects
 * @desc Create new project
 * @access Private
 * @param {string} name - Project name (required)
 * @param {string} description - Project description
 * @returns {Object} Created project
 */
app.post('/api/projects', authenticate, async (req, res) => {
  // ...
});
```

## Practice Exercises

```
1. Design your application API
2. Define resource structure
3. Choose versioning strategy
4. Implement authentication
5. Write OpenAPI documentation
6. Test API
```

**Good API design is the foundation of developer experience. Investing time in API design pays back in long-term maintainability and usability.**
