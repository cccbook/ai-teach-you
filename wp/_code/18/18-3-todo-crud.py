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
