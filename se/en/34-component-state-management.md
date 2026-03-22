# 34. Component Design and State Management

## Component Design Principles

```
┌─────────────────────────────────────────────────────────┐
│               Component Design Principles                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Single Responsibility                                 │
│   └─ Each component does one thing                     │
│                                                         │
│   Reusable                                            │
│   └─ Components can be used in different scenarios      │
│                                                         │
│   Testable                                            │
│   └─ Component logic can be tested in isolation       │
│                                                         │
│   Composable                                          │
│   └─ Components can be combined into complex ones      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI-Assisted Component Design

### Atomic Design

```
You:
Please explain Atomic Design.

AI:
## Atomic Design

### Hierarchy
```
Atoms
  └─ Buttons, inputs, labels - smallest units

Molecules
  └─ Search box (input + button)
  └─ Card header (title + avatar + time)

Organisms
  └─ Navigation bar (Logo + menu + search)
  └─ Product card (image + title + price + button)

Templates
  └─ Page layout (navbar + sidebar + content)

Pages
  └─ Concrete page instances
```

### Directory Structure
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

### Component Implementation
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
      <Button type="submit">Search</Button>
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
        <Button>Login</Button>
      )}
    </nav>
  );
}
```

## State Management Patterns

```
You:
What are frontend state management patterns?

AI:
## State Management Patterns

### 1. Local State (Component State)
```jsx
// Simple UI state
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### 2. Lifting State Up
```jsx
// Share state between sibling components
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

### 3. Context API (Cross-component sharing)
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
  return <button className={theme}>Toggle Theme</button>;
}
```

### 4. State Management Libraries (Redux/Zustand/Pinia)

**Zustand (Recommended)**
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

// Usage
function CartPage() {
  const { cart, cartTotal } = useStore()
  return <div>Total: {cartTotal()}</div>
}
```

**Pinia (Vue)**
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

### 5. Server State (React Query/SWR)
```jsx
// React Query
function UserProfile({ userId }) {
  const { data, isLoading, error } = useQuery(
    ['user', userId],
    () => fetch(`/api/users/${userId}`).then(r => r.json()),
    {
      staleTime: 5 * 60 * 1000,  // Don't refetch within 5 minutes
    }
  )
  
  if (isLoading) return <Skeleton />
  if (error) return <Error />
  return <div>{data.name}</div>
}
```

## Complex Form Handling

```
You:
How to elegantly handle complex forms?

AI:
## Complex Form Handling

### Using Form Libraries
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
      <input {...register('name', { required: 'Name is required' })} />
      {errors.name && <span>{errors.name.message}</span>}
      
      <input {...register('email', { 
        required: 'Email is required',
        pattern: { value: /^\S+@\S$/, message: 'Invalid email' }
      })} />
      
      <input type="password" {...register('password', { 
        required: 'Password is required',
        minLength: { value: 8, message: 'Password must be at least 8 characters' }
      })} />
      
      <input type="password" {...register('confirmPassword', {
        validate: value => value === watchPassword || 'Passwords do not match'
      })} />
      
      <button type="submit">Submit</button>
    </form>
  )
}
```

### Dynamic Form Fields
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
          <button type="button" onClick={() => remove(index)}>Remove</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ name: '', phone: '' })}>
        Add Contact
      </button>
    </form>
  )
}
```

### Form Validation Schema
```javascript
// Zod validation
import { z } from 'zod'

export const userSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email format'),
  age: z.number().min(18, 'Must be 18 or older').optional(),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase')
    .regex(/[0-9]/, 'Password must contain number'),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword']
})

// Type inference
type UserForm = z.infer<typeof userSchema>
```

## Component Testing

```
You:
How to test React components?

AI:
## Component Testing

### 1. Unit Tests
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

### 2. Async Tests
```jsx
import { render, screen, waitFor } from '@testing-library/react'
import { UserProfile } from './UserProfile'
import { rest } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  rest.get('/api/users/1', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: 'John' }))
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

it('loads and displays user', async () => {
  render(<UserProfile userId={1} />)
  
  await waitFor(() => {
    expect(screen.getByText('John')).toBeInTheDocument()
  })
})
```

### 3. State Management Testing
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

## Practice Exercises

```
1. Create component directory structure
2. Implement basic atomic components
3. Compose into more complex components
4. Choose state management solution
5. Implement form handling
6. Write component tests
7. Create documentation
```

**Good component design makes code more maintainable and extensible. Investing time in design pays back in long-term development efficiency.**
