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
