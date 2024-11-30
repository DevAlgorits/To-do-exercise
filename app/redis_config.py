import redis
import json
from datetime import timedelta

# Configuração Redis
redis_host = "localhost"  # 127.0.0.1 ou outro host
redis_port = 6379         # Porta padrão
redis_db = 0              # Banco de dados padrão do Redis

# Conectar Redis
r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# verificar a conexão
def check_redis_connection():
    try:
        r.ping()  
        print("Conectado ao Redis!")
    except redis.ConnectionError:
        print("Erro ao conectar ao Redis.")

# adicionar dados no cache
def set_cache(key, data, expiration_time=3600):
    r.setex(key, timedelta(seconds=expiration_time), json.dumps(data))

# Função para obter dados do cache
def get_cache(key):
    cached_data = r.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None
