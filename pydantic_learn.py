from enum import IntEnum
from typing import List, Optional, Any, Coroutine
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Priority(IntEnum):
    low = 1
    medium = 2
    high = 3

class TodoBase(BaseModel):
    """
    The Field function is used to provide additional metadata, validation constraints, and set default values for the fields.
    """
    todo_name: str = Field(..., min_length=3, max_length=50, description="The name of the todo item")
    todo_description: str = Field(..., min_length=5, max_length=200, description="A brief description of the todo item")
    priority: Priority = Field(default=Priority.low, description="The priority of the todo item")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    """
    The To_do model is used to represent a to_do item in the system.
    """
    todo_id: int = Field(..., description="The unique identifier of the todo item")

class TodoUpdate(TodoBase):
    """
    when updating a to_do item, not all field need to be updated, so we use Optional.
    """
    todo_name: Optional[str] = Field(None, min_length=3, max_length=50, description="The name of the todo item")
    todo_description: Optional[str] = Field(None, min_length=5, max_length=200, description="A brief description of the todo item")
    priority: Optional[Priority] = Field(None, description="The priority of the todo item")

# ok so after we defined all models, we can create a list of todos by using the To_do model
all_todos = [
    Todo(todo_id=1, todo_name="Learn FastAPI", todo_description="Learn how to build APIs with FastAPI", priority=Priority.high),
    Todo(todo_id=2, todo_name="Learn Pydantic", todo_description="Learn how to use Pydantic for data validation", priority=Priority.medium),
    Todo(todo_id=3, todo_name="Build a full-stack App", todo_description="Build a full-stack application using FastAPI and React", priority=Priority.low)
]

@app.get("/")
def index() -> dict:
    """
    The index endpoint returns a welcome message.
    """
    return {"message": "Welcome to the Todo API"}

@app.get("/todos")
def get_todos() -> List[Todo]:
    """
    The get_todos endpoint returns a list of all to_do items.
    """
    return all_todos

@app.get("/todos/{todo_id}")
def search_todo(target_todo_id: int) -> Todo | dict:
    """
    search target to_do item by id
    :param target_todo_id: the target to_do item id you want to search for
    :return: as shown
    """
    for todo in all_todos:
        if todo.todo_id == target_todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos/create", response_model=Todo | dict)
async def create_todo(todo: TodoCreate) -> dict[str, str | Todo]:
    """
    create a new to_do item
    :return: as shown, should be a dict contains the newly created to_do item
    """
    new_todo = Todo(
        todo_id = max(todo.todo_id for todo in all_todos) + 1,
        todo_name = todo.todo_name,
        todo_description = todo.todo_description,
        priority = todo.priority
    )
    all_todos.append(new_todo)
    return {"message": "Todo created successfully", "todo": new_todo}


@app.put("/todos/update/{todo_id}", response_model=Todo | dict)
async def update_todo(target_todo_id: int, updated_todo: TodoUpdate) -> dict[str, Todo] | dict:
    """
    same same just an update operation
    """
    for todo in all_todos:
        if todo.todo_id == target_todo_id:
            if updated_todo.todo_name:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_description:
                todo.todo_description = updated_todo.todo_description
            if updated_todo.priority:
                todo.priority = updated_todo.priority
        return {"message": "Todo updated successfully", "updated_todo": todo}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/delete/{todo_id}", response_model = Todo | dict)
async def delete_todo(target_todo_id: int) -> dict[str, Todo] | dict:
    """
    just delete the to_do item by id
    """
    for todo in all_todos:
        if todo.todo_id == target_todo_id:
            all_todos.remove(todo)
            return {"message": "Todo deleted successfully", "deleted_todo": todo}
    raise HTTPException(status_code=404, detail="Todo not found")