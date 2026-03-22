# 34. 元件設計與狀態管理

## 組件設計原則

```
┌─────────────────────────────────────────────────────────┐
│                   组件设计原则                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   单一职责（Single Responsibility）                     │
│   └─ 每个组件只做一件事                                 │
│                                                         │
│   可复用（Reusable）                                    │
│   └─ 组件可以在不同场景使用                             │
│                                                         │
│   可测试（Testable）                                    │
│   └─ 组件逻辑可以单独测试                               │
│                                                         │
│   可组合（Composable）                                  │
│   └─ 组件可以组合成更复杂的组件                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 輔助組件設計

### 原子設計

```
你：
请解释原子设计（Atomic Design）。

AI：
## Atomic Design 原子设计

### 层级结构
```
原子（Atoms）
  └─ 按钮、输入框、标签等最小单元

分子（Molecules）
  └─ 搜索框（输入框 + 按钮）
  └─ 卡片头部（标题 + 头像 + 时间）

有机体（Organisms）
  └─ 导航栏（Logo + 菜单 + 搜索框）
  └─ 产品卡片（图片 + 标题 + 价格 + 按钮）

模板（Templates）
  └─ 页面布局（导航栏 + 侧边栏 + 内容）

页面（Pages）
  └─ 具体页面实例
```

### 示例结构
```
src/
├── components/
│   ├── atoms/
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Badge/
│   │   └── Avatar/
│   │
│   ├── molecules/
│   │   ├── SearchBar/
│   │   ├── CardHeader/
│   │   ├── FormField/
│   │   └── UserInfo/
│   │
│   ├── organisms/
│   │   ├── Navbar/
│   │   ├── ProductCard/
│   │   ├── CommentList/
│   │   └── DataTable/
│   │
│   └── templates/
│       ├── MainLayout/
│       └── AdminLayout/
```

### 组件实现
```jsx
// atoms/Button.jsx
function Button({ children, variant = 'primary', size = 'md', ...props }) {
  return (
    <button 
      className={`btn btn-${variant} btn-${size}`}
      {...props}
    >
      {children}
    </button>
  );
}

// molecules/SearchBar.jsx
function SearchBar({ onSearch, placeholder }) {
  const [query, setQuery] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <Input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
      />
      <Button type="submit">搜索</Button>
    </form>
  );
}

// organisms/Navbar.jsx
function Navbar({ user, onLogout }) {
  return (
    <nav className="navbar">
      <Logo />
      <SearchBar onSearch={handleSearch} />
      {user ? (
        <UserMenu user={user} onLogout={onLogout} />
      ) : (
        <Button>登录</Button>
      )}
    </nav>
  );
}
```
```

## 狀態管理模式

```
你：
前端状态管理有哪些模式？

AI：
## 状态管理模式

### 1. Local State（组件内状态）
```jsx
// 简单的 UI 状态
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### 2. Lifting State Up（状态提升）
```jsx
// 兄弟组件共享状态
function Parent() {
  const [value, setValue] = useState('');
  
  return (
    <>
      <Input value={value} onChange={setValue} />
      <Display value={value} />
    </>
  );
}
```

### 3. Context API（跨组件共享）
```jsx
// ThemeContext.jsx
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function ThemedButton() {
  const { theme, setTheme } = useContext(ThemeContext);
  return <button className={theme}>切换主题</button>;
}
```

### 4. 状态管理库（Redux/Zustand/Pinia）

**Zustand（推荐）**
```javascript
import { create } from 'zustand'

const useStore = create((set, get) => ({
  // State
  user: null,
  cart: [],
  
  // Actions
  setUser: (user) => set({ user }),
  addToCart: (item) => set(state => ({
    cart: [...state.cart, item]
  })),
  
  // Computed
  cartTotal: () => get().cart.reduce((sum, i) => sum + i.price, 0)
}))

// 使用
function CartPage() {
  const { cart, cartTotal } = useStore()
  return <div>总计: {cartTotal()}</div>
}
```

**Pinia（Vue）**
```javascript
// stores/cart.js
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  
  const total = computed(() => 
    items.value.reduce((sum, item) => sum + item.price, 0)
  )
  
  function addItem(item) {
    items.value.push(item)
  }
  
  return { items, total, addItem }
})
```

### 5. 服务器状态（React Query/SWR）
```jsx
// React Query
function UserProfile({ userId }) {
  const { data, isLoading, error } = useQuery(
    ['user', userId],
    () => fetch(`/api/users/${userId}`).then(r => r.json()),
    {
      staleTime: 5 * 60 * 1000,  // 5分钟内不重新获取
    }
  )
  
  if (isLoading) return <Skeleton />
  if (error) return <Error />
  return <div>{data.name}</div>
}
```
```

