from pymongo import MongoClient
from bson import ObjectId
from app.models import Task  # Importe seu modelo Task (Pydantic)

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Acessar o banco de dados "todo_list"
db = client.todo_list

# Função para converter ObjectId para string
def str_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise ValueError("ObjectId expected")

# Função para inserir uma tarefa
def insert_task(task):
    db.tasks.insert_one(task)

# Função para listar todas as tarefas
def get_tasks():
    tasks = list(db.tasks.find())  # Pega todas as tarefas
    # Convertendo ObjectId para string para cada tarefa
    return [
        {
            "id": str_objectid(task["_id"]),  # Converte o ObjectId
            "title": task["title"],
            "description": task["description"],
            "done": task["done"]
        }
        for task in tasks
    ]

# Função para atualizar uma tarefa
def update_task(task_id: str, updates: dict):
    # Converter o ID da tarefa para ObjectId
    object_id = ObjectId(task_id)
    # Atualizar a tarefa no MongoDB
    result = db.tasks.update_one({"_id": object_id}, {"$set": updates})

    # Verificar se alguma tarefa foi atualizada
    if result.matched_count == 0:
        raise ValueError("Task not found")  # Levantar erro se não encontrar a tarefa

# Função para excluir uma tarefa
def delete_task(task_id: str):
    object_id = ObjectId(task_id)  # Converte o task_id para ObjectId
    db.tasks.delete_one({"_id": object_id})  # Deleta a tarefa pelo _id

