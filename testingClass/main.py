from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Clase Task siguiendo el principio SRP
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    status: str

# Clase TaskManager siguiendo el principio SRP
# The TaskManager class is a Python class that manages a list of tasks, allowing users to add, update,
# delete, and retrieve tasks.
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task) -> Task:
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def update_task(self, task_id: int, updated_task: Task) -> Optional[Task]:
        task = self.get_task(task_id)
        if task:
            task.title = updated_task.title
            task.description = updated_task.description
            task.status = updated_task.status
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

task_manager = TaskManager()

# Rutas de FastAPI siguiendo el principio KISS
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    return task_manager.add_task(task)

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    task = task_manager.get_task(task_id)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    task = task_manager.update_task(task_id, updated_task)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_manager.delete_task(task_id):
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/", response_model=List[Task])
def read_all_tasks():
    return task_manager.get_all_tasks()