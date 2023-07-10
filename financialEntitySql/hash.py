import bcrypt

_ENCODING  = 'utf-8'

def hash_password(password:str):
    return bcrypt.hashpw(password.encode(_ENCODING), bcrypt.gensalt()).decode(_ENCODING)

def is_valid(password:str, hash:str):
    return bcrypt.checkpw(password.encode(_ENCODING), hash.encode(_ENCODING))
