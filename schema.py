from pydantic import BaseModel


class TodoIn(BaseModel):
    title: str


class Todo(TodoIn):
    id: int
    completed: bool
