task_db = []

class Task:
    def __init__(self, id: int, title: str, desc: str, done: bool = False):
        self.id = id
        self.title = title
        self.desc = desc
        self.done = done

    def mark_as_done(self):
        self.done = True

from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    desc: str



from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Message": "Hello World"}

@app.post("/tasks/")
def create_task(task: TaskCreate):
    new_task = Task(id=len(task_db)+1, title=task.title, desc=task.desc)
    task_db.append(new_task)
    return {"id": new_task.id, "title": new_task.title, "desc": new_task.desc}

@app.get("/tasks/")
def get_tasks():
    return [{"id": task.id, "title": task.title, "desc": task.desc} for task in task_db]

from fastapi import HTTPException
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    # Find the task by id
    for existing_task in task_db:
        if existing_task.id == task_id:
            existing_task.title = task.title
            existing_task.desc = task.desc
            return {"id": existing_task.id, "title": existing_task.title, "desc": existing_task.desc}
    
    # if task with teh given id is not found
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for existing_task in task_db:
        if existing_task.id == task_id:
            task_db.remove(existing_task)
            return {"Message": f"Task with id {task_id} has been deleted."}
    
    raise HTTPException(status_code=404, detail="Task not found")