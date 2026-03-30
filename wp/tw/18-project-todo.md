# 第 18 章：專案實戰 - TodoApp

## 概述

本章實作一個完整的待辦事項應用程式，從後端 API 到前端介面，涵蓋 CRUD 功能。

## 18.1 後端 API

FastAPI 後端提供 Todo 的 CRUD API。

[程式檔案：18-1-todo-backend.py](../_code/18/18-1-todo-backend.py)

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False
    created_at: Optional[datetime] = None

todos_db: List[Todo] = []
todo_id_counter = 1

@app.get("/todos", response_model=List[Todo])
async def get_todos():
    return todos_db

@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    global todo_id_counter
    new_todo = Todo(
        id=todo_id_counter,
        title=todo.title,
        completed=todo.completed,
        created_at=datetime.now()
    )
    todos_db.append(new_todo)
    todo_id_counter += 1
    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo):
    for t in todos_db:
        if t.id == todo_id:
            t.title = todo.title
            t.completed = todo.completed
            return t
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    global todos_db
    todos_db = [t for t in todos_db if t.id != todo_id]
    return {"status": "deleted"}

@app.delete("/todos")
async def delete_completed():
    global todos_db
    todos_db = [t for t in todos_db if not t.completed]
    return {"status": "cleared"}
```

## 18.2 資料模型

Pydantic 模型定義。

[程式檔案：18-2-todo-models.py](../_code/18/18-2-todo-models.py)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TodoStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    completed: Optional[bool] = None

class TodoInDB(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Todo(TodoInDB):
    pass
```

## 18.3 CRUD 路由

完整的 CRUD 路由實作。

[程式檔案：18-3-todo-crud.py](../_code/18/18-3-todo-crud.py)

```python
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from 18-2-todo-models import Todo, TodoCreate, TodoUpdate, TodoStatus

router = APIRouter(prefix="/api/todos", tags=["todos"])

todos_db = []

@router.get("", response_model=List[Todo])
async def list_todos(
    status: Optional[TodoStatus] = None,
    search: Optional[str] = None
):
    result = todos_db.copy()
    if status:
        result = [t for t in result if t.completed == (status == TodoStatus.COMPLETED)]
    if search:
        result = [t for t in result if search.lower() in t.title.lower()]
    return result

@router.post("", response_model=Todo, status_code=201)
async def create_todo(todo: TodoCreate):
    from datetime import datetime
    new_todo = Todo(
        id=len(todos_db) + 1,
        title=todo.title,
        completed=todo.completed,
        created_at=datetime.now()
    )
    todos_db.append(new_todo)
    return new_todo

@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoUpdate):
    for t in todos_db:
        if t.id == todo_id:
            if todo.title is not None:
                t.title = todo.title
            if todo.completed is not None:
                t.completed = todo.completed
            return t
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    global todos_db
    todos_db = [t for t in todos_db if t.id != todo_id]
    return {"status": "deleted"}
```

## 18.4 前端主元件

React 主應用程式元件。

[程式檔案：18-4-todo-frontend.jsx](../_code/18/18-4-todo-frontend.jsx)

```javascript
import { useState, useEffect } from 'react';
import TodoList from './18-5-todo-list.jsx';
import TodoForm from './18-6-todo-form.jsx';
import TodoFilter from './18-8-todo-filter.jsx';
import './TodoApp.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/todos';

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const res = await fetch(API_URL);
      const data = await res.json();
      setTodos(data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (title) => {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, completed: false }),
    });
    const newTodo = await res.json();
    setTodos([...todos, newTodo]);
  };

  const toggleTodo = async (id) => {
    const todo = todos.find(t => t.id === id);
    const res = await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...todo, completed: !todo.completed }),
    });
    const updated = await res.json();
    setTodos(todos.map(t => t.id === id ? updated : t));
  };

  const deleteTodo = async (id) => {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    setTodos(todos.filter(t => t.id !== id));
  };

  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });

  if (loading) return <div>Loading...</div>;

  return (
    <div className="todo-app">
      <h1>Todo App</h1>
      <TodoForm onAdd={addTodo} />
      <TodoList todos={filteredTodos} onToggle={toggleTodo} onDelete={deleteTodo} />
      <TodoFilter filter={filter} setFilter={setFilter} />
    </div>
  );
}

export default TodoApp;
```

## 18.5 待辦清單元件

顯示待辦事項列表。

[程式檔案：18-5-todo-list.jsx](../_code/18/18-5-todo-list.jsx)