## 複雜表單處理

```
你：
如何优雅地处理复杂表单？

AI：
## 复杂表单处理

### 使用表单库
```jsx
// React Hook Form
import { useForm } from 'react-hook-form'

function UserForm({ defaultValues, onSubmit }) {
  const { register, handleSubmit, watch, formState: { errors } } = useForm({
    defaultValues,
    resolver: yupResolver(validationSchema)
  })
  
  const watchPassword = watch('password')
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name', { required: '姓名必填' })} />
      {errors.name && <span>{errors.name.message}</span>}
      
      <input {...register('email', { 
        required: '邮箱必填',
        pattern: { value: /^\S+@\S$/, message: '邮箱格式错误' }
      })} />
      
      <input type="password" {...register('password', { 
        required: '密码必填',
        minLength: { value: 8, message: '密码至少8位' }
      })} />
      
      <input type="password" {...register('confirmPassword', {
        validate: value => value === watchPassword || '密码不一致'
      })} />
      
      <button type="submit">提交</button>
    </form>
  )
}
```

### 动态表单项
```jsx
function DynamicForm() {
  const { register, handleSubmit, fields, append, remove } = useFieldArray({
    name: 'contacts'
  })
  
  return (
    <form>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`contacts.${index}.name`)} />
          <input {...register(`contacts.${index}.phone`)} />
          <button type="button" onClick={() => remove(index)}>删除</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ name: '', phone: '' })}>
        添加联系人
      </button>
    </form>
  )
}
```

### 表单验证 Schema
```javascript
// Zod 验证
import { z } from 'zod'

export const userSchema = z.object({
  name: z.string().min(2, '姓名至少2个字符'),
  email: z.string().email('邮箱格式错误'),
  age: z.number().min(18, '必须年满18岁').optional(),
  password: z.string()
    .min(8, '密码至少8位')
    .regex(/[A-Z]/, '密码包含大写字母')
    .regex(/[0-9]/, '密码包含数字'),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: '密码不一致',
  path: ['confirmPassword']
})

// 类型推断
type UserForm = z.infer<typeof userSchema>
```
```

## 組件測試

```
你：
如何测试 React 组件？

AI：
## 组件测试

### 1. 单元测试
```jsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Counter } from './Counter'

describe('Counter', () => {
  it('renders initial count', () => {
    render(<Counter initialCount={5} />)
    expect(screen.getByText('5')).toBeInTheDocument()
  })
  
  it('increments count', () => {
    render(<Counter initialCount={0} />)
    fireEvent.click(screen.getByRole('button', { name: '+' }))
    expect(screen.getByText('1')).toBeInTheDocument()
  })
  
  it('decrements count', () => {
    render(<Counter initialCount={1} />)
    fireEvent.click(screen.getByRole('button', { name: '-' }))
    expect(screen.getByText('0')).toBeInTheDocument()
  })
})
```

### 2. 异步测试
```jsx
import { render, screen, waitFor } from '@testing-library/react'
import { UserProfile } from './UserProfile'
import { rest } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  rest.get('/api/users/1', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: '张三' }))
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

it('loads and displays user', async () => {
  render(<UserProfile userId={1} />)
  
  await waitFor(() => {
    expect(screen.getByText('张三')).toBeInTheDocument()
  })
})
```

### 3. 状态管理测试
```jsx
import { render } from '@testing-library/react'
import { Counter } from './Counter'
import { CounterProvider } from './CounterContext'

it('shares state between components', () => {
  render(
    <CounterProvider>
      <CounterDisplay />
      <CounterControls />
    </CounterProvider>
  )
  
  fireEvent.click(screen.getByRole('button', { name: '+' }))
  expect(screen.getByText('1')).toBeInTheDocument()
})
```
```

## 實踐練習

```
1. 创建组件目录结构
2. 实现基础原子组件
3. 组合成更复杂的组件
4. 选择状态管理方案
5. 实现表单处理
6. 编写组件测试
7. 创建文档
```

**好的組件設計讓代碼更易維護和擴展。投資時間在設計上，回報是長期的開發效率。**
