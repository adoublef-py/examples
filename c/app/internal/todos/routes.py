from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# fake database of todos


class Todo(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str | None = None
    completed: bool = False


todo_list = [
    Todo(title="Learn Rust", description="Learn how to use Rust"),
    Todo(title="Learn C", description="Learn how to use C"),
    Todo(title="Learn Go", description="Learn how to use Go"),
]

router = APIRouter()


@router.get("/")
async def handle_get_todos():
    return {"todos": todo_list}


@router.delete("/{todo_id}")
async def handle_delete(todo_id: UUID):
    for todo in todo_list:
        if todo.id == todo_id:
            todo_list.remove(todo)
            return {"message": "delete was successful"}
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/")
async def handle_post(todo_in: Todo):
    todo_list.append(todo_in)
    return {"message": "post was successful"}
