from typing import List
from fastapi import FastAPI, status
from sqlalchemy.sql import not_
from uvicorn import run

import config
from models import database, todo
from schema import Todo, TodoIn

app = FastAPI(title=config.APP_NAME)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/todos", response_model=List[Todo])
async def get_todo():
    query = todo.select()
    items = await database.fetch_all(query)
    return items


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_in: TodoIn):
    query = todo.insert(todo_in.dict())
    todo_id = await database.execute(query)
    return {**todo_in.dict(), "id": todo_id, "completed": False}


@app.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo_id: int):
    query = todo.update().where(todo.c.id == todo_id).values(completed=not_(todo.c.completed))
    await database.execute(query)


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id):
    query = todo.delete().where(todo.c.id == todo_id)
    await database.execute(query)


if __name__ == "__main__":
    run("main:app", reload=True)
