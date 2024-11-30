from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import insert_task, get_tasks, update_task, delete_task
from pydantic import BaseModel
from .redis_config import set_cache, get_cache
from app.auth import create_access_token, verify_token, revoke_token
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from fastapi.responses import JSONResponse

app = FastAPI()

# Configuração do esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo Pydantic para Tarefa
class Task(BaseModel):
    title: str
    description: str
    done: bool

# Modelo para login
class LoginModel(BaseModel):
    username: str
    password: str


# Função para converter ObjectId
def custom_jsonable_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Converte ObjectId para string
    return obj


# Endpoint para adicionar uma nova tarefa
@app.post("/tasks/")
async def create_task(task: Task):
    try:
        task_data = task.dict()  # Converte o modelo para um dicionário
        inserted_task = insert_task(task_data)  # Insere no MongoDB
        
        # Atualiza o cache após adicionar uma nova tarefa
        tasks = get_tasks()  # Obtém todas as tarefas do banco de dados
        set_cache("tasks", tasks)  # Atualiza o cache com as tarefas

        # Adiciona o ID da tarefa ao retorno
        task_data["_id"] = str(inserted_task["_id"])  # Converte o ObjectId para string
        return JSONResponse(content=jsonable_encoder(task_data))

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Endpoint para listar todas as tarefas
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


# Endpoint para atualizar uma tarefa
@app.put("/tasks/{task_id}")
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


# Endpoint para excluir uma tarefa
@app.delete("/tasks/{task_id}")
async def delete_task_endpoint(task_id: str):
    try:
        delete_task(task_id)  # Chama a função para excluir a tarefa
        
        # Atualiza o cache após excluir a tarefa
        tasks = get_tasks()  # Obtém as tarefas atualizadas do banco de dados
        set_cache("tasks", tasks)  # Atualiza o cache com as tarefas
        
        return {"message": f"Task with ID '{task_id}' deleted!"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Endpoint para login
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Aqui você valida as credenciais e retorna um token JWT
    if form_data.username != "admin" or form_data.password != "password":
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint para dados seguros
@app.get("/secure-data")
def get_secure_data(current_user=Depends(verify_token)):
    return {"message": "Este é um dado seguro", "user": current_user}


# Endpoint para logout
@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    try:
        revoke_token(token)
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during logout: {str(e)}")
