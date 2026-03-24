# 33. Modern Frontend Framework Comparison

## Frontend Framework Ecosystem

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend Framework Selection              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   React        Maintained by Facebook, most popular    │
│   ├─ Flexible component model                         │
│   ├─ Large ecosystem                                  │
│   └─ Need to choose additional tools (router, state)   │
│                                                         │
│   Vue          Progressive, easy to learn                │
│   ├─ Single file components                            │
│   ├─ Built-in reactivity system                       │
│   └─ Excellent documentation                          │
│                                                         │
│   Svelte      Compile-time optimization, no virtual DOM  │
│   ├─ Extremely small bundle size                      │
│   ├─ No framework code after compilation              │
│   └─ Relatively new ecosystem                         │
│                                                         │
│   Angular     Maintained by Google, enterprise-grade   │
│   ├─ Complete solution                                │
│   ├─ TypeScript-first                                │
│   └─ Steep learning curve                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Framework Selection

```
You:
Our team has 3 people, developing an internal management system. Recommend a frontend framework.

AI:
## Recommended: Vue 3 + Element Plus

### Reasons
1. **Gentle learning curve** - Team can get up to speed quickly
2. **Active Chinese community** - Easy to find answers to problems
3. **Element Plus** - Ready-to-use component library
4. **Complete tooling** - Vite build, Pinia state management

### Tech Stack Recommendation
```json
{
  "framework": "Vue 3 (Composition API)",
  "build": "Vite",
  "ui": "Element Plus",
  "state": "Pinia",
  "router": "Vue Router 4",
  "http": "Axios"
}
```

### For Different Scenarios

| Scenario | Recommended |
|----------|------------|
| Rapid MVP development | Vue 3 |
| Need SSR | Nuxt 3 (Vue) or Next.js (React) |
| Large complex app | React + TypeScript |
| Ultimate performance | Svelte |
| Enterprise internal tools | Vue 3 or Angular |
| Mobile | React Native or Flutter |

## Deep Dive: React

### Component Patterns

```
You:
Please demonstrate common React component patterns.

AI:
## React Component Patterns

### 1. Function Components + Hooks
```jsx
// Basic component
function UserCard({ name, email, avatar }) {
  return (
    <div className="user-card">
      <img src={avatar} alt={name} />
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
}

// Component with state
function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+</button>
      <button onClick={() => setCount(c => c - 1)}>-</button>
    </div>
  );
}
```

### 2. Composition Pattern
```jsx
// Layout component
function Card({ children, title, footer }) {
  return (
    <div className="card">
      {title && <div className="card-header">{title}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

// Usage
function App() {
  return (
    <Card title="User Info" footer={<button>Edit</button>}>
      <p>User details...</p>
    </Card>
  );
}
```

### 3. Render Props
```jsx
// Mouse position component
function MousePosition({ render }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  
  useEffect(() => {
    const handleMouseMove = (e) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);
  
  return render(position);
}

// Usage
<MousePosition 
  render={({ x, y }) => <div>Mouse position: {x}, {y}</div>}
/>
```

### 4. Custom Hooks
```jsx
// Data fetching hook
function useUser(userId) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    async function fetchUser() {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        setUser(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }
    fetchUser();
  }, [userId]);
  
  return { user, loading, error };
}

// Usage
function UserProfile({ userId }) {
  const { user, loading, error } = useUser(userId);
  
  if (loading) return <Loading />;
  if (error) return <Error error={error} />;
  if (!user) return null;
  
  return <div>{user.name}</div>;
}
```

## Deep Dive: Vue

```
You:
Please demonstrate Vue 3 core features.

AI:
## Vue 3 Core

### 1. Composition API
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

// Reactive state
const count = ref(0)
const doubled = computed(() => count.value * 2)

// Methods
function increment() {
  count.value++
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Doubled: {{ doubled }}</p>
    <button @click="increment">+</button>
  </div>
</template>
```

### 2. Composables
```javascript
// useUser.js
import { ref, onMounted } from 'vue'

export function useUser(userId) {
  const user = ref(null)
  const loading = ref(true)
  const error = ref(null)
  
  async function fetchUser() {
    try {
      loading.value = true
      const response = await fetch(`/api/users/${userId}`)
      user.value = await response.json()
    } catch (err) {
      error.value = err
    } finally {
      loading.value = false
    }
  }
  
  onMounted(fetchUser)
  
  return { user, loading, error }
}
```

### 3. Pinia State Management
```javascript
// stores/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const profile = ref(null)
  const isLoggedIn = computed(() => !!profile.value)
  
  async function login(credentials) {
    const response = await api.post('/auth/login', credentials)
    profile.value = response.user
  }
  
  function logout() {
    profile.value = null
  }
  
  return { profile, isLoggedIn, login, logout }
})
```