```javascript
import TodoItem from './18-7-todo-item.jsx';

function TodoList({ todos, onToggle, onDelete }) {
  if (todos.length === 0) {
    return <p className="no-todos">No todos yet!</p>;
  }

  return (
    <ul className="todo-list">
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={() => onToggle(todo.id)}
          onDelete={() => onDelete(todo.id)}
        />
      ))}
    </ul>
  );
}

export default TodoList;
```

## 18.6 新增表單

新增待辦事項的表單。

[程式檔案：18-6-todo-form.jsx](../_code/18/18-6-todo-form.jsx)

```javascript
import { useState } from 'react';

function TodoForm({ onAdd }) {
  const [title, setTitle] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    onAdd(title.trim());
    setTitle('');
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="What needs to be done?"
        className="todo-input"
      />
      <button type="submit" className="todo-button">Add</button>
    </form>
  );
}

export default TodoForm;
```

## 18.7 待辦項目元件

單一待辦事項元件。

[程式檔案：18-7-todo-item.jsx](../_code/18/18-7-todo-item.jsx)

```javascript
function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <li className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <label>
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={onToggle}
        />
        <span className="todo-title">{todo.title}</span>
      </label>
      <button onClick={onDelete} className="delete-button">
        Delete
      </button>
    </li>
  );
}

export default TodoItem;
```

## 18.8 篩選功能

過濾待辦事項的元件。

[程式檔案：18-8-todo-filter.jsx](../_code/18/18-8-todo-filter.jsx)

```javascript
function TodoFilter({ filter, setFilter }) {
  return (
    <div className="todo-filter">
      <button
        className={filter === 'all' ? 'active' : ''}
        onClick={() => setFilter('all')}
      >
        All
      </button>
      <button
        className={filter === 'active' ? 'active' : ''}
        onClick={() => setFilter('active')}
      >
        Active
      </button>
      <button
        className={filter === 'completed' ? 'active' : ''}
        onClick={() => setFilter('completed')}
      >
        Completed
      </button>
    </div>
  );
}

export default TodoFilter;
```

## 18.9 本地儲存

使用 LocalStorage 持久化資料。

[程式檔案：18-9-todo-storage.jsx](../_code/18/18-9-todo-storage.jsx)

```javascript
import { useState, useEffect } from 'react';

const STORAGE_KEY = 'todos';

export const useLocalStorage = () => {
  const [todos, setTodos] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
  }, [todos]);

  const addTodo = (title) => {
    const newTodo = {
      id: Date.now(),
      title,
      completed: false,
      createdAt: new Date().toISOString(),
    };
    setTodos([...todos, newTodo]);
  };

  const toggleTodo = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  const clearCompleted = () => {
    setTodos(todos.filter(todo => !todo.completed));
  };

  return { todos, addTodo, toggleTodo, deleteTodo, clearCompleted };
};

export default useLocalStorage;
```

## 18.10 完整實作說明

[程式檔案：18-10-todo-complete.md](../_code/18/18-10-todo-complete.md)

```markdown
# TodoApp Complete Implementation

## Backend (FastAPI)
- `18-1-todo-backend.py` - Main FastAPI server with CRUD endpoints
- `18-2-todo-models.py` - Pydantic models for validation
- `18-3-todo-crud.py` - CRUD routes with filtering and search

## Frontend (React)
- `18-4-todo-frontend.jsx` - Main App component with state management
- `18-5-todo-list.jsx` - List component for displaying todos
- `18-6-todo-form.jsx` - Form for adding new todos
- `18-7-todo-item.jsx` - Individual todo item component
- `18-8-todo-filter.jsx` - Filter buttons (All/Active/Completed)
- `18-9-todo-storage.jsx` - LocalStorage hook for persistence

## Features
1. Create, read, update, delete todos
2. Mark todos as complete/incomplete
3. Filter by status (all, active, completed)
4. Persist to localStorage or API
5. Clean, responsive UI

## Running the App
# Backend
cd backend
uvicorn 18-1-todo-backend:app --reload

# Frontend
cd frontend
npm start
```

## 重點回顧

| 功能 | 說明 |
|------|------|
| CRUD | 建立、讀取、更新、刪除 |
| 過濾 | All/Active/Completed |
| 持久化 | LocalStorage |
| 響應式 | CSS 樣式 |

## 練習題

1. 加入編輯待辦事項功能
2. 實作待辦事項分類
3. 加入截止日期功能
4. 實作離線支援
