from fastapi import FastAPI, HTTPException, status
import redis

REDIS_HOSTNAME="127.0.0.1"
REDIS_PORT=6379
REDIS_DB=0

redis_client = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, db=REDIS_DB)

def get_cbu(key: str):
        cbu = redis_client.get(key)
        if cbu:
            return cbu.decode()
        return None
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
        
def set_cbu(key: str, cbu: str):
    if not redis_client.get(key):
        if redis_client.set(key, cbu):
            return True
        raise redis.RedisError
    return False

        
#TODO: Delete key
def delete_key(key: str):
    if redis_client.get(key):
        if redis_client.delete(key):
            return True
        raise redis.RedisError
    return False

def get_all_keys():
    return redis_client.keys()

def delete_all_keys():
    return redis_client.flushall()