## Performance Optimization

```
You:
What are frontend performance optimization methods?

AI:
## Frontend Performance Optimization

### 1. Code Splitting
```javascript
// React lazy loading
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Suspense>
  )
}
```

### 2. Caching
```javascript
// React Query / TanStack Query
const { data, isLoading } = useQuery(
  ['user', userId],
  () => fetchUser(userId),
  {
    staleTime: 5 * 60 * 1000,    // Don't refetch within 5 minutes
    cacheTime: 30 * 60 * 1000,   // Clear cache after 30 minutes
  }
)
```

### 3. Virtual Scrolling
```jsx
// Large list rendering
import { FixedSizeList } from 'react-window'

function VirtualList({ items }) {
  return (
    <FixedSizeList
      height={400}
      itemCount={items.length}
      itemSize={50}
    >
      {({ index, style }) => (
        <div style={style}>{items[index].name}</div>
      )}
    </FixedSizeList>
  )
}
```

### 4. Lazy Load Images
```jsx
<img 
  src={lazyImage}
  loading="lazy"
  alt="..."
/>

// Or use Intersection Observer
const [isVisible, setIsVisible] = useState(false)

useEffect(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        setIsVisible(true)
        observer.disconnect()
      }
    }
  )
  observer.observe(ref.current)
}, [])
```

### 5. State Optimization
```javascript
// React - Avoid unnecessary re-renders
const MemoizedComponent = React.memo(
  ({ data, onClick }) => {
    return <div onClick={onClick}>{data.map(item => <Item key={item.id} {...item} />)}</div>
  },
  (prevProps, nextProps) => {
    return prevProps.data === nextProps.data
  }
)

// Vue - computed caching
const double = computed(() => count.value * 2)
```

## SSR and SSG

```
You:
When do I need SSR or SSG?

AI:
## SSR vs SSG vs CSR

| Mode | Description | Best For |
|------|-------------|----------|
| CSR | Client-side rendering | SPAs, admin dashboards |
| SSR | Server-side rendering | SEO important, fast first load |
| SSG | Static generation | Infrequently changing content |
| ISR | Incremental static | Infrequently changing content |

### Decision Guide
```
Need SEO?
├─ Yes → SSR (Next.js/Nuxt)
│   Content changes frequently?
│   ├─ Yes → SSR
│   └─ No → SSG/ISR
└─ No
  Need fast first load?
  ├─ Yes → SSG/SSR
  └─ No → CSR
```

### Next.js SSR Example
```javascript
// pages/user/[id].js
export async function getServerSideProps({ params }) {
  const user = await fetchUser(params.id)
  
  if (!user) {
    return { notFound: true }
  }
  
  return {
    props: { user }
  }
}

function UserPage({ user }) {
  return <div>{user.name}</div>
}
```

### Next.js SSG Example
```javascript
// pages/blog/[slug].js
export async function getStaticPaths() {
  const posts = await getAllPosts()
  return {
    paths: posts.map(post => ({ params: { slug: post.slug } })),
    fallback: 'blocking'  // Static generation for non-existent pages
  }
}

export async function getStaticProps({ params }) {
  const post = await getPostBySlug(params.slug)
  return { props: { post } }
}
```

## Type Checking

```
You:
What is the role of TypeScript in frontend?

AI:
## TypeScript Benefits

### 1. Type Safety
```typescript
// Interface definition
interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'user'
}

// Function types
function createUser(data: Omit<User, 'id'>): User {
  return {
    id: generateId(),
    ...data
  }
}

// Error detection
createUser({ name: 'John', email: 'test' })
// Error: Missing 'role'
```

### 2. IntelliSense
```typescript
// Editor provides hints based on types
const user: User = await fetchUser(id)
user.name  // Auto-suggests string methods
user.role  // Auto-suggests 'admin' | 'user'
```

### 3. Safe Refactoring
```typescript
// After modifying interface, TypeScript highlights all places needing changes
interface User {
  id: string
  fullName: string  // Changed from name to fullName
  email: string
}
```

### 4. Utility Types
```typescript
// Partial - all properties optional
type PartialUser = Partial<User>

// Pick - select some properties
type UserPreview = Pick<User, 'id' | 'name'>

// Omit - exclude some properties
type CreateUserInput = Omit<User, 'id'>

// Record - key-value pairs
type UserMap = Record<string, User>
```

## Practice Exercises

```
1. Choose the right frontend framework for you
2. Configure development environment
3. Create a sample project
4. Integrate component library
5. Configure state management
6. Implement routing
7. Add TypeScript
8. Optimize performance
```

**Choosing a framework is not a one-time decision. Choose the most appropriate tool based on project requirements and team situation.**
