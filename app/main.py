from fastapi import FastAPI, HTTPException
from app.database import insert_task, get_tasks, update_task, delete_task
from pydantic import BaseModel

app = FastAPI()

# Modelo Pydantic para Tarefa
class Task(BaseModel):
    title: str
    description: str
    done: bool

@app.post("/tasks/")
async def add_task(task: Task):
    task_data = task.dict()  # Converte para um dicionário
    insert_task(task_data)
    return {"message": "Task added successfully!"}

@app.get("/tasks/")
async def list_tasks():
    tasks = get_tasks()
    return tasks

@app.put("/tasks/")
async def update_task_endpoint(task_id: str, task: Task):
    try:
        task_data = task.dict()  # Converte para um dicionário
        update_task(task_id, task_data)
        return {"message": f"Task '{task_id}' updated!"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/tasks/")
async def delete_task_endpoint(task_id: str):
    try:
        delete_task(task_id)  # Chama a função para excluir a tarefa
        return {"message": f"Task with ID '{task_id}' deleted!"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

