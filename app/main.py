from fastapi import FastAPI, HTTPException
from app.database import insert_task, get_tasks, update_task, delete_task
from pydantic import BaseModel
from .redis_config import set_cache, get_cache
import json

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
    
    # Atualiza o cache após adicionar uma nova tarefa
    tasks = get_tasks()  # Obtém todas as tarefas do banco de dados
    set_cache("tasks", tasks)  # Atualiza o cache com as tarefas
    
    return {"message": "Task added successfully!"}

@app.get("/tasks/")
async def list_tasks():
    # Tenta pegar as tarefas do cache primeiro
    tasks = get_cache("tasks")
    if tasks:
        return {"source": "cache", "tasks": tasks}  # Retorna tarefas do cache

    # Caso não tenha no cache, obtém as tarefas do banco de dados
    tasks = get_tasks()
    
    # Armazena no cache para futuras requisições
    set_cache("tasks", tasks)
    
    return {"source": "database", "tasks": tasks}

@app.put("/tasks/")
async def update_task_endpoint(task_id: str, task: Task):
    try:
        task_data = task.dict()  # Converte para um dicionário
        update_task(task_id, task_data)
        
        # Atualiza o cache após a alteração
        tasks = get_tasks()  # Obtém as tarefas atualizadas do banco de dados
        set_cache("tasks", tasks)  # Atualiza o cache com as tarefas
        
        return {"message": f"Task '{task_id}' updated!"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/tasks/")
async def delete_task_endpoint(task_id: str):
    try:
        delete_task(task_id)  # Chama a função para excluir a tarefa
        
        # Atualiza o cache após excluir a tarefa
        tasks = get_tasks()  # Obtém as tarefas atualizadas do banco de dados
        set_cache("tasks", tasks)  # Atualiza o cache com as tarefas
        
        return {"message": f"Task with ID '{task_id}' deleted!"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
