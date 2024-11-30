from datetime import datetime, timedelta
from jose import JWTError, jwt
from redis import Redis
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer

# Configurações
SECRET_KEY = "minha-chave-secreta"  # Substitua por uma chave mais forte!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Inicialize o Redis
redis_client = Redis(host='localhost', port=6379, decode_responses=True)

# Endpoint para extrair token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Salvar no Redis (opcional, mas útil para gerenciar sessões)
    redis_client.set(f"token:{encoded_jwt}", "active", ex=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not redis_client.exists(f"token:{token}"):
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


def revoke_token(token: str):
    redis_client.delete(f"token:{token}")
