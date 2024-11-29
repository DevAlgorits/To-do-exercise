from pydantic import BaseModel

class Task(BaseModel):
    id: str  # O id agora é tratado como string
    title: str
    description: str
    done: bool