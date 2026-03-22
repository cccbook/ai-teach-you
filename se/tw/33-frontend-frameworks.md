# 33. 現代前端框架比較

## 前端框架生態

```
┌─────────────────────────────────────────────────────────┐
│                   前端框架选择                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   React        Facebook 维护，最流行                    │
│   ├─ 灵活的组件模型                                     │
│   ├─ 庞大的生态系统                                     │
│   └─ 需要选择额外工具（路由、状态）                     │
│                                                         │
│   Vue          渐进式，简单易学                          │
│   ├─ 单文件组件                                         │
│   ├─ 内置响应式系统                                     │
│   └─ 优秀的文档                                         │
│                                                         │
│   Svelte      编译时优化，无虚拟 DOM                    │
│   ├─ 极小的包体积                                       │
│   ├─ 编译后无框架代码                                   │
│   └─ 相对较新的生态                                     │
│                                                         │
│   Angular     Google 维护，企业级                       │
│   ├─ 完整解决方案                                       │
│   ├─ TypeScript 优先                                    │
│   └─ 学习曲线陡峭                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助框架選擇

```
你：
我们团队 3 人，要开发一个中台管理系统，请推荐前端框架。

AI：
## 框架推荐：Vue 3 + Element Plus

### 推荐理由
1. **学习曲线平缓** - 团队可以快速上手
2. **中文社区活跃** - 遇到问题容易找到答案
3. **Element Plus** - 开箱即用的组件库
4. **配套工具完善** - Vite 构建，Pinia 状态管理

### 技术栈建议
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

### 如果是以下场景

| 场景 | 推荐 |
|------|------|
| 快速开发 MVP | Vue 3 |
| 需要 SSR | Nuxt 3 (Vue) 或 Next.js (React) |
| 大型复杂应用 | React + TypeScript |
| 极致性能 | Svelte |
| 企业级中台 | Vue 3 或 Angular |
| 移动端 | React Native 或 Flutter |
```

## React 深入

### 組件模式

```
你：
请展示 React 的常用组件模式。

AI：
## React 组件模式

### 1. 函数组件 + Hooks
```jsx
// 基础组件
function UserCard({ name, email, avatar }) {
  return (
    <div className="user-card">
      <img src={avatar} alt={name} />
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
}

// 带状态的组件
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

### 2. 组合模式
```jsx
// 布局组件
function Card({ children, title, footer }) {
  return (
    <div className="card">
      {title && <div className="card-header">{title}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

// 使用
function App() {
  return (
    <Card title="用户信息" footer={<button>编辑</button>}>
      <p>用户详情...</p>
    </Card>
  );
}
```

### 3. Render Props
```jsx
// 鼠标位置组件
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

// 使用
<MousePosition 
  render={({ x, y }) => <div>鼠标位置: {x}, {y}</div>}
/>
```

### 4. 自定义 Hooks
```jsx
// 数据获取 Hook
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

// 使用
function UserProfile({ userId }) {
  const { user, loading, error } = useUser(userId);
  
  if (loading) return <Loading />;
  if (error) return <Error error={error} />;
  if (!user) return null;
  
  return <div>{user.name}</div>;
}
```

## Vue 深入

```
你：
请展示 Vue 3 的核心特性。

AI：
## Vue 3 核心

### 1. Composition API
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

// 响应式状态
const count = ref(0)
const doubled = computed(() => count.value * 2)

// 方法
function increment() {
  count.value++
}

// 生命周期
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

### 2. 组合函数 (Composables)
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

### 3. Pinia 状态管理
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
```

## 效能優化

```
你：
前端性能优化有哪些方法？

AI：
## 前端性能优化

### 1. 代码分割
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

### 2. 缓存
```javascript
// React Query / TanStack Query
const { data, isLoading } = useQuery(
  ['user', userId],
  () => fetchUser(userId),
  {
    staleTime: 5 * 60 * 1000,    // 5分钟内不重新获取
    cacheTime: 30 * 60 * 1000,   // 30分钟后清理缓存
  }
)
```

### 3. 虚拟滚动
```jsx
// 大列表渲染
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

### 4. 懒加载图片
```jsx
<img 
  src={lazyImage}
  loading="lazy"
  alt="..."
/>

// 或使用 Intersection Observer
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

### 5. 状态优化
```javascript
// React - 避免不必要的渲染
const MemoizedComponent = React.memo(
  ({ data, onClick }) => {
    return <div onClick={onClick}>{data.map(item => <Item key={item.id} {...item} />)}</div>
  },
  (prevProps, nextProps) => {
    return prevProps.data === nextProps.data
  }
)

// Vue - computed 缓存
const double = computed(() => count.value * 2)
```
```

## SSR 與 SSG

```
你：
什么时候需要 SSR 或 SSG？

AI：
## SSR vs SSG vs CSR

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| CSR | 客户端渲染 | 单页应用、管理后台 |
| SSR | 服务端渲染 | SEO 重要、首次加载快 |
| SSG | 静态生成 | 内容不频繁变化 |
| ISR | 增量静态 | 内容变化不频繁 |

### 选择建议
```
需要 SEO？
├─ 是 → SSR (Next.js/Nuxt)
│   内容经常变化？
│   ├─ 是 → SSR
│   └─ 否 → SSG/ISR
└─ 否
    需要首次加载快？
    ├─ 是 → SSG/SSR
    └─ 否 → CSR
```

### Next.js SSR 示例
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

### Next.js SSG 示例
```javascript
// pages/blog/[slug].js
export async function getStaticPaths() {
  const posts = await getAllPosts()
  return {
    paths: posts.map(post => ({ params: { slug: post.slug } })),
    fallback: 'blocking'  // 静态不存在的页面
  }
}

export async function getStaticProps({ params }) {
  const post = await getPostBySlug(params.slug)
  return { props: { post } }
}
```

## 類型檢查

```
你：
TypeScript 在前端的作用是什么？

AI：
## TypeScript 优势

### 1. 类型安全
```typescript
// 接口定义
interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'user'
}

// 函数类型
function createUser(data: Omit<User, 'id'>): User {
  return {
    id: generateId(),
    ...data
  }
}

// 错误检测
createUser({ name: '张三', email: 'test' })
// 错误：缺少 'role'
```

### 2. 智能提示
```typescript
// 编辑器会根据类型提供提示
const user: User = await fetchUser(id)
user.name  // 自动提示字符串方法
user.role  // 自动提示 'admin' | 'user'
```

### 3. 重构安全
```typescript
// 修改接口后，TypeScript 会提示所有需要修改的地方
interface User {
  id: string
  fullName: string  // 从 name 改为 fullName
  email: string
}
```

### 4. 实用类型
```typescript
// Partial - 所有属性可选
type PartialUser = Partial<User>

// Pick - 选择部分属性
type UserPreview = Pick<User, 'id' | 'name'>

// Omit - 排除部分属性
type CreateUserInput = Omit<User, 'id'>

// Record - 键值对
type UserMap = Record<string, User>
```
```

## 實踐練習

```
1. 选择适合你的前端框架
2. 配置开发环境
3. 创建一个示例项目
4. 实现组件库集成
5. 配置状态管理
6. 实现路由
7. 添加 TypeScript
8. 优化性能
```

**選擇框架不是一次性決定。根據項目需求和團隊情況，選擇最合適的工具。**
