from fastapi import FastAPI, HTTPException, status
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Ejemplo 1: Agregar claves de usuarios con sus CBUs correspondientes
redis_client.set('usuario1@mail.com', 'CBU123')
redis_client.set('+123456789', 'CBU456')
redis_client.set('12345678901', 'CBU789')

# Ejemplo 2: Agregar claves aleatorias de usuarios con CBUs correspondientes
redis_client.set('random_key1', 'CBU987')
redis_client.set('random_key2', 'CBU654')
redis_client.set('random_key3', 'CBU321')


def get_user_cbu_by_key(key: str):
        cbu = redis_client.get(key)
        if cbu:
                return cbu.decode()
        else:
                return None
                # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
        
def set_user_cbu_by_key(key: str, cbu: str):
    with redis_client.pipeline() as pipe:
        while True:
            try:
                pipe.watch(key)  # Observar la clave
                cbu_existence = pipe.get(key)
                
                if cbu_existence is None:
                    pipe.multi()  # Comenzar la transacción
                    pipe.set(key, cbu)  # Agregar la clave con el CBU
                    pipe.execute()  # Ejecutar la transacción
                    
                    break  # Salir del bucle while
                else:
                     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key already exists")
                #     raise ValueError("Already exists a key with that CBU")
            except redis.WatchError:
                continue
        return True    
        
