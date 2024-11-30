import redis
from typing import Any

# Configuração do Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
def set_cache(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Armazena um valor no Redis com uma chave específica e um tempo de expiração.
    :param key: Chave do cache.
    :param value: Valor a ser armazenado.
    :param ttl: Tempo de expiração em segundos (padrão é 1 hora).
    :return: True se o valor foi armazenado com sucesso, False caso contrário.
    """
    try:
        redis_client.setex(key, ttl, value)
        return True
    except redis.RedisError:
        return False

def get_cache(key: str) -> Any:
    """
    Recupera um valor do Redis com base na chave.
    :param key: Chave do cache.
    :return: Valor armazenado ou None se a chave não existir.
    """
    try:
        value = redis_client.get(key)
        return value
    except redis.RedisError:
        return None

def delete_cache(key: str) -> bool:
    """
    Deleta uma chave do cache.
    :param key: Chave do cache.
    :return: True se a chave foi deletada com sucesso, False caso contrário.
    """
    try:
        redis_client.delete(key)
        return True
    except redis.RedisError:
        return False
