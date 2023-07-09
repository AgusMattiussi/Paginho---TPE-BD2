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
        redis_client.set(key, cbu)
        return True
    else:
        return False
    # with redis_client.pipeline() as pipe:
    #     while True:
    #         try:
    #             pipe.watch(key)  # Observar la clave
    #             cbu_existence = pipe.get(key)
                
    #             if cbu_existence is None:
    #                 pipe.multi()  # Comenzar la transacción
    #                 pipe.set(key, cbu)  # Agregar la clave con el CBU
    #                 pipe.execute()  # Ejecutar la transacción
                    
    #                 break  # Salir del bucle while
    #             else:
    #                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key already exists")
    #             #     raise ValueError("Already exists a key with that CBU")
    #         except redis.WatchError:
    #             continue
    #     return True 
        
