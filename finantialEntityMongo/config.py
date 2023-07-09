from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    MONGO_DB_DBNAME: str
    MONGO_DB_HOST: str
    MONGO_DB_HOSTNAME: str


    class Config:
        env_file = './.env'

settings = Settings()

