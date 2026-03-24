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
