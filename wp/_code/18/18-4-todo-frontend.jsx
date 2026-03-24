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
