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